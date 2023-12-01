#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi       https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes
# for ComfyUI                                             https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import os
import sys
import io
import comfy.sd
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json
import folder_paths
import typing as tg
import random
from .graphics_functions import random_hex_color
from ..categories import icons

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------#
# Aspect Ratio Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_AspectRatioSD15:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
    
        aspect_ratios = ["custom",
                         "1:1 square 512x512",
                         "1:1 square 1024x1024",
                         "2:3 portrait 512x768",
                         "3:4 portrait 512x682",
                         "3:2 landscape 768x512",
                         "4:3 landscape 682x512",
                         "16:9 cinema 910x512",
                         "1.85:1 cinema 952x512",
                         "2:1 cinema 1024x512",
                         "2.39:1 anamorphic 1224x512"]
               
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 64, "max": 8192}),
                "aspect_ratio": (aspect_ratios,),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 100}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", "LATENT", "STRING", )
    RETURN_NAMES = ("width", "height", "upscale_factor", "batch_size", "empty_latent", "show_help", )
    FUNCTION = "Aspect_Ratio"
    CATEGORY = icons.get("Comfyroll/Aspect Ratio")

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, batch_size):
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

        if swap_dimensions == "On":
            temp = width
            width = height
            height = temp
           
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])

        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Aspect-Ratio-Nodes#cr-sd15-aspect-ratio"
           
        return(width, height, upscale_factor, batch_size, {"samples":latent}, show_help, )   

#---------------------------------------------------------------------------------------------------------------------#
class CR_SDXLAspectRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
    
        aspect_ratios = ["custom",
                                  "1:1 square 1024x1024",
                                  "3:4 portrait 896x1152",
                                  "5:8 portrait 832x1216",
                                  "9:16 portrait 768x1344",
                                  "9:21 portrait 640x1536",
                                  "4:3 landscape 1152x896",
                                  "3:2 landscape 1216x832",
                                  "16:9 landscape 1344x768",
                                  "21:9 landscape 1536x640"]
        
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "aspect_ratio": (aspect_ratios,),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 100}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", "LATENT", "STRING", )
    RETURN_NAMES = ("width", "height", "upscale_factor", "batch_size", "empty_latent", "show_help", )
    FUNCTION = "Aspect_Ratio"
    CATEGORY = icons.get("Comfyroll/Aspect Ratio")

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, batch_size):
        if aspect_ratio == "1:1 square 1024x1024":
            width, height = 1024, 1024
        elif aspect_ratio == "3:4 portrait 896x1152":
            width, height = 896, 1152
        elif aspect_ratio == "5:8 portrait 832x1216":
            width, height = 832, 1216
        elif aspect_ratio == "9:16 portrait 768x1344":
            width, height = 768, 1344
        elif aspect_ratio == "9:21 portrait 640x1536":
            width, height = 640, 1536
        elif aspect_ratio == "4:3 landscape 1152x896":
            width, height = 1152, 896
        elif aspect_ratio == "3:2 landscape 1216x832":
            width, height = 1216, 832
        elif aspect_ratio == "16:9 landscape 1344x768":
            width, height = 1344, 768
        elif aspect_ratio == "21:9 landscape 1536x640":
            width, height = 1536, 640

        if swap_dimensions == "On":
            temp = width
            width = height
            height = temp
           
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])

        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Aspect-Ratio-Nodes#cr-sdxl-aspect-ratio"
           
        return(width, height, upscale_factor, batch_size, {"samples":latent}, show_help, )  

#---------------------------------------------------------------------------------------------------------------------#
class CR_AspectRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
    
        aspect_ratios = ["custom",
                         "SD1.5 - 1:1 square 512x512",
                         "SD1.5 - 2:3 portrait 512x768",
                         "SD1.5 - 3:4 portrait 512x682",
                         "SD1.5 - 3:2 landscape 768x512",
                         "SD1.5 - 4:3 landscape 682x512",
                         "SD1.5 - 16:9 cinema 910x512",
                         "SD1.5 - 1.85:1 cinema 952x512",
                         "SD1.5 - 2:1 cinema 1024x512",
                         "SDXL - 1:1 square 1024x1024",
                         "SDXL - 3:4 portrait 896x1152",
                         "SDXL - 5:8 portrait 832x1216",
                         "SDXL - 9:16 portrait 768x1344",
                         "SDXL - 9:21 portrait 640x1536",
                         "SDXL - 4:3 landscape 1152x896",
                         "SDXL - 3:2 landscape 1216x832",
                         "SDXL - 16:9 landscape 1344x768",
                         "SDXL - 21:9 landscape 1536x640"]
               
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "aspect_ratio": (aspect_ratios,),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 100}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", "LATENT", "STRING", )
    RETURN_NAMES = ("width", "height", "upscale_factor", "batch_size", "empty_latent", "show_help", )
    FUNCTION = "Aspect_Ratio"
    CATEGORY = icons.get("Comfyroll/Aspect Ratio")

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, batch_size):
        
        # SD1.5
        if aspect_ratio == "SD1.5 - 1:1 square 512x512":
            width, height = 512, 512
        elif aspect_ratio == "SD1.5 - 2:3 portrait 512x768":
            width, height = 512, 768
        elif aspect_ratio == "SD1.5 - 16:9 cinema 910x512":
            width, height = 910, 512
        elif aspect_ratio == "SD1.5 - 3:4 portrait 512x682":
            width, height = 512, 682
        elif aspect_ratio == "SD1.5 - 3:2 landscape 768x512":
            width, height = 768, 512    
        elif aspect_ratio == "SD1.5 - 4:3 landscape 682x512":
            width, height = 682, 512
        elif aspect_ratio == "SD1.5 - 1.85:1 cinema 952x512":            
            width, height = 952, 512
        elif aspect_ratio == "SD1.5 - 2:1 cinema 1024x512":
            width, height = 1024, 512
        elif aspect_ratio == "SD1.5 - 2.39:1 anamorphic 1224x512":
            width, height = 1224, 512 
        # SDXL   
        if aspect_ratio == "SDXL - 1:1 square 1024x1024":
            width, height = 1024, 1024
        elif aspect_ratio == "SDXL - 3:4 portrait 896x1152":
            width, height = 896, 1152
        elif aspect_ratio == "SDXL - 5:8 portrait 832x1216":
            width, height = 832, 1216
        elif aspect_ratio == "SDXL - 9:16 portrait 768x1344":
            width, height = 768, 1344
        elif aspect_ratio == "SDXL - 9:21 portrait 640x1536":
            width, height = 640, 1536
        elif aspect_ratio == "SDXL - 4:3 landscape 1152x896":
            width, height = 1152, 896
        elif aspect_ratio == "SDXL - 3:2 landscape 1216x832":
            width, height = 1216, 832
        elif aspect_ratio == "SDXL - 16:9 landscape 1344x768":
            width, height = 1344, 768
        elif aspect_ratio == "SDXL - 21:9 landscape 1536x640":
            width, height = 1536, 640                
        
        if swap_dimensions == "On":
            temp = width
            width = height
            height = temp
           
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])

        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Aspect-Ratio-Nodes#cr-aspect-ratio"
           
        return(width, height, upscale_factor, batch_size, {"samples":latent}, show_help, )    
#---------------------------------------------------------------------------------------------------------------------#
# Other Nodes
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

        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-image-output"

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
    
    RETURN_TYPES =("INT", "STRING", )
    RETURN_NAMES =("INT", "show_help", )
    FUNCTION = "int_multiple_of"    
    CATEGORY = icons.get("Comfyroll/Other")
    
    def int_multiple_of(self, integer, multiple=8):
        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-integer-multiple"
        if multiple == 0:
            return (int(integer), show_help, )
        integer = integer * multiple        
        return (int(integer), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Seed:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})}}

    RETURN_TYPES = ("INT", "STRING", )
    RETURN_NAMES = ("seed", "show_help", )
    FUNCTION = "seedint"
    OUTPUT_NODE = True
    CATEGORY = icons.get("Comfyroll/Other")

    @staticmethod
    def seedint(seed):
        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-seed"
        return (seed, show_help,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_LatentBatchSize:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"latent": ("LATENT", ),
                             "batch_size": ("INT", {"default": 2, "min": 1, "max": 16, "step": 1}),
                            }
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

        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-latent-batch-size"

        return ({
            'samples': torch.cat(sample_list),
        }, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_PromptText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"prompt": ("STRING", {"default": "prompt", "multiline": True})}}

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("prompt", "show_help", )
    FUNCTION = "get_value"
    CATEGORY = icons.get("Comfyroll/Other")

    def get_value(self, prompt):
        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-prompt-text"
        return (prompt, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SplitString:

    @classmethod
    def INPUT_TYPES(s):  
    
        return {"required": {"text": ("STRING", {"multiline": False, "default": "text"}),
                             "delimiter": ("STRING", {"multiline": False, "default": ","}), 
                }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("string_1", "string_2", "string_3", "string_4", "show_help", )    
    FUNCTION = "split"
    CATEGORY = icons.get("Comfyroll/Other")

    def split(self, text, delimiter):

        # Split the text string
        parts = text.split(delimiter)
        strings = [part.strip() for part in parts[:4]]
        string_1, string_2, string_3, string_4 = strings + [""] * (4 - len(strings))            

        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-split-string"

        return (string_1, string_2, string_3, string_4, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Value:

    @classmethod
    def INPUT_TYPES(s):  
        return {"required": {"value": ("FLOAT", {"default": 1.0,},)}}

    RETURN_TYPES = ("FLOAT", "INT", "STRING", )
    RETURN_NAMES = ("FLOAT", "INT", "show_help", )
    CATEGORY = icons.get("Comfyroll/Other")
    FUNCTION = "get_value"

    def get_value(self, value):
        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-value"
        return (float(value), int(value), show_help, )

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

    RETURN_TYPES = ("CONDITIONING", "STRING", )
    RETURN_NAMES = ("CONDITIONING", "show_help", )
    FUNCTION = "conditioning"
    CATEGORY = icons.get("Comfyroll/Other")
    
    def conditioning(self, mix_method, conditioning_1, conditioning_2, average_strength):

        conditioning_from = conditioning_1
        conditioning_to = conditioning_2
        conditioning_to_strength = average_strength

        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-conditioning-mixer"
    
        if mix_method == "Combine":
            return (conditioning_1 + conditioning_2, show_help, )

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
            return (out, show_help, )

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
            return (out, show_help, )
            
#---------------------------------------------------------------------------------------------------------------------#
class CR_SelectModel:
    
    @classmethod
    def INPUT_TYPES(cls):
    
        checkpoint_files = ["None"] + folder_paths.get_filename_list("checkpoints")
        
        return {"required": {"ckpt_name1": (checkpoint_files,),
                             "ckpt_name2": (checkpoint_files,),
                             "ckpt_name3": (checkpoint_files,),
                             "ckpt_name4": (checkpoint_files,),
                             "ckpt_name5": (checkpoint_files,),
                             "select_model": ("INT", {"default": 1, "min": 1, "max": 5}),
                            }    
               }


    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "VAE", "ckpt_name", "show_help", )
    FUNCTION = "select_model"
    CATEGORY = icons.get("Comfyroll/Other")

    def select_model(self, ckpt_name1, ckpt_name2, ckpt_name3, ckpt_name4, ckpt_name5, select_model):
    
        # Initialise the list
        model_list = list()
    
        if select_model == 1:
            model_name = ckpt_name1
        elif select_model == 2:
            model_name = ckpt_name2
        elif select_model == 3:
            model_name = ckpt_name3
        elif select_model == 4:
            model_name = ckpt_name4
        elif select_model == 5:
            model_name = ckpt_name5
            
        if  model_name == "None":
            print(f"CR Select Model: No model selected")
            return()

        ckpt_path = folder_paths.get_full_path("checkpoints", model_name)
        model, clip, vae, clipvision = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True,
                                                     embedding_directory=folder_paths.get_folder_paths("embeddings"))
            
        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-select-model"
            
        return (model, clip, vae, model_name, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_RandomHexColor:
    
    @classmethod
    def INPUT_TYPES(cls):
        
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),}}

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("hex_color1", "hex_color2", "hex_color3", "hex_color4", "show_help", )
    OUTPUT_NODE = True
    FUNCTION = "get_colors"
    CATEGORY = icons.get("Comfyroll/Other")

    def get_colors(self, seed):
    
        # Set the seed
        random.seed(seed)
    
        hex_color1 = random_hex_color()
        hex_color2 = random_hex_color()
        hex_color3 = random_hex_color()
        hex_color4 = random_hex_color()
        
        show_help = "https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-random-hex-color"
             
        return (hex_color1, hex_color2, hex_color3, hex_color4, show_help, )
                     
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### Aspect ratio
    "CR SD1.5 Aspect Ratio": CR_AspectRatioSD15,
    "CR SDXL Aspect Ratio":CR_SDXLAspectRatio,
    "CR Aspect Ratio": CR_AspectRatio,
    ### Other
    "CR Image Output": CR_ImageOutput,
    "CR Integer Multiple": CR_IntegerMultipleOf,
    "CR Latent Batch Size":CR_LatentBatchSize
    "CR Seed":CR_Seed,
    "CR Prompt Text":CR_PromptText,
    "CR Split String":CR_SplitString,
    "CR Value": CR_Value,
    "CR Conditioning Mixer":CR_ConditioningMixer,
    "CR Select Model": CR_SelectModel, 
    "CR Random Hex Color": CR_RandomHexColor,    
}
'''

