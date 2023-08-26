#---------------------------------------------------------------------------------------------------------------------------------------------------#
# CR Animation Pack by RockOfFire and Akatsuzi              https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             #
# for ComfyUI                                               https://github.com/comfyanonymous/ComfyUI                                               #
#---------------------------------------------------------------------------------------------------------------------------------------------------#

from PIL import Image
import comfy.sd
import re
import torch
import numpy as np
import os
import sys
import folder_paths
import math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASE INSTRUCTIONS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Change Categories to "CR" before release in new pack
# Remove CR_LoadAnimationFrames from Comfyroll_Nodes.py
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# TBD
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# NODES
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED IN TEST, REQUIRES UPDATE IN NEXT RELEASE
# cloned from vid2vid Load Image Sequence
class CR_LoadAnimationFrames:

    input_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'input')
    @classmethod
    def INPUT_TYPES(s):
        if not os.path.exists(s.input_dir):
            os.makedirs(s.input_dir)
        image_folder = [name for name in os.listdir(s.input_dir) if os.path.isdir(os.path.join(s.input_dir,name)) and len(os.listdir(os.path.join(s.input_dir,name))) != 0]
        return {"required":{
                    "image_sequence_folder": (sorted(image_folder), ),
                    "start_index": ("INT", {"default": 1, "min": 1, "max": 10000}),
                    "max_frames": ("INT", {"default": 1, "min": 1, "max": 10000})
                    }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT",)
    RETURN_NAMES = ("frames", "masks", "max_frames")
    FUNCTION = "load_image_sequence"
    CATEGORY = "Comfyroll/Test/Animation"
    
    def load_image_sequence(self, image_sequence_folder, start_index, max_frames):
        image_path = os.path.join(self.input_dir, image_sequence_folder)
        file_list = sorted(os.listdir(image_path), key=lambda s: sum(((s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)), ()))
        sample_frames = []
        sample_frames_mask = []
        sample_index = list(range(start_index-1, len(file_list), 1))[:max_frames]
        for num in sample_index:
            i = Image.open(os.path.join(image_path, file_list[num]))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            image = image.squeeze()
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            sample_frames.append(image)
            sample_frames_mask.append(mask)
            
        return (torch.stack(sample_frames), sample_frames_mask, max_frames,)  

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST 
class CR_PromptList:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "prompt_1": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_2": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_3": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_4": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_5": ("STRING", {"multiline": True, "default": "prompt"}),
                },
                "optional": {"prompt_list": ("PROMPT_LIST",)
                },
        }

    RETURN_TYPES = ("PROMPT_LIST",)
    RETURN_NAMES = ("PROMPT_LIST",)
    FUNCTION = "prompt_stacker"
    CATEGORY = "Comfyroll/Test/Animation"

    def prompt_stacker(self, prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_list=None):

        # Initialise the list
        prompts = list()
        
        # Extend the list for each prompt in the stack
        if prompt_list is not None:
            prompts.extend([l for l in prompt_list])
        
        if prompt_1 != "":
            prompts.extend([(prompt_1)]),

        if prompt_2 != "":
            prompts.extend([(prompt_2)]),

        if prompt_3 != "":
            prompts.extend([(prompt_3)]),

        if prompt_4 != "":
            prompts.extend([(prompt_4)]),
            
        if prompt_5 != "":
            prompts.extend([(prompt_5)]),
            
        #print(f"[TEST] CR Prompt List: {prompts}")        
            
        return (prompts,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# PROTOTYPE FOR RELEASE INTO TEST
class CR_PromptListKeyframes:
    @classmethod
    def INPUT_TYPES(s):
    
        #transition_types = ["Morph", "Dissolve", "Cross-Fade", "Jump Cut"]
        transition_types = ["Default"]
        #transition_speeds = ["Slow", "Medium", "Fast", "Custom"]
        transition_speeds = ["Default"]
        #transition_profiles = ["Sin Wave", "Sawtooth", "Custom"]
        transition_profiles = ["Default"]
        
        return {"required": {"prompt_list": ("PROMPT_LIST",),
                            "keyframe_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),
                            "loops": ("INT", {"default": 1, "min": 1, "max": 100}),
                            "transition_type": (transition_types,),
                            "transition_speed": (transition_speeds,),
                            "transition_profile": (transition_profiles,),
                            "keyframe_format": (["Deforum"],),
                },         
        }
    
    RETURN_TYPES = ("STRING",  "STRING", )
    RETURN_NAMES = ("keyframe_list", "keyframe_format")
    FUNCTION = "make_keyframes"

    CATEGORY = "Comfyroll/Test/Animation"

    def make_keyframes(self, prompt_list, keyframe_interval, loops, transition_type, transition_speed, transition_profile, keyframe_format, ):
    
        keyframe_format = "Deforum"
        keyframe_list = list()
        
        #print(f"[TEST] CR Prompt List Keyframes: {prompt_list}") 
        
        # example output "\"1\": \"1girl, solo, long red hair\"",
        
        i = 0

        for j in range(1, loops + 1): 
            for index, prompt in enumerate(prompt_list):
                if i == 0:
                    keyframe_list.extend(["\"1\": \"" + prompt + "\",\n"])
                    i+=keyframe_interval  
                    continue
                       
                keyframe_list.extend(["\"" + str(i) + "\": \"" + prompt + "\",\n"])
                i+=keyframe_interval 
        
        keyframes_out = " ".join(keyframe_list)[:-2]
        
        #print(f"[TEST] CR Prompt List Keyframes: {keyframes_out}")   
        
        return (keyframes_out, keyframe_format,)
 
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST
class CR_AnimationStack:

    @classmethod
    def INPUT_TYPES(cls):
        
        #transition_types = ["Morph", "Dissolve", "Cross-Fade", "Jump Cut"]
        transition_types = ["Default"]
        #transition_speeds = ["Slow", "Medium", "Fast", "Custom"]
        transition_speeds = ["Default"]
        #transition_profiles = ["Sin Wave", "Sawtooth", "Custom"]
        transition_profiles = ["Default"]
    
        return {"required": {
                    "keyframe_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),
                    "loops": ("INT", {"default": 1, "min": 1, "max": 100}),                                
                    "prompt_1": ("STRING", {"multiline": True, "default": "prompt"}),
                    "transition_type1": (transition_types,),
                    "transition_speed1": (transition_speeds,),
                    "transition_profile1": (transition_profiles,),
                    "prompt_2": ("STRING", {"multiline": True, "default": "prompt"}),
                    "transition_type2": (transition_types,),
                    "transition_speed2": (transition_speeds,),
                    "transition_profile2": (transition_profiles,),
                    "prompt_3": ("STRING", {"multiline": True, "default": "prompt"}),
                    "transition_type3": (transition_types,),
                    "transition_speed3": (transition_speeds,),
                    "transition_profile3": (transition_profiles,),
                    "prompt_4": ("STRING", {"multiline": True, "default": "prompt"}),
                    "transition_type4": (transition_types,),
                    "transition_speed4": (transition_speeds,),
                    "transition_profile4": (transition_profiles,),
                    "prompt_5": ("STRING", {"multiline": True, "default": "prompt"}),
                    "transition_type5": (transition_types,),
                    "transition_speed5": (transition_speeds,),
                    "transition_profile5": (transition_profiles,),
                },
                "optional": {"animation_stack": ("ANIMATION_STACK",)
                },
        }

    RETURN_TYPES = ("ANIMATION_STACK",)
    RETURN_NAMES = ("ANIMATION_STACK",)
    FUNCTION = "animation_stacker"
    CATEGORY = "Comfyroll/Test/Animation"

    def animation_stacker(self, keyframe_interval, loops, prompt_1, transition_type1, transition_speed1, transition_profile1, prompt_2, transition_type2, transition_speed2, transition_profile2, prompt_3, transition_type3, transition_speed3, transition_profile3, prompt_4, transition_type4, transition_speed4, transition_profile4, prompt_5, transition_type5, transition_speed5, transition_profile5, animation_stack=None):
  
        # Initialise the list
        keyframe_list=list()

        # Extend the list for each prompt in the stack        
        if animation_stack is not None:
            keyframe_list.extend([l for l in animation_stack if l[0] != "None"])

        for j in range(1, loops + 1): 
        
            if prompt_1 != "":
                keyframe_list.extend([(prompt_1, transition_type1, transition_speed1, transition_profile1, keyframe_interval, j)]),

            if prompt_2 != "":
                keyframe_list.extend([(prompt_2, transition_type2, transition_speed2, transition_profile2, keyframe_interval, j)]),

            if prompt_3 != "":
                keyframe_list.extend([(prompt_3, transition_type3, transition_speed3, transition_profile3, keyframe_interval, j)]),

            if prompt_4 != "":
                keyframe_list.extend([(prompt_4, transition_type4, transition_speed4, transition_profile4, keyframe_interval, j)]),
                
            if prompt_5 != "":
                keyframe_list.extend([(prompt_5, transition_type5, transition_speed5, transition_profile5, keyframe_interval, j)]),
        
        #print(f"[TEST] CR Animation Stack: {keyframe_list}") 
       
        return (keyframe_list,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST
class CR_AnimationStackKeyframes:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"animation_stack": ("ANIMATION_STACK",),
                "keyframe_format": (["Deforum"],),
                }         
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "keyframe_format")
    FUNCTION = "make_keyframes"
    CATEGORY = "Comfyroll/Test/Animation"

    def make_keyframes(self, animation_stack, keyframe_format):
    
        keyframe_format = "Deforum"
        keyframe_list = list()
        
        #print(f"[TEST] CR Animation Stack Keyframes: {animation_stack}") 
        
        # example output "\"1\": \"1girl, solo, long grey hair, grey eyes, black sweater, dancing\"",
        
        i = 0
            
        for index, prompt_tuple in enumerate(animation_stack):
            prompt, transition_type, transition_speed, transition_profile, keyframe_interval, loops = prompt_tuple
            
            # 1st frame
            if i == 0:
                keyframe_list.extend(["\"1\": \"" + prompt + "\",\n"])
                i+=keyframe_interval  
                continue

            keyframe_list.extend(["\"" + str(i) + "\": \"" + prompt + "\",\n"])
            i+=keyframe_interval 
        
        keyframes_out = " ".join(keyframe_list)[:-2]
        
        #print(f"[TEST] CR Animation Stack Keyframes: {keyframes_out}")   
        
        return (keyframes_out, keyframe_format,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST
class CR_KeyframeList:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "keyframe_list": ("STRING", {"multiline": True,}),       
                    "keyframe_format": (["Deforum"],),
                }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "keyframe_format")
    FUNCTION = "keyframelist"
    CATEGORY = "Comfyroll/Test/Animation"

    def keyframelist(self, keyframe_list, keyframe_format):
          
        return (keyframe_list, keyframe_format)
       
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST
# cloned from ltdrdata Image Batch To Image List node
class CR_DebatchFrames:
   
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "frames": ("IMAGE",), } }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("debatched_frames")
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "debatch"
    CATEGORY = "Comfyroll/Test/Animation"

    def debatch(self, frames):
        images = [frames[i:i + 1, ...] for i in range(frames.shape[0])]
        return (images, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST
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
    CATEGORY = "Comfyroll/Test/Animation"
    
    def increment(self, index, interval):
        index+=interval
        return (index, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST       
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
    CATEGORY = "Comfyroll/Test/Animation"
    
    def multiply(self, index, factor):
        index = index * factor
        return (index, factor) 

#---------------------------------------------------------------------------------------------------------------------------------------------------#     
# READY FOR RELEASE INTO TEST       
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
    CATEGORY = "Comfyroll/Test/Animation"
    
    def reset(self, index, reset_to):
        index = reset_to
        return (index, reset_to)    
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#PROTOTYPE NOT FOR RELEASE
class CR_ScheduleLoRAs:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"clip": ("CLIP", ),
                            "lora_stack": ("LORA_STACK",),
                            "lora_schedule": ("STRING", {"multiline": True,}),
                            "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                            "max_frames": ("INT", {"default": 1, "min": 1, "max": 10000}),
                            "schedule_format": (["CR"],),
                },
        }
    
    RETURN_TYPES = ("CLIP", )
    FUNCTION = "schedule"
    CATEGORY = "Comfyroll/Test/Animation"

    def schedule(self, max_frames, schedule_format, lora_schedule, lora_stack, current_frame):

        return (None)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#PROTOTYPE NOT FOR RELEASE   
class CR_ScheduleModels:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model_stack": ("MODEL_STACK",),
                             "model_schedule": ("STRING", {"multiline": True,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "max_frames": ("INT", {"default": 1, "min": 1, "max": 10000}),
                             "schedule_format": (["CR"],),
                },
        }
    
    RETURN_TYPES = ("CLIP", )
    FUNCTION = "schedule"
    CATEGORY = "Comfyroll/Test/Animation"

    def schedule(self, max_frames, schedule_format, model_schedule, model_stack, current_frame):
   
        return (None)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#PROTOTYPE NOT FOR RELEASE   
class CR_ScheduleControlNets:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"conditioning": ("CONDITIONING", ),
                            "controlnet_stack": ("CONTROL_NET_STACK",),
                            "controlnet_schedule": ("STRING", {"multiline": True,}),
                            "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "max_frames": ("INT", {"default": 1, "min": 1, "max": 10000}),
                             "schedule_format": (["CR"],),
                },
        }
    
    RETURN_TYPES = ("CONDITIONING", )
    FUNCTION = "schedule"
    CATEGORY = "Comfyroll/Test/Animation"

    def schedule(self, max_frames, schedule_format, controlnet_schedule, controlnet_stack, current_frame):
    
        return (None)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# READY FOR RELEASE INTO TEST   
class CR_PromptText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "prompt": ("STRING", {"default": "prompt", "multiline": True}),
                    },
                }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("prompt", )
    FUNCTION = "get_value"
    CATEGORY = "Comfyroll/Test/Animation"

    def get_value(self, prompt):
        return (prompt,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

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
    CATEGORY = "Comfyroll/Test/Animation"

    def joinlist(self, text_list):
    
        string_out = " ".join(text_list)
        
        return (string_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Next Prototypes
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#PROTOTYPE NOT FOR RELEASE
class CR_AnimateTransition:
    @classmethod
    def INPUT_TYPES(s):
        transition_types = ["Morph", "Dissolve", "Cross-Fade", "Jump Cut", "Swipe-Left", "Swipe-Right", "Fade to Black"]
        return {"required": {
                    "image1": ("IMAGE",),
                    "image2": ("IMAGE",),
                    "transition_type": (transition_types,),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "start_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "end_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = "get_image"
    CATEGORY = "Comfyroll/Test/Animation"

    def get_image(self, image1, image2, transition_type, current_frame, start_keyframe, end_keyframe):
    
        image_out = image1
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#PROTOTYPE NOT FOR RELEASE
class CR_CameraZoom:
    @classmethod
    def INPUT_TYPES(s):
        zoom_types = ["Zoom In", "Zoom Out"]
        return {"required": {
                    "image": ("IMAGE",),
                    "zoom_type": (zoom_types,),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "start_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "end_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = "get_image"
    CATEGORY = "Comfyroll/Test/Animation"

    def get_image(self, image, zoom_type, current_frame, start_keyframe, end_keyframe):
    
        image_out = image1
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#PROTOTYPE NOT FOR RELEASE
class CR_CameraRotation:
    @classmethod
    def INPUT_TYPES(s):
        rotation_types = ["Tilt Up", "Tilt Down", "Pan Left", "Pan Right"]
        return {"required": {
                    "image": ("IMAGE",),
                    "rotation_type": (rotation_types,),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "start_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "end_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = "get_image"
    CATEGORY = "Comfyroll/Test/Animation"

    def get_image(self, image, rotation_type, current_frame, start_keyframe, end_keyframe):
    
        image_out = image1
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#PROTOTYPE NOT FOR RELEASE
class CR_MorphLayers:
    @classmethod
    def INPUT_TYPES(s):
        morph_types = ["Morph Background", "Morph Foreground", "Morph Face"]
        return {"required": {
                    "image": ("IMAGE",),
                    "mask": ("MASK",),
                    "rotation_type": (morph_types,),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "start_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "end_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = "get_image"
    CATEGORY = "Comfyroll/Test/Animation"

    def get_image(self, image1, image2, morph_type, current_frame, start_keyframe, end_keyframe):
    
        image_out = image1
        
        return (image_out,)


#---------------------------------------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    # RELEASE IN TEST
    "CR Load Animation Frames":Comfyroll_LoadAnimationFrames,
    # READY FOR RELEASE INTO TEST
    "CR Debatch Frames":CR_DebatchFrames,
    "CR Index Increment":CR_IncrementIndex,
    "CR Index Multiply":CR_MultiplyIndex,
    "CR Index Reset":CR_IndexReset,    
    "CR Prompt List":CR_PromptList,
    "CR Animation Stack":CR_AnimationStack,
    "CR Prompt Text":CR_PromptText,
    "CR Keyframe List":CR_KeyframeList,
    "CR Text List To String":CR_TextListToString,
    "CR Prompt List Keyframes":CR_PromptListKeyframes,
    "CR Animation Stack Keyframes":CR_AnimationStackKeyframes,    
    # PROTOTYPES NOT FOR RELEASE
    "CR Schedule LoRAs":CR_ScheduleLoRAs,
    "CR Schedule Models":CR_ScheduleModels,
    "CR Schedule LoRAs":CR_ScheduleLoRAs,
    # PROTOTYPES FOR 2ND NODE SET
    "CR Animate Transition":CR_AnimateTransition,
    "CR Camera Zoom":CR_CameraZoom,
    "CR Camera Rotation":CR_CameraRotation, 
    "CR Morph Layers":CR_MorphLayers, 
    # IN SEPERATE TEST FILE
    "CR Prompt List Scheduler":CR_PromptListScheduler,
    "CR Animation Stack Scheduler":CR_AnimationStackScheduler,
    "CR Advanced Prompt Scheduler":CR_AdvancedPromptScheduler,
    "CR Image Stack":CR_ImageStack,  
    "CR Animation PopImage":CR_AnimationPopImage,
}
'''

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# CREDITS
# Fizz
# Dr Data
# Efficiency
# MTB
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# WASasquatch       https://github.com/WASasquatch/was-node-suite-comfyui
# MTB               https://github.com/melMass/comfy_mtb
# Fizz              https://github.com/FizzleDorf/ComfyUI_FizzNodes                              
# SeargeDP          https://github.com/SeargeDP/SeargeSDXL                                                                    
#---------------------------------------------------------------------------------------------------------------------------------------------------#

