#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Nodes by RockOfFire and Akatsuzi      https://github.com/RockOfFire/CR-Animation-Nodes
# for ComfyUI                                     https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#
# NODES
#---------------------------------------------------------------------------------------------------------------------
class CR_StringToNumber: 

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": False, "default": "text"}),                             
                },
        }

    RETURN_TYPES = ("INT", "FLOAT",)   
    FUNCTION = "convert"
    CATEGORY = "Comfyroll/Text"

    def convert(self, text):

        # Check if number
        if text.replace('.','',1).isdigit():
            float_out = float(text)
            int_out = int(float_out)
        else:
            print(f"[Error] CR String To Number. Not a number.")         
        
        return (int_out, float_out,)
        
#---------------------------------------------------------------------------------------------------------------------
class CR_SplitString:

    @classmethod
    def INPUT_TYPES(s):  
    
        return {"required": {"text": ("STRING", {"multiline": False, "default": "text"}),
                             "delimiter": ("STRING", {"multiline": False, "default": ","}), 
                },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("string_1", "string_2", "string_3", "string_4",)    
    FUNCTION = "split"
    CATEGORY = "Comfyroll/Text"

    def split(self, text, delimiter):

        # Split the text string
        parts = text.split(delimiter)
        strings = [part.strip() for part in parts[:4]]
        string_1, string_2, string_3, string_4 = strings + [""] * (4 - len(strings))            

        return (string_1, string_2, string_3, string_4)

#---------------------------------------------------------------------------------------------------------------------
class CR_Trigger: 

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"index": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "trigger_value": ("INT", {"default": 1, "min": 0, "max": 10000}),        
                },
        }

    RETURN_TYPES = ("INT", "BOOLEAN",)
    RETURN_NAMES = ("index", "trigger", )
    FUNCTION = "trigger"
    CATEGORY = "Comfyroll/Utils"

    def trigger(self, index, trigger_value):

        return (index, index == trigger_value,)

#---------------------------------------------------------------------------------------------------------------------
class CR_Index: 

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"index": ("INT", {"default": 1, "min": 0, "max": 10000}),        
                },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "index"
    CATEGORY = "Comfyroll/Utils"

    def index(self, index):

        return (index,)

#---------------------------------------------------------------------------------------------------------------------
class CR_FloatToInteger:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"_float": ("FLOAT", {"default": 0.0})}}

    RETURN_TYPES = ("INT",)
    FUNCTION = "convert"
    CATEGORY = "Comfyroll/Utils"

    def convert(self, _float):
        return (int(_float),)

#---------------------------------------------------------------------------------------------------------------------
class CR_IncrementIndex:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "index": ("INT", {"default": 1, "min": -10000, "max": 10000}),
                    "interval": ("INT", {"default": 1, "min": -10000, "max": 10000}),
                    }
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("index", "interval")
    FUNCTION = "increment"
    CATEGORY = "Comfyroll/Utils"
    
    def increment(self, index, interval):
        index+=interval
        return (index, )

#---------------------------------------------------------------------------------------------------------------------#   
class CR_MultiplyIndex:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "index": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    "factor": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    }
        }


    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("index", "factor")
    FUNCTION = "multiply"
    CATEGORY = "Comfyroll/Utils"
    
    def multiply(self, index, factor):
        index = index * factor
        return (index, factor) 

#---------------------------------------------------------------------------------------------------------------------#   
class CR_IndexReset:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "index": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    "reset_to": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    }
        }


    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("index", "reset_to")
    FUNCTION = "reset"
    CATEGORY = "Comfyroll/Utils"
    
    def reset(self, index, reset_to):
        index = reset_to
        return (index, reset_to)    

#---------------------------------------------------------------------------------------------------------------------# 
class CR_TextListToString:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                "text_list": ("STRING", {"forceInput": True}),
                    },
                }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("STRING", )
    FUNCTION = "joinlist"
    CATEGORY = "Comfyroll/Text"

    def joinlist(self, text_list):
    
        string_out = " ".join(text_list)
        
        return (string_out,)

#---------------------------------------------------------------------------------------------------------------------#  
# based on Repeater node by pythongosssss 
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

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
    CATEGORY = "Comfyroll/Text"

    def convert(self, text):
    
        text_list = list()
        
        if text != "":
            values = text.split(',')
            text_list = values[0]
            print(text_list)
        
        return (text_list, )
 
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 10 nodes published
'''
NODE_CLASS_MAPPINGS = {
    # Index
    "CR Index":CR_Index,    
    "CR Index Increment":CR_IncrementIndex,
    "CR Index Multiply":CR_MultiplyIndex,
    "CR Index Reset":CR_IndexReset,
    "CR Trigger":CR_Trigger,    
    # Utils  
    "CR Text List To String":CR_TextListToString,
    "CR String To Combo":CR_StringToCombo, 
    "CR String To Number":CR_StringToNumber,
    "CR Split String":CR_SplitString,  
    "CR Float To Integer":CR_FloatToInteger,
}
'''    
     
