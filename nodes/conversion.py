#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Nodes by RockOfFire and Akatsuzi      https://github.com/RockOfFire/CR-Animation-Nodes
# for ComfyUI                                     https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

from ..categories import icons

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

#---------------------------------------------------------------------------------------------------------------------# 
class CR_StringToNumber: 

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": False, "default": "text"}),                             
                },
        }

    RETURN_TYPES = ("INT", "FLOAT",)   
    FUNCTION = "convert"
    CATEGORY = icons.get("Comfyroll/Utils/Conversion")

    def convert(self, text):

        # Check if number
        if text.replace('.','',1).isdigit():
            float_out = float(text)
            int_out = int(float_out)
        else:
            print(f"[Error] CR String To Number. Not a number.")         
        
        return (int_out, float_out,)
        
#---------------------------------------------------------------------------------------------------------------------# 
class CR_TextListToString:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                "text_list": ("STRING", {"forceInput": True}),
                    },
                }

    RETURN_TYPES = ("STRING", )
    FUNCTION = "joinlist"
    CATEGORY = icons.get("Comfyroll/Utils/Conversion")

    def joinlist(self, text_list):
    
        string_out = " ".join(text_list)
        
        return (string_out,)

#---------------------------------------------------------------------------------------------------------------------#  
# based on Repeater node by pythongosssss 
class CR_StringToCombo:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": False, "default": "", "forceInput": True}),
            },
        }

    RETURN_TYPES = (any,)
    FUNCTION = "convert"
    CATEGORY = icons.get("Comfyroll/Utils/Conversion")

    def convert(self, text):
    
        text_list = list()
        
        if text != "":
            values = text.split(',')
            text_list = values[0]
            print(text_list)
        
        return (text_list, )
        
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Cloned from Mikey Nodes
class CR_IntegerToString:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"int_": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                }
        }

    RETURN_TYPES = ('STRING',)
    FUNCTION = 'convert'
    CATEGORY = icons.get("Comfyroll/Utils/Conversion")

    def convert(self, int_):
        return (f'{int_}', )

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Cloned from Mikey Nodes
class CR_FloatToString:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"float_": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1000000.0}),
                }        
        }

    RETURN_TYPES = ('STRING',)
    FUNCTION = 'convert'
    CATEGORY = icons.get("Comfyroll/Utils/Conversion")

    def convert(self, float_):
        return (f'{float_}', )

#---------------------------------------------------------------------------------------------------------------------
class CR_FloatToInteger:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"_float": ("FLOAT", {"default": 0.0})}}

    RETURN_TYPES = ("INT",)
    FUNCTION = "convert"
    CATEGORY = icons.get("Comfyroll/Utils/Conversion")

    def convert(self, _float):
        return (int(_float),)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# This node is used to convert type Seed to type INT
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

    RETURN_TYPES = ("INT",)
    FUNCTION = "seed_to_int"
    CATEGORY = icons.get("Comfyroll/Utils/Conversion")

    def seed_to_int(self, seed):
        return (seed.get('seed'),)
 
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 10 nodes published
'''
NODE_CLASS_MAPPINGS = {   
    "CR String To Number":CR_StringToNumber,
    "CR String To Combo":CR_StringToCombo,    
    "CR Float To String":CR_FloatToString,
    "CR Float To Integer":CR_FloatToInteger,
    "CR Integer To String":CR_IntegerToString,    
    "CR Text List To String":CR_TextListToString,
    "CR Seed to Int": CR_SeedToInt, 
}
'''    
     
