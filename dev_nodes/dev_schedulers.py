#-----------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/CR-Animation-Nodes
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#-----------------------------------------------------------------------------------------------------------#

import comfy.sd
import os
import sys
import folder_paths
from nodes import LoraLoader
from ..animation_nodes.functions import keyframe_scheduler, prompt_scheduler
from ..categories import icons

#-----------------------------------------------------------------------------------------------------------#
# NODES
#-----------------------------------------------------------------------------------------------------------#
# Schedulers      
#-----------------------------------------------------------------------------------------------------------#
class CR_PromptWeightScheduler:

    @classmethod
    def INPUT_TYPES(s):
        modes = ["Default Value", "Schedule"]
        return {"required": {"mode": (modes,),
                             "current_prompt": ("STRING", {"multiline": False, "default": "prepend text"}),
                             "next_prompt": ("STRING", {"multiline": False, "default": "append text"}),         
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),
                             "default_text": ("STRING", {"default": "default prompt", "multiline": False}),
                             "schedule_format": (["CR", "Deforum"],),
                },
                "optional": {"schedule": ("SCHEDULE",),               
                }                    
        }
    
    RETURN_TYPES = ("STRING", "STRING", "FLOAT", )
    RETURN_NAMES = ("current_prompt", "next_prompt", "weight", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, mode, current_prompt, next_prompt, current_frame, schedule_alias, default_value, schedule_format, schedule=None):
                        
        if mode == "Default Value":
            print(f"[Info] CR Prompt Weight Scheduler: Scheduler {schedule_alias} is disabled")
            text_out = default_value
            return (text_out,)
        
        # Get params
        params = keyframe_scheduler(schedule, schedule_alias, current_frame)
         
        # Handle case where there is no schedule line for frame 0 
        if params == "":
            if current_frame == 0:
                print(f"[Warning] CR Prompt Weight Scheduler. No frame 0 found in schedule. Starting with default value at frame 0")
            text_out = default_value,
        else:
            # Try the params
            try:
                weight = float(params)
            except ValueError:
                print(f"[Warning] CR Prompt Weight Scheduler. Invalid params: {params}")
                return()
          
        # Insert prepend and append text
        current_prompt_out = default_text
        next_prompt_out = default_text
                
        return (current_prompt_out, next_prompt_out, weight_out, ) 

#-----------------------------------------------------------------------------------------------------------#
class CR_LoadScheduledControlNets:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Off", "Load default ControlNet", "Schedule"]

        return {"required": {"mode": (modes,),
                             "conditioning": ("CONDITIONING", ),      
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),
                             "default_controlnet": (folder_paths.get_filename_list("loras"), ),
                             "strength": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),                
                             "schedule_format": (["CR", "Deforum"],)
                },
                "optional": {"controlnet_list": ("CONTROLNET_LIST",),
                             "schedule": ("SCHEDULE",) 
                },                
        }
 
    RETURN_TYPES = ("CONDITIONING", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, mode, conditioning, current_frame, schedule_alias, default_controlnet, strength, schedule_format, controlnet_list=None, schedule=None):
     
        controlnet_name = ""

        # Off mode
        if mode == "Off":
            print(f"[Info] CR Load Scheduled ControlNets. Disabled.")    
            return (conditioning,) 
    
        # Load Default ControlNet mode
        if mode == "Load default ControlNet":
            if default_controlnet == None:
                return (conditioning,)
            if strength_model == 0 and strength_clip == 0:
                return (conditioning,)                   
            model, clip = ControlNetLoader().load_controlnet(control_net_name)
            print(f"[Info] CR Load Scheduled ControlNets. Loading default ControlNet {controlnet_name}.")    
            return (conditioning,)           
        
        # Get params
        params = keyframe_scheduler(schedule, schedule_alias, current_frame)
        
        # Handle case where there is no schedule line for a frame 
        if params == "":
            print(f"[Warning] CR Load Scheduled ControlNets. No ControlNet specified in schedule for frame {current_frame}. Using default controlnet.")
            if default_controlnet != None:
                conditioning = LoraLoader().load_controlnet(model, clip, default_controlnet, strength_model, strength_clip)
            return (conditioning,)      
        else:
            # Unpack the parameters
            parts = params.split(',')
            if len(parts) == 3:
                s_controlnet_alias = parts[0].strip()
                s_strength_model = float(parts[1].strip())
                s_strength_clip = float(parts[1].strip())    
            else:
                print(f"[Warning] CR Load Scheduled ControlNets. Skipped invalid line: {line}")
                return()

        # Iterate through the LoRA list to get the LoRA name
        for l_controlnet_alias, l_controlnet_name, l_strength_model, l_strength_clip in controlnet_list:
            print(l_controlnet_alias, l_controlnet_name, l_strength_model, l_strength_clip)
            if l_controlnet_alias == s_controlnet_alias:
                print(f"[Info] CR Load Scheduled ControlNets. LoRA alias match found for {s_controlnet_alias}")
                controlnet_name = l_controlnet_name
                break  # Exit the loop early once a match is found, ignores any duplicate matches
    
        # Check if a matching LoRA has been found        
        if controlnet_name == "":
            print(f"[Info] CR Load Scheduled ControlNets. No ControlNet alias match found for {s_controlnet_alias}. Frame {current_frame}.")
            return()
        else:
            print(f"[Info] CR Load Scheduled ControlNets. controlnet_name {controlnet_name}")
        # Load the new LoRA
        model, clip = LoraLoader().load_controlnet(model, clip, controlnet_name, s_strength_model, s_strength_clip)
        print(f"[Debug] CR Load Scheduled ControlNets. Loading new controlnet {controlnet_name}")
        return (conditioning,)
 
#-----------------------------------------------------------------------------------------------------------#     
class CR_ScheduleCameraMovements:
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image": ("IMAGE",),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "max_frames": ("INT", {"default": 1, "min": 1, "max": 10000}), 
                             "schedule": ("SCHEDULE",),   
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),                    
                             "schedule_format": (["CR", "Deforum"],),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "get_image"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def get_image(self, image, camera_schedule, current_frame, max_frames, schedule_format, ):
    
        image_out = image1
        
        return (image_out,)
     
#-----------------------------------------------------------------------------------------------------------#
class CR_ScheduleStyles:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "max_frames": ("INT", {"default": 120, "min": 1, "max": 10000}),
                             "schedule": ("SCHEDULE",),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),
                             "schedule_format": (["CR", "Deforum"],),
                },
                "optional": {"style_list": ("STYLE_LIST",),
                }
        }
    
    RETURN_TYPES = ("STYLE", )
    RETURN_NAMES = ("STYLE", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, current_frame, max_frames, schedule, schedule_alias, schedule_format, style_list=None):
            
        #loop through tuple list in schedule
        #expand tuples
        #do something
        #return output

        return (None,)

#-----------------------------------------------------------------------------------------------------------#
# MAPPINGS
#-----------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 11 nodes
'''
NODE_CLASS_MAPPINGS = {
    # Schedulers
    "CR Simple Prompt Scheduler":CR_SimplePromptScheduler,    
    "CR Load Scheduled ControlNets":CR_LoadScheduledControlNets,   
    "CR Prompt Weight Scheduler":CR_PromptWeightScheduler,
    "CR Schedule Camera Movements":CR_ScheduleCameraMovements,
    "CR Schedule Styles":CR_ScheduleStyles,    
    "CR Schedule ControlNets":CR_ScheduleControlNets,    
}
'''

