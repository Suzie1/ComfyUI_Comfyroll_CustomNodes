#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi         https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             #
# for ComfyUI                                               https://github.com/comfyanonymous/ComfyUI                                               #
#---------------------------------------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
from PIL import Image, ImageEnhance
import os
import sys
import pip

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

import folder_paths
from nodes import MAX_RESOLUTION, ControlNetApply
import typing as tg

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# NODES
#---------------------------------------------------------------------------------------------------------------------------------------------------#

class Comfyroll_prompt_mixer:
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

class Comfyroll_AspectRatio_SDXL:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "aspect_ratio": (["custom", "1:1 square 1024x1024", "3:4 portrait 896x1152", "5:8 portrait 832x1216", "9:16 portrait 768x1344", "9:21 portrait 640x1536", "4:3 landscape 1152x896", "3:2 landscape 1216x832", "16:9 landscape 1344x768", "21:9 landscape 1536x640"],),
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
                "aspect_ratio": (["custom", "1:1 square 1024x1024", "3:4 portrait 896x1152", "5:8 portrait 832x1216", "9:16 portrait 768x1344", "9:21 portrait 640x1536", "4:3 landscape 1152x896", "3:2 landscape 1216x832", "16:9 landscape 1344x768", "21:9 landscape 1536x640"],),
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
            return(height, width, upscale_factor, batch_size,)
        else:
            return(width, height, upscale_factor, batch_size,)        

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------------------------------------#



            
'''
NODE_CLASS_MAPPINGS = {
    "CR Aspect Ratio SDXL": Comfyroll_AspectRatio_SDXL,
    "CR SDXL Prompt Mixer": Comfyroll_prompt_mixer,
    "CR SDXL Style Text": Comfyroll_SDXLStyleText,
    "CR SDXL Base Prompt Encoder": Comfyroll_SDXLBasePromptEncoder, 
    "CR SDXL Prompt Mix Presets": Comfyroll_prompt_mixer_v2,
    "CR SDXL Aspect Ratio":Comfyroll_SDXL_AspectRatio_v2,
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


