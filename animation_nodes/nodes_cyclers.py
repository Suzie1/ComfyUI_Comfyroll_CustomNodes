#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/Suzie1/CR-Animation-Nodes
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

import comfy.sd
import torch
import os
import sys
import folder_paths
import random
from PIL import Image, ImageEnhance
import numpy as np
import io
from ..categories import icons

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))
#---------------------------------------------------------------------------------------------------------------------# 
# FUNCTIONS
#---------------------------------------------------------------------------------------------------------------------# 
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
#---------------------------------------------------------------------------------------------------------------------# 
# NODES
#---------------------------------------------------------------------------------------------------------------------# 
class CR_CycleModels:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Off", "Sequential"]

        return {"required": {"mode": (modes,),
                             "model": ("MODEL",),
                             "clip": ("CLIP",),
                             "model_list": ("MODEL_LIST",),
                             "frame_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),        
                             "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "VAE", "show_help", )
    FUNCTION = "cycle_models"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def cycle_models(self, mode, model, clip, model_list, frame_interval, loops, current_frame,):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Cycler-Nodes#cr-cycle-models"

        # Initialize the list
        model_params = list()

        # Extend lora_params with the lora_list items
        if model_list:
            for _ in range(loops):
                model_params.extend(model_list)
            #print(f"[Debug] CR Cycle Models:{model_params}")
                
        if mode == "Off":
            return (model, clip, show_help, )               

        elif mode == "Sequential":
            if current_frame == 0:
                return (model, clip, show_help, ) 
            else:    
                # Calculate the index of the current model based on the current_frame and frame_interval
                current_model_index = (current_frame // frame_interval) % len(model_params)
                #print(f"[Debug] CR Cycle Models:{current_model_index}")
                
                # Get the parameters of the current model
                current_model_params = model_params[current_model_index]
                model_alias, ckpt_name = current_model_params
                print(f"[Info] CR Cycle Models: Current model is {ckpt_name}")
                
                # Load the current model
                ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
                out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, 
                embedding_directory=folder_paths.get_folder_paths("embeddings"))
                return (out, show_help, )
        #else:
        #    return (model, clip) 
 
#---------------------------------------------------------------------------------------------------------------------# 
class CR_CycleLoRAs:

    @classmethod
    def INPUT_TYPES(s):
        
        modes = ["Off", "Sequential"]
    
        return {"required": {"mode": (modes,),
                             "model": ("MODEL",),
                             "clip": ("CLIP",),
                             "lora_list": ("LORA_LIST",),
                             "frame_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),
                             "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),                             
                },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "show_help", )
    FUNCTION = "cycle"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def cycle(self, mode, model, clip, lora_list, frame_interval, loops, current_frame):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Cycler-Nodes#cr-cycle-loras"

        # Initialize the list
        lora_params = list()

        # Extend lora_params with lora_list items
        if lora_list:
            for _ in range(loops):
                lora_params.extend(lora_list)
            #print(f"[Debug] CR Cycle LoRAs:{lora_params}")            
        else:
            return (model, clip, show_help, )

        if mode == "Sequential":
            # Calculate the index of the current LoRA based on the current_frame and frame_interval
            current_lora_index = (current_frame // frame_interval) % len(lora_params)
            #print(f"[Debug] CR Cycle LoRAs:{current_lora_index}")
            
            # Get the parameters of the current LoRA
            current_lora_params = lora_params[current_lora_index]
            lora_alias, lora_name, model_strength, clip_strength = current_lora_params
            
            # Load the current LoRA
            lora_path = folder_paths.get_full_path("loras", lora_name)
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            print(f"[Info] CR_CycleLoRAs: Current LoRA is {lora_name}")

            # Apply the current LoRA to the model and clip
            model_lora, clip_lora = comfy.sd.load_lora_for_models(
            model, clip, lora, model_strength, clip_strength)
            return (model_lora, clip_lora, show_help, )
        else:
            return (model, clip, show_help, )

#---------------------------------------------------------------------------------------------------------------------#        
class CR_CycleText:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Sequential"]
    
        return {"required": {"mode": (modes,),
                             "text_list": ("TEXT_LIST",),
                             "frame_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),         
                             "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "cycle_text"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def cycle_text(self, mode, text_list, frame_interval, loops, current_frame,):
        
        # Initialize the list
        text_params = list()

        # Extend text_params with text_list items
        if text_list:
            for _ in range(loops):
                text_params.extend(text_list)
            #print(f"[Debug] CR Cycle Text:{text_params}")

        if mode == "Sequential":
            # Calculate the index of the current text string based on the current_frame and frame_interval
            current_text_index = (current_frame // frame_interval) % len(text_params)
            #print(f"[Debug] CR Cycle Text:{current_text_index}")

            # Get the parameters of the current text            
            current_text_params = text_params[current_text_index]
            print(f"[Debug] CR Cycle Text:{current_text_params}")
            text_alias, current_text_item = current_text_params            
            #print(f"[Debug] CR Cycle Text:{current_text_item}")
            
            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Cycler-Nodes#cr-cycle-text"

            return (current_text_item, show_help, )

#---------------------------------------------------------------------------------------------------------------------#        
class CR_CycleTextSimple:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Sequential"]
    
        return {"required": {"mode": (modes,),
                             "frame_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),         
                             "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
                "optional": {"text_1": ("STRING", {"multiline": False, "default": ""}),
                             "text_2": ("STRING", {"multiline": False, "default": ""}),
                             "text_3": ("STRING", {"multiline": False, "default": ""}),
                             "text_4": ("STRING", {"multiline": False, "default": ""}),               
                             "text_5": ("STRING", {"multiline": False, "default": ""}),
                             "text_list_simple": ("TEXT_LIST_SIMPLE",),
                },                                           
        }
    
    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "cycle_text"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def cycle_text(self, mode, frame_interval, loops, current_frame,
        text_1, text_2, text_3, text_4, text_5,
        text_list_simple=None ):
        
        # Initialize the list
        text_params = list()
        
        text_list = list() 
        if text_1 != "":
            text_list.append(text_1)
        if text_2 != "":     
            text_list.append(text_2)
        if text_3 != "":             
            text_list.append(text_3)
        if text_4 != "":             
            text_list.append(text_4)
        if text_5 != "": 
            text_list.append(text_5)
        
        # Extend text_params with text items
        for _ in range(loops):
            if text_list_simple:
                text_params.extend(text_list_simple)
            text_params.extend(text_list)     
        #print(f"[Debug] CR Cycle Text:{len(text_params)}")
        #print(f"[Debug] CR Cycle Text:{text_params}")
        
        if mode == "Sequential":
            # Calculate the index of the current text string based on the current_frame and frame_interval
            current_text_index = (current_frame // frame_interval) % len(text_params)
            #print(f"[Debug] CR Cycle Text:{current_text_index}")

            # Get the parameters of the current text            
            current_text_item = text_params[current_text_index]          
            #print(f"[Debug] CR Cycle Text
            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Cycler-Nodes#cr-cycle-text-simple"

            return (current_text_item, show_help, )

#---------------------------------------------------------------------------------------------------------------------#        
class CR_CycleImages:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Sequential"]
    
        return {"required": {"mode": (modes,),
                             "image_list": ("IMAGE_LIST",),
                             "frame_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),         
                             "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "cycle"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def cycle(self, mode, image_list, frame_interval, loops, current_frame,):
    
        # Initialize the list
        image_params = list()

        # Extend image_params with image_list items
        if image_list:
            for _ in range(loops):
                image_params.extend(image_list)

        if mode == "Sequential":
            # Calculate the index of the current image string based on the current_frame and frame_interval
            current_image_index = (current_frame // frame_interval) % len(image_params)
            print(f"[Debug] CR Cycle Image:{current_image_index}")

            # Get the parameters of the current image            
            current_image_params = image_params[current_image_index]
            image_alias, current_image_item = current_image_params            
            
            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Cycler-Nodes#cr-cycle-images"

            return (current_image_item, show_help, ) 
                
#---------------------------------------------------------------------------------------------------------------------#        
class CR_CycleImagesSimple:

    @classmethod
    def INPUT_TYPES(s):
    
        modes = ["Sequential"]
    
        return {"required": {"mode": (modes,),
                             "frame_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),         
                             "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,})
                },
                "optional": {"image_1": ("IMAGE",),
                             "image_2": ("IMAGE",),
                             "image_3": ("IMAGE",),
                             "image_4": ("IMAGE",),              
                             "image_5": ("IMAGE",),
                             "image_list_simple": ("IMAGE_LIST_SIMPLE",)
                }                                           
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "cycle_image"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def cycle_image(self, mode, frame_interval, loops, current_frame,
        image_1=None, image_2=None, image_3=None, image_4=None, image_5=None,
        image_list_simple=None ):
        
        # Initialize the list
        image_params = list()
        
        image_list = list()
        if image_1 != None:        
            image_list.append(image_1),
        if image_2 != None: 
            image_list.append(image_2),
        if image_3 != None: 
            image_list.append(image_3),
        if image_4 != None: 
            image_list.append(image_4),
        if image_5 != None: 
            image_list.append(image_5),
        
        # Extend image_params with image items
        for _ in range(loops):
            if image_list_simple:
                image_params.extend(image_list_simple)
            image_params.extend(image_list)     

        if mode == "Sequential":
            # Calculate the index of the current image string based on the current_frame and frame_interval
            current_image_index = (current_frame // frame_interval) % len(image_params)
            print(f"[Debug] CR Cycle Text:{current_image_index}")

            # Get the parameters of the current image            
            current_image_item = image_params[current_image_index]          
            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Cycler-Nodes#cr-cycle-images-simple"
            return (current_image_item, show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 6 nodes
'''
NODE_CLASS_MAPPINGS = {  
    ### Cyclers
    "CR Cycle Models":CR_CycleModels,    
    "CR Cycle LoRAs":CR_CycleLoRAs,
    "CR Cycle Images":CR_CycleImages,
    "CR Cycle Images":CR_CycleImagesSimple,
    "CR Cycle Text":CR_CycleText,
    "CR Cycle Text Simple":CR_CycleTextSimple,   
}
'''

