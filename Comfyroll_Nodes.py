import torch
import numpy as np
from PIL import Image, ImageEnhance
from PIL.PngImagePlugin import PngInfo
import os
import sys
import comfy.sd
import comfy.model_management
import folder_paths
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))


class ComfyRoll_InputImages_Old:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "image1": ("IMAGE",),
                "image2": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_NODE = True
    FUNCTION = "InputImages_Old"

    CATEGORY = "Comfyroll/Logic"

    def InputImages_Old(self, Input, image1, image2):
        if Input == 1:
            return (image1, )
        else:
            return (image2, )


class ComfyRoll_InputImages_Old_4way:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 4}),
                "image1": ("IMAGE",),
            },
            "optional": {
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_NODE = True
    FUNCTION = "InputImages_Old_4"

    CATEGORY = "Comfyroll/Logic"

    def InputImages_Old_4(self, Input, image1, image2=None, image3=None, image4=None):
        if Input == 1:
            return (image1, )
        elif Input == 2:
            return (image2, )
        elif Input == 3:
            return (image3, )
        else:
            return (image4, )



class ComfyRoll_InputLatents_Old:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "latent1": ("LATENT",),
                "latent2": ("LATENT",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    OUTPUT_NODE = True
    FUNCTION = "InputLatents_Old"

    CATEGORY = "Comfyroll/Logic"

    def InputLatents_Old(self, Input, latent1, latent2):
        if Input == 1:
            return (latent1, )
        else:
            return (latent2, )




class ComfyRoll_InputConditioning_Old:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "conditioning1": ("CONDITIONING",),
                "conditioning2": ("CONDITIONING",)
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    OUTPUT_NODE = True
    FUNCTION = "InputConditioning_Old"

    CATEGORY = "Comfyroll/Logic"

    def InputConditioning_Old(self, Input, conditioning1, conditioning2):
        if Input == 1:
            return (conditioning1, )
        else:
            return (conditioning2, )



class ComfyRoll_InputClip_Old:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "clip1": ("CLIP",),
                "clip2": ("CLIP",)
            }
        }

    RETURN_TYPES = ("CLIP",)
    OUTPUT_NODE = True
    FUNCTION = "InputClip_Old"

    CATEGORY = "Comfyroll/Logic"

    def InputClip_Old(self, Input, clip1, clip2):
        if Input == 1:
            return (clip1, )
        else:
            return (clip2, )

#("MODEL",)

class ComfyRoll_InputModel_Old:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "model1": ("MODEL",),
                "model2": ("MODEL",)
            }
        }

    RETURN_TYPES = ("MODEL",)
    OUTPUT_NODE = True
    FUNCTION = "InputModel_Old"

    CATEGORY = "Comfyroll/Logic"

    def InputModel_Old(self, Input, model1, model2):
        if Input == 1:
            return (model1, )
        else:
            return (model2, )


class ComfyRoll_InputControlNet_Old:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "control_net1": ("CONTROL_NET",),
                "control_net2": ("CONTROL_NET",)
            }
        }
        
    RETURN_TYPES = ("CONTROL_NET",)
    OUTPUT_NODE = True
    FUNCTION = "InputControlNet_Old"

    CATEGORY = "Comfyroll/Logic"

    def InputControlNet_Old(self, Input, control_net1, control_net2):
        if Input == 1:
            return (control_net1, )
        else:
            return (control_net2, )



#1 = Do Nothing
#2 = Load Lora
class ComfyRoll_LoraLoader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "clip": ("CLIP", ),
                              "switch": ([
                                "On",
                                "Off"],),
                              "lora_name": (folder_paths.get_filename_list("loras"), ),
                              "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                              "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_lora"

    CATEGORY = "Comfyroll/IO"

    def load_lora(self, model, clip, switch, lora_name, strength_model, strength_clip):
        if switch == "Off":
            return (model, clip)
        else:
            lora_path = folder_paths.get_full_path("loras", lora_name)
            model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora_path, strength_model, strength_clip)
            return (model_lora, clip_lora)


class ComfyRoll_ImageSize_Float:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT")
    #RETURN_NAMES = ("Width", "Height")
    FUNCTION = "ImageSize_Float"

    CATEGORY = "Comfyroll/IO"

    def ImageSize_Float(self, width, height, upscale_factor):
        return(width, height, upscale_factor)





class ComfyRoll_ImageOutput:
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
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "Comfyroll/IO"

    def save_images(self, images, filename_prefix="ComfyUI", output_type = "Preview", prompt=None, extra_pnginfo=None):
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
            print("Saving image outside the output folder is not allowed.")
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

        return { "ui": { "images": results } }


class CR_Int_Multiple_Of:
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
    
    CATEGORY = "Comfyroll/Math"
    
    def int_multiple_of(self, integer, multiple=8):
        if multiple == 0:
            return (int(integer), )
        integer = integer * multiple
        return (int(integer), )


class ComfyRoll_AspectRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "aspect_ratio": (["custom", "1:1 square 512x512", "2:3 portrait 512x768", "3:4 portrait 512x682", "3:2 landscape 768x512", "4:3 landscape 682x512", "16:9 cinema 910x512", "2:1 cinema 1024x512"],),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT")
    #RETURN_NAMES = ("Width", "Height")
    FUNCTION = "Aspect_Ratio"

    CATEGORY = "Comfyroll/Test"

    def Aspect_Ratio(self, width, height, aspect_ratio, upscale_factor, swap_dimensions):
        if swap_dimensions == "Off":
            if aspect_ratio == "2:3 portrait 512x768":
                width, height = 512, 768
            elif aspect_ratio == "3:2 landscape 768x512":
                width, height = 768, 512
            elif aspect_ratio == "1:1 square 512x512":
                width, height = 512, 512
            elif aspect_ratio == "16:9 cinema 910x512":
                width, height = 910, 512
            elif aspect_ratio == "3:4 portrait 512x682":
                width, height = 512, 682
            elif aspect_ratio == "4:3 landscape 682x512":
                width, height = 682, 512
            elif aspect_ratio == "2:1 cinema 1024x512":
                width, height = 1024, 512
            return(width, height, upscale_factor)
        elif swap_dimensions == "On":
            if aspect_ratio == "2:3 portrait 512x768":
                width, height = 512, 768
            elif aspect_ratio == "3:2 landscape 768x512":
                width, height = 768, 512
            elif aspect_ratio == "1:1 square 512x512":
                width, height = 512, 512
            elif aspect_ratio == "16:9 cinema 910x512":
                width,height = 910, 512
            elif aspect_ratio == "3:4 portrait 512x682":
                width, height = 512, 682
            elif aspect_ratio == "4:3 landscape 682x512":
                width, height = 682, 512
            elif aspect_ratio == "2:1 cinema 1024x512":
                width, height = 1024, 512
            return(height, width, upscale_factor)



class ComfyRoll_SeedToInt:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("SEED", ),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "seed_to_int"

    CATEGORY = "Comfyroll/Test"

    def seed_to_int(self, seed):
        return (seed.get('seed'),)



NODE_CLASS_MAPPINGS = {
    "CR Image Input Switch": ComfyRoll_InputImages_Old,
    "CR Image Input Switch (4 way)":ComfyRoll_InputImages_Old_4way,
    "CR Latent Input Switch": ComfyRoll_InputLatents_Old,
    "CR Conditioning Input Switch": ComfyRoll_InputConditioning_Old,
    "CR Clip Input Switch": ComfyRoll_InputClip_Old,
    "CR Model Input Switch": ComfyRoll_InputModel_Old,
    "CR ControlNet Input Switch": ComfyRoll_InputControlNet_Old,
    "CR Load LoRA": ComfyRoll_LoraLoader,
    "CR Image Size":ComfyRoll_ImageSize_Float,
    "CR Image Output": ComfyRoll_ImageOutput,
    "CR Integer Multiple": CR_Int_Multiple_Of,
    "CR Image Size Test": ComfyRoll_AspectRatio,
    "CR Seed to Int": ComfyRoll_SeedToInt
}
