#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import os
import sys
import csv
import comfy.sd
import json
import folder_paths
import typing as tg
import datetime
import io
from server import PromptServer, BinaryEventTypes
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from pathlib import Path
from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
# Text Util Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_SplitString:

    @classmethod
    def INPUT_TYPES(s):  
    
        return {"required": {"text": ("STRING", {"multiline": False, "default": "text"}),
                             "delimiter": ("STRING", {"multiline": False, "default": ","}), 
                }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("string_1", "string_2", "string_3", "string_4", "show_help", )    
    FUNCTION = "split"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def split(self, text, delimiter):

        # Split the text string
        parts = text.split(delimiter)
        strings = [part.strip() for part in parts[:4]]
        string_1, string_2, string_3, string_4 = strings + [""] * (4 - len(strings))            

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-split-string"

        return (string_1, string_2, string_3, string_4, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Text:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("text", "show_help", )
    FUNCTION = "text_multiline"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def text_multiline(self, text):
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-text"

        return (text, show_help,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_MultilineText:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": True}),
                "convert_from_csv": ("BOOLEAN", {"default": False}),
                "csv_quote_char": ("STRING", {"default": "'", "choices": ["'", '"']}),
                "remove_chars": ("BOOLEAN", {"default": False}),
                "chars_to_remove": ("STRING", {"multiline": False, "default": ""}),
                "split_string": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("multiline_text", "show_help", )
    FUNCTION = "text_multiline"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def text_multiline(self, text, chars_to_remove, split_string=False, remove_chars=False, convert_from_csv=False, csv_quote_char="'"):
    
        new_text = []

        # Remove trailing commas
        text = text.rstrip(',')

        if convert_from_csv:
            # Convert CSV to multiline text
            csv_reader = csv.reader(io.StringIO(text), quotechar=csv_quote_char)
            for row in csv_reader:
                new_text.extend(row)       
        if split_string: 
            if text.startswith("'") and text.endswith("'"):
                text = text[1:-1]  # Remove outer single quotes
                values = [value.strip() for value in text.split("', '")]
                new_text.extend(values)
            elif text.startswith('"') and text.endswith('"'):
                    text = text[1:-1]  # Remove outer single quotes
                    values = [value.strip() for value in text.split('", "')]
                    new_text.extend(values)   
            elif ',' in text and text.count("'") % 2 == 0:
                # Assume it's a list-like string and split accordingly
                text = text.replace("'", '')  # Remove single quotes
                values = [value.strip() for value in text.split(",")]
                new_text.extend(values)
            elif ',' in text and text.count('"') % 2 == 0:
                    # Assume it's a list-like string and split accordingly
                    text = text.replace('"', '')  # Remove single quotes
                    values = [value.strip() for value in text.split(",")]
                    new_text.extend(values)                 
        if convert_from_csv == False and split_string == False:
            # Process multiline text
            for line in io.StringIO(text):    
                if not line.strip().startswith('#'):
                    if not line.strip().startswith("\n"):
                        line = line.replace("\n", '')
                    if remove_chars:
                        # Remove quotes from each line
                        line = line.replace(chars_to_remove, '')
                    new_text.append(line)                

        new_text = "\n".join(new_text)
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-multiline-text"

        return (new_text, show_help,)

#---------------------------------------------------------------------------------------------------------------------# 
class CR_SaveTextToFile:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                        "multiline_text": ("STRING", {"multiline": True, "default": ""}),
                        "output_file_path": ("STRING", {"multiline": False, "default": ""}),
                        "file_name": ("STRING", {"multiline": False, "default": ""}),
                        "file_extension": (["txt", "csv"],),
                        }
        }
        
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("show_help", ) 
    OUTPUT_NODE= True
    FUNCTION = 'save_list'
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def save_list(self, multiline_text, output_file_path, file_name, file_extension):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-save-text-to-file" 
    
        filepath = output_file_path + "\\" + file_name + "." + file_extension
 
        index = 1

        if(output_file_path == "" or file_name == ""):
            print(f"[Warning] CR Save Text List. No file details found. No file output.") 
            return ()

        while os.path.exists(filepath):
            if os.path.exists(filepath):
                filepath = output_file_path + "\\" + file_name + "_" + str(index) + "." + file_extension
                index = index + 1
            else:
                break            
        
        print(f"[Info] CR Save Text List: Saving to {filepath}")        
        
        if file_extension == "csv":
            text_list = []
            for i in multiline_text.split("\n"):
                text_list.append(i.strip())
        
            with open(filepath, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write each line as a separate row in the CSV file
                for line in text_list:           
                    csv_writer.writerow([line])    
        else:
            with open(filepath, "w", newline="") as text_file:
                for line in multiline_text:
                    text_file.write(line)
        
        return (show_help, )  

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextConcatenate:

    @ classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                "text1": ("STRING", {"multiline": False, "default": "", "forceInput": True}),
                "text2": ("STRING", {"multiline": False, "default": "", "forceInput": True}),
                "separator": ("STRING", {"multiline": False, "default": ""}),
        }}

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "concat_text"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def concat_text(self, text1, text2, separator, ):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-save-text-to-file" 
        
        return (text1 + separator + text2, )
   
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### Utils Text
    "CR Text": CR_Text,
    "CR Multiline Text": CR_MultilineText,
    "CR Split String": CR_SplitString,
    "CR Text Concatenate": CR_TextConcatenate,
    "CR Save Text To File": CR_SaveTextToFile,     
}
'''

