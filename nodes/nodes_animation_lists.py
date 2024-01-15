#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/Suzie1/CR-Animation-Nodes
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

import comfy.sd
import torch
import os
import sys
import folder_paths
from ..categories import icons

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------# 
# NODES
#---------------------------------------------------------------------------------------------------------------------# 
class CR_ModelList:

    @classmethod
    def INPUT_TYPES(cls):
    
        checkpoint_files = ["None"] + folder_paths.get_filename_list("checkpoints")
        
        return {"required": {
                    "ckpt_name1": (checkpoint_files,),
                    "alias1": ("STRING", {"multiline": False, "default": ""}),
                    "ckpt_name2": (checkpoint_files,),
                    "alias2": ("STRING", {"multiline": False, "default": ""}),
                    "ckpt_name3": (checkpoint_files,),
                    "alias3": ("STRING", {"multiline": False, "default": ""}),
                    "ckpt_name4": (checkpoint_files,),
                    "alias4": ("STRING", {"multiline": False, "default": ""}),                    
                    "ckpt_name5": (checkpoint_files,),
                    "alias5": ("STRING", {"multiline": False, "default": ""}),                    
                },
                "optional": {"model_list": ("MODEL_LIST",)
                },
        }

    RETURN_TYPES = ("MODEL_LIST", "STRING", )
    RETURN_NAMES = ("MODEL_LIST", "show_text", )
    FUNCTION = "model_list"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def model_list(self, ckpt_name1, alias1, ckpt_name2, alias2, ckpt_name3, alias3, ckpt_name4, alias4,
        ckpt_name5, alias5, model_list=None):

        # Initialise the list
        models = list()
        model_text = list()
        
        # Extend the list for each model in the stack
        if model_list is not None:
            models.extend([l for l in model_list if l[0] != None]) #"None"
            model_text += "\n".join(map(str, model_list)) + "\n"

        if ckpt_name1 != "None":
            model1_tup = [(alias1, ckpt_name1)]
            models.extend(model1_tup),        
            model_text += "\n".join(map(str, model1_tup)) + "\n"

        if ckpt_name2 != "None":
            model2_tup = [(alias2, ckpt_name2)]
            models.extend(model2_tup),
            model_text += "\n".join(map(str, model2_tup)) + "\n"

        if ckpt_name3 != "None":
            model3_tup = [(alias3, ckpt_name3)]
            models.extend(model3_tup),
            model_text += "\n".join(map(str, model3_tup)) + "\n"

        if ckpt_name4 != "None":
            model4_tup = [(alias4, ckpt_name4)]
            models.extend(model4_tup),
            model_text += "\n".join(map(str, model4_tup)) + "\n"
            
        if ckpt_name5 != "None":
            model5_tup = [(alias5, ckpt_name5)]       
            models.extend(model5_tup),
            model_text += "\n".join(map(str, model5_tup)) + "\n"
            
        #print(f"[TEST] CR Model List: {models}")

        show_text = "".join(model_text)
            
        return (models, show_text, )

#---------------------------------------------------------------------------------------------------------------------#  
class CR_LoRAList:
    
    @classmethod
    def INPUT_TYPES(cls):
    
        lora_files = ["None"] + folder_paths.get_filename_list("loras")
        
        return {"required": {                    
                    "lora_name1": (lora_files,),
                    "alias1": ("STRING", {"multiline": False, "default": ""}),                    
                    "model_strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    
                    "lora_name2": (lora_files,),
                    "alias2": ("STRING", {"multiline": False, "default": ""}),
                    "model_strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    
                    "lora_name3": (lora_files,),
                    "alias3": ("STRING", {"multiline": False, "default": ""}),                       
                    "model_strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),  
                },
                "optional": {"lora_list": ("lora_LIST",)
                },
        }

    RETURN_TYPES = ("LORA_LIST", "STRING", )
    RETURN_NAMES = ("LORA_LIST", "show_text", )
    FUNCTION = "lora_list"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def lora_list(self, lora_name1, model_strength_1, clip_strength_1, alias1,
    lora_name2, model_strength_2, clip_strength_2, alias2,
    lora_name3, model_strength_3, clip_strength_3, alias3, lora_list=None):

        # Initialise the list
        loras = list()
        lora_text = list()
        
        # Extend the list for each lora in the stack
        if lora_list is not None:
            loras.extend([l for l in lora_list if l[0] != None]) #"None"
            lora_text += "\n".join(map(str, lora_list)) + "\n"
        
        if lora_name1 != "None":
            lora1_tup = [(alias1, lora_name1, model_strength_1, clip_strength_1)]
            loras.extend(lora1_tup),
            lora_text += "\n".join(map(str, lora1_tup)) + "\n"
            
        if lora_name2 != "None":
            lora2_tup = [(alias2, lora_name2, model_strength_2, clip_strength_2)]        
            loras.extend(lora2_tup),
            lora_text += "\n".join(map(str, lora2_tup)) + "\n"

        if lora_name3 != "None":
            lora3_tup = [(alias3, lora_name3, model_strength_3, clip_strength_3)]          
            loras.extend(lora3_tup),        
            lora_text += "\n".join(map(str, lora3_tup)) + "\n"
           
        #print(f"[DEBUG] CR Lora List: {lora_text}")

        show_text = "".join(lora_text)
            
        return (loras, show_text, )
    
#---------------------------------------------------------------------------------------------------------------------#
'''
class CR_TextList:

    @classmethod
    def INPUT_TYPES(cls):
  
        return {"required": {
                    "text_1": ("STRING", {"multiline": False, "default": ""}),
                    "alias1": ("STRING", {"multiline": False, "default": ""}),
                    "text_2": ("STRING", {"multiline": False, "default": ""}),
                    "alias2": ("STRING", {"multiline": False, "default": ""}),
                    "text_3": ("STRING", {"multiline": False, "default": ""}),
                    "alias3": ("STRING", {"multiline": False, "default": ""}),
                    "text_4": ("STRING", {"multiline": False, "default": ""}),
                    "alias4": ("STRING", {"multiline": False, "default": ""}),                    
                    "text_5": ("STRING", {"multiline": False, "default": ""}),
                    "alias5": ("STRING", {"multiline": False, "default": ""}),                    
                },
                "optional": {"text_list": ("text_LIST",)
                },
        }

    RETURN_TYPES = ("TEXT_LIST", "STRING", )
    RETURN_NAMES = ("TEXT_LIST", "show_text", )
    FUNCTION = "text_list"
    CATEGORY = icons.get("Comfyroll/Animation/List")

    def text_list(self, text_1, alias1, text_2, alias2, text_3, alias3, text_4, alias4, text_5, alias5, text_list=None):

        # Initialise the list
        texts = list()
        showtext = list()
        
        # Extend the list for each text item in a connected list
        if text_list is not None:
            texts.extend([l for l in text_list])
        
        # Extend the list for each text item in the list
        if text_1 != "":
            text1_tup = [(alias1, text_1)]        
            texts.extend(text1_tup),
            showtext.extend([(alias1 + "," + text_1 + "\n")]),

        if text_2 != "":
            text2_tup = [(alias2, text_2)]        
            texts.extend(text2_tup),
            showtext.extend([(alias2 + "," + text_2 + "\n")]),

        if text_3 != "":
            text3_tup = [(alias3, text_3)]        
            texts.extend(text3_tup),
            showtext.extend([(alias3 + "," + text_3 + "\n")]),

        if text_4 != "":
            text4_tup = [(alias4, text_4)]        
            texts.extend(text4_tup),
            showtext.extend([(alias4 + "," + text_4 + "\n")]),
            
        if text_5 != "":
            text5_tup = [(alias5, text_5)]        
            texts.extend(text5_tup),
            showtext.extend([(alias5 + "," + text_5 + "\n")]),
            
        #print(f"[Debug] CR Text List: {texts}")

        show_text = "".join(showtext)
            
        return (texts, show_text, )
'''
#---------------------------------------------------------------------------------------------------------------------#
class CR_TextListSimple:

    @classmethod
    def INPUT_TYPES(cls):
  
        return {"required": {            
                },
                "optional": {"text_1": ("STRING", {"multiline": False, "default": ""}),
                             "text_2": ("STRING", {"multiline": False, "default": ""}),
                             "text_3": ("STRING", {"multiline": False, "default": ""}),
                             "text_4": ("STRING", {"multiline": False, "default": ""}),                    
                             "text_5": ("STRING", {"multiline": False, "default": ""}),
                             "text_list_simple": ("TEXT_LIST_SIMPLE",)
                },
        }

    RETURN_TYPES = ("TEXT_LIST_SIMPLE", "STRING", )
    RETURN_NAMES = ("TEXT_LIST_SIMPLE", "show_help", )
    FUNCTION = "text_list_simple"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def text_list_simple(self, text_1, text_2, text_3,  text_4, text_5, text_list_simple=None):

        # Initialise the list
        texts = list()
        
        # Extend the list for each text in the stack
        if text_list_simple is not None:
            texts.extend(l for l in text_list_simple)
        
        if text_1 != "" and text_1 != None:
            texts.append(text_1),

        if text_2 != "" and text_2 != None:
            texts.append(text_2)

        if text_3 != "" and text_3 != None:
            texts.append(text_3)

        if text_4 != "" and text_4 != None:
            texts.append(text_4),
            
        if text_5 != "" and text_5 != None:
            texts.append(text_5),
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-text-list-simple"

        return (texts, show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageList:

    @classmethod
    def INPUT_TYPES(cls):
    
        return {"required": {
                },
                "optional": {"image_1": ("IMAGE",),
                             "alias1": ("STRING", {"multiline": False, "default": ""}),
                             "image_2": ("IMAGE",),
                             "alias2": ("STRING", {"multiline": False, "default": ""}),
                             "image_3": ("IMAGE",),
                             "alias3": ("STRING", {"multiline": False, "default": ""}),
                             "image_4": ("IMAGE",),
                             "alias4": ("STRING", {"multiline": False, "default": ""}),                    
                             "image_5": ("IMAGE",),
                             "alias5": ("STRING", {"multiline": False, "default": ""}),
                             "image_list": ("image_LIST",)
                },
        }

    RETURN_TYPES = ("IMAGE_LIST", "STRING", )
    RETURN_NAMES = ("IMAGE_LIST", "show_help", )
    FUNCTION = "image_list"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def image_list(self,
        image_1=None, alias1=None,
        image_2=None, alias2=None,
        image_3=None, alias3=None,
        image_4=None, alias4=None,
        image_5=None, alias5=None,
        image_list=None):

        # Initialise the list
        images = list()
        
        # Extend the list for each image in the stack
        if image_list is not None:
            image_tup = [(alias1, image_1)] 
            images.extend([l for l in image_list])
        
        if image_1 != None:
            images.extend([(alias1, image_1)]),

        if image_2 != None:
            images.extend([(alias2, image_2)]), 

        if image_3 != None:
            images.extend([(alias3, image_3)]),           

        if image_4 != None:
            images.extend([(alias4, image_4)]), 
            
        if image_5 != None:
            images.extend([(alias5, image_5)]),

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-image-list"          

        return (images, show_help, )   
        
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageListSimple:

    @classmethod
    def INPUT_TYPES(cls):
  
        return {"required": {
                },
                "optional": {"image_1": ("IMAGE",),
                             "image_2": ("IMAGE",),
                             "image_3": ("IMAGE",),
                             "image_4": ("IMAGE",),                    
                             "image_5": ("IMAGE",),  
                             "image_list_simple": ("IMAGE_LIST_SIMPLE",)
                },
        }

    RETURN_TYPES = ("IMAGE_LIST_SIMPLE", "STRING", )
    RETURN_NAMES = ("IMAGE_LIST_SIMPLE", "show_help", )
    FUNCTION = "image_list_simple"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def image_list_simple(self,
        image_1=None, image_2=None, image_3=None,  image_4=None, image_5=None,
        image_list_simple=None):

        # Initialise the list
        images = list()
        
        # Extend the list for each image in the stack
        if image_list_simple is not None:
            images.append(l for l in image_list_simple)
        
        if image_1 != None:
            images.append(image_1),

        if image_2 != None:
            images.append(image_2)

        if image_3 != None:
            images.append(image_3)

        if image_4 != None:
            images.append(image_4),
            
        if image_5 != None:
            images.append(image_5),

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-image-list-simple"         

        return (images, show_help, )

#---------------------------------------------------------------------------------------------------------------------#   
class CR_InputTextList:

    @classmethod
    def INPUT_TYPES(cls):
  
        return {"required": {"text": ("STRING", {"multiline": True, "default": ""}),        
                }
        }

    RETURN_TYPES = ("TEXT_LIST_SIMPLE", "STRING", )
    RETURN_NAMES = ("TEXT_LIST_SIMPLE", "show_help", )
    FUNCTION = "text_list_simple"
    CATEGORY = icons.get("Comfyroll/Animation/Legacy")

    def text_list_simple(self, text):

        # Initialise the list
        texts = list()
        
        # Extend the list for each text line
        lines = text.split('\n')        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                print(f"[Warning] CR MultilineText. Skipped blank line: {line}")
                continue
                
            texts.append(line),    
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Animation-Utility-Nodes#cr-input-text-list"

        return (texts, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### Lists
    "CR Model List":CR_ModelList,
    "CR LoRA List":CR_LoRAList,     
    #"CR Text List":CR_TextList,
    "CR Text List Simple":CR_TextListSimple,
    "CR Image List":CR_ImageList,    
    "CR Image List Simple":CR_ImageListSimple,
    "CR Input Text List":CR_InputTextList,     
}
'''

