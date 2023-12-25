#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
from PIL import Image, ImageEnhance
import os
import sys
import folder_paths
from nodes import MAX_RESOLUTION, ControlNetApply
from ..categories import icons

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------#
# SDXL Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_PromptMixPresets:
    def __init__(self):
        pass

    @classmethod        
    def INPUT_TYPES(s):
        return {
            "required":{
            },
            "optional":{
                "prompt_positive": ("STRING", {"multiline": True, "default": "prompt_pos"}),
                "prompt_negative": ("STRING", {"multiline": True, "default": "prompt_neg"}),
                "style_positive": ("STRING", {"multiline": True, "default": "style_pos"}),
                "style_negative": ("STRING", {"multiline": True, "default": "style_neg"}),
                "preset": (["default with no style text", "default with style text",
                            "style boost 1", "style boost 2", "style text to refiner"],),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("pos_g", "pos_l", "pos_r", "neg_g", "neg_l", "neg_r", "show_help", )
    FUNCTION = "mixer"
    CATEGORY = icons.get("Comfyroll/SDXL")

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
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/SDXL-Nodes#cr-sdxl-prompt-mix-presets"            
        return (pos_g, pos_l, pos_r, neg_g, neg_l, neg_r, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SDXLStyleText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "positive_style": ("STRING", {"default": "POS_STYLE", "multiline": True}),
                    "negative_style": ("STRING", {"default": "NEG_STYLE", "multiline": True}),
                    },
                }

    RETURN_TYPES = ("STRING", "STRING", "STRING", )
    RETURN_NAMES = ("positive_prompt_text_l", "negative_prompt_text_l" , "show_help", )
    FUNCTION = "get_value"
    CATEGORY = icons.get("Comfyroll/SDXL")

    def get_value(self, positive_style, negative_style):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/SDXL-Nodes#cr-sdxl-style-text"
        return (positive_style, negative_style, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SDXLBasePromptEncoder:
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

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", )
    RETURN_NAMES = ("base_positive", "base_negative", "show_help", )
    FUNCTION = "encode"
    CATEGORY = icons.get("Comfyroll/SDXL")

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
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/SDXL-Nodes#cr-sdxl-base-prompt-encoder"
        return (base_positive, base_negative, show_help, )
               
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py            
'''
NODE_CLASS_MAPPINGS = {
    "CR SDXL Style Text":CR_SDXLStyleText,
    "CR SDXL Base Prompt Encoder":CR_SDXLBasePromptEncoder, 
    "CR SDXL Prompt Mix Presets":CR_PromptMixPresets,
}
'''            

