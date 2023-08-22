#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi         https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             #
# for ComfyUI                                               https://github.com/comfyanonymous/ComfyUI                                               #
#---------------------------------------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
from PIL import Image, ImageEnhance
from PIL.PngImagePlugin import PngInfo
import os
import sys
import io
import pip

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

import comfy.sd
import comfy.utils
import comfy.model_management

import folder_paths
import json
from nodes import MAX_RESOLUTION, ControlNetApply
import typing as tg


try:
    import matplotlib.pyplot as plt
except ImportError:
    pip.main(['install', 'matplotlib'])
    import matplotlib.pyplot as plt


#---------------------------------------------------------------------------------------------------------------------------------------------------#

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_InputImages:
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
    FUNCTION = "InputImages"

    CATEGORY = "Comfyroll/Logic"

    def InputImages(self, Input, image1, image2):
        if Input == 1:
            return (image1, )
        else:
            return (image2, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_InputImages_4way:
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
    FUNCTION = "InputImages_4"

    CATEGORY = "Comfyroll/Logic"

    def InputImages_4(self, Input, image1, image2=None, image3=None, image4=None):
        if Input == 1:
            return (image1, )
        elif Input == 2:
            return (image2, )
        elif Input == 3:
            return (image3, )
        else:
            return (image4, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_InputLatents:
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
    FUNCTION = "InputLatents"

    CATEGORY = "Comfyroll/Logic"

    def InputLatents(self, Input, latent1, latent2):
        if Input == 1:
            return (latent1, )
        else:
            return (latent2, )
            


#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_InputConditioning:
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
    FUNCTION = "InputConditioning"

    CATEGORY = "Comfyroll/Logic"

    def InputConditioning(self, Input, conditioning1, conditioning2):
        if Input == 1:
            return (conditioning1, )
        else:
            return (conditioning2, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_InputClip:
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
    FUNCTION = "InputClip"

    CATEGORY = "Comfyroll/Logic"

    def InputClip(self, Input, clip1, clip2):
        if Input == 1:
            return (clip1, )
        else:
            return (clip2, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_InputModel:
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
    FUNCTION = "InputModel"

    CATEGORY = "Comfyroll/Logic"

    def InputModel(self, Input, model1, model2):
        if Input == 1:
            return (model1, )
        else:
            return (model2, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#        

class ComfyRoll_InputControlNet:
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
    FUNCTION = "InputControlNet"

    CATEGORY = "Comfyroll/Logic"

    def InputControlNet(self, Input, control_net1, control_net2):
        if Input == 1:
            return (control_net1, )
        else:
            return (control_net2, )
#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_InputLatentsText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["txt2img", "img2img"],),
                "txt2img": ("LATENT",),
                "img2img": ("LATENT",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    OUTPUT_NODE = True
    FUNCTION = "InputLatentsText"

    CATEGORY = "Comfyroll/Process"

    def InputLatentsText(self, Input, txt2img, img2img):
        if Input == "txt2img":
            return (txt2img, )
        else:
            return (img2img, )            


#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_HiResFixSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["latent_upscale", "image_upscale"],),
                "latent_upscale": ("LATENT",),
                "image_upscale": ("LATENT",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    OUTPUT_NODE = True
    FUNCTION = "InputHiResText"

    CATEGORY = "Comfyroll/Process"

    def InputHiResText(self, Input, latent_upscale, image_upscale):
        if Input == "latent_upscale":
            return (latent_upscale, )
        else:
            return (image_upscale, )  


#---------------------------------------------------------------------------------------------------------------------------------------------------#                       
            
class ComfyRoll_LoraLoader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        file_list = folder_paths.get_filename_list("loras")
        file_list.insert(0, "None")
        return {"required": { "model": ("MODEL",),
                              "clip": ("CLIP", ),
                              "switch": ([
                                "On",
                                "Off"],),
                              "lora_name": (file_list, ),
                              "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                              "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_lora"

    CATEGORY = "Comfyroll/IO"

    def load_lora(self, model, clip, switch, lora_name, strength_model, strength_clip):
        if strength_model == 0 and strength_clip == 0:
            return (model, clip)

        if switch == "Off" or  lora_name == "None":
            return (model, clip)

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                del self.loaded_lora

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        return (model_lora, clip_lora)

#---------------------------------------------------------------------------------------------------------------------------------------------------#           

class ComfyRoll_ApplyControlNet:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"conditioning": ("CONDITIONING", ),
                             "control_net": ("CONTROL_NET", ),
                             "image": ("IMAGE", ),
                             "switch": ([
                                "On",
                                "Off"],),
                             "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01})
                             }}
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "apply_controlnet"

    CATEGORY = "Comfyroll/Conditioning"

    def apply_controlnet(self, conditioning, control_net, image, switch, strength):
        if strength == 0 or switch == "Off":
            return (conditioning, )

        c = []
        control_hint = image.movedim(-1,1)
        for t in conditioning:
            n = [t[0], t[1].copy()]
            c_net = control_net.copy().set_cond_hint(control_hint, strength)
            if 'control' in t[1]:
                c_net.set_previous_controlnet(t[1]['control'])
            n[1]['control'] = c_net
            c.append(n)
        return (c, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#

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

    CATEGORY = "Comfyroll/Image"

    def ImageSize_Float(self, width, height, upscale_factor):
        return(width, height, upscale_factor)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

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

    CATEGORY = "Comfyroll/Legacy"

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

#---------------------------------------------------------------------------------------------------------------------------------------------------#

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

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_AspectRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "aspect_ratio": (["custom", "1:1 - square 512x512", "1:1 - square 1024x1024", "2:3 - portrait 512x768", "3:4 - portrait 512x682", "3:2 - landscape 768x512", "4:3 - landscape 682x512", "16:9 - cinema 910x512", "2:1 - cinema 1024x512"],),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor1": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "upscale_factor2": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT", "INT")
    #RETURN_NAMES = ("Width", "Height")
    FUNCTION = "Aspect_Ratio"

    CATEGORY = "Comfyroll/Legacy"

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor1, upscale_factor2, batch_size):
        if swap_dimensions == "Off":
            if aspect_ratio == "2:3 - portrait 512x768":
                width, height = 512, 768
            elif aspect_ratio == "3:2 - landscape 768x512":
                width, height = 768, 512
            elif aspect_ratio == "1:1 - square 512x512":
                width, height = 512, 512
            elif aspect_ratio == "1:1 - square 1024x1024":
                width, height = 1024, 1024
            elif aspect_ratio == "16:9 - cinema 910x512":
                width, height = 910, 512
            elif aspect_ratio == "3:4 - portrait 512x682":
                width, height = 512, 682
            elif aspect_ratio == "4:3 - landscape 682x512":
                width, height = 682, 512
            elif aspect_ratio == "2:1 - cinema 1024x512":
                width, height = 1024, 512
            return(width, height, upscale_factor1, upscale_factor2, batch_size)
        elif swap_dimensions == "On":
            if aspect_ratio == "2:3 - portrait 512x768":
                width, height = 512, 768
            elif aspect_ratio == "3:2 - landscape 768x512":
                width, height = 768, 512
            elif aspect_ratio == "1:1 - square 512x512":
                width, height = 512, 512              
            elif aspect_ratio == "1:1 - square 1024x1024":
                width, height = 1024, 1024
            elif aspect_ratio == "16:9 - cinema 910x512":
                width,height = 910, 512
            elif aspect_ratio == "3:4 - portrait 512x682":
                width, height = 512, 682
            elif aspect_ratio == "4:3 - landscape 682x512":
                width, height = 682, 512
            elif aspect_ratio == "2:1 - cinema 1024x512":
                width, height = 1024, 512
            return(height, width, upscale_factor1, upscale_factor2, batch_size)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_AspectRatio_SDXL:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "aspect_ratio": (["custom", "1:1 - square 1024x1024", "3:4 - portrait 896x1152", "5:8 - portrait 832x1216", "9:16 - portrait 768x1344", "9:21 - portrait 640x1536", "4:3 - landscape 1152x896", "3:2 - landscape 1216x832", "16:9 - landscape 1344x768", "21:9 - landscape 1536x640"],),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor1": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "upscale_factor2": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT", "INT")
    #RETURN_NAMES = ("Width", "Height")
    FUNCTION = "Aspect_Ratio"

    CATEGORY = "Comfyroll/Legacy"

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor1, upscale_factor2, batch_size):
        if aspect_ratio == "1:1 - square 1024x1024":
            width, height = 1024, 1024
        elif aspect_ratio == "3:4 - portrait 896x1152":
            width, height = 896, 1152
        elif aspect_ratio == "5:8 - portrait 832x1216":
            width, height = 832, 1216
        elif aspect_ratio == "9:16 - portrait 768x1344":
            width, height = 768, 1344
        elif aspect_ratio == "9:21 - portrait 640x1536":
            width, height = 640, 1536
        elif aspect_ratio == "4:3 - landscape 1152x896":
            width, height = 1152, 896
        elif aspect_ratio == "3:2 - landscape 1216x832":
            width, height = 1216, 832
        elif aspect_ratio == "16:9 - landscape 1344x768":
            width, height = 1344, 768
        elif aspect_ratio == "21:9 - landscape 1536x640":
            width, height = 1536, 640
            
        if swap_dimensions == "On":
            return(height, width, upscale_factor1, upscale_factor2, batch_size,)
        else:
            return(width, height, upscale_factor1, upscale_factor2, batch_size,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_SDXL_AspectRatio_v2:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "aspect_ratio": (["custom", "1:1 - square 1024x1024", "3:4 - portrait 896x1152", "5:8 - portrait 832x1216", "9:16 - portrait 768x1344", "9:21 - portrait 640x1536", "4:3 - landscape 1152x896", "3:2 - landscape 1216x832", "16:9 - landscape 1344x768", "21:9 - landscape 1536x640"],),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT")
    RETURN_NAMES = ("width", "height", "upscale_factor", "batch_size")
    FUNCTION = "Aspect_Ratio"

    CATEGORY = "Comfyroll/SDXL"

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, batch_size):
        if aspect_ratio == "1:1 - square 1024x1024":
            width, height = 1024, 1024
        elif aspect_ratio == "3:4 - portrait 896x1152":
            width, height = 896, 1152
        elif aspect_ratio == "5:8 - portrait 832x1216":
            width, height = 832, 1216
        elif aspect_ratio == "9:16 - portrait 768x1344":
            width, height = 768, 1344
        elif aspect_ratio == "9:21 - portrait 640x1536":
            width, height = 640, 1536
        elif aspect_ratio == "4:3 - landscape 1152x896":
            width, height = 1152, 896
        elif aspect_ratio == "3:2 - landscape 1216x832":
            width, height = 1216, 832
        elif aspect_ratio == "16:9 - landscape 1344x768":
            width, height = 1344, 768
        elif aspect_ratio == "21:9 - landscape 1536x640":
            width, height = 1536, 640
            
        if swap_dimensions == "On":
            return(height, width, upscale_factor, batch_size,)
        else:
            return(width, height, upscale_factor, batch_size,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_AspectRatio_v2:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "aspect_ratio": (["custom", "1:1 - square 512x512", "1:1 - square 1024x1024", "2:3 - portrait 512x768", "3:4 - portrait 512x682", "3:2 - landscape 768x512", "4:3 - landscape 682x512", "16:9 - cinema 910x512", "2:1 - cinema 1024x512"],),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT")
    RETURN_NAMES = ("width", "height", "upscale_factor", "batch_size")
    FUNCTION = "Aspect_Ratio"

    CATEGORY = "Comfyroll/Image"

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, batch_size):
        if swap_dimensions == "Off":
            if aspect_ratio == "2:3 - portrait 512x768":
                width, height = 512, 768
            elif aspect_ratio == "3:2 - landscape 768x512":
                width, height = 768, 512
            elif aspect_ratio == "1:1 - square 512x512":
                width, height = 512, 512
            elif aspect_ratio == "1:1 - square 1024x1024":
                width, height = 1024, 1024
            elif aspect_ratio == "16:9 - cinema 910x512":
                width, height = 910, 512
            elif aspect_ratio == "3:4 - portrait 512x682":
                width, height = 512, 682
            elif aspect_ratio == "4:3 - landscape 682x512":
                width, height = 682, 512
            elif aspect_ratio == "2:1 - cinema 1024x512":
                width, height = 1024, 512
            return(width, height, upscale_factor, batch_size)

        if swap_dimensions == "On":
            return(height, width, upscale_factor, batch_size,)
        else:
            return(width, height, upscale_factor, batch_size,)  
            
#---------------------------------------------------------------------------------------------------------------------------------------------------#


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

    CATEGORY = "Comfyroll/Number"

    def seed_to_int(self, seed):
        return (seed.get('seed'),)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_Seed:
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

    CATEGORY = "Comfyroll/Number"

    @staticmethod
    def seedint(seed):
        return seed,


#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_Color_Tint:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1
                }),
                "mode": (["white", "black", "sepia", "red", "green", "blue", "cyan", "magenta", "yellow", "purple", "orange", "warm", "cool",  "lime", "navy", "vintage", "rose", "teal", "maroon", "peach", "lavender", "olive"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "color_tint"

    CATEGORY = "Comfyroll/Image"

    def color_tint(self, image: torch.Tensor, strength: float, mode: str = "sepia"):
        if strength == 0:
            return (image,)

        sepia_weights = torch.tensor([0.2989, 0.5870, 0.1140]).view(1, 1, 1, 3).to(image.device)
      
        mode_filters = {
            "white": torch.tensor([1.0, 1.0, 1.0]),
            "black": torch.tensor([0, 0, 0]),
            "sepia": torch.tensor([1.0, 0.8, 0.6]),
            "red": torch.tensor([1.0, 0.6, 0.6]),
            "green": torch.tensor([0.6, 1.0, 0.6]),
            "blue": torch.tensor([0.6, 0.8, 1.0]),
            "cyan": torch.tensor([0.6, 1.0, 1.0]),
            "magenta": torch.tensor([1.0, 0.6, 1.0]),
            "yellow": torch.tensor([1.0, 1.0, 0.6]),
            "purple": torch.tensor([0.8, 0.6, 1.0]),
            "orange": torch.tensor([1.0, 0.7, 0.3]),
            "warm": torch.tensor([1.0, 0.9, 0.7]),
            "cool": torch.tensor([0.7, 0.9, 1.0]),
            "lime": torch.tensor([0.7, 1.0, 0.3]),
            "navy": torch.tensor([0.3, 0.4, 0.7]),
            "vintage": torch.tensor([0.9, 0.85, 0.7]),
            "rose": torch.tensor([1.0, 0.8, 0.9]),
            "teal": torch.tensor([0.3, 0.8, 0.8]),
            "maroon": torch.tensor([0.7, 0.3, 0.5]),
            "peach": torch.tensor([1.0, 0.8, 0.6]),
            "lavender": torch.tensor([0.8, 0.6, 1.0]),
            "olive": torch.tensor([0.6, 0.7, 0.4]),
        }

        scale_filter = mode_filters[mode].view(1, 1, 1, 3).to(image.device)

        grayscale = torch.sum(image * sepia_weights, dim=-1, keepdim=True)
        tinted = grayscale * scale_filter

        result = tinted * strength + image * (1 - strength)
        return (result,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class ComfyRoll_prompt_mixer:
    def __init__(self):
        pass

    @classmethod        
    def INPUT_TYPES(s):
        return {
            "required":{
            },
            "optional":{
                "prompt_positive": ("STRING", {"multiline": True, "default": "BASE_POSITIVE"}),
                "prompt_negative": ("STRING", {"multiline": True, "default": "BASE_NEGATIVE"}),
                "style_positive": ("STRING", {"multiline": True, "default": "REFINER_POSTIVE"}),
                "style_negative": ("STRING", {"multiline": True, "default": "REFINER_NEGATIVE"}),
                "preset": (["preset 1", "preset 2", "preset 3", "preset 4", "preset 5"],),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("pos_g", "pos_l", "pos_r", "neg_g", "neg_l", "neg_r", )
    FUNCTION = "mixer"

    CATEGORY = "Comfyroll/Legacy"

    def mixer(self, prompt_positive, prompt_negative, style_positive, style_negative, preset):
        if preset == "preset 1":
            pos_g = prompt_positive
            pos_l = prompt_positive
            pos_r = prompt_positive
            neg_g = prompt_negative
            neg_l = prompt_negative
            neg_r = prompt_negative
        elif preset == "preset 2":
            pos_g = prompt_positive
            pos_l = style_positive
            pos_r = prompt_positive
            neg_g = prompt_negative
            neg_l = style_negative
            neg_r = prompt_negative
        elif preset == "preset 3":
            pos_g = style_positive
            pos_l = prompt_positive
            pos_r = style_positive
            neg_g = style_negative
            neg_l = prompt_negative
            neg_r = style_negative
        elif preset == "preset 4":
            pos_g = prompt_positive + style_positive
            pos_l = prompt_positive + style_positive
            pos_r = prompt_positive + style_positive
            neg_g = prompt_negative + style_negative
            neg_l = prompt_negative + style_negative
            neg_r = prompt_negative + style_negative
        elif preset == "preset 5":
            pos_g = prompt_positive
            pos_l = prompt_positive
            pos_r = style_positive
            neg_g = prompt_negative
            neg_l = prompt_negative
            neg_r = style_negative
        return (pos_g, pos_l, pos_r, neg_g, neg_l, neg_r, )


#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_prompt_mixer_v2:
    def __init__(self):
        pass

    @classmethod        
    def INPUT_TYPES(s):
        return {
            "required":{
            },
            "optional":{
                "prompt_positive": ("STRING", {"multiline": True, "default": "BASE_POSITIVE"}),
                "prompt_negative": ("STRING", {"multiline": True, "default": "BASE_NEGATIVE"}),
                "style_positive": ("STRING", {"multiline": True, "default": "REFINER_POSTIVE"}),
                "style_negative": ("STRING", {"multiline": True, "default": "REFINER_NEGATIVE"}),
                "preset": (["default with no style text", "default with style text", "style boost 1", "style boost 2", "style text to refiner"],),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("pos_g", "pos_l", "pos_r", "neg_g", "neg_l", "neg_r", )
    FUNCTION = "mixer"

    CATEGORY = "Comfyroll/SDXL"

    def mixer(self, prompt_positive, prompt_negative, style_positive, style_negative, preset):
        if preset == "default with no style text":
            pos_g = prompt_positive
            pos_l = prompt_positive
            pos_r = prompt_positive
            neg_g = prompt_negative
            neg_l = prompt_negative
            neg_r = prompt_negative
        elif preset == "default with style text":
            pos_g = prompt_positive + style_positive
            pos_l = prompt_positive + style_positive
            pos_r = prompt_positive + style_positive
            neg_g = prompt_negative + style_negative
            neg_l = prompt_negative + style_negative
            neg_r = prompt_negative + style_negative
        elif preset == "style boost 1":
            pos_g = prompt_positive
            pos_l = style_positive
            pos_r = prompt_positive
            neg_g = prompt_negative
            neg_l = style_negative
            neg_r = prompt_negative
        elif preset == "style boost 2":
            pos_g = style_positive
            pos_l = prompt_positive
            pos_r = style_positive
            neg_g = style_negative
            neg_l = prompt_negative
            neg_r = style_negative
        elif preset == "style text to refiner":
            pos_g = prompt_positive
            pos_l = prompt_positive
            pos_r = style_positive
            neg_g = prompt_negative
            neg_l = prompt_negative
            neg_r = style_negative
        return (pos_g, pos_l, pos_r, neg_g, neg_l, neg_r, )


#---------------------------------------------------------------------------------------------------------------------------------------------------#


class Comfyroll_SDXLStyleText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "positive_style": ("STRING", {"default": "POS_STYLE", "multiline": True}),
                    "negative_style": ("STRING", {"default": "NEG_STYLE", "multiline": True}),
                    },
                }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("positive_prompt_text_l", "negative_prompt_text_l" )
    FUNCTION = "get_value"

    CATEGORY = "Comfyroll/SDXL"

    def get_value(self, positive_style, negative_style):
        return (positive_style, negative_style,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_SDXLBasePromptEncoder:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "base_clip": ("CLIP", ),
                    "pos_g": ("STRING", {"multiline": True, "default": "POS_G"}),
                    "pos_l": ("STRING", {"multiline": True, "default": "POS_L"}),
                    "neg_g": ("STRING", {"multiline": True, "default": "NEG_G"}),
                    "neg_l": ("STRING", {"multiline": True, "default": "NEG_L"}),
                    "preset": (["preset A", "preset B", "preset C"],), 
                    "base_width": ("INT", {"default": 4096.0, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                    "base_height": ("INT", {"default": 4096.0, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                    "crop_w": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                    "crop_h": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                    "target_width": ("INT", {"default": 4096.0, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                    "target_height": ("INT", {"default": 4096.0, "min": 0, "max": MAX_RESOLUTION, "step": 64}),
                    },
                }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", )
    RETURN_NAMES = ("base_positive", "base_negative", )
    FUNCTION = "encode"

    CATEGORY = "Comfyroll/SDXL"

    def encode(self, base_clip, pos_g, pos_l, neg_g, neg_l, base_width, base_height, crop_w, crop_h, target_width, target_height, preset,):
        empty = base_clip.tokenize("")

        # positive prompt
        tokens1 = base_clip.tokenize(pos_g)
        tokens1["l"] = base_clip.tokenize(pos_l)["l"]

        if len(tokens1["l"]) != len(tokens1["g"]):
            while len(tokens1["l"]) < len(tokens1["g"]):
                tokens1["l"] += empty["l"]
            while len(tokens1["l"]) > len(tokens1["g"]):
                tokens1["g"] += empty["g"]

        cond1, pooled1 = base_clip.encode_from_tokens(tokens1, return_pooled=True)
        res1 = [[cond1, {"pooled_output": pooled1, "width": base_width, "height": base_height, "crop_w": crop_w, "crop_h": crop_h, "target_width": target_width, "target_height": target_height}]]

        # negative prompt
        tokens2 = base_clip.tokenize(neg_g)
        tokens2["l"] = base_clip.tokenize(neg_l)["l"]

        if len(tokens2["l"]) != len(tokens2["g"]):
            while len(tokens2["l"]) < len(tokens2["g"]):
                tokens2["l"] += empty["l"]
            while len(tokens2["l"]) > len(tokens2["g"]):
                tokens2["g"] += empty["g"]

        cond2, pooled2 = base_clip.encode_from_tokens(tokens2, return_pooled=True)
        res2 = [[cond2, {"pooled_output": pooled2, "width": base_width, "height": base_height, "crop_w": crop_w, "crop_h": crop_h, "target_width": target_width, "target_height": target_height}]]

        # positive style
        tokens2 = base_clip.tokenize(pos_l)
        tokens2["l"] = base_clip.tokenize(neg_l)["l"]

        if len(tokens2["l"]) != len(tokens2["g"]):
            while len(tokens2["l"]) < len(tokens2["g"]):
                tokens2["l"] += empty["l"]
            while len(tokens2["l"]) > len(tokens2["g"]):
                tokens2["g"] += empty["g"]

        cond2, pooled2 = base_clip.encode_from_tokens(tokens2, return_pooled=True)
        res3 = [[cond2, {"pooled_output": pooled2, "width": base_width, "height": base_height, "crop_w": crop_w, "crop_h": crop_h, "target_width": target_width, "target_height": target_height}]]

        # negative style
        tokens2 = base_clip.tokenize(neg_l)
        tokens2["l"] = base_clip.tokenize(neg_l)["l"]

        if len(tokens2["l"]) != len(tokens2["g"]):
            while len(tokens2["l"]) < len(tokens2["g"]):
                tokens2["l"] += empty["l"]
            while len(tokens2["l"]) > len(tokens2["g"]):
                tokens2["g"] += empty["g"]

        cond2, pooled2 = base_clip.encode_from_tokens(tokens2, return_pooled=True)
        res4 = [[cond2, {"pooled_output": pooled2, "width": base_width, "height": base_height, "crop_w": crop_w, "crop_h": crop_h, "target_width": target_width, "target_height": target_height}]]

        if preset == "preset A":
            base_positive = res1
            base_negative = res2
        elif preset == "preset B":
            base_positive = res3
            base_negative = res4
        elif preset == "preset C":
            base_positive = res1 + res3
            base_negative = res2 + res4
            
        return (base_positive, base_negative, )



#---------------------------------------------------------------------------------------------------------------------------------------------------#


class Comfyroll_Halftone_Grid:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "dot_style": (["Accent","afmhot","autumn","binary","Blues","bone","BrBG","brg",
                            "BuGn","BuPu","bwr","cividis","CMRmap","cool","coolwarm","copper","cubehelix","Dark2","flag",
                            "gist_earth","gist_gray","gist_heat","gist_rainbow","gist_stern","gist_yarg","GnBu","gnuplot","gnuplot2","gray","Greens",
                            "Greys","hot","hsv","inferno","jet","magma","nipy_spectral","ocean","Oranges","OrRd",
                            "Paired","Pastel1","Pastel2","pink","PiYG","plasma","PRGn","prism","PuBu","PuBuGn",
                            "PuOr","PuRd","Purples","rainbow","RdBu","RdGy","RdPu","RdYlBu","RdYlGn","Reds","seismic",
                            "Set1","Set2","Set3","Spectral","spring","summer","tab10","tab20","tab20b","tab20c","terrain",
                            "turbo","twilight","twilight_shifted","viridis","winter","Wistia","YlGn","YlGnBu","YlOrBr","YlOrRd"],),
                    "reverse_dot_style": (["No", "Yes"],),
                    "dot_frequency": ("INT", {"default": 50, "min": 1, "max":200, "step": 1}),
                    "background_color": (["custom", "white", "black", "red", "green", "blue", "cyan", "magenta", "yellow", "purple", "orange", "lime", "navy", "teal", "maroon", "lavender", "olive"],),
                    "background_R": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                    "background_G": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                    "background_B": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                    "x_pos": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": .01}),
                    "y_pos": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": .01}),                    
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "halftone"

    CATEGORY = "Comfyroll/Image"

    def halftone(self, width, height, dot_style, reverse_dot_style, dot_frequency, background_color, background_R, background_G, background_B, x_pos, y_pos):
        #install_matplotlib()
    
        if background_color == "custom":
            bgc = (background_R/255, background_G/255, background_B/255)
        else:
            bgc = background_color
            
        reverse = ""
        
        if reverse_dot_style == "Yes":
            reverse = "_r"
        
        #img = Image.new(mode = 'RGB', size = (300, 200), color = (red, green, blue))
        fig, ax = plt.subplots(figsize=(width/100,height/100))
        #fig, ax = plt.subplots(figsize=(width/20,height/20))
        
    
        dotsx = np.linspace(0, 1, dot_frequency)
        dotsy = np.linspace(0, 1, dot_frequency)
    
        X, Y = np.meshgrid(dotsx, dotsy)
    
        dist = np.sqrt((X - x_pos)**2 + (Y - y_pos)**2)
    
        fig.patch.set_facecolor(bgc)
        ax.scatter(X, Y, c=dist, cmap=dot_style+reverse)
        

        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(tight=True)
        #plt.show()
      
        
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)
        
        return(pil2tensor(img),)

#---------------------------------------------------------------------------------------------------------------------------------------------------#



class Comfyroll_LatentBatchSize:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT", ),
                "batch_size": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 16,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ("LATENT", )

    FUNCTION = "batchsize"

    OUTPUT_NODE = False

    CATEGORY = "Comfyroll/Latent"

    def batchsize(self, latent: tg.Sequence[tg.Mapping[tg.Text, torch.Tensor]], batch_size: int):
        samples = latent['samples']
        shape = samples.shape

        sample_list = [samples] + [
            torch.clone(samples) for _ in range(batch_size - 1)
        ]

        return ({
            'samples': torch.cat(sample_list),
        }, )


#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_ApplyLoRA_Stack:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"model": ("MODEL",),
                            "clip": ("CLIP", ),
                            "lora_stack": ("LORA_STACK", ),
                            }
        }

    RETURN_TYPES = ("MODEL", "CLIP",)
    RETURN_NAMES = ("MODEL", "CLIP", )
    FUNCTION = "apply_lora_stack"
    CATEGORY = "Comfyroll/IO"

    def apply_lora_stack(self, model, clip, lora_stack=None,):

        # Initialise the list
        lora_params = list()
 
        # Extend lora_params with lora-stack items 
        if lora_stack:
            lora_params.extend(lora_stack)
        else:
            return (model, clip,)

        #print(lora_params)

        # Initialise the model and clip
        model_lora = model
        clip_lora = clip

        # Loop through the list
        for tup in lora_params:
            lora_name, strength_model, strength_clip = tup
            print(lora_name, strength_model, strength_clip)
            
            lora_path = folder_paths.get_full_path("loras", lora_name)
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            
            model_lora, clip_lora = comfy.sd.load_lora_for_models(model_lora, clip_lora, lora, strength_model, strength_clip)  

        return (model_lora, clip_lora,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

# Based on Efficiency Nodes
class Comfyroll_LoRA_Stack:

    loras = ["None"] + folder_paths.get_filename_list("loras")

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "switch_1": ([
                        "Off",
                        "On"],),
                    "lora_name_1": (cls.loras,),
                    "model_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "switch_2": ([
                        "Off",
                        "On"],),
                    "lora_name_2": (cls.loras,),
                    "model_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "switch_3": ([
                        "Off",
                        "On"],),
                    "lora_name_3": (cls.loras,),
                    "model_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                },
                "optional": {"lora_stack": ("LORA_STACK",)
                },
        }

    RETURN_TYPES = ("LORA_STACK",)
    RETURN_NAMES = ("LORA_STACK",)
    FUNCTION = "lora_stacker"
    CATEGORY = "Comfyroll/IO"

    def lora_stacker(self, lora_name_1, model_weight_1, clip_weight_1, switch_1, lora_name_2, model_weight_2, clip_weight_2, switch_2, lora_name_3, model_weight_3, clip_weight_3, switch_3, lora_stack=None):

        # Initialise the list
        lora_list=list()
        
        if lora_stack is not None:
            lora_list.extend([l for l in lora_stack if l[0] != "None"])
        
        if lora_name_1 != "None" and  switch_1 == "On":
            lora_list.extend([(lora_name_1, model_weight_1, clip_weight_1)]),

        if lora_name_2 != "None" and  switch_2 == "On":
            lora_list.extend([(lora_name_2, model_weight_2, clip_weight_2)]),

        if lora_name_3 != "None" and  switch_3 == "On":
            lora_list.extend([(lora_name_3, model_weight_3, clip_weight_3)]),
           
        return (lora_list,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_ControlNetStack:

    controlnets = ["None"] + folder_paths.get_filename_list("controlnet")
    
    @classmethod
    def INPUT_TYPES(cls):
        #controlnets = ["None"]
        return {"required": {
                },
                "optional": {
                    "image_1": ("IMAGE",),
                    "image_2": ("IMAGE",),
                    "image_3": ("IMAGE",),
                    "switch_1": ([
                        "Off",
                        "On"],),
                    "controlnet_1": (cls.controlnets,),
                    "controlnet_strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "start_percent_1": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    "end_percent_1": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    #
                    "switch_2": ([
                        "Off",
                        "On"],),
                    "controlnet_2": (cls.controlnets,),
                    "controlnet_strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "start_percent_2": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    "end_percent_2": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    #
                    "switch_3": ([
                        "Off",
                        "On"],),
                    "controlnet_3": (cls.controlnets,),
                    "controlnet_strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "start_percent_3": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    "end_percent_3": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    "controlnet_stack": ("CONTROL_NET_STACK",)
                },
        }

    RETURN_TYPES = ("CONTROL_NET_STACK",)
    RETURN_NAMES = ("CONTROLNET_STACK",)
    FUNCTION = "controlnet_stacker"
    CATEGORY = "Comfyroll/Conditioning"

    def controlnet_stacker(self, switch_1, controlnet_1, image_1, controlnet_strength_1, start_percent_1, end_percent_1, switch_2, controlnet_2, image_2, controlnet_strength_2, start_percent_2, end_percent_2, switch_3, controlnet_3, image_3, controlnet_strength_3, start_percent_3, end_percent_3, controlnet_stack=None):

        # Initialise the list
        controlnet_list=list()
        
        if controlnet_stack is not None:
            controlnet_list.extend([l for l in controlnet_stack if l[0] != "None"])
        
        if controlnet_1 != "None" and  switch_1 == "On":
            controlnet_list.extend([(controlnet_1, image_1, controlnet_strength_1)]),

        if controlnet_2 != "None" and  switch_2 == "On":
            controlnet_list.extend([(controlnet_2, image_2, controlnet_strength_2)]),

        if controlnet_3 != "None" and  switch_3 == "On":
            controlnet_list.extend([(controlnet_3, image_3, controlnet_strength_3)]),

        return (controlnet_list,)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_ApplyControlNetStack:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"base_positive": ("CONDITIONING", ),
                             "switch": ([
                                "Off",
                                "On"],),
                             "controlnet_stack": ("CONTROL_NET_STACK", ),
                            }
        }                    

    RETURN_TYPES = ("CONDITIONING", )
    RETURN_NAMES = ("base_pos", )
    FUNCTION = "apply_controlnet_stack"
    CATEGORY = "Comfyroll/Conditioning"

    def apply_controlnet_stack(self, base_positive, switch, controlnet_stack=None,):

        if switch == "Off":
            return (base_positive, )
    
        if controlnet_stack is not None:
            for controlnet_tuple in controlnet_stack:
                controlnet_name, image, strength = controlnet_tuple
                
                if type(controlnet_name) == str:
                    controlnet_path = folder_paths.get_full_path("controlnet", controlnet_name)
                    controlnet = comfy.sd.load_controlnet(controlnet_path)
                else:
                    controlnet = controlnet_name
                
                base_positive = ControlNetApply().apply_controlnet(base_positive, controlnet, image, strength)[0]

        return (base_positive,)


#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_BatchProcessSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["image", "image batch"],),
                "image": ("IMAGE", ),
                "image_batch": ("IMAGE", )
            }
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_NODE = True
    FUNCTION = "InputControlNet"

    CATEGORY = "Comfyroll/Process"

    def InputControlNet(self, Input, image, image_batch):
        if Input == "image":
            return (image, )
        else:
            return (image_batch, ) 


#---------------------------------------------------------------------------------------------------------------------------------------------------#


'''
NODE_CLASS_MAPPINGS = {
    "CR Image Input Switch": ComfyRoll_InputImages,
    "CR Image Input Switch (4 way)": ComfyRoll_InputImages_4way,
    "CR Latent Input Switch": ComfyRoll_InputLatents,
    "CR Process Switch": ComfyRoll_InputLatentsText,
    "CR Conditioning Input Switch": ComfyRoll_InputConditioning,
    "CR Clip Input Switch": ComfyRoll_InputClip,
    "CR Model Input Switch": ComfyRoll_InputModel,
    "CR ControlNet Input Switch": ComfyRoll_InputControlNet,
    "CR Load LoRA": ComfyRoll_LoraLoader,
    "CR Apply ControlNet": ComfyRoll_ApplyControlNet,
    "CR Image Size": ComfyRoll_ImageSize_Float,
    "CR Image Output": ComfyRoll_ImageOutput,
    "CR Integer Multiple": CR_Int_Multiple_Of,
    "CR Aspect Ratio": ComfyRoll_AspectRatio,
    "CR Aspect Ratio SDXL": ComfyRoll_AspectRatio_SDXL,
    "CR Seed to Int": ComfyRoll_SeedToInt,
    "CR Color Tint": Comfyroll_Color_Tint,
    "CR SDXL Prompt Mixer": ComfyRoll_prompt_mixer,
    "CR SDXL Style Text": Comfyroll_SDXLStyleText,
    "CR SDXL Base Prompt Encoder": Comfyroll_SDXLBasePromptEncoder, 
    "CR Hires Fix Process Switch": ComfyRoll_HiResFixSwitch,
    "CR Halftones" :Comfyroll_Halftone_Grid,
    "CR LoRA Stack":Comfyroll_LoRA_Stack,
    "CR Apply LoRA Stack":Comfyroll_ApplyLoRA_Stack,
    "CR Latent Batch Size":Comfyroll_LatentBatchSize
    "CR Batch Process Switch": Comfyroll_BatchProcessSwitch,
    "CR Multi-ControlNet Stack":Comfyroll_ControlNetStack,
    "CR Apply Multi-ControlNet":Comfyroll_ApplyControlNetStack,
    "CR SDXL Prompt Mix Presets": Comfyroll_prompt_mixer_v2,
    "CR Seed":Comfyroll_Seed,
}
'''

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Credits                                                                                                                                           #
# WASasquatch                             https://github.com/WASasquatch/was-node-suite-comfyui                                                     #
# hnmr293				                  https://github.com/hnmr293/ComfyUI-nodes-hnmr      		                                                #
# SeargeDP                                https://github.com/SeargeDP/SeargeSDXL                                                                    #
# LucianoCirino                           https://github.com/LucianoCirino/efficiency-nodes-comfyui                                                 #
# credit SLAPaper                         https://github.com/SLAPaper/ComfyUI-Image-Selector                                                        #
#---------------------------------------------------------------------------------------------------------------------------------------------------#


