#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi   https://github.com/RockOfFire/CR-Animation-Nodes
# for ComfyUI                                     https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

import torch
from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
class CR_EncodeScheduledPrompts:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"clip": ("CLIP",),
                             "current_prompt": ("STRING", {"multiline": True}),
                             "next_prompt": ("STRING", {"multiline": True}),
                             "weight": ("FLOAT", {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01,}),
                            }
        }
    
    RETURN_TYPES = ("CONDITIONING", )
    RETURN_NAMES = ("CONDITIONING",)
    FUNCTION = "condition"
    CATEGORY = icons.get("Comfyroll/Animation/Conditioning")

    def condition(self, clip, current_prompt, next_prompt, weight):      
        
        # CLIP text encoding
        tokens = clip.tokenize(str(next_prompt))
        cond_from, pooled_from = clip.encode_from_tokens(tokens, return_pooled=True)
        tokens = clip.tokenize(str(current_prompt))
        cond_to, pooled_to = clip.encode_from_tokens(tokens, return_pooled=True)
        
        #return (addWeighted([[cond_to, {"pooled_output": pooled_to}]], [[cond_from, {"pooled_output": pooled_from}]], weight),)
        print(weight)
        
        # Average conditioning
        conditioning_to_strength = weight
        conditioning_from = [[cond_from, {"pooled_output": pooled_from}]]
        conditioning_to = [[cond_to, {"pooled_output": pooled_to}]]
        out = []

        if len(conditioning_from) > 1:
            print("Warning: Conditioning from contains more than 1 cond, only the first one will actually be applied to conditioning_to.")

        cond_from = conditioning_from[0][0]
        pooled_output_from = conditioning_from[0][1].get("pooled_output", None)

        for i in range(len(conditioning_to)):
            t1 = conditioning_to[i][0]
            pooled_output_to = conditioning_to[i][1].get("pooled_output", pooled_output_from)
            t0 = cond_from[:,:t1.shape[1]]
            if t0.shape[1] < t1.shape[1]:
                t0 = torch.cat([t0] + [torch.zeros((1, (t1.shape[1] - t0.shape[1]), t1.shape[2]))], dim=1)

            tw = torch.mul(t1, conditioning_to_strength) + torch.mul(t0, (1.0 - conditioning_to_strength))
            t_to = conditioning_to[i][1].copy()
            if pooled_output_from is not None and pooled_output_to is not None:
                t_to["pooled_output"] = torch.mul(pooled_output_to, conditioning_to_strength) + torch.mul(pooled_output_from, (1.0 - conditioning_to_strength))
            elif pooled_output_from is not None:
                t_to["pooled_output"] = pooled_output_from

            n = [tw, t_to]
            out.append(n)
        return (out,)

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 0 nodes released
'''
NODE_CLASS_MAPPINGS = {
    # Conditioning
    "CR Encode Scheduled Prompts":CR_EncodeScheduledPrompts,
}
'''
