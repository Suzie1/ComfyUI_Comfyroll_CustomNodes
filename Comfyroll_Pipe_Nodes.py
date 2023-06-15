#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Comfyroll Pipe Nodes by Akatsuzi                          https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             #
# for ComfyUI                                               https://github.com/comfyanonymous/ComfyUI                                               #
#---------------------------------------------------------------------------------------------------------------------------------------------------#

import os
import sys
import json
import torch
import comfy.sd
import comfy.utils
import numpy as np

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class module_pipe_loader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                #"model": ("MODEL",),
            },
            "optional": {
                "model": ("MODEL",),
                "pos": ("CONDITIONING",),
                "neg": ("CONDITIONING",),
                "latent": ("LATENT",),
                "vae": ("VAE",),
                "clip": ("CLIP",),
                "controlnet": ("CONTROL_NET",),
                "image": ("IMAGE",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})            
            },
        }

    RETURN_TYPES = ("PIPE_LINE", )
    RETURN_NAMES = ("pipe", )
    FUNCTION = "flush"

    CATEGORY = "Comfyroll/Module"

    def flush(self, model=0, pos=0, neg=0, latent=0, vae=0, clip=0, controlnet=0, image=0, seed=0):
        pipe_line = (model, pos, neg, latent, vae, clip, controlnet, image, seed)
        return (pipe_line, )
        
#---------------------------------------------------------------------------------------------------------------------------------------------------#       
        
class module_input:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"pipe": ("PIPE_LINE",)},
            }

    RETURN_TYPES = ("PIPE_LINE", "MODEL", "CONDITIONING", "CONDITIONING", "LATENT", "VAE", "CLIP", "CONTROL_NET", "IMAGE", "INT")
    RETURN_NAMES = ("pipe", "model", "pos", "neg", "latent", "vae", "clip", "controlnet", "image", "seed")
    FUNCTION = "flush"

    CATEGORY = "Comfyroll/Module"
    
    def flush(self, pipe):
        model, pos, neg, latent, vae, clip, controlnet, image, seed = pipe
        return pipe, model, pos, neg, latent, vae, clip, controlnet, image, seed

#---------------------------------------------------------------------------------------------------------------------------------------------------#
 
class module_output:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"pipe": ("PIPE_LINE",)},
                "optional": {
                    "model": ("MODEL",),
                    "pos": ("CONDITIONING",),
                    "neg": ("CONDITIONING",),
                    "latent": ("LATENT",),
                    "vae": ("VAE",),
                    "clip": ("CLIP",),
                    "controlnet": ("CONTROL_NET",),
                    "image": ("IMAGE",),
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
                },
            }

    RETURN_TYPES = ("PIPE_LINE", )
    RETURN_NAMES = ("pipe", )
    FUNCTION = "flush"

    CATEGORY = "Comfyroll/Module"

    def flush(self, pipe, model=None, pos=None, neg=None, latent=None, vae=None, clip=None, controlnet=None, image=None, seed=None):
        new_model, new_pos, new_neg, new_latent, new_vae, new_clip, new_controlnet, new_image, new_seed = pipe

        if model is not None:
            new_model = model
        
        if pos is not None:
            new_pos = pos

        if neg is not None:
            new_neg = neg

        if latent is not None:
            new_latent = latent

        if vae is not None:
            new_vae = vae

        if clip is not None:
            new_clip = clip
            
        if controlnet is not None:
            new_controlnet = controlnet
            
        if image is not None:
            new_image = image
            
        if seed is not None:
            new_seed = seed
       
        pipe = new_model, new_pos, new_neg, new_latent, new_vae, new_clip, new_controlnet, new_image, new_seed
        return (pipe, )
        
#---------------------------------------------------------------------------------------------------------------------------------------------------#
        
class image_pipe_in:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                #"model": ("MODEL",),
            },
            "optional": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000})
            },
        }

    RETURN_TYPES = ("PIPE_LINE", )
    RETURN_NAMES = ("pipe", )
    FUNCTION = "flush"

    CATEGORY = "Comfyroll/Module"

    def flush(self, image=0, width=0, height=0, upscale_factor=0):
        pipe_line = (image, width, height, upscale_factor)
        return (pipe_line, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class image_pipe_edit:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"pipe": ("PIPE_LINE",)},
                "optional": {
                    "image": ("IMAGE",),
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000})
                },
            }

    RETURN_TYPES = ("PIPE_LINE", )
    RETURN_NAMES = ("pipe", )
    FUNCTION = "flush"

    CATEGORY = "Comfyroll/Module"

    def flush(self, pipe, image=None, width=None, height=None, upscale_factor=None):
        new_image, new_width, new_height, new_upscale_factor = pipe

        if image is not None:
            new_image = image
            
        if width is not None:
            new_width = width
            
        if height is not None:
            new_height = height

        if upscale_factor is not None:
            new_upscale_factor = upscale_factor
            
        pipe = new_image, new_width, new_height, new_upscale_factor
        return (pipe, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class image_pipe_out:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"pipe": ("PIPE_LINE",)},
            }

    RETURN_TYPES = ("PIPE_LINE", "IMAGE", "INT", "INT", "FLOAT",)
    RETURN_NAMES = ("pipe", "image", "width", "height", "upscale_factor")
    FUNCTION = "flush"

    CATEGORY = "Comfyroll/Module"
    
    def flush(self, pipe):
        #if switch == "Off":
            #return (pipe, )
        #else:  
            image, width, height, upscale_factor = pipe
            return pipe, image, width, height, upscale_factor

#---------------------------------------------------------------------------------------------------------------------------------------------------#

class input_switch_pipe:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "pipe1": ("PIPE_LINE",),
                "pipe2": ("PIPE_LINE",)
            }
        }

    RETURN_TYPES = ("PIPE_LINE",)
    OUTPUT_NODE = True
    FUNCTION = "InputSwitchPipe"

    CATEGORY = "Comfyroll/Module"

    def InputSwitchPipe(self, Input, pipe1, pipe2):
        if Input == 1:
            return (pipe1, )
        else:
            return (pipe2, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#
'''
NODE_CLASS_MAPPINGS_2 = {
    "CR Module Pipe Loader": module_pipe_loader,
    "CR Module Input": module_input,
    "CR Module Output": module_output,
    "CR Image Pipe In": image_pipe_in,
    "CR Image Pipe Edit": image_pipe_edit,
    "CR Image Pipe Out": image_pipe_out,
    "CR Pipe Switch": input_switch_pipe,
}
'''
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Credits   
# TinyTerra                               https://github.com/TinyTerra/ComfyUI_tinyterraNodes                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------------------#
