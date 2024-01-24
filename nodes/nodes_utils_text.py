#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import os
import csv
import io
from ..categories import icons

class AnyType(str):
    """A special type that can be connected to any other types. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

#---------------------------------------------------------------------------------------------------------------------#
# Text Util Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_SplitString:

    @classmethod
    def INPUT_TYPES(s):  
    
        return {"required": {
                    "text": ("STRING", {"multiline": False, "default": "text"}),
                },
                "optional": {
                    "delimiter": ("STRING", {"multiline": False, "default": ","}),
                }            
        }

    RETURN_TYPES = (any_type, any_type, any_type, any_type, "STRING", )
    RETURN_NAMES = ("string_1", "string_2", "string_3", "string_4", "show_help", )    
    FUNCTION = "split"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def split(self, text, delimiter=""):

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

    RETURN_TYPES = (any_type, "STRING", )
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

    RETURN_TYPES = (any_type, "STRING", )
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
                },
                "optional": {
                "text1": ("STRING", {"multiline": False, "default": "", "forceInput": True}),                
                "text2": ("STRING", {"multiline": False, "default": "", "forceInput": True}), 
                "separator": ("STRING", {"multiline": False, "default": ""}),                
            },
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "concat_text"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def concat_text(self, text1="", text2="", separator=""):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-save-text-to-file" 
        
        return (text1 + separator + text2, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextReplace:

    @ classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "", "forceInput": True}),            
                },
            "optional": {
                "find1": ("STRING", {"multiline": False, "default": ""}),
                "replace1": ("STRING", {"multiline": False, "default": ""}),
                "find2": ("STRING", {"multiline": False, "default": ""}),
                "replace2": ("STRING", {"multiline": False, "default": ""}),
                "find3": ("STRING", {"multiline": False, "default": ""}),
                "replace3": ("STRING", {"multiline": False, "default": ""}),    
            },
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "replace_text"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def replace_text(self, text, find1="", replace1="", find2="", replace2="", find3="", replace3=""):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-text-replace" 
        
        text = text.replace(find1, replace1)
        text = text.replace(find2, replace2)
        text = text.replace(find3, replace3)
        
        return (text, show_help)    

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextBlacklist:

    @ classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "blacklist_words": ("STRING", {"multiline": True, "default": ""}),
                },
            "optional": {
                "replacement_text": ("STRING", {"multiline": False, "default": ""}),    
            },
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "replace_text"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def replace_text(self, text, blacklist_words, replacement_text=""):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-text-blacklist" 
         
        text_out = text 
        
        for line in blacklist_words.split('\n'):  # Splitting based on line return
            if line.strip():
                text_out = text_out.replace(line.strip(), replacement_text)       
    
        return (text_out, show_help)   

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextOperation:

    @ classmethod
    def INPUT_TYPES(cls):
      
        operations = ["uppercase", "lowercase", "capitalize", "invert_case", "reverse", "trim", "remove_spaces"]
    
        return {
            "required": {
                "text": ("STRING", {"multiline": False, "default": "", "forceInput": True}),            
                "operation": (operations,),
            },
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "text_operation"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def text_operation(self, text, operation):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-text_operation" 
  
        if operation == "uppercase":
            text_out = text.upper()
        elif operation == "lowercase":
            text_out = text.lower()
        elif operation == "capitalize":
            text_out = text.capitalize()
        elif operation == "invert_case":
            text_out = text.swapcase()
        elif operation == "reverse":
            text_out = text[::-1]
        elif operation == "trim":
            text_out = text.strip()
        elif operation == "remove_spaces":
            text_out = text.replace(" ", "")
        else:
            return "CR Text Operation: Invalid operation."

        return (text_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextLength:

    @ classmethod
    def INPUT_TYPES(cls):
         
        return {
            "required": {
                "text": ("STRING", {"multiline": False, "default": "", "forceInput": True}),            
            },
        }

    RETURN_TYPES = ("INT", "STRING", )
    RETURN_NAMES = ("INT", "show_help", )
    FUNCTION = "len_text"
    CATEGORY = icons.get("Comfyroll/Utils/Text")

    def len_text(self, text):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-text-length" 
  
        int_out = len(text)

        return (int_out, show_help, )
  
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
    "CR Text Replace": CR_TextReplace,
    "CR Text Blacklist": CR_TextBlacklist,   
    "CR Text Length": CR_TextLength,    
    "CR Text Operation": CR_TextOperation, 
    "CR Save Text To File": CR_SaveTextToFile,    
}
'''

