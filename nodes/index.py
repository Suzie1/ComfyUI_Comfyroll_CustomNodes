#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Nodes by RockOfFire and Akatsuzi      https://github.com/RockOfFire/CR-Animation-Nodes
# for ComfyUI                                     https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#
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
    CATEGORY = "Comfyroll/Utils/Index"

    def trigger(self, index, trigger_value):

        return (index, index == trigger_value,)

#---------------------------------------------------------------------------------------------------------------------
class CR_Index: 

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"index": ("INT", {"default": 1, "min": 0, "max": 10000}),
                             "print_to_console": (["Yes","No"],),        
                },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "index"
    CATEGORY = "Comfyroll/Utils/Index"

    def index(self, index, print_to_console):
    
        if print_to_console == "Yes":
            print(f"[Info] CR Index:{index}")

        return (index,)

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
    CATEGORY = "Comfyroll/Utils/Index"
    
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
    CATEGORY = "Comfyroll/Utils/Index"
    
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
    CATEGORY = "Comfyroll/Utils/Index"
    
    def reset(self, index, reset_to):
        index = reset_to
        return (index, reset_to)    
 
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    # Index
    "CR Index":CR_Index,    
    "CR Index Increment":CR_IncrementIndex,
    "CR Index Multiply":CR_MultiplyIndex,
    "CR Index Reset":CR_IndexReset,
    "CR Trigger":CR_Trigger,    
}
'''    
     
