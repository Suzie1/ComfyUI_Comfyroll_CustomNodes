#---------------------------------------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi              https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             #
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
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASE INSTRUCTIONS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Change Categories to "CR" before release in new pack
# Remove CR_LoadAnimationFrames from Comfyroll_Nodes.py
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# # DROP 1 NODES
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST
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
    CATEGORY = "Comfyroll/Test/Animation/IO"
    
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
# RELEASED INTO TEST   
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
    CATEGORY = "Comfyroll/Test/Animation/Prompt"

    def prompt_stacker(self, prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_list=None):

        # Initialise the list
        prompts = list()
        
        # Extend the list for each prompt in connected stacks
        if prompt_list is not None:
            prompts.extend([l for l in prompt_list])
        
        # Extend the list for each prompt in the stack
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
# RELEASED INTO TEST   
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
                            "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                            "transition_type": (transition_types,),
                            "transition_speed": (transition_speeds,),
                            "transition_profile": (transition_profiles,),
                            "keyframe_format": (["Deforum"],),
                },         
        }
    
    RETURN_TYPES = ("STRING",  "STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "keyframe_format", "show_text", )
    FUNCTION = "make_keyframes"

    CATEGORY = "Comfyroll/Test/Animation/Prompt"

    def make_keyframes(self, prompt_list, keyframe_interval, loops, transition_type, transition_speed, transition_profile, keyframe_format, ):
    
        keyframe_format = "Deforum"
        keyframe_list = list()
        
        #print(f"[TEST] CR Prompt List Keyframes: {prompt_list}") 
        
        # example output "\"1\": \"1girl, solo, long red hair\"",
        
        i = 0

        for j in range(1, loops + 1): 
            for index, prompt in enumerate(prompt_list):
                if i == 0:
                    keyframe_list.extend(["\"0\": \"" + prompt + "\",\n"])
                    i+=keyframe_interval  
                    continue
                
                new_keyframe = "\"" + str(i) + "\": \"" + prompt + "\",\n"
                keyframe_list.extend([new_keyframe])
                i+=keyframe_interval 
        
        keyframes_out = " ".join(keyframe_list)[:-2]
        show_text = keyframes_out
              
        #print(f"[TEST] CR Prompt List Keyframes: {keyframes_out}")   
        
        return (keyframes_out, keyframe_format, show_text,)
 
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST   
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
    CATEGORY = "Comfyroll/Test/Animation/Prompt"

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
        
        #print(f"[TEST] Comfyroll/Test/Animation Stack: {keyframe_list}") 
       
        return (keyframe_list,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST   
class CR_AnimationStackKeyframes:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"animation_stack": ("ANIMATION_STACK",),
                "keyframe_format": (["Deforum"],),
                }         
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "keyframe_format", )
    FUNCTION = "make_keyframes"
    CATEGORY = "Comfyroll/Test/Animation/Prompt"

    def make_keyframes(self, animation_stack, keyframe_format):
    
        keyframe_format = "Deforum"
        keyframe_list = list()
        
        #print(f"[TEST] Comfyroll/Test/Animation Stack Keyframes: {animation_stack}") 
        
        # example output "\"0\": \"1girl, solo, long grey hair, grey eyes, black sweater, dancing\"",
        
        i = 0
            
        for index, prompt_tuple in enumerate(animation_stack):
            prompt, transition_type, transition_speed, transition_profile, keyframe_interval, loops = prompt_tuple
            
            # 1st frame
            if i == 0:
                keyframe_list.extend(["\"1\": \"" + prompt + "\",\n"])
                i+=keyframe_interval  
                continue
                
            new_keyframe = "\"" + str(i) + "\": \"" + prompt + "\",\n"
            keyframe_list.extend([new_keyframe])
            i+=keyframe_interval 
        
        keyframes_out = "".join(keyframe_list)[:-2]
        
        #print(f"[TEST] Comfyroll/Test/Animation Stack Keyframes: {keyframes_out}")   
        
        return (keyframes_out, keyframe_format, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST   
class CR_KeyframeList:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "keyframe_list": ("STRING", {"multiline": True,}),       
                    "keyframe_format": (["Deforum"],),
                }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "keyframe_format",)
    FUNCTION = "keyframelist"
    CATEGORY = "Comfyroll/Test/Animation/Prompt"

    def keyframelist(self, keyframe_list, keyframe_format):
          
        return (keyframe_list, keyframe_format)
       
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST   
# cloned from ltdrdata Image Batch To Image List node
class CR_DebatchFrames:
   
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "frames": ("IMAGE",), } }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("debatched_frames",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "debatch"
    CATEGORY = "Comfyroll/Test/Animation/Utils"

    def debatch(self, frames):
        images = [frames[i:i + 1, ...] for i in range(frames.shape[0])]
        return (images, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST   
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
    CATEGORY = "Comfyroll/Test/Animation/Index"
    
    def increment(self, index, interval):
        index+=interval
        return (index, )

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST       
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
    CATEGORY = "Comfyroll/Test/Animation/Index"
    
    def multiply(self, index, factor):
        index = index * factor
        return (index, factor) 

#---------------------------------------------------------------------------------------------------------------------------------------------------#     
# RELEASED INTO TEST        
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
    CATEGORY = "Comfyroll/Test/Animation/Index"
    
    def reset(self, index, reset_to):
        index = reset_to
        return (index, reset_to)    

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST   
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
    CATEGORY = "Comfyroll/Test/Animation/Prompt"

    def get_value(self, prompt):
        return (prompt,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# RELEASED INTO TEST   
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
    CATEGORY = "Comfyroll/Test/Animation/Utils"

    def joinlist(self, text_list):
    
        string_out = " ".join(text_list)
        
        return (string_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#DROP 2 
class CR_GradientInteger:

    @classmethod
    def INPUT_TYPES(s):
        gradient_profiles = ["Lerp"]
       
        return {"required": {"start_value": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "end_value": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "gradient_profile": (gradient_profiles,) 
                },
        }
    
    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("INT", )
    FUNCTION = "gradient"
    CATEGORY = "Comfyroll/Test/Animation/Interpolate"

    def gradient(self, start_value, end_value, start_frame, frame_duration, current_frame, gradient_profile):
    
        if current_frame < start_frame:
            return (start_value,)

        if current_frame > start_frame + frame_duration:
            return (end_value,)
            
        step = (end_value - start_value) / frame_duration
        
        current_step = current_frame - start_frame
        
        int_out = start_value + int(current_step * step)
        
        return (int_out,)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#DROP 2 
class CR_GradientFloat:

    @classmethod
    def INPUT_TYPES(s):
        gradient_profiles = ["Lerp"]    
    
        return {"required": {"start_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.01,}),
                             "end_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.01,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "max_frames": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "gradient_profile": (gradient_profiles,)                              
                },
        }
    
    RETURN_TYPES = ("FLOAT", )
    RETURN_NAMES = ("FLOAT", )    
    FUNCTION = "gradient"
    CATEGORY = "Comfyroll/Test/Animation/Interpolate"

    def gradient(self, start_value, end_value, start_frame, max_frames, current_frame, gradient_profile):
    
        if current_frame < start_frame:
            return (start_value,)

        if current_frame > start_frame + max_frames:
            return (end_value,)
            
        step = (end_value - start_value) / max_frames
        
        current_step = current_frame - start_frame        
        
        float_out = start_value + current_step * step
        
        return (float_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#DROP 2
class CR_IncrementFloat:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {"start_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.001,}),
                             "step": ("FLOAT", {"default": 0.1, "min": -9999.0, "max": 9999.0, "step": 0.001,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.00,}),
                             "max_frames": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("FLOAT",)
    OUTPUT_NODE = True    
    FUNCTION = "increment"
    CATEGORY = "Comfyroll/Test/Animation/Interpolate"

    def increment(self, start_value, step, start_frame, max_frames, current_frame):
  
        #print(f"current frame {current_frame}")
        if current_frame < start_frame:
            return (start_value,)
  
        current_value = start_value + (current_frame - start_frame) * step
        if current_frame <= start_frame + max_frames:
            current_value += step
            #print(f"<current value {current_value}")    
            return (current_value,)
                
        return (current_value,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#DROP 2
class CR_IncrementInteger:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {"start_value": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "step": ("INT", {"default": 1.0, "min": -9999.0, "max": 9999.0, "step": 1.0,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "max_frames": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("INT",)
    OUTPUT_NODE = True    
    FUNCTION = "increment"
    CATEGORY = "Comfyroll/Test/Animation/Interpolate"

    def increment(self, start_value, step, start_frame, max_frames, current_frame):
  
        #print(f"current frame {current_frame}")
        if current_frame < start_frame:
            return (start_value,)
  
        current_value = start_value + (current_frame - start_frame) * step
        if current_frame <= start_frame + max_frames:
            current_value += step
            #print(f"<current value {current_value}")    
            return (current_value,)
                
        return (current_value,)
         
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### Drop 1 - 12 nodes
    # IO
    "CR Load Animation Frames":CR_LoadAnimationFrames,
    # Prompt
    "CR Prompt List":CR_PromptList,
    "CR Prompt List Keyframes":CR_PromptListKeyframes,
    "Comfyroll/Test/Animation Stack":CR_AnimationStack,    
    "Comfyroll/Test/Animation Stack Keyframes":CR_AnimationStackKeyframes,
    "CR Keyframe List":CR_KeyframeList,    
    "CR Prompt Text":CR_PromptText,    
    # Index
    "CR Index Increment":CR_IncrementIndex,
    "CR Index Multiply":CR_MultiplyIndex,
    "CR Index Reset":CR_IndexReset,    
    # Utils
    "CR Debatch Frames":CR_DebatchFrames,    
    "CR Text List To String":CR_TextListToString,
    ### Drop 2 - 4 nodes
    # Interpolate
    "CR Gradient Float":CR_GradientFloat,
    "CR Gradient Integer":CR_GradientInteger,
    "CR Increment Float":CR_IncrementFloat,        
    "CR Increment Integer":CR_IncrementInteger,      
}
'''

#---------------------------------------------------------------------------------------------------------------------------------------------------#
# CREDITS
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# WASasquatch           https://github.com/WASasquatch/was-node-suite-comfyui
# melMass               https://github.com/melMass/comfy_mtb
# FizzleDorf            https://github.com/FizzleDorf/ComfyUI_FizzNodes                              
# SeargeDP              https://github.com/SeargeDP/SeargeSDXL       
# ltdrdata              https://github.com/ltdrdata/ComfyUI-Impact-Pack
# LucianoCirino         https://github.com/LucianoCirino/efficiency-nodes-comfyui
# sylym                 https://github.com/sylym/comfy_vid2vid                                                
#---------------------------------------------------------------------------------------------------------------------------------------------------#

