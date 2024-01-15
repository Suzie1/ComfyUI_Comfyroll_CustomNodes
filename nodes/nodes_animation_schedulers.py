#-----------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/Suzie1/CR-Animation-Nodes
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#-----------------------------------------------------------------------------------------------------------#

import comfy.sd
import os
import sys
import folder_paths
from nodes import LoraLoader
from .functions_animation import keyframe_scheduler, prompt_scheduler
from ..categories import icons

#-----------------------------------------------------------------------------------------------------------#
# NODES
#-----------------------------------------------------------------------------------------------------------#
# Schedulers      
#-----------------------------------------------------------------------------------------------------------#
class CR_ValueScheduler:

    @classmethod
    def INPUT_TYPES(s):
        modes = ["Default Value", "Schedule"]
        return {"required": {"mode": (modes,),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),
                             "default_value": ("FLOAT", {"default": 1.0, "min": -9999.0, "max": 9999.0, "step": 0.01,}), 
                             "schedule_format": (["CR", "Deforum"],),
                },
                "optional": {"schedule": ("SCHEDULE",),               
                }                    
        }
    
    RETURN_TYPES = ("INT", "FLOAT", "STRING", )
    RETURN_NAMES = ("INT", "FLOAT", "show_help", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, mode, current_frame, schedule_alias, default_value, schedule_format, schedule=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-value-scheduler"

        if mode == "Default Value":
            print(f"[Info] CR Value Scheduler: Scheduler {schedule_alias} is disabled")
            int_out, float_out = int(default_value), float(default_value)    
            return (int_out, float_out, show_help, )

        # Get params
        params = keyframe_scheduler(schedule, schedule_alias, current_frame)

        # Handle case where there is no schedule line for frame 0          
        if params == "":
            if current_frame == 0:
                print(f"[Warning] CR Value Scheduler. No frame 0 found in schedule. Starting with default value at frame 0")
            int_out, float_out = int(default_value), float(default_value) 
        else:
            # Try the params
            try:
                value = float(params)
                int_out, float_out = int(value), float(value)
            except ValueError:
                print(f"[Warning] CR Value Scheduler. Invalid params: {params}")
                return()
        return (int_out, float_out, show_help, )

#-----------------------------------------------------------------------------------------------------------#
class CR_TextScheduler:

    @classmethod
    def INPUT_TYPES(s):
        modes = ["Default Text", "Schedule"]
        return {"required": {"mode": (modes,),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),
                             "default_text": ("STRING", {"multiline": False, "default": "default text"}),
                             "schedule_format": (["CR", "Deforum"],),
                },
                "optional": {"schedule": ("SCHEDULE",),               
                }                    
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, mode, current_frame, schedule_alias, default_text, schedule_format, schedule=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-text-scheduler"

        if mode == "Default Text":
            print(f"[Info] CR Text Scheduler: Scheduler {schedule_alias} is disabled")
            text_out = default_text
            return (text_out, show_help, )

        # Get params
        params = keyframe_scheduler(schedule, schedule_alias, current_frame)
         
        # Handle case where there is no schedule line for frame 0 
        if params == "":
            if current_frame == 0:
                print(f"[Warning] CR Text Scheduler. No frame 0 found in schedule. Starting with default value at frame 0")
            text_out = default_value,
        else:
            # Try the params
            try:
                text_out = params
            except ValueError:
                print(f"[Warning] CR Text Scheduler. Invalid params: {params}")
                return()
        return (text_out, show_help, )


#-----------------------------------------------------------------------------------------------------------#
class CR_PromptScheduler:

    @classmethod
    def INPUT_TYPES(s):
        modes = ["Default Prompt", "Keyframe List", "Schedule"]
        return {"required": {"mode": (modes,),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "default_prompt": ("STRING", {"multiline": False, "default": "default prompt"}),
                             "schedule_format": (["CR", "Deforum"],),
                             #"pingpong_keyframes": (["No", "Yes"],),
                             "interpolate_prompt": (["Yes", "No"],),
                },
                "optional": {"schedule": ("SCHEDULE",),
                             "schedule_alias": ("STRING", {"default prompt": "", "multiline": False}),
                             "keyframe_list": ("STRING", {"multiline": True, "default": "keyframe list"}), 
                             "prepend_text": ("STRING", {"multiline": True, "default": "prepend text"}),
                             "append_text": ("STRING", {"multiline": True, "default": "append text"}),                 
                }                    
        }
    
    RETURN_TYPES = ("STRING", "STRING", "FLOAT", "STRING", )
    RETURN_NAMES = ("current_prompt", "next_prompt", "weight", "show_help", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, mode, prepend_text, append_text, current_frame, schedule_alias, default_prompt, schedule_format, interpolate_prompt, keyframe_list="", schedule=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-prompt-scheduler"

        schedule_lines = list()    
    
        if mode == "Default Prompt":
            print(f"[Info] CR Prompt Scheduler: Scheduler {schedule_alias} is disabled")
            return (default_prompt, default_prompt, 1.0, show_help, )

        if mode == "Keyframe List":
            if keyframe_list == "":
                print(f"[Error] CR Prompt Scheduler: No keyframe list found.")
                return ()
            else:
                lines = keyframe_list.split('\n')
                for line in lines:
                    # If deforum, convert to CR format
                    if schedule_format == "Deforum":
                        line = line.replace(":", ",")
                        line = line.rstrip(',')
                        line = line.lstrip()
                    # Strip empty lines
                    if not line.strip():
                        print(f"[Warning] CR Simple Prompt Scheduler. Skipped blank line at line {i}")
                        continue
                    schedule_lines.extend([(schedule_alias, line)])
                schedule = schedule_lines
        
        if mode == "Schedule":
            if schedule is None:
                print(f"[Error] CR Prompt Scheduler: No schedule found.")
                return ()
            # If deforum, convert to CR format   
            if schedule_format == "Deforum":
                for item in schedule:
                    alias, line = item
                    line = line.replace(":", ",")
                    line = line.rstrip(',')
                    schedule_lines.extend([(schedule_alias, line)])
                schedule = schedule_lines               
        
        current_prompt, next_prompt, current_keyframe, next_keyframe = prompt_scheduler(schedule, schedule_alias, current_frame)

        if current_prompt == "":
            print(f"[Warning] CR Simple Prompt Scheduler. No prompt found for frame. Schedules should start at frame 0.")
        else:        
            try:
                current_prompt_out = prepend_text + ", " + str(current_prompt) + ", " + append_text
                next_prompt_out = prepend_text + ", " + str(next_prompt) + ", " + append_text
                from_index = int(current_keyframe)
                to_index = int(next_keyframe)
            except ValueError:
                print(f"[Warning] CR Simple Text Scheduler. Invalid keyframe at frame {current_frame}")
              
        if from_index == to_index or interpolate_prompt == "No":
            weight_out = 1.0
        else:
            weight_out = (to_index - current_frame) / (to_index - from_index)        

        #if pingpong_keyframes == "Yes":
        #    temp = current_prompt_out
        #    current_prompt_out = next_prompt_out
        #    next_prompt_out = temp
        #    weight_out = 1 - weight_out
                
        return (current_prompt_out, next_prompt_out, weight_out, show_help, ) 

#-----------------------------------------------------------------------------------------------------------#
class CR_SimplePromptScheduler:
        
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"keyframe_list": ("STRING", {"multiline": True, "default": "frame_number, text"}),  
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "keyframe_format": (["CR", "Deforum"],),
                },
        }
    
    RETURN_TYPES = ("STRING", "STRING", "FLOAT", "STRING", )
    RETURN_NAMES = ("current_prompt", "next_prompt", "weight", "show_help", )
    FUNCTION = "simple_schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def simple_schedule(self, keyframe_list, keyframe_format, current_frame):
        
        keyframes = list()
        
        if keyframe_list == "":
            print(f"[Error] CR Simple Prompt Scheduler. No lines in keyframe list") 
            return ()   
        lines = keyframe_list.split('\n')
        for line in lines:
            # If deforum, convert to CR format
            if keyframe_format == "Deforum":
                line = line.replace(":", ",")
                line = line.rstrip(',')
            if not line.strip():
                print(f"[Warning] CR Simple Prompt Scheduler. Skipped blank line at line {i}")
                continue                  
            keyframes.extend([("SIMPLE", line)])        
              
        #print(f"[Debug] CR Simple Prompt Scheduler. Calling function") 
        current_prompt, next_prompt, current_keyframe, next_keyframe = prompt_scheduler(keyframes, "SIMPLE", current_frame)

        if current_prompt == "":
            print(f"[Warning] CR Simple Prompt Scheduler. No prompt found for frame. Simple schedules must start at frame 0.")
        else:        
            try:
                current_prompt_out = str(current_prompt)
                next_prompt_out = str(next_prompt)
                from_index = int(current_keyframe)
                to_index = int(next_keyframe)
            except ValueError:
                print(f"[Warning] CR Simple Text Scheduler. Invalid keyframe at frame {current_frame}")
            
            if from_index == to_index:
                weight_out = 1.0
            else:
                weight_out = (to_index - current_frame) / (to_index - from_index)
            
            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-simple-prompt-scheduler"

            return(current_prompt_out, next_prompt_out, weight_out, show_help, )
            
#-----------------------------------------------------------------------------------------------------------#
class CR_SimpleValueScheduler:
        
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"schedule": ("STRING", {"multiline": True, "default": "frame_number, value"}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("INT", "FLOAT", "STRING", )
    RETURN_NAMES = ("INT", "FLOAT", "show_help", )
    FUNCTION = "simple_schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def simple_schedule(self, schedule, current_frame):

        schedule_lines = list()
        
        if schedule == "":
            print(f"[Warning] CR Simple Value Scheduler. No lines in schedule") 
            return ()
            
        lines = schedule.split('\n')
        for line in lines:        
            schedule_lines.extend([("SIMPLE", line)])        
        
        params = keyframe_scheduler(schedule_lines, "SIMPLE", current_frame)

        if params == "":
            print(f"[Warning] CR Simple Value Scheduler. No schedule found for frame. Simple schedules must start at frame 0.")
        else:
            try:
                int_out = int(params.split('.')[0]) #rounds down
                float_out = float(params)
            except ValueError:
                print(f"[Warning] CR Simple Value Scheduler. Invalid params {params} at frame {current_frame}")

            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-simple-value-scheduler"

            return (int_out, float_out, show_help, )
        
#-----------------------------------------------------------------------------------------------------------#
class CR_SimpleTextScheduler:
        
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"schedule": ("STRING", {"multiline": True, "default": "frame_number, text"}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "simple_schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def simple_schedule(self, schedule, current_frame):
        
        schedule_lines = list()
        
        if schedule == "":
            print(f"[Warning] CR Simple Text Scheduler. No lines in schedule") 
            return ()
            
        lines = schedule.split('\n')
        for line in lines:       
            schedule_lines.extend([("SIMPLE", line)])        
        
        params = keyframe_scheduler(schedule_lines, "SIMPLE", current_frame)

        if params == "":
            print(f"[Warning] CR Simple Text Scheduler. No schedule found for frame. Simple schedules must start at frame 0.")
        else:        
            try:
                text_out = str(params)
            except ValueError:
                print(f"[Warning] CR Simple Text Scheduler. Invalid params {params} at frame {current_frame}")

            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-simple-text-scheduler"

            return(text_out, show_help, )

#-----------------------------------------------------------------------------------------------------------#
class CR_LoadScheduledModels:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Load default Model", "Schedule"]

        return {"required": {"mode": (modes,),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),
                             "default_model": (folder_paths.get_filename_list("checkpoints"), ), 
                             "schedule_format": (["CR", "Deforum"],)
                },
                "optional": {"model_list": ("MODEL_LIST",),
                            "schedule": ("SCHEDULE",) 
                },                
        }
 
    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "VAE", "show_help", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, mode, current_frame, schedule_alias, default_model, schedule_format, model_list=None, schedule=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-load-scheduled-models"

        #model_name = ""
    
        # Load default Model mode
        if mode == "Load default Model":
            ckpt_path = folder_paths.get_full_path("checkpoints", default_model)
            out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
            print(f"[Debug] CR Load Scheduled Models. Loading default model.")    
            return (out[:3], show_help, )
        
        # Get params
        params = keyframe_scheduler(schedule, schedule_alias, current_frame)
        
        # Handle case where there is no schedule line for a frame 
        if params == "":
            print(f"[Warning] CR Load Scheduled Models. No model specified in schedule for frame {current_frame}. Using default model.")
            ckpt_path = folder_paths.get_full_path("checkpoints", default_model)
            out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
            return (out[:3], show_help, )
        else:
            # Try the params
            try:
                model_alias = str(params)
            except ValueError:
                print(f"[Warning] CR Load Scheduled Models. Invalid params: {params}")
                return()                    

        # Iterate through the model list to get the model name
        for ckpt_alias, ckpt_name in model_list:
            if ckpt_alias == model_alias:
                model_name = ckpt_name
                break  # Exit the loop early once a match is found, ignores any duplicate matches
                
        # Check if a matching model has been found        
        if model_name == "":
            print(f"[Info] CR Load Scheduled Models. No model alias match found for {model_alias}. Frame {current_frame} will produce an error.")
            return()
        else:
            print(f"[Info] CR Load Scheduled Models. Model alias {model_alias} matched to {model_name}")
        
        # Load the new model
        ckpt_path = folder_paths.get_full_path("checkpoints", model_name)
        out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
        print(f"[Info] CR Load Scheduled Models. Loading new checkpoint model {model_name}")
        return (out[:3], show_help, )
 
#-----------------------------------------------------------------------------------------------------------# 
class CR_LoadScheduledLoRAs:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Off", "Load default LoRA", "Schedule"]

        return {"required": {"mode": (modes,),
                             "model": ("MODEL",),
                             "clip": ("CLIP", ),        
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "schedule_alias": ("STRING", {"default": "", "multiline": False}),
                             "default_lora": (folder_paths.get_filename_list("loras"), ),
                             "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                             "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),                      
                             "schedule_format": (["CR", "Deforum"],)
                },
                "optional": {"lora_list": ("LORA_LIST",), 
                            "schedule": ("SCHEDULE",) 
                },                
        }
 
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "show_help", )
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/Animation/Schedulers")

    def schedule(self, mode, model, clip, current_frame, schedule_alias, default_lora, strength_model, strength_clip, schedule_format, lora_list=None, schedule=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Scheduler-Nodes#cr-load-scheduled-loras"
        #lora_name = ""

        # Off mode
        if mode == "Off":
            print(f"[Info] CR Load Scheduled LoRAs. Disabled.")    
            return (model, clip, show_help, ) 
    
        # Load Default LoRA mode
        if mode == "Load default LoRA":
            if default_lora == None:
                return (model, clip, show_help, )
            if strength_model == 0 and strength_clip == 0:
                return (model, clip, show_help, )                   
            model, clip = LoraLoader().load_lora(model, clip, default_lora, strength_model, strength_clip)  
            print(f"[Info] CR Load Scheduled LoRAs. Loading default LoRA {lora_name}.")    
            return (model, clip, show_help, )           
        
        # Get params
        params = keyframe_scheduler(schedule, schedule_alias, current_frame)
        
        # Handle case where there is no schedule line for a frame 
        if params == "":
            print(f"[Warning] CR Load Scheduled LoRAs. No LoRA specified in schedule for frame {current_frame}. Using default lora.")
            if default_lora != None:
                model, clip = LoraLoader().load_lora(model, clip, default_lora, strength_model, strength_clip)
            return (model, clip, show_help, )      
        else:
            # Unpack the parameters
            parts = params.split(',')
            if len(parts) == 3:
                s_lora_alias = parts[0].strip()
                s_strength_model = float(parts[1].strip())
                s_strength_clip = float(parts[1].strip())    
            else:
                print(f"[Warning] CR Simple Value Scheduler. Skipped invalid line: {line}")
                return()

        # Iterate through the LoRA list to get the LoRA name
        for l_lora_alias, l_lora_name, l_strength_model, l_strength_clip in lora_list:
            print(l_lora_alias, l_lora_name, l_strength_model, l_strength_clip)
            if l_lora_alias == s_lora_alias:
                print(f"[Info] CR Load Scheduled LoRAs. LoRA alias match found for {s_lora_alias}")
                lora_name = l_lora_name
                break  # Exit the loop early once a match is found, ignores any duplicate matches
    
        # Check if a matching LoRA has been found        
        if lora_name == "":
            print(f"[Info] CR Load Scheduled LoRAs. No LoRA alias match found for {s_lora_alias}. Frame {current_frame}.")
            return()
        else:
            print(f"[Info] CR Load Scheduled LoRAs. LoRA {lora_name}")
            
        # Load the new LoRA
        model, clip = LoraLoader().load_lora(model, clip, lora_name, s_strength_model, s_strength_clip)
        print(f"[Debug] CR Load Scheduled LoRAs. Loading new LoRA {lora_name}")
        return (model, clip, show_help, )
 
#-----------------------------------------------------------------------------------------------------------#
# MAPPINGS
#-----------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 11 nodes
'''
NODE_CLASS_MAPPINGS = {
    ### Schedulers
    "CR Simple Value Scheduler":CR_SimpleValueScheduler,
    "CR Simple Text Scheduler":CR_SimpleTextScheduler,
    "CR Simple Prompt Scheduler":CR_SimplePromptScheduler,    
    "CR Load Scheduled Models":CR_LoadScheduledModels,
    "CR Load Scheduled LoRAs":CR_LoadScheduledLoRAs,
    "CR Load Scheduled ControlNets":CR_LoadScheduledControlNets,   
    "CR Value Scheduler":CR_ValueScheduler,
    "CR Text Scheduler":CR_TextScheduler,
    "CR Prompt Scheduler":CR_PromptScheduler,  
}
'''

