#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import random
import os
import math
from PIL import Image, ImageDraw

from .functions_graphics import get_color_values
from .shapes import (
    draw_circle, draw_oval, draw_diamond, draw_square,
    draw_triangle, draw_hexagon, draw_octagon,
    draw_half_circle, draw_quarter_circle, draw_starburst, draw_star, draw_cross
    )
from ..categories import icons
from ..config import color_mapping, COLORS

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

#---------------------------------------------------------------------------------------------------------------------#
class CR_BinaryPatternSimple:
    
    @classmethod
    def INPUT_TYPES(cls):
                 
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
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pattern-Nodes-2#cr-simple-binary-pattern"
 
        # Convert the PIL image back to a torch tensor
        return (image_out, show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_BinaryPattern:
    
    @classmethod
    def INPUT_TYPES(cls):
                 
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
                    "bias": ("FLOAT", {"default": 0.50, "min": 0.00, "max": 1.00, "step": 0.05}),
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
                     jitter_distance = 0, bias=0.5):
                     
        # Get RGB values
        color0 = get_color_values(color_0, color0_hex, color_mapping)         
        color1 = get_color_values(color_1, color1_hex, color_mapping) 
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping) 
        outline_color = get_color_values(outline_color, outline_color_hex, color_mapping) 
        
        # Convert multiline binary pattern to a 2D list
        rows = binary_pattern.strip().split('\n')
        grid = [[int(bit) for bit in row.strip()] for row in rows]

        # Calculate the size of each square
        square_width = width / len(rows[0])
        square_height = height / len(rows)

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
                #color = color1 if bit == 1 else color0
                
                # Adjust color based on bias
                if random.uniform(0, 1) < abs(bias):
                    color = color1
                else:
                    color = color0

                draw.rectangle([x1, y1, x2, y2], fill=color, outline=outline_color, width=outline_thickness)

        image_out = pil2tensor(image)
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pattern-Nodes-2#cr-binary-pattern"
 
        # Convert the PIL image back to a torch tensor
        return (image_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#class CR_DrawShape:
class CR_DrawShape:

    @classmethod
    def INPUT_TYPES(cls):
                
        shapes = ["circle","oval","square","diamond","triangle","hexagon","octagon",
                  "quarter circle","half circle","quarter circle",
                  "starburst","star","cross",
                  "diagonal regions"]
        
        return {"required": {
                    "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 4096}),        
                    "shape": (shapes,),
                    "shape_color": (COLORS,), 
                    "back_color": (COLORS,),                  
                    "x_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "y_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "zoom": ("FLOAT", {"default": 1.00, "min": 0.00, "max": 10.00, "step": 0.05}),
                    "rotation": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3600.0, "step": 0.1}),
               },
                "optional": {
                    "shape_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "make_shape"
    CATEGORY = icons.get("Comfyroll/Graphics/Shape")
    
    def make_shape(self, width, height, rotation,
                      shape, shape_color, back_color,
                      x_offset=0, y_offset=0, zoom=1.0,
                      shape_color_hex='#000000', bg_color_hex='#000000'):

        bg_color = get_color_values(back_color, bg_color_hex, color_mapping) 
        shape_color = get_color_values(shape_color, shape_color_hex, color_mapping) 
          
        back_img = Image.new("RGB", (width, height), color=bg_color)
        shape_img = Image.new("RGB", (width, height), color=shape_color)
        shape_mask = Image.new('L', (width, height))
        draw = ImageDraw.Draw(shape_mask)   

        center_x = width // 2 + x_offset
        center_y = height // 2 + y_offset         
        size = min(width - x_offset, height - y_offset) * zoom
        aspect_ratio = width / height
        color = 'white'

        shape_functions = {
            'circle': draw_circle,
            'oval': draw_oval,
            'diamond': draw_diamond,
            'square': draw_square,
            'triangle': draw_triangle,
            'hexagon': draw_hexagon,
            'octagon': draw_octagon,
            'quarter circle': draw_quarter_circle,
            'half circle': draw_half_circle,
            'starburst': draw_starburst,
            'star': draw_star, 
            'cross': draw_cross,
        }

        if shape in shape_functions:
            shape_function = shape_functions.get(shape)
            shape_function(draw, center_x, center_y, size, aspect_ratio, color)

        if shape == "diagonal regions":
            draw.polygon([(width, 0), (width, height), (0, height)], fill=color)

        shape_mask = shape_mask.rotate(rotation, center=(center_x, center_y))
        
        result_image = Image.composite(shape_img, back_img, shape_mask) 

        image_out = pil2tensor(result_image)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pattern-Nodes-2#cr-draw-shape"

        return (image_out, show_help, )  

#---------------------------------------------------------------------------------------------------------------------#class CR_DrawShape:
'''
class CR_ShapeScheduler:

    @classmethod
    def INPUT_TYPES(cls):
                
        shapes = ["circle","oval","square","diamond","triangle","hexagon","octagon",
                  "quarter circle","half circle","quarter circle","starburst","star","cross","diagonal regions"]
        
        return {"required": {
                    "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 4096}),        
                    "shape": (shapes,),
                    "shape_color": (COLORS,), 
                    "back_color": (COLORS,),                  
                    "x_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "y_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "zoom": ("FLOAT", {"default": 1.00, "min": 0.00, "max": 10.00, "step": 0.05}),
                    "rotation": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3600.0, "step": 0.1}),
                    "schedule": ("STRING", {"multiline": True, "default": "schedule"}),
               },
                "optional": {
                    "shape_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "make_shape"
    CATEGORY = icons.get("Comfyroll/Graphics/Shape")
    
    def make_shape(self, width, height, rotation,
                      shape, shape_color, back_color, schedule,
                      x_offset=0, y_offset=0, zoom=1.0,
                      shape_color_hex='#000000', bg_color_hex='#000000'):

        bg_color = get_color_values(back_color, bg_color_hex, color_mapping) 
        shape_color = get_color_values(shape_color, shape_color_hex, color_mapping) 
          
        back_img = Image.new("RGB", (width, height), color=bg_color)
        shape_img = Image.new("RGB", (width, height), color=shape_color)
        shape_mask = Image.new('L', (width, height))
        draw = ImageDraw.Draw(shape_mask)   

        center_x = width // 2 + x_offset
        center_y = height // 2 + y_offset         
        size = min(width - x_offset, height - y_offset) * zoom
        aspect_ratio = width / height
        num_rays = 16
        color = 'white'

        shape_functions = {
            'circle': draw_circle,
            'oval': draw_oval,
            'diamond': draw_diamond,
            'square': draw_square,
            'triangle': draw_triangle,
            'hexagon': draw_hexagon,
            'octagon': draw_octagon,
            'quarter circle': draw_quarter_circle,
            'half circle': draw_half_circle,
            'starburst': draw_starburst,
            'star': draw_star, 
            'cross': draw_cross,
        }

        if shape in shape_functions:
            shape_function = shape_functions.get(shape)
            shape_function(draw, center_x, center_y, size, aspect_ratio, color)

        if shape == "diagonal regions":
            draw.polygon([(width, 0), (width, height), (0, height)], fill=color)

        shape_mask = shape_mask.rotate(rotation, center=(center_x, center_y))
        
        result_image = Image.composite(shape_img, back_img, shape_mask) 

        image_out = pil2tensor(result_image)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pattern-Nodes-2#cr-draw-shape"

        return (image_out, show_help, )  
'''
#---------------------------------------------------------------------------------------------------------------------#class CR_DrawShape:
class CR_DrawPie:

    @classmethod
    def INPUT_TYPES(cls):
                       
        return {"required": {
                    "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 4096}),        
                    "pie_start": ("FLOAT", {"default": 30.0, "min": 0.0, "max": 9999.0, "step": 0.1}),
                    "pie_stop": ("FLOAT", {"default": 330.0, "min": 0.0, "max": 9999.0, "step": 0.1}),
                    "shape_color": (COLORS,), 
                    "back_color": (COLORS,),                  
                    "x_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "y_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "zoom": ("FLOAT", {"default": 1.00, "min": 0.00, "max": 10.00, "step": 0.05}),
                    "rotation": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3600.0, "step": 0.1}),
               },
                "optional": {
                    "shape_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "make_shape"
    CATEGORY = icons.get("Comfyroll/Graphics/Shape")
    
    def make_shape(self, width, height, rotation,
                      pie_start, pie_stop, shape_color, back_color,
                      x_offset=0, y_offset=0, zoom=1.0,
                      shape_color_hex='#000000', bg_color_hex='#000000'):

        bg_color = get_color_values(back_color, bg_color_hex, color_mapping) 
        shape_color = get_color_values(shape_color, shape_color_hex, color_mapping) 
          
        back_img = Image.new("RGB", (width, height), color=bg_color)
        shape_img = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))     
        draw = ImageDraw.Draw(shape_img, 'RGBA')        

        center_x = width // 2 + x_offset
        center_y = height // 2 + y_offset         
        size = min(width - x_offset, height - y_offset) * zoom
        aspect_ratio = width / height
        num_rays = 16
        color = 'white'

        draw.pieslice([(center_x - size / 2, center_y - size / 2),
                   (center_x + size / 2, center_y + size / 2)], start=pie_start, end=pie_stop, fill=color, outline=None)

        shape_img = shape_img.rotate(rotation, center=(center_x, center_y))      

        # Composite the images with anti-aliasing
        result_image = Image.alpha_composite(back_img.convert("RGBA"), shape_img)

        image_out = pil2tensor(result_image.convert("RGB"))

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pattern-Nodes-2#cr-draw-pie"

        return (image_out, show_help, )  

#---------------------------------------------------------------------------------------------------------------------#
class CR_RandomShapePattern:

    @classmethod
    def INPUT_TYPES(cls):
                
        shapes = ["circle","oval","square","diamond","triangle",
                  "hexagon","octagon","half circle","quarter circle",
                  "starburst","star", "cross"]
        
        return {"required": {
                    "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 4096}),  
                    "num_rows": ("INT", {"default": 5, "min": 1, "max": 128}),
                    "num_cols": ("INT", {"default": 5, "min": 1, "max": 128}),                    
                    "color1": (COLORS,), 
                    "color2": (COLORS,),
               },
                "optional": {
                    "color1_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "color2_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "plot_random_shapes"
    CATEGORY = icons.get("Comfyroll/Graphics/Shape")

    def plot_random_shapes(self, num_rows, num_cols, width, height, color1, color2,
                           color1_hex="#000000", color2_hex="#000000"):
                           
        color1 = get_color_values(color1, color1_hex, color_mapping) 
        color2 = get_color_values(color2, color2_hex, color_mapping) 
                           
        image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(image)

        shape_functions = [
            draw_circle,
            draw_oval,
            draw_diamond,
            draw_square,
            draw_triangle,
            draw_hexagon,
            draw_octagon,
            draw_half_circle,
            draw_quarter_circle,
            draw_starburst,
            draw_star,
            draw_cross,
        ]

        for row in range(num_rows):
            for col in range(num_cols):
                shape_function = random.choice(shape_functions)
                color = random.choice([color1, color2])
                size = random.uniform(20, min(width, height) / 2)
                aspect_ratio = random.uniform(0.5, 2.0)  # For shapes that use aspect ratio

                center_x = col * (width / num_cols) + (width / num_cols) / 2
                center_y = row * (height / num_rows) + (height / num_rows) / 2
                
                shape_function(draw, center_x, center_y, size, aspect_ratio, color)

        image_out = pil2tensor(image)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pattern-Nodes-2#cr-random-shape-pattern"

        return (image_out, show_help, )  
     
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Simple Binary Pattern Simple": CR Binary Pattern Simple,    
    "CR Binary Pattern": CR_BinaryPattern,
    "CR Draw Shape": CR_DrawShape,
    "CR Random Shape Pattern: CR_RandomShapePattern,
    "CR Draw Pie": CR_DrawPie,
}
'''

