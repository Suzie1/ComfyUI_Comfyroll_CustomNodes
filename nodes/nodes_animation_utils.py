#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/Suzie1/CR-Animation-Nodes 
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
  
class CR_DebatchFrames:
   # cloned from ltdrdata Image Batch To Image List node
   
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "frames": ("IMAGE",), } }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("debatched_frames",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "debatch"
    CATEGORY = icons.get("Comfyroll/Animation/Utils")

    def debatch(self, frames):
        images = [frames[i:i + 1, ...] for i in range(frames.shape[0])]
        return (images, )

#---------------------------------------------------------------------------------------------------------------------# 
class CR_CurrentFrame:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "index": ("INT", {"default": 1, "min": -10000, "max": 10000}),
                    "print_to_console": (["Yes","No"],),
                    }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("index",)
    FUNCTION = "to_console"
    CATEGORY = icons.get("Comfyroll/Animation/Utils")
    
    def to_console(self, index, print_to_console):
        if print_to_console == "Yes":
            print(f"[Info] CR Current Frame:{index}")
            
        return (index, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 8 nodes
'''
NODE_CLASS_MAPPINGS = {
    # Utils
    "CR Debatch Frames":CR_DebatchFrames,    
    "CR Current Frame":CR_CurrentFrame,
}
'''

