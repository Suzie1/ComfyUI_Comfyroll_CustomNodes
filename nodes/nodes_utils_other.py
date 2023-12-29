#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
# Maths Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_ClampValue:
       
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
                "range_min": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
                "range_max": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
            }
        }
    
    RETURN_TYPES =("FLOAT", "STRING", )
    RETURN_NAMES =("a", "show_help", )
    FUNCTION = "clamp_value"    
    CATEGORY = icons.get("Comfyroll/Utils/Other")
    
    def clamp_value(self, a, range_min, range_max):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-clamp-value"

        a = max(range_min, min(a, range_max))        
        
        return (a, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SetValueOnBoolean:
       
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "boolean_number": ("INT", {"default": 1, "min": 0, "max": 1}),
                "value_if_true": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),   
                "value_if_false": ("FLOAT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),   
            }
        }
    
    RETURN_TYPES =("INT", "FLOAT", "STRING", )
    RETURN_NAMES =("INT", "FLOAT", "show_help", )
    FUNCTION = "set_value"    
    CATEGORY = icons.get("Comfyroll/Utils/Other")
    
    def set_value(self, boolean_number, value_if_true, value_if_false):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-set-value-on-boolean"

        if boolean_number == 1:
            return (int(value_if_true), value_if_true, show_help, )   
        else:
            return (int(value_if_false), value_if_false, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_IntegerMultipleOf:
       
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
    CATEGORY = icons.get("Comfyroll/Utils/Other")
    
    def int_multiple_of(self, integer, multiple=8):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-integer-multiple"
        
        if multiple == 0:
            return (int(integer), show_help, )
        integer = integer * multiple   
        
        return (int(integer), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Value:

    @classmethod
    def INPUT_TYPES(cls):  
        return {"required": {"value": ("FLOAT", {"default": 1.0,},)}}

    RETURN_TYPES = ("FLOAT", "INT", "STRING", )
    RETURN_NAMES = ("FLOAT", "INT", "show_help", )
    CATEGORY = icons.get("Comfyroll/Other")
    FUNCTION = "get_value"

    def get_value(self, value):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-value"
        
        return (float(value), int(value), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### Utility Other
    "CR Integer Multiple": CR_IntegerMultipleOf,
    "CR Clamp Value": CR_ClampValue,
    "CR Set Value On Boolean": CR_SetValueOnBoolean,
    "CR Value": CR_Value,    
}
'''

