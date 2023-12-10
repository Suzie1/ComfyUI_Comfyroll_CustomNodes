#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import random
import os 
from PIL import Image, ImageDraw
from .graphics_functions import get_color_values
from ..categories import icons
from ..config import color_mapping, COLORS

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

#---------------------------------------------------------------------------------------------------------------------#
class CR_BinaryPatternSimple:
    
    @classmethod
    def INPUT_TYPES(s):
                 
        return {"required": {
                    "binary_pattern": ("STRING", {"multiline": True, "default": "10101"}),
                    "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                }    
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "draw_pattern"
    CATEGORY = icons.get("Comfyroll/Graphics/Pattern")

    def draw_pattern(self, binary_pattern, width, height):
        # Convert multiline binary pattern to a 2D list
        rows = binary_pattern.strip().split('\n')
        grid = [[int(bit) for bit in row.strip()] for row in rows]

        # Calculate the size of each square
        square_width = width // len(rows[0])
        square_height = height // len(rows)

        # Create a new image
        image = Image.new("RGB", (width, height), color='black')
        draw = ImageDraw.Draw(image)

        # Draw grid based on the binary pattern
        for row_index, row in enumerate(grid):
            for col_index, bit in enumerate(row):
                x1 = col_index * square_width
                y1 = row_index * square_height
                x2 = x1 + square_width
                y2 = y1 + square_height

                # Draw black square if bit is 1, else draw white square
                color = 'black' if bit == 1 else 'white'
                draw.rectangle([x1, y1, x2, y2], fill=color, outline="black")

        image_out = pil2tensor(image)
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Text-Nodes#cr-simple-binary-pattern"
 
        # Convert the PIL image back to a torch tensor
        return (image_out, show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_BinaryPattern:
    
    @classmethod
    def INPUT_TYPES(s):
                 
        return {"required": {
                    "binary_pattern": ("STRING", {"multiline": True, "default": "10101"}),
                    "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                    "background_color": (COLORS,), 
                    "color_0": (COLORS,),
                    "color_1": (COLORS,),
                    "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}), 
                    "outline_color": (COLORS,),
                    "jitter_distance": ("INT", {"default": 0, "min": 0, "max": 1024}),
                },
                "optional": {
                    "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "color0_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "color1_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "outline_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                }     
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "draw_pattern"
    CATEGORY = icons.get("Comfyroll/Graphics/Pattern")

    def draw_pattern(self, binary_pattern, width, height,
                     background_color, outline_color,
                     color_0="white", color_1="black", outline_thickness=0,
                     color0_hex='#000000', color1_hex='#000000',
                     bg_color_hex='#000000', outline_color_hex='#000000',
                     jitter_distance = 0):
                     
        # Get RGB values
        color0 = get_color_values(color_0, color0_hex, color_mapping)         
        color1 = get_color_values(color_1, color1_hex, color_mapping) 
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping) 
        outline_color = get_color_values(outline_color, outline_color_hex, color_mapping) 
        
        # Convert multiline binary pattern to a 2D list
        rows = binary_pattern.strip().split('\n')
        grid = [[int(bit) for bit in row.strip()] for row in rows]

        # Calculate the size of each square
        square_width = width // len(rows[0])
        square_height = height // len(rows)

        # Create a new image
        image = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(image)
        
        x_jitter = 0
        y_jitter = 0
        
        # Draw grid based on the binary pattern
        for row_index, row in enumerate(grid):
            for col_index, bit in enumerate(row):
                if jitter_distance != 0:
                    x_jitter = random.uniform(0, jitter_distance)
                    y_jitter = random.uniform(0, jitter_distance)
                x1 = col_index * square_width + x_jitter
                y1 = row_index * square_height + y_jitter 
                x2 = x1 + square_width + x_jitter
                y2 = y1 + square_height + y_jitter 

                # Draw black square if bit is 1, else draw white square
                color = color1 if bit == 1 else color0
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=outline_color, width=outline_thickness)

        image_out = pil2tensor(image)
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Text-Nodes#cr-binary-pattern"
 
        # Convert the PIL image back to a torch tensor
        return (image_out, show_help, )
           
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Simple Binary Pattern Simple": CR Binary Pattern Simple,    
    "CR Binary Pattern": CR_BinaryPattern,
}
'''

