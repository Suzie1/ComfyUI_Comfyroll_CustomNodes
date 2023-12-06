#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi         https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             #
# for ComfyUI                                               https://github.com/comfyanonymous/ComfyUI                                               #
#---------------------------------------------------------------------------------------------------------------------------------------------------#

from ..categories import icons
         
#---------------------------------------------------------------------------------------------------------------------------------------------------#
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
    CATEGORY = icons.get("Comfyroll/Other/Legacy")

    def ImageSize(self, width, height, upscale_factor):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Legacy-Nodes#cr-image-size"
        return(width, height, upscale_factor, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------------------------------------#
class CR_AspectRatio_SDXL:
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
    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT", "INT", "STRING", )
    RETURN_NAMES = ("INT", "INT", "FLOAT", "FLOAT", "INT", "show_help", )
    #RETURN_NAMES = ("Width", "Height")
    FUNCTION = "Aspect_Ratio"

    CATEGORY = icons.get("Comfyroll/Other/Legacy")

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
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Legacy-Nodes#cr-aspect-ratio-sdxl"

        if swap_dimensions == "On":
            return(height, width, upscale_factor1, upscale_factor2, batch_size,show_help,)
        else:
            return(width, height, upscale_factor1, upscale_factor2, batch_size,show_help,)        

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Image Size": CR_ImageSize,
    "CR Aspect Ratio SDXL": CR_AspectRatio_SDXL,
}
'''

