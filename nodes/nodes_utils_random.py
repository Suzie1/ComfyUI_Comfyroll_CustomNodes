#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import random
import string
from .functions_graphics import random_hex_color, random_rgb
from ..categories import icons

try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
except ImportError:
    import pip
    pip.main(['install', 'matplotlib'])
    
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class AnyType(str):
    # Credit to pythongosssss    

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

#---------------------------------------------------------------------------------------------------------------------#
# Random values
#---------------------------------------------------------------------------------------------------------------------#
class CR_RandomHexColor:
    
    @classmethod
    def INPUT_TYPES(cls):
        
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),}}

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("hex_color1", "hex_color2", "hex_color3", "hex_color4", "show_help", )
    FUNCTION = "get_colors"
    CATEGORY = icons.get("Comfyroll/Utils/Random")

    def get_colors(self, seed):
    
        # Set the seed
        random.seed(seed)
    
        hex_color1 = random_hex_color()
        hex_color2 = random_hex_color()
        hex_color3 = random_hex_color()
        hex_color4 = random_hex_color()
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-random-hex-color"
             
        return (hex_color1, hex_color2, hex_color3, hex_color4, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_RandomRGB:
    
    @classmethod
    def INPUT_TYPES(cls):
        
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),}}

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("rgb_1", "rgb_2", "rgb_3", "rgb_4", "show_help", )
    FUNCTION = "get_colors"
    CATEGORY = icons.get("Comfyroll/Utils/Random")

    def get_colors(self, seed):
    
        # Set the seed
        random.seed(seed)
    
        rgb_1 = random_rgb()
        rgb_2 = random_rgb()
        rgb_3 = random_rgb()
        rgb_4 = random_rgb()
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-random-rgb"
             
        return (rgb_1, rgb_2, rgb_3, rgb_4, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_RandomMultilineValues:
    
    @classmethod
    def INPUT_TYPES(cls):
    
        types = ["binary", "decimal", "natural", "hexadecimal", "alphabetic", "alphanumeric", "custom"]
        
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                             "value_type": (types,),
                             "rows": ("INT", {"default": 5, "min": 1, "max": 2048}),
                             "string_length": ("INT", {"default": 5, "min": 1, "max": 1024}),
                             "custom_values": ("STRING", {"multiline": False, "default": "123ABC"}),
                             "prepend_text": ("STRING", {"multiline": False, "default": ""}),
               }
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("multiline_text", "show_help", )
    FUNCTION = "generate"
    CATEGORY = icons.get("Comfyroll/Utils/Random")

    def generate(self, value_type, rows, string_length, custom_values, seed, prepend_text):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-random-multiline-values"
        
        # Set the seed
        random.seed(seed)
        
        if value_type == "binary":
            choice_str = '01'
        elif value_type == "decimal":
            choice_str = '0123456789'
        elif value_type == "natural":
            choice_str = '123456789'             
        elif value_type == "hexadecimal":
            choice_str = '0123456789ABCDEF'       
        elif value_type == "alphabetic":
            choice_str = string.ascii_letters
        elif value_type == "alphanumeric":
            choice_str = string.ascii_letters + string.digits           
        elif value_type == "custom":
            choice_str = custom_values
        else:
            pass

        multiline_text = '\n'.join([prepend_text + ''.join(random.choice(choice_str) for _ in range(string_length)) for _ in range(rows)]) 
                           
        return (multiline_text, show_help, )

#---------------------------------------------------------------------------------------------------------------------#

class CR_RandomMultilineColors:
    
    @classmethod
    def INPUT_TYPES(cls):
    
        types = ["rgb", "hex color", "matplotlib xkcd"]
        
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                             "value_type": (types,),
                             "rows": ("INT", {"default": 5, "min": 1, "max": 2048}),
               }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("multiline_text", "show_help", )
    FUNCTION = "generate"
    CATEGORY = icons.get("Comfyroll/Utils/Random")

    def generate(self, value_type, rows, seed):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-random-multiline-colors"
        
        # Set the seed
        random.seed(seed)
        
        # Get the list of XKCD color names
        xkcd_colors = mcolors.XKCD_COLORS
        
        if value_type == "hex color":
            choice_str = '0123456789ABCDEF'

        if value_type == "hex color":
            multiline_text = '\n'.join(['#' + ''.join(random.choice(choice_str) for _ in range(6)) for _ in range(rows)]) 
        elif value_type == "rgb":
            multiline_text = '\n'.join([f'{random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)}' for _ in range(rows)])
        elif value_type == "matplotlib xkcd":
            multiline_text = '\n'.join([random.choice(list(xkcd_colors.keys())).replace('xkcd:', '') for _ in range(rows)])   
        else:
            pass
                   
        return (multiline_text, show_help, )

#---------------------------------------------------------------------------------------------------------------------#

class CR_RandomPanelCodes:
    
    @classmethod
    def INPUT_TYPES(cls):
            
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                             "rows": ("INT", {"default": 5, "min": 1, "max": 2048}),
                             "string_length": ("INT", {"default": 5, "min": 1, "max": 1024}),
                             "values": ("STRING", {"multiline": False, "default": "123"}),
               }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("multiline_text", "show_help", )
    FUNCTION = "generate"
    CATEGORY = icons.get("Comfyroll/Utils/Random")

    def generate(self, rows, string_length, values, seed):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-random-panel-codes"
        
        # Set the seed
        random.seed(seed)
        
        start_letter = random.choice('HV')
        value_range = random.choice(values)
            
        codes = []
        for _ in range(rows):
            # Generate a random number within the specified range
            number = ''.join(random.choice(values) for _ in range(string_length))
            # Append the code to the list
            codes.append(f"{start_letter}{number}")
            
        multiline_text = '\n'.join(codes)   
                 
        return (multiline_text, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_RandomRGBGradient:
    
    @classmethod
    def INPUT_TYPES(cls):
    
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                             "rows": ("INT", {"default": 5, "min": 1, "max": 2048}),
               }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("multiline_text", "show_help", )
    FUNCTION = "generate"
    CATEGORY = icons.get("Comfyroll/Utils/Random")

    def generate(self, rows, seed):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-random-RGB-gradient"
    
        # Set the seed
        random.seed(seed)
        
        temp = 0
        multiline_text = ""
         
        for i in range(1, rows + 1):
            print(temp)
            if temp <= 99 - rows + i:
                upper_bound = min(99, temp + (99 - temp) // (rows - i + 1))
                current_value = random.randint(temp, upper_bound)
                multiline_text += f'{current_value}:{random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)}\n'
                
                temp = current_value + 1

        return (multiline_text, show_help, )
                     
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    # Random
    "CR Random Hex Color": CR_RandomHexColor, 
    "CR Random RGB": CR_RandomRGB,
    "CR Random Multiline Values": CR_RandomMultilineValues,
    "CR Random Multiline Colors": CR_RandomMultilineColors,
    "CR Random RGB Gradient": CR_RandomRGBGradient,
    "CR Random Panel Codes": CR_RandomPanelCodes,    
}
'''

