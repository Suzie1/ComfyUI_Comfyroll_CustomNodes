#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import os
import sys
import comfy.controlnet
import comfy.sd
import folder_paths
from nodes import ControlNetApplyAdvanced
from ..categories import icons

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------#
# This node will apply any type of ControlNet.
class CR_ApplyControlNet:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"conditioning": ("CONDITIONING", ),
                             "control_net": ("CONTROL_NET", ),
                             "image": ("IMAGE", ),
                             "switch": (["On","Off"],),
                             "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01})
                             }
               }
               
    RETURN_TYPES = ("CONDITIONING", "STRING", )
    RETURN_NAMES = ("CONDITIONING", "show_help", )
    FUNCTION = "apply_controlnet"
    CATEGORY = icons.get("Comfyroll/ControlNet")

    def apply_controlnet(self, conditioning, control_net, image, switch, strength):
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/ControlNet-Nodes#cr-apply-controlnet"
        
        if strength == 0 or switch == "Off":
            return (conditioning, show_help, )

        c = []
        control_hint = image.movedim(-1,1)
        for t in conditioning:
            n = [t[0], t[1].copy()]
            c_net = control_net.copy().set_cond_hint(control_hint, strength)
            if 'control' in t[1]:
                c_net.set_previous_controlnet(t[1]['control'])
            n[1]['control'] = c_net
            c.append(n)
            
        return (c, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# This node is a stack of controlnets each with their own switch.
class CR_ControlNetStack:

    controlnets = ["None"] + folder_paths.get_filename_list("controlnet")
    
    @classmethod
    def INPUT_TYPES(cls):
        #controlnets = ["None"]
        return {"required": {
                },
                "optional": {
                    "switch_1": (["Off","On"],),
                    "controlnet_1": (cls.controlnets,),
                    "controlnet_strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "start_percent_1": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    "end_percent_1": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    #
                    "switch_2": (["Off","On"],),
                    "controlnet_2": (cls.controlnets,),
                    "controlnet_strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "start_percent_2": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    "end_percent_2": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    #
                    "switch_3": (["Off","On"],),
                    "controlnet_3": (cls.controlnets,),
                    "controlnet_strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "start_percent_3": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    "end_percent_3": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                    #
                    "image_1": ("IMAGE",),
                    "image_2": ("IMAGE",),
                    "image_3": ("IMAGE",),
                    "controlnet_stack": ("CONTROL_NET_STACK",)
                },
        }

    RETURN_TYPES = ("CONTROL_NET_STACK", "STRING", )
    RETURN_NAMES = ("CONTROLNET_STACK", "show_help", )
    FUNCTION = "controlnet_stacker"
    CATEGORY = icons.get("Comfyroll/ControlNet")

    def controlnet_stacker(self, switch_1, controlnet_1, controlnet_strength_1, start_percent_1, end_percent_1,
                           switch_2, controlnet_2, controlnet_strength_2, start_percent_2, end_percent_2,
                           switch_3, controlnet_3, controlnet_strength_3, start_percent_3, end_percent_3,
                           image_1=None, image_2=None, image_3=None, controlnet_stack=None):

        # Initialise the list
        controlnet_list= []
        
        if controlnet_stack is not None:
            controlnet_list.extend([l for l in controlnet_stack if l[0] != "None"])
        
        if controlnet_1 != "None" and  switch_1 == "On" and image_1 is not None:
            controlnet_path = folder_paths.get_full_path("controlnet", controlnet_1)
            controlnet_1 = comfy.controlnet.load_controlnet(controlnet_path)
            controlnet_list.extend([(controlnet_1, image_1, controlnet_strength_1, start_percent_1, end_percent_1)]),

        if controlnet_2 != "None" and  switch_2 == "On" and image_2 is not None:
            controlnet_path = folder_paths.get_full_path("controlnet", controlnet_2)
            controlnet_2 = comfy.controlnet.load_controlnet(controlnet_path)
            controlnet_list.extend([(controlnet_2, image_2, controlnet_strength_2, start_percent_2, end_percent_2)]),

        if controlnet_3 != "None" and  switch_3 == "On" and image_3 is not None:
            controlnet_path = folder_paths.get_full_path("controlnet", controlnet_3)
            controlnet_3 = comfy.controlnet.load_controlnet(controlnet_path)
            controlnet_list.extend([(controlnet_3, image_3, controlnet_strength_3, start_percent_3, end_percent_3)]),

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/ControlNet-Nodes#cr-multi-controlnet-stack"

        return (controlnet_list, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
# This applies the ControlNet stack.
class CR_ApplyControlNetStack:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"base_positive": ("CONDITIONING", ),
                             "base_negative": ("CONDITIONING",),
                             "switch": (["Off","On"],),
                             "controlnet_stack": ("CONTROL_NET_STACK", ),
                            }
        }                    

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", )
    RETURN_NAMES = ("base_pos", "base_neg", "show_help", )
    FUNCTION = "apply_controlnet_stack"
    CATEGORY = icons.get("Comfyroll/ControlNet")

    def apply_controlnet_stack(self, base_positive, base_negative, switch, controlnet_stack=None,):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/ControlNet-Nodes#cr-apply-multi-controlnet-stack"

        if switch == "Off":
            return (base_positive, base_negative, show_help, )
    
        if controlnet_stack is not None:
            for controlnet_tuple in controlnet_stack:
                controlnet_name, image, strength, start_percent, end_percent  = controlnet_tuple
                
                if type(controlnet_name) == str:
                    controlnet_path = folder_paths.get_full_path("controlnet", controlnet_name)
                    controlnet = comfy.sd.load_controlnet(controlnet_path)
                else:
                    controlnet = controlnet_name
                
                controlnet_conditioning = ControlNetApplyAdvanced().apply_controlnet(base_positive, base_negative,
                                                                                     controlnet, image, strength,
                                                                                     start_percent, end_percent)

                base_positive, base_negative = controlnet_conditioning[0], controlnet_conditioning[1]

        return (base_positive, base_negative, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Apply ControlNet": CR_ApplyControlNet,
    "CR Multi-ControlNet Stack":CR_ControlNetStack,
    "CR Apply Multi-ControlNet":CR_ApplyControlNetStack,
}
'''

