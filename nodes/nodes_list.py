#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import os
import sys
import folder_paths
import re
import comfy.sd
import csv
import math
from PIL import Image
from pathlib import Path
from ..categories import icons

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

def tensor2rgba(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t.unsqueeze(3).repeat(1, 1, 1, 4)
    elif size[3] == 1:
        return t.repeat(1, 1, 1, 4)
    elif size[3] == 3:
        alpha_tensor = torch.ones((size[0], size[1], size[2], 1))
        return torch.cat((t, alpha_tensor), dim=3)
    else:
        return t

#---------------------------------------------------------------------------------------------------------------------#
# List Nodes                
#---------------------------------------------------------------------------------------------------------------------#
class AnyType(str):
    """A special type that can be connected to any other types. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

#---------------------------------------------------------------------------------------------------------------------#
class CR_FontFileList:

    @classmethod
    def INPUT_TYPES(s):
    
        comfyroll_font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        comfyroll_file_list = [f for f in os.listdir(comfyroll_font_dir) if os.path.isfile(os.path.join(comfyroll_font_dir, f)) and f.lower().endswith(".ttf")]

        sources = ["system", "Comfyroll", "from folder"]
        
        return {"required": {"source_folder": (sources,),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),                            
                            },
                "optional": {"folder_path": ("STRING", {"default": "C:\Windows\Fonts", "multiline": False}),
                }
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("LIST", "show_help", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, source_folder, start_index, max_rows, folder_path="C:\Windows\Fonts"):

        if source_folder == "system":
            system_root = os.environ.get('SystemRoot')
            system_font_dir = os.path.join(system_root, 'Fonts')   
            file_list = [f for f in os.listdir(system_font_dir) if os.path.isfile(os.path.join(system_font_dir, f)) and f.lower().endswith(".ttf")]
        elif source_folder == "Comfyroll":
            comfyroll_font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
            file_list = [f for f in os.listdir(comfyroll_font_dir) if os.path.isfile(os.path.join(comfyroll_font_dir, f)) and f.lower().endswith(".ttf")]
        elif source_folder == "from folder":
            if folder_path != '' and folder_path is not None:
                if not os.path.exists(folder_path):
                    print(f"[Warning] CR Font File List: The folder_path `{folder_path}` does not exist")
                    return None
                font_dir = folder_path     
                file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
            else:    
                print(f"[Warning] CR Font File List: No folder_path entered")
                return None                
        else:
            pass
        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(file_list) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_rows, len(file_list))

        # Extract the desired portion of the list
        selected_files = file_list[start_index:end_index]

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-font-file-list"

        return (selected_files, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextList:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {"multiline_text": ("STRING", {"multiline": True, "default": "text"}),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),
                            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, multiline_text, start_index, max_rows):

        lines = multiline_text.split('\n')

        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(lines) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_rows, len(lines))

        # Extract the desired portion of the list
        selected_rows = lines[start_index:end_index]

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-text-list"

        return (selected_rows, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadImageList:

    @classmethod
    def INPUT_TYPES(s):
    
        input_dir = folder_paths.input_directory
        image_folder = [name for name in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,name))] 
    
        return {"required": {"input_folder": (sorted(image_folder), ),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_images": ("INT", {"default": 1, "min": 1, "max": 9999}),
               },
               "optional": {"input_path": ("STRING", {"default": '', "multiline": False}),     
               }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, start_index, max_images, input_folder, input_path=None):

        # Set the input path
        if input_path != '' and input_path is not None:
            if not os.path.exists(input_path):
                print(f"[Warning] CR Image List: The input_path `{input_path}` does not exist")
                return ("",)  
            in_path = input_path
        else:
            input_dir = folder_paths.input_directory
            in_path = os.path.join(input_dir, input_folder)

        # Check if the folder is empty
        if not os.listdir(in_path):
            print(f"[Warning] CR Image List: The folder `{in_path}` is empty")
            return None

        file_list = sorted(os.listdir(in_path), key=lambda s: sum(((s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)), ()))
        
        image_list = []
        
        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(file_list) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_images, len(file_list) - 1)
                    
        for num in range(start_index, end_index):
            img = Image.open(os.path.join(in_path, file_list[num]))
            image = img.convert("RGB")
            image_list.append(pil2tensor(image))
        
        if not image_list:
            # Handle the case where the list is empty
            print("CR Load Image List: No images found.")
            return None
            
        images = torch.cat(image_list, dim=0)
        images_out = [images[i:i + 1, ...] for i in range(images.shape[0])]

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-image-list"

        return (images_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadImageListPlus:

    @classmethod
    def INPUT_TYPES(s):
    
        input_dir = folder_paths.input_directory
        image_folder = [name for name in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,name))] 
    
        return {"required": {"input_folder": (sorted(image_folder), ),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_images": ("INT", {"default": 1, "min": 1, "max": 9999}),
               },
               "optional": {"input_path": ("STRING", {"default": '', "multiline": False}),     
               }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT", "STRING", "INT", "INT", "INT", "STRING", )
    RETURN_NAMES = ("IMAGE", "MASK", "index", "filename", "width", "height", "list_length", "show_help", )
    OUTPUT_IS_LIST = (True, True, True, True, False, False, False, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, start_index, max_images, input_folder, input_path=None, vae=None):

        # Set the input path
        if input_path != '' and input_path is not None:
            if not os.path.exists(input_path):
                print(f"[Warning] CR Image List: The input_path `{input_path}` does not exist")
                return ("",)  
            in_path = input_path
        else:
            input_dir = folder_paths.input_directory
            in_path = os.path.join(input_dir, input_folder)

        # Check if the folder is empty
        if not os.listdir(in_path):
            print(f"[Warning] CR Image List: The folder `{in_path}` is empty")
            return None

        file_list = sorted(os.listdir(in_path), key=lambda s: sum(((s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)), ()))
        
        image_list = []
        mask_list = []
        index_list = []        
        filename_list = []
        exif_list = []         
        
        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(file_list) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_images, len(file_list) - 1)
                    
        for num in range(start_index, end_index):
            filename = file_list[num]
            img_path = os.path.join(in_path, filename)
            
            img = Image.open(os.path.join(in_path, file_list[num]))            
            tensor_img = pil2tensor(img)
            image_list.append(pil2tensor(img.convert("RGB")))
            mask_list.append(tensor2rgba(tensor_img)[:,:,:,0])
           
            # Populate the image index
            index_list.append(num)

            # Populate the filename_list
            filename_list.append(filename)
            
        if not image_list:
            # Handle the case where the list is empty
            print("CR Load Image List: No images found.")
            return None

        width, height = Image.open(os.path.join(in_path, file_list[start_index])).size
            
        images = torch.cat(image_list, dim=0)
        images_out = [images[i:i + 1, ...] for i in range(images.shape[0])]

        masks = torch.cat(mask_list, dim=0)
        mask_out = [masks[i:i + 1, ...] for i in range(masks.shape[0])]
        
        list_length = end_index - start_index
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-image-list-plus"

        return (images_out, mask_out, index_list, filename_list, index_list, width, height, list_length, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ListSchedule:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"schedule": ("STRING",
                             {"multiline": True, "default": "frame_number, item_alias, [attr_value1, attr_value2]"}
                             ),
                             "end_index": ("INT", {"default": 1, "min": 1, "max": 9999}),
                },
        }
    
    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("LIST", "show_help", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "schedule"
    CATEGORY = icons.get("Comfyroll/List")

    def schedule(self, schedule, end_index):

        schedule_lines = []
      
        # Extend the list for each line in the schedule
        if schedule != "":
            lines = schedule.split('\n')
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    print(f"[Warning] CR Simple Schedule. Skipped blank line: {line}")
                    continue            
                schedule_lines.append(line)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-integer-range-list"

        return (schedule_lines, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_FloatRangeList:

    @classmethod
    def INPUT_TYPES(s):
    
        operations = ["none","sin","cos","tan"]
        
        return {"required": {"start": ("FLOAT", {"default": 0.00, "min": -99999.99, "max": 99999.99, "step": 0.01}),
                             "end": ("FLOAT", {"default": 1.00, "min": -99999.99, "max": 99999.99, "step": 0.01}),
                             "step": ("FLOAT", {"default": 1.00, "min": -99999.99, "max": 99999.99, "step": 0.01}),
                             "operation": (operations, ),
                             "decimal_places": ("INT", {"default": 2, "min": 0, "max": 10}),
                             "ignore_first_value": ("BOOLEAN", {"default": True}),
                             "max_values_per_loop": ("INT", {"default": 128, "min": 1, "max": 99999}),                              
                             "loops": ("INT", {"default": 1, "min": 1, "max": 999}),
                             "ping_pong": ("BOOLEAN", {"default": False}),
                            },
        }                        

    RETURN_TYPES = ("FLOAT", "STRING",)
    RETURN_NAMES = ("FLOAT", "show_help", )    
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'make_range'
    CATEGORY = icons.get("Comfyroll/List")

    def make_range(self, start, end, step, max_values_per_loop, operation, decimal_places, ignore_first_value, loops, ping_pong):
        
        range_values = list()
        
        for i in range(loops):
        
            if end < start and step > 0:
                step = -step
                
            current_range = list(np.arange(start, end + step, step))

            # Apply math operations to each value in the range
            if operation == "sin":
                current_range = [math.sin(value) for value in current_range]
            elif operation == "cos":
                current_range = [math.cos(value) for value in current_range]    
            elif operation == "tan":
                current_range = [math.tan(value) for value in current_range]  
            
            current_range = [round(value, decimal_places) for value in current_range]  
            
            if ping_pong:
                # Reverse the direction of the range on even iterations
                if i % 2 == 1:
                    if ignore_first_value:
                        current_range = current_range[:-1]
                    current_range = current_range[:max_values_per_loop]
                    range_values += reversed(current_range)
                else:
                    if ignore_first_value:
                        current_range = current_range[1:]
                    current_range = current_range[:max_values_per_loop]
                    range_values += current_range  
            else:
                if ignore_first_value:
                    current_range = current_range[1:]
                current_range = current_range[:max_values_per_loop]
                range_values += current_range
                    
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-float-range-list"      

        return (range_values, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_IntegerRangeList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"start": ("INT", {"default": 0, "min": -99999, "max": 99999}),
                             "end": ("INT", {"default": 0, "min": -99999, "max": 99999}),
                             "step": ("INT", {"default": 1, "min": 1, "max": 99999}),
                             "loops": ("INT", {"default": 1, "min": 1, "max": 999}),
                             "ping_pong": ("BOOLEAN", {"default": False}),
                            },
        }
        
    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("INT", "show_help", )    
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'make_range'
    CATEGORY = icons.get("Comfyroll/List")

    def make_range(self, start, end, step, loops, ping_pong):
    
        range_values = list()
        for i in range(loops):
            current_range = list(range(start, end, step))
            
            if ping_pong:
                # Reverse the direction of the range on even iterations
                if i % 2 == 1:
                    range_values += reversed(current_range)
                else:
                    range_values += current_range     
            else:
                range_values += current_range           
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-list-schedule"      

        return (range_values, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadTextList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                        "input_file_path": ("STRING", {"multiline": False, "default": ""}),
                        "file_name": ("STRING", {"multiline": False, "default": ""}),
                        "file_extension": (["txt", "csv"],),
                        }
        }
        
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help", ) 
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'load_list'
    CATEGORY = icons.get("Comfyroll/List")

    def load_list(self, input_file_path, file_name, file_extension):
           
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-load-value-list"      

        filepath = input_file_path + "\\" + file_name + "." + file_extension
        print(f"CR Load Values: Loading {filepath}")

        list = []
            
        if file_extension == "csv":
            with open(filepath, "r") as csv_file:
                for row in csv_file:
                    list.append(row)
                    
        elif file_extension == "txt":
            with open(filepath, "r") as txt_file:
                for row in txt_file:
                    list.append(row)
        else:
            pass
        
        return(list, show_help, )        

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
    CATEGORY = icons.get("Comfyroll/Other")

    def save_list(self, multiline_text, output_file_path, file_name, file_extension):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-save-text-list" 
    
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
class CR_IntertwineLists:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                            "list1": ("STRING", {"multiline": True, "default": ""}),
                            "list2": ("STRING", {"multiline": True, "default": ""}),
                            }              
        }
        
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help", )  
    OUTPUT_IS_LIST = (True, False)      
    FUNCTION = 'make_list'
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, list1, list2):
           
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-intertwine-lists"      

        # Ensure both lists have the same length
        min_length = min(len(list1), len(list2))
        
         # Initialize an empty list to store the combined elements
        combined_list = []
        
        combined_element = str(list1) + ", " + str(list2)
        combined_list.append(combined_element)
        
        return(combined_list, show_help, )            

#---------------------------------------------------------------------------------------------------------------------#
class CR_BinaryToList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                        "bit_string": ("STRING", {"multiline": True, "default": ""}),
                        }
        }
        
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help", )  
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'make_list'
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, bit_string):
           
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-binary-to-list" 
        
        list_out = [str(bit) for bit in bit_string]

        return(list_out, show_help, ) 

#---------------------------------------------------------------------------------------------------------------------#
class CR_BatchImagesFromList:
# based on ImageListToImageBatch by DrLtData

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image_list": ("IMAGE", ),}}

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image_batch", "show_help", ) 
    INPUT_IS_LIST = True
    FUNCTION = "make_batch"
    CATEGORY = "Comfyroll/List"
   
    def make_batch(self, image_list):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-binary-to-list" 
    
        if len(image_list) <= 1:
            return (image_list,)
            
        batched_images = torch.cat(image_list, dim=0)    

        return (batched_images, show_help, )            

#---------------------------------------------------------------------------------------------------------------------# 
class CR_TextListToString:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                "text_list": ("STRING", {"forceInput": True}),
                    },
                }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    INPUT_IS_LIST = True    
    FUNCTION = "joinlist"
    CATEGORY = icons.get("Comfyroll/List")

    def joinlist(self, text_list):
    
        string_out = "\n".join(text_list)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Conversion-Nodes#cr-text-list-to-string"

        return (string_out, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### List nodes
    "CR Font File List": CR_FontFileList,  
    "CR Text List": CR_TextList, 
    "CR Load Image List": CR_LoadImageList,
    "CR Load Image List Plus": CR_LoadImageListPlus,
    "CR List Schedule": CR_ListSchedule,
    "CR Float Range List": CR_FloatRangeList,
    "CR Load Text List": CR_LoadTextList,
    #"CR Save Text To File": CR_SaveTextToFile,
    "CR Intertwine Lists" : CR_IntertwineLists,
    "CR Binary To List": CR_BinaryToList,
    "CR Batch Images From List": CR_BatchImagesFromList,
    "CR Text List To String":CR_TextListToString,    
}
'''
