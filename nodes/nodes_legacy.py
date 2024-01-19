#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

from ..categories import icons
         
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageSize:
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
    RETURN_TYPES = ("INT", "INT", "FLOAT", "STRING", )
    RETURN_NAMES = ("Width", "Height", "upscale_factor", "show_help", )
    FUNCTION = "ImageSize"
    CATEGORY = icons.get("Comfyroll/Essential/Legacy")

    def ImageSize(self, width, height, upscale_factor):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Legacy-Nodes#cr-image-size"
        return(width, height, upscale_factor, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
class CR_AspectRatio_SDXL:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "aspect_ratio": (["custom", "1:1 square 1024x1024", "3:4 portrait 896x1152", "5:8 portrait 832x1216", "9:16 portrait 768x1344",
                "9:21 portrait 640x1536", "4:3 landscape 1152x896", "3:2 landscape 1216x832", "16:9 landscape 1344x768", "21:9 landscape 1536x640"],),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor1": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "upscale_factor2": ("FLOAT", {"default": 1, "min": 1, "max": 2000}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT", "INT", "STRING", )
    RETURN_NAMES = ("INT", "INT", "FLOAT", "FLOAT", "INT", "show_help", )
    #RETURN_NAMES = ("Width", "Height")
    FUNCTION = "Aspect_Ratio"

    CATEGORY = icons.get("Comfyroll/Essential/Legacy")

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor1, upscale_factor2, batch_size):
       
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Legacy-Nodes#cr-aspect-ratio-sdxl"

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
            return(height, width, upscale_factor1, upscale_factor2, batch_size,show_help,)
        else:
            return(width, height, upscale_factor1, upscale_factor2, batch_size,show_help,)        

#---------------------------------------------------------------------------------------------------------------------------------------------------#
class CR_PromptMixer:
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

    CATEGORY = icons.get("Comfyroll/Essential/Legacy")

    def mixer(self, prompt_positive, prompt_negative, style_positive, style_negative, preset):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Legacy-Nodes#cr-prompt-mixer"

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
class CR_SeedToInt:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("SEED", ),
            }
        }

    RETURN_TYPES = ("INT", "STRING", )
    RETURN_NAMES = ("INT", "show_help", )
    FUNCTION = "seed_to_int"
    CATEGORY = icons.get("Comfyroll/Essential/Legacy")

    def seed_to_int(self, seed):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Conversion-Nodes#cr-seed-to-int"
        return (seed.get('seed'), show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Image Size": CR_ImageSize,
    "CR Aspect Ratio SDXL": CR_AspectRatio_SDXL,
    "CR SDXL Prompt Mixer": CR_PromptMixer,     
    "CR Seed to Int": CR_SeedToInt,     
}
'''

