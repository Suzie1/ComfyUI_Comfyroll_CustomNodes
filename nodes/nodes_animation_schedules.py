#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import comfy.sd
import os
import sys
import folder_paths
from nodes import LoraLoader
from .functions_animation import keyframe_scheduler, prompt_scheduler
from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
# Schedules    
#---------------------------------------------------------------------------------------------------------------------#
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
    
    RETURN_TYPES = ("SCHEDULE", "STRING", )
    RETURN_NAMES = ("SCHEDULE", "show_help", )
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

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Schedule-Nodes#cr-simple-schedule"

        return (schedule_lines, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
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

#---------------------------------------------------------------------------------------------------------------------#
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

#---------------------------------------------------------------------------------------------------------------------#
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

    RETURN_TYPES = ("SCHEDULE", "STRING", )
    RETURN_NAMES = ("SCHEDULE", "show_help", )
    OUTPUT_NODE = True
    FUNCTION = "switch"

    CATEGORY = icons.get("Comfyroll/Animation/Schedule")

    def switch(self, Input, schedule1, schedule2):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Schedule-Nodes#cr-schedule-input-switch"
        if Input == 1:
            return (schedule1, show_help, )
        else:
            return (schedule2, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_OutputScheduleToFile:
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "output_file_path": ("STRING", {"multiline": False, "default": ""}),
            "file_name": ("STRING", {"multiline": False, "default": ""}),
            "file_extension": (["txt", "csv"],),
            "schedule": ("SCHEDULE",),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "csvoutput"
    CATEGORY = icons.get("Comfyroll/Animation/Schedule") 
    
    def csvoutput(self, output_file_path, file_name, schedule, file_extension):
        filepath = output_file_path + "\\" + file_name + "." + file_extension
        
        index = 2

        if(output_file_path == "" or file_name == ""):
            print(f"[Warning] CR Output Schedule To File. No file details found. No file output.") 
            return ()

        while os.path.exists(filepath):
            if os.path.exists(filepath):
                filepath = output_file_path + "\\" + file_name + str(index) + "." + file_extension

                index = index + 1
            else:
                break            
        
        print(f"[Info] CR Output Schedule To File: Saving to {filepath}")        
        
        if file_extension == "csv":
            with open(filepath, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(schedule)
        else:
            with open(filepath, "w", newline="") as text_writer:
                for line in schedule:
                    str_item = f'{line[0]},"{line[1]}"\n'
                    text_writer.write(str_item)
        
        
        return ()

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadScheduleFromFile:
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "input_file_path": ("STRING", {"multiline": False, "default": ""}),
            "file_name": ("STRING", {"multiline": False, "default": ""}),
            "file_extension": (["txt", "csv"],),
            }
        }

    RETURN_TYPES = ("SCHEDULE", "STRING", )
    RETURN_NAMES = ("SCHEDULE", "show_text", )
    FUNCTION = "csvinput"
    CATEGORY = icons.get("Comfyroll/Animation/Schedule")    
    
    def csvinput(self, input_file_path, file_name, file_extension):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Schedule-Nodes#cr-load-schedule-from-file"
        
        filepath = input_file_path + "\\" + file_name + "." + file_extension
        print(f"CR Load Schedule From File: Loading {filepath}")
        
        lists = []
            
        if file_extension == "csv":
            with open(filepath, "r") as csv_file:
                reader = csv.reader(csv_file)
        
                for row in reader:
                    lists.append(row)
                    
        else:
            with open(filepath, "r") as txt_file:
                for row in txt_file:
                    parts = row.strip().split(",", 1)
                    
                    if len(parts) >= 2:
                        second_part = parts[1].strip('"')
                        lists.append([parts[0], second_part])

        #print(lists)
        
        return(lists,str(lists),)

def binary_string_to_schedule(binary_string):
    schedule = []
    for i, bit in enumerate(binary_string):
        schedule.append(f"{i},{int(bit)}")
    return '\n'.join(schedule)
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_BitSchedule:
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "binary_string": ("STRING", {"multiline": True, "default": ""}),
            "interval": ("INT", {"default": 1, "min": 1, "max": 99999}),
            "loops": ("INT", {"default": 1, "min": 1, "max": 99999}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("SCHEDULE", "show_text", )
    FUNCTION = "bit_schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedule")    

    def bit_schedule(self, binary_string, interval, loops=1):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Schedule-Nodes#cr-bit-schedule"
    
        schedule = []

        # Remove spaces and line returns from the input
        binary_string = binary_string.replace(" ", "").replace("\n", "")
        '''
        for i in range(len(binary_string) * loops):
            index = i % len(binary_string)  # Use modulo to ensure the index continues in a single sequence
            bit = int(binary_string[index])
            schedule.append(f"{i},{bit}")
        '''    
        for i in range(len(binary_string) * loops):
            schedule_index = i * interval
            bit_index = i % len(binary_string)
            bit = int(binary_string[bit_index])
            schedule.append(f"{schedule_index},{bit}")            
                
        schedule_out = '\n'.join(schedule)
        
        return (schedule_out, show_help,)
    
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
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
    "CR Output Schedule To File":CR_OutputScheduleToFile,
    "CR Load Schedule From File":CR_LoadScheduleFromFile,
    "CR Bit Schedule": CR_BitCyclicSchedule,
}
'''

