#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi  https://github.com/Suzie1/CR-Animation-Nodes
# for ComfyUI                                    https://github.com/comfyanonymous/ComfyUI 
#---------------------------------------------------------------------------------------------------------------------#

import os
import folder_paths
import json
import torch
from .functions_json import load_styles_from_directory
from ..categories import icons

'''
def extract_values_from_json(json_string):
    try:
        data = json.loads(json_string)
        print(data)
        name = data.get('name', '')
        prompt = data.get('prompt', '')
        negative_prompt = data.get('negative_prompt', '')

        return name, prompt, negative_prompt
    except json.JSONDecodeError as e:
        return None, None, None
'''

#---------------------------------------------------------------------------------------------------------------------#
# NODES
#---------------------------------------------------------------------------------------------------------------------#
class CR_SimplePromptList:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "prompt_1": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_2": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_3": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_4": ("STRING", {"multiline": True, "default": "prompt"}),
                    "prompt_5": ("STRING", {"multiline": True, "default": "prompt"}),
                },
                "optional": {"simple_prompt_list": ("SIMPLE_PROMPT_LIST",)
                },
        }

    RETURN_TYPES = ("SIMPLE_PROMPT_LIST", "STRING", )
    RETURN_NAMES = ("SIMPLE_PROMPT_LIST", "show_help", )
    FUNCTION = "prompt_stacker"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def prompt_stacker(self, prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, simple_prompt_list=None):

        # Initialise the list
        prompts = list()
        
        # Extend the list for each prompt in connected stacks
        if simple_prompt_list is not None:
            prompts.extend([l for l in simple_prompt_list])
        
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
            
        #print(f"[TEST] CR Simple Prompt List: {prompts}")        

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Prompt-Nodes#cr-simple-prompt-list"           

        return (prompts, show_help, )

#---------------------------------------------------------------------------------------------------------------------# 
class CR_SimplePromptListKeyframes:
    @classmethod
    def INPUT_TYPES(s):
    
        #transition_types = ["Morph", "Dissolve", "Cross-Fade", "Jump Cut"]
        transition_types = ["Default"]
        #transition_speeds = ["Slow", "Medium", "Fast", "Custom"]
        transition_speeds = ["Default"]
        #transition_profiles = ["Sin Wave", "Sawtooth", "Custom"]
        transition_profiles = ["Default"]
        
        return {"required": {"simple_prompt_list": ("SIMPLE_PROMPT_LIST",),
                            "keyframe_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),
                            "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                            "transition_type": (transition_types,),
                            "transition_speed": (transition_speeds,),
                            "transition_profile": (transition_profiles,),
                            "keyframe_format": (["Deforum"],),
                },         
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "show_help", )
    FUNCTION = "make_keyframes"

    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def make_keyframes(self, simple_prompt_list, keyframe_interval, loops, transition_type, transition_speed, transition_profile, keyframe_format, ):
    
        keyframe_format = "Deforum"
        keyframe_list = list()
        
        #print(f"[TEST] CR Prompt List Keyframes: {prompt_list}") 
        
        # example output "\"1\": \"1girl, solo, long red hair\"",
        
        i = 0

        for j in range(1, loops + 1): 
            for index, prompt in enumerate(simple_prompt_list):
                if i == 0:
                    keyframe_list.extend(["\"0\": \"" + prompt + "\",\n"])
                    i+=keyframe_interval  
                    continue
                
                new_keyframe = "\"" + str(i) + "\": \"" + prompt + "\",\n"
                keyframe_list.extend([new_keyframe])
                i+=keyframe_interval 
        
        keyframes_out = " ".join(keyframe_list)[:-2]
              
        #print(f"[TEST] CR Simple Prompt List Keyframes: {keyframes_out}")   
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Prompt-Nodes#cr-simple-prompt-list-keyframes"

        return (keyframes_out, show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
'''
# Legacy node, node and class name reused
class CR_PromptList:

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
                "optional": {"prompt_list": ("PROMPT_LIST",)
                },
        }

    RETURN_TYPES = ("PROMPT_LIST", "STRING", )
    RETURN_NAMES = ("PROMPT_LIST", "show_help", )
    FUNCTION = "animation_stacker"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def animation_stacker(self, keyframe_interval, loops, 
        prompt_1, transition_type1, transition_speed1, transition_profile1, 
        prompt_2, transition_type2, transition_speed2, transition_profile2,
        prompt_3, transition_type3, transition_speed3, transition_profile3, 
        prompt_4, transition_type4, transition_speed4, transition_profile4, 
        prompt_5, transition_type5, transition_speed5, transition_profile5, 
        prompt_list=None):
  
        # Initialise the list
        keyframe_list=list()

        # Extend the list for each prompt in the stack        
        if prompt_list is not None:
            keyframe_list.extend([l for l in prompt_list if l[0] != "None"])

        for j in range(1, loops + 1): 
        
            if prompt_1 != "":
                keyframe_list.extend([(prompt_1, transition_type1, transition_speed1, 
                transition_profile1, keyframe_interval, j)]),

            if prompt_2 != "":
                keyframe_list.extend([(prompt_2, transition_type2, transition_speed2, 
                transition_profile2, keyframe_interval, j)]),

            if prompt_3 != "":
                keyframe_list.extend([(prompt_3, transition_type3, transition_speed3, 
                transition_profile3, keyframe_interval, j)]),

            if prompt_4 != "":
                keyframe_list.extend([(prompt_4, transition_type4, transition_speed4, 
                transition_profile4, keyframe_interval, j)]),
                
            if prompt_5 != "":
                keyframe_list.extend([(prompt_5, transition_type5, transition_speed5, 
                transition_profile5, keyframe_interval, j)]),
        
        #print(f"[TEST] CR Prompt List: {keyframe_list}") 
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Prompt-Nodes#cr-prompt-list"

        return (keyframe_list, show_help, )
'''
#---------------------------------------------------------------------------------------------------------------------#  
class CR_PromptListKeyframes:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"prompt_list": ("PROMPT_LIST",),
                "keyframe_format": (["Deforum"],),
                }         
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "show_help", )
    FUNCTION = "make_keyframes"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def make_keyframes(self, prompt_list, keyframe_format):
    
        keyframe_format = "Deforum"
        keyframe_list = list()
        
        #print(f"[TEST] CR Animation Stack Keyframes: {prompt_list}") 
        
        # example output "\"0\": \"1girl, solo, long grey hair, grey eyes, black sweater, dancing\"",
        
        i = 0
            
        for index, prompt_tuple in enumerate(prompt_list):
            prompt, transition_type, transition_speed, transition_profile, keyframe_interval, loops = prompt_tuple
            
            # 1st frame
            if i == 0:
                keyframe_list.extend(["\"0\": \"" + prompt + "\",\n"])
                i+=keyframe_interval  
                continue
                
            new_keyframe = "\"" + str(i) + "\": \"" + prompt + "\",\n"
            keyframe_list.extend([new_keyframe])
            i+=keyframe_interval 
        
        keyframes_out = "".join(keyframe_list)[:-2]
        
        #print(f"[TEST] CR Prompt List Keyframes: {keyframes_out}")   
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Prompt-Nodes#cr-prompt-list-keyframes"

        return (keyframes_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------# 
class CR_KeyframeList:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "keyframe_list": ("STRING", {"multiline": True, "default": "keyframes"}),       
                    "keyframe_format": (["Deforum","CR"],),
                }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("keyframe_list", "show_help", )
    FUNCTION = "keyframelist"
    CATEGORY = icons.get("Comfyroll/Animation/Prompt")

    def keyframelist(self, keyframe_list, keyframe_format):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Prompt-Nodes#cr-keyframe-list"          
        return (keyframe_list, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadPromptStyle:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        style_directory = os.path.join(folder_paths.base_path, "styles")
        #style_directory = os.path.dirname(os.path.realpath(__file__))
        self.json_data, styles = load_styles_from_directory(style_directory)
        file_types = ["json"]

        #if not os.path.exists(style_dir):
        #   os.makedirs(style_dir)
        
        return {
            "required": {
                "style": ((styles), ),
                "file_type": (file_types, ),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("prepend_text", "append_text", "negative_text", "show_help", )
    FUNCTION = 'prompt_styler'
    CATEGORY = icons.get("Comfyroll/Animation/Prompt")

    def prompt_styler(self, style, file_type):

        for template in self.json_data:
            if template['name'] == style:
                template_str = str(template)     
        print(f"[Info] CR Load Prompt Style: Got style template {template_str}")

        #name, prompt, negative_prompt = extract_values_from_json(template_str)
        #print(name, prompt, negative_prompt)
        #split_prompt = prompt.split("{prompt}", 1)
        #prepend_text = split_prompt[0]
        #append_text = split_prompt[1]
        #negative_text = negative_prompt
 
        # Note: This will fail if negative_prompt is before the prompt
        split1 = template_str.split("{prompt}", 1)
        split2 = split1[0].split("prompt': '", 1)
        split3 = split1[1].split("', 'negative_prompt", 1)   
        split4 = split1[1].split("negative_prompt': '", 1)
        prepend_text = split2[1]
        append_text = split3[0].replace(" . ","")
        negative_text = split4[1][:-2]
      
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Prompt-Nodes#cr-load-prompt-style"
        
        return (prepend_text, append_text, negative_text, show_help, )

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
    
    RETURN_TYPES = ("CONDITIONING", "STRING", )
    RETURN_NAMES = ("CONDITIONING", "show_help", )
    FUNCTION = "condition"
    CATEGORY = icons.get("Comfyroll/Animation/Prompt")

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
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Prompt-Nodes#cr-encode-scheduled-prompts"
        return (out, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 7 nodes
'''
NODE_CLASS_MAPPINGS = {
    "CR Prompt List":CR_PromptList,
    "CR Prompt List Keyframes":CR_PromptListKeyframes,
    "CR Simple Prompt List":CR_SimplePromptList,    
    "CR Simple Prompt List Keyframes":CR_SimplePromptListKeyframes,
    "CR Keyframe List":CR_KeyframeList,    
    "CR Load Prompt Style":CR_LoadPromptStyle,
    "CR Encode Scheduled Prompts":CR_EncodeScheduledPrompts,    
}
'''
