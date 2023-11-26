#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi       https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes
# for ComfyUI                                             https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import os
import sys
import io
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json
import folder_paths
import typing as tg
from ..categories import icons

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------#
class CR_AspectRatioSD15:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
    
        aspect_ratios = ["custom", "1:1 square 512x512", "1:1 square 1024x1024",
            "2:3 portrait 512x768", "3:4 portrait 512x682",
            "3:2 landscape 768x512", "4:3 landscape 682x512",
            "16:9 cinema 910x512", "1.85:1 cinema 952x512", "2:1 cinema 1024x512",
            "2.39:1 anamorphic 1224x512"]
               
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "aspect_ratio": (aspect_ratios,),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT")
    RETURN_NAMES = ("width", "height", "upscale_factor", "batch_size")
    FUNCTION = "Aspect_Ratio"
    CATEGORY = icons.get("Comfyroll/Other")

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, batch_size):
        if swap_dimensions == "Off":
            if aspect_ratio == "2:3 portrait 512x768":
                width, height = 512, 768
            elif aspect_ratio == "3:2 landscape 768x512":
                width, height = 768, 512
            elif aspect_ratio == "1:1 square 512x512":
                width, height = 512, 512
            elif aspect_ratio == "1:1 square 1024x1024":
                width, height = 1024, 1024
            elif aspect_ratio == "16:9 cinema 910x512":
                width, height = 910, 512
            elif aspect_ratio == "3:4 portrait 512x682":
                width, height = 512, 682
            elif aspect_ratio == "4:3 landscape 682x512":
                width, height = 682, 512
            elif aspect_ratio == "1.85:1 cinema 952x512":            
                width, height = 952, 512
            elif aspect_ratio == "2:1 cinema 1024x512":
                width, height = 1024, 512
            elif aspect_ratio == "2.39:1 anamorphic 1224x512":
                width, height = 1224, 512
            return(width, height, upscale_factor, batch_size)

        if swap_dimensions == "On":
            return(height, width, upscale_factor, batch_size,)
        else:
            return(width, height, upscale_factor, batch_size,)  
            
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageOutput:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),
                    "output_type": (["Preview", "Save"],),
                     "filename_prefix": ("STRING", {"default": "ComfyUI"})},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                "optional": {
                    "trigger": ("BOOLEAN", {"default": False},),}
                }

    RETURN_TYPES = ("BOOLEAN", )
    RETURN_NAMES = ("trigger", )
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = icons.get("Comfyroll/Other")

    def save_images(self, images, filename_prefix="ComfyUI", trigger = False, output_type = "Preview", prompt=None, extra_pnginfo=None):
        def map_filename(filename):
            prefix_len = len(os.path.basename(filename_prefix))
            prefix = filename[:prefix_len + 1]
            try:
                digits = int(filename[prefix_len + 1:].split('_')[0])
            except:
                digits = 0
            return (digits, prefix)

        def compute_vars(input):
            input = input.replace("%width%", str(images[0].shape[1]))
            input = input.replace("%height%", str(images[0].shape[0]))
            return input

        if output_type == "Save":
            self.output_dir = folder_paths.get_output_directory()
            self.type = "output"
        elif output_type == "Preview":
            self.output_dir = folder_paths.get_temp_directory()
            self.type = "temp"

        filename_prefix = compute_vars(filename_prefix)

        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        filename = os.path.basename(os.path.normpath(filename_prefix))

        full_output_folder = os.path.join(self.output_dir, subfolder)

        if os.path.commonpath((self.output_dir, os.path.abspath(full_output_folder))) != self.output_dir:
            return {}

        try:
            counter = max(filter(lambda a: a[1][:-1] == filename and a[1][-1] == "_", map(map_filename, os.listdir(full_output_folder))))[0] + 1
        except ValueError:
            counter = 1
        except FileNotFoundError:
            os.makedirs(full_output_folder, exist_ok=True)
            counter = 1

        results = list()
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = PngInfo()
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=4)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "ui": { "images": results }, "result": (trigger,) }


#---------------------------------------------------------------------------------------------------------------------#
class CR_IntegerMultipleOf:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "integer": ("INT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
                "multiple": ("FLOAT", {"default": 8, "min": 1, "max": 18446744073709551615}),
            }
        }
    
    RETURN_TYPES =("INT",)
    FUNCTION = "int_multiple_of"    
    CATEGORY = icons.get("Comfyroll/Other")
    
    def int_multiple_of(self, integer, multiple=8):
        if multiple == 0:
            return (int(integer), )
        integer = integer * multiple
        return (int(integer), )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Seed:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "seedint"
    OUTPUT_NODE = True
    CATEGORY = icons.get("Comfyroll/Other")

    @staticmethod
    def seedint(seed):
        return seed,

#---------------------------------------------------------------------------------------------------------------------#
class CR_LatentBatchSize:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT", ),
                "batch_size": ("INT", {"default": 2, "min": 1, "max": 16, "step": 1}),
            },
        }

    RETURN_TYPES = ("LATENT", )
    FUNCTION = "batchsize"
    CATEGORY = icons.get("Comfyroll/Other")

    def batchsize(self, latent: tg.Sequence[tg.Mapping[tg.Text, torch.Tensor]], batch_size: int):
        samples = latent['samples']
        shape = samples.shape

        sample_list = [samples] + [
            torch.clone(samples) for _ in range(batch_size - 1)
        ]

        return ({
            'samples': torch.cat(sample_list),
        }, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_PromptText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "prompt": ("STRING", {"default": "prompt", "multiline": True}),
                    },
                }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("prompt", )
    FUNCTION = "get_value"
    CATEGORY = icons.get("Comfyroll/Other")

    def get_value(self, prompt):
        return (prompt,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_SplitString:

    @classmethod
    def INPUT_TYPES(s):  
    
        return {"required": {"text": ("STRING", {"multiline": False, "default": "text"}),
                             "delimiter": ("STRING", {"multiline": False, "default": ","}), 
                },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("string_1", "string_2", "string_3", "string_4",)    
    FUNCTION = "split"
    CATEGORY = icons.get("Comfyroll/Other")

    def split(self, text, delimiter):

        # Split the text string
        parts = text.split(delimiter)
        strings = [part.strip() for part in parts[:4]]
        string_1, string_2, string_3, string_4 = strings + [""] * (4 - len(strings))            

        return (string_1, string_2, string_3, string_4)

#---------------------------------------------------------------------------------------------------------------------#
class CR_Value:

    @classmethod
    def INPUT_TYPES(s):  
        return {"required": {
                    "value": ("FLOAT", {"default": 1.0,},)
               },
        }

    RETURN_TYPES = ("FLOAT", "INT",)
    CATEGORY = icons.get("Comfyroll/Other")
    FUNCTION = "get_value"

    def get_value(self, value):
        return (float(value), int(value), )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ConditioningMixer:

    @classmethod
    def INPUT_TYPES(s):
    
        mix_methods = ["Combine", "Average", "Concatenate"]
        
        return {"required":
                    {"conditioning_1": ("CONDITIONING", ),
                     "conditioning_2": ("CONDITIONING", ),      
                     "mix_method": (mix_methods, ),
                     "average_strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                     }
                }

    RETURN_TYPES = ("CONDITIONING", )
    FUNCTION = "conditioning"
    CATEGORY = icons.get("Comfyroll/Other")
    
    def conditioning(self, mix_method, conditioning_1, conditioning_2, average_strength):

        conditioning_from = conditioning_1
        conditioning_to = conditioning_2
        conditioning_to_strength = average_strength
    
        if mix_method == "Combine":
            return (conditioning_1 + conditioning_2, )

        if mix_method == "Average":
        
            out = []

            if len(conditioning_from) > 1:
                print("Warning: ConditioningAverage conditioning_from contains more than 1 cond, only the first one will actually be applied to conditioning_to.")

            cond_from = conditioning_from[0][0]
            pooled_output_from = conditioning_from[0][1].get("pooled_output", None)

            for i in range(len(conditioning_to)):
                t1 = conditioning_to[i][0]
                pooled_output_to = conditioning_to[i][1].get("pooled_output", pooled_output_from)
                t0 = cond_from[:,:t1.shape[1]]
                if t0.shape[1] < t1.shape[1]:
                    t0 = torch.cat([t0] + [torch.zeros((1, (t1.shape[1] - t0.shape[1]), t1.shape[2]))], dim=1)

                tw = torch.mul(t1, conditioning_to_strength) + torch.mul(t0, (1.0 - conditioning_to_strength))
                t_to = conditioning_to[i][1].copy()
                if pooled_output_from is not None and pooled_output_to is not None:
                    t_to["pooled_output"] = torch.mul(pooled_output_to, conditioning_to_strength) + torch.mul(pooled_output_from, (1.0 - conditioning_to_strength))
                elif pooled_output_from is not None:
                    t_to["pooled_output"] = pooled_output_from

                n = [tw, t_to]
                out.append(n)
            return (out,)

        if mix_method == "Concatenate":
        
            out = []

            if len(conditioning_from) > 1:
                print("Warning: ConditioningConcat conditioning_from contains more than 1 cond, only the first one will actually be applied to conditioning_to.")

            cond_from = conditioning_from[0][0]

            for i in range(len(conditioning_to)):
                t1 = conditioning_to[i][0]
                tw = torch.cat((t1, cond_from),1)
                n = [tw, conditioning_to[i][1].copy()]
                out.append(n)
            return (out, )
            
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Image Output": CR_ImageOutput,
    "CR Integer Multiple": CR_IntegerMultipleOf,
    "CR SD1.5 Aspect Ratio": CR_AspectRatioSD15,
    "CR Latent Batch Size":CR_LatentBatchSize
    "CR Seed":CR_Seed,
    "CR Prompt Text":CR_PromptText,
    "CR Split String":CR_SplitString,
    "CR Value": CR_Value,
    "CR Conditioning Mixer":CR_ConditioningMixer,    
}
'''

