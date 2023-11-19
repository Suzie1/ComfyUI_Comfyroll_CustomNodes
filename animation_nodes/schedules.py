#-----------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/CR-Animation-Nodes
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#-----------------------------------------------------------------------------------------------------------#

import comfy.sd
import os
import sys
import folder_paths
from nodes import LoraLoader
from .functions import keyframe_scheduler, prompt_scheduler
from ..categories import icons

#-----------------------------------------------------------------------------------------------------------#
# Schedules    
#-----------------------------------------------------------------------------------------------------------#
class CR_SimpleSchedule:

    @classmethod
    def INPUT_TYPES(s):
        schedule_types = ["Value", "Text", "Prompt", "Prompt Weight", "Model", "LoRA", "ControlNet", "Style", "Upscale", "Camera", "Job"]
        return {"required": {"schedule": ("STRING",
                             {"multiline": True, "default": "frame_number, item_alias, [attr_value1, attr_value2]"}
                             ),
                             "schedule_type": (schedule_types,),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),  
                             "schedule_format": (["CR", "Deforum"],),
                },
        }
    
    RETURN_TYPES = ("SCHEDULE", )
    FUNCTION = "send_schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedule")

    def send_schedule(self, schedule, schedule_type, schedule_alias, schedule_format):

        schedule_lines = list()
      
      # Extend the list for each line in the schedule
        if schedule != "" and schedule_alias != "":
            lines = schedule.split('\n')
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    print(f"[Warning] CR Simple Schedule. Skipped blank line: {line}")
                    continue            
            
                schedule_lines.extend([(schedule_alias, line)])
        #print(f"[Debug] CR Simple Schedule: {schedule_lines}")

        return (schedule_lines, )

#-----------------------------------------------------------------------------------------------------------#
class CR_CombineSchedules:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                },
                "optional":{
                    "schedule_1": ("SCHEDULE",),                
                    "schedule_2": ("SCHEDULE",),
                    "schedule_3": ("SCHEDULE",),
                    "schedule_4": ("SCHEDULE",),                   
                },
        }

    RETURN_TYPES = ("SCHEDULE", "STRING", )
    RETURN_NAMES = ("SCHEDULE", "show_text", )
    FUNCTION = "combine"
    CATEGORY = icons.get("Comfyroll/Animation/Schedule")

    def combine(self, schedule_1=None, schedule_2=None, schedule_3=None, schedule_4=None):

        # Initialise the list
        schedules = list()
        schedule_text = list()
 
        # Extend the list for each schedule in connected stacks
        if schedule_1 is not None:
            schedules.extend([l for l in schedule_1]),
            schedule_text.extend(schedule_1),

        if schedule_2 is not None:
            schedules.extend([l for l in schedule_2]),
            schedule_text.extend(schedule_2),            

        if schedule_3 is not None:
            schedules.extend([l for l in schedule_3]),
            schedule_text.extend(schedule_3),               

        if schedule_4 is not None:
            schedules.extend([l for l in schedule_4]),
            schedule_text.extend(schedule_4),

        print(f"[Debug] CR Combine Schedules: {schedules}")

        show_text = "".join(str(schedule_text))
            
        return (schedules, show_text, )

#-----------------------------------------------------------------------------------------------------------#
class CR_CentralSchedule:
   
    @classmethod
    def INPUT_TYPES(cls):
        schedule_types = ["Value", "Text", "Prompt", "Prompt Weight", "Model", "LoRA", "ControlNet", "Style", "Upscale", "Camera", "Job"]
        return {"required": {
                    "schedule_1": ("STRING", {"multiline": True, "default": "schedule"}),
                    "schedule_type1": (schedule_types,),
                    "schedule_alias1": ("STRING", {"multiline": False, "default": ""}),
                    "schedule_2": ("STRING", {"multiline": True, "default": "schedule"}),
                    "schedule_type2": (schedule_types,),
                    "schedule_alias2": ("STRING", {"multiline": False, "default": ""}),
                    "schedule_3": ("STRING", {"multiline": True, "default": "schedule"}),
                    "schedule_type3": (schedule_types,),
                    "schedule_alias3": ("STRING", {"multiline": False, "default": ""}),
                    "schedule_format": (["CR", "Deforum"],),
                },
                "optional": {"schedule": ("SCHEDULE",)
                },
        }

    RETURN_TYPES = ("SCHEDULE", "STRING", )
    RETURN_NAMES = ("SCHEDULE", "show_text", )
    FUNCTION = "build_schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedule")

    def build_schedule(self, schedule_1, schedule_type1, schedule_alias1, schedule_2, schedule_type2, schedule_alias2, schedule_3, schedule_type3, schedule_alias3, schedule_format, schedule=None):
    
        # schedule_type and schedule_format are not used in the function

        # Initialise the list
        schedules = list()
        schedule_text = list()
        
        # Extend the list for each schedule in linked stacks
        if schedule is not None:
            schedules.extend([l for l in schedule])
            schedule_text.extend([l for l in schedule]),
        
        # Extend the list for each schedule in the stack
        if schedule_1 != "" and schedule_alias1 != "":
            lines = schedule_1.split('\n')
            for line in lines:
                schedules.extend([(schedule_alias1, line)]),
            schedule_text.extend([(schedule_alias1 + "," + schedule_1 + "\n")]),

        if schedule_2 != "" and schedule_alias2 != "":
            lines = schedule_2.split('\n')
            for line in lines:        
                schedules.extend([(schedule_alias2, line)]),
            schedule_text.extend([(schedule_alias2 + "," + schedule_2 + "\n")]),

        if schedule_3 != "" and schedule_alias3 != "":
            lines = schedule_3.split('\n')
            for line in lines: 
                schedules.extend([(schedule_alias3, line)]),
            schedule_text.extend([(schedule_alias3 + "," + schedule_3 + "\n")]),
            
        #print(f"[Debug] CR Schedule List: {schedules}")

        show_text = "".join(schedule_text)
            
        return (schedules, show_text, )    

#-----------------------------------------------------------------------------------------------------------#
class Comfyroll_ScheduleInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "schedule1": ("SCHEDULE",),
                "schedule2": ("SCHEDULE",)
            }
        }

    RETURN_TYPES = ("SCHEDULE",)
    OUTPUT_NODE = True
    FUNCTION = "switch"

    CATEGORY = icons.get("Comfyroll/Animation/Schedule")

    def switch(self, Input, schedule1, schedule2):
        if Input == 1:
            return (schedule1, )
        else:
            return (schedule2, )
            
#-----------------------------------------------------------------------------------------------------------#
# MAPPINGS
#-----------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 11 nodes
'''
NODE_CLASS_MAPPINGS = {
    ### Schedules
    "CR Simple Schedule":CR_SimpleSchedule,
    "CR Combine Schedules":CR_CombineSchedules,
    "CR Central Schedule":CR_CentralSchedule,
    "CR Schedule To ScheduleList":CR_ScheduleToScheduleList,  
    "CR Schedule Input Switch": Comfyroll_ScheduleInputSwitch, 
}
'''

