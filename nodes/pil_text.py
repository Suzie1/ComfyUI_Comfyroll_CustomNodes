#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import os 
from PIL import Image, ImageDraw, ImageOps
from .pil_text_functions import (draw_masked_text,
                                 draw_text_on_image,
                                 get_font_size)

font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

#---------------------------------------------------------------------------------------------------------------------#

# Dictionary to map color names to RGB values
color_mapping = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "gray": (128, 128, 128),
    "lightgray": (211, 211, 211),
    "darkgray": (169, 169, 169),
    "olive": (128, 128, 0),
    "lime": (0, 128, 0),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "maroon": (128, 0, 0),
    "fuchsia": (255, 0, 128),
    "aqua": (0, 255, 128),
    "silver": (192, 192, 192),
    "gold": (255, 215, 0),
    "turquoise": (64, 224, 208),
    "lavender": (230, 230, 250),
    "violet": (238, 130, 238),
    "coral": (255, 127, 80),
    "indigo": (75, 0, 130),    
}

COLORS = ["custom", "white", "black", "red", "green", "blue", "yellow",
          "cyan", "magenta", "orange", "purple", "pink", "brown", "gray",
          "lightgray", "darkgray", "olive", "lime", "teal", "navy", "maroon",
          "fuchsia", "aqua", "silver", "gold", "turquoise", "lavender",
          "violet", "coral", "indigo"]
          
ALIGN_OPTIONS = ["top", "center", "bottom"]                 
ROTATE_OPTIONS = ["text center", "image center"]
JUSTIFY_OPTIONS = ["left", "center", "right"]
PERSPECTIVE_OPTIONS = ["top", "bottom", "left", "right"]

#---------------------------------------------------------------------------------------------------------------------#

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Remove the '#' character, if present
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)
    
#---------------------------------------------------------------------------------------------------------------------#
class CR_OverlayText:

    @classmethod
    def INPUT_TYPES(s):
                        
        return {"required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (COLORS,), 
                "align": (ALIGN_OPTIONS,),
                "justify": (JUSTIFY_OPTIONS,),
                "margins": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "line_spacing": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                "rotation_options": (ROTATE_OPTIONS,),
                },
                "optional": {"font_color_hex": ("STRING", {"multiline": False, "default": "#000000"})
                }        
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "overlay_text"
    CATEGORY = "Comfyroll/Image/Text"

    def overlay_text(self, image, text, font_name, font_size, font_color,  
                     margins, line_spacing,
                     position_x, position_y,
                     align, justify,
                     rotation_angle, rotation_options,
                     font_color_hex='#000000'):

        # Get RGB values for the text color  
        if font_color == "custom":
            text_color = hex_to_rgb(font_color_hex)
        else:
            text_color = color_mapping.get(font_color, (0, 0, 0))  # Default to black if the color is not found

        # Convert tensor images
        image_3d = image[0, :, :, :]

        # Create PIL images for the text and background layers and text mask
        back_image = tensor2pil(image_3d)
        text_image = Image.new('RGB', back_image.size, text_color)
        text_mask = Image.new('L', back_image.size)
        
        # Draw the text on the text mask
        rotated_text_mask = draw_masked_text(text_mask, text, font_name, font_size,
                                             margins, line_spacing, 
                                             position_x, position_y,
                                             align, justify,
                                             rotation_angle, rotation_options)

        # Composite the text image onto the background image using the rotated text mask       
        image_out = Image.composite(text_image, back_image, rotated_text_mask)       
        
        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out), 

#---------------------------------------------------------------------------------------------------------------------#
class CR_DrawText:

    @classmethod
    def INPUT_TYPES(s):
                        
        return {"required": {
                "image_width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "image_height": ("INT", {"default": 512, "min": 64, "max": 2048}),  
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (COLORS,),
                "background_color": (COLORS,),
                "align": (ALIGN_OPTIONS,),
                "justify": (JUSTIFY_OPTIONS,),
                "margins": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "line_spacing": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                "rotation_options": (ROTATE_OPTIONS,),            
                },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"})
                }          
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw_text"
    CATEGORY = "Comfyroll/Image/Text"

    def draw_text(self, image_width, image_height, text,
                  font_name, font_size, font_color, background_color,
                  margins, line_spacing,
                  position_x, position_y,
                  align, justify,
                  rotation_angle, rotation_options,
                  font_color_hex='#000000', bg_color_hex='#000000'):

        # Get RGB values for the text and background colors    
        if font_color == "custom":
            text_color = hex_to_rgb(font_color_hex)
        else:
            text_color = color_mapping.get(font_color, (0, 0, 0))  # Default to black if the color is not found
        if background_color == "custom":
            bg_color = hex_to_rgb(bg_color_hex)
        else:
            bg_color = color_mapping.get(background_color, (255, 255, 255))  # Default to white if the color is not found
        
        # Create PIL images for the text and background layers and text mask
        size = (image_width, image_height)
        text_image = Image.new('RGB', size, text_color)
        back_image = Image.new('RGB', size, bg_color)
        text_mask = Image.new('L', back_image.size)

        # Draw the text on the text mask
        rotated_text_mask = draw_masked_text(text_mask, text, font_name, font_size,
                                             margins, line_spacing,
                                             position_x, position_y,
                                             align, justify,
                                             rotation_angle, rotation_options)

        # Composite the text image onto the background image using the rotated text mask
        image_out = Image.composite(text_image, back_image, rotated_text_mask)
        
        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out), 
    
#---------------------------------------------------------------------------------------------------------------------#
class CR_MaskText:

    @classmethod
    def INPUT_TYPES(s):
                      
        return {"required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "background_color": (COLORS,),
                "align": (ALIGN_OPTIONS,),
                "justify": (JUSTIFY_OPTIONS,),
                "margins": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "line_spacing": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                "rotation_options": (ROTATE_OPTIONS,),             
                },
                "optional": {
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"})
                }         
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "mask_text"
    CATEGORY = "Comfyroll/Image/Text"
    
    def mask_text(self, image, text, font_name, font_size,
                  margins, line_spacing, 
                  position_x, position_y, background_color, 
                  align, justify,
                  rotation_angle, rotation_options,
                  bg_color_hex='#000000'):

        # Get RGB values for the background color
        if background_color == "custom":
            bg_color = hex_to_rgb(bg_color_hex)
        else:
            bg_color = color_mapping.get(background_color, (255, 255, 255))  # Default to white if the color is not found
        
        # Convert tensor images
        image_3d = image[0, :, :, :]
            
        # Create PIL images for the text and background layers and text mask
        text_image = tensor2pil(image_3d)        
        text_mask = Image.new('L', text_image.size)
        background_image = Image.new('RGB', text_mask.size, bg_color)        

        # Draw the text on the text mask
        rotated_text_mask = draw_masked_text(text_mask, text, font_name, font_size,
                                             margins, line_spacing,
                                             position_x, position_y,
                                             align, justify,
                                             rotation_angle, rotation_options)

        # Invert the text mask (so the text is white and the background is black)
        text_mask = ImageOps.invert(rotated_text_mask)        

        # Composite the text image onto the background image using the inverted text mask        
        image_out = Image.composite(background_image, text_image, text_mask)
        
        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out),

#---------------------------------------------------------------------------------------------------------------------#
class CR_CompositeText:

    @classmethod
    def INPUT_TYPES(s):
                             
        return {"required": {
                "image_text": ("IMAGE",),
                "image_background": ("IMAGE",),
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "align": (ALIGN_OPTIONS,),
                "justify": (JUSTIFY_OPTIONS,),
                "margins": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "line_spacing": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                "rotation_options": (ROTATE_OPTIONS,),
                }        
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "composite_text"
    CATEGORY = "Comfyroll/Image/Text"
    
    def composite_text(self, image_text, image_background, text,
                       font_name, font_size, 
                       margins, line_spacing,
                       position_x, position_y,
                       align, justify,
                       rotation_angle, rotation_options):

        # Convert tensor images
        image_text_3d = image_text[0, :, :, :]
        image_back_3d = image_background[0, :, :, :]
            
        # Create PIL images for the text and background layers and text mask
        text_image = tensor2pil(image_text_3d)
        back_image = tensor2pil(image_back_3d)
        text_mask = Image.new('L', back_image.size)

        # Draw the text on the text mask
        rotated_text_mask = draw_masked_text(text_mask, text, font_name, font_size,
                                             margins, line_spacing,
                                             position_x, position_y,
                                             align, justify,
                                             rotation_angle, rotation_options)
                                             
        # Composite the text image onto the background image using the rotated text mask
        image_out = Image.composite(text_image, back_image, rotated_text_mask)
        
        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out),
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleMemeTemplate:

    @classmethod
    def INPUT_TYPES(s):

        bar_opts = ["no bars", "top", "bottom", "top and bottom"]
        colors = COLORS[1:]
        simple_meme_presets = ["custom",
                               "One Does Not Simply ... MEME IN COMFY",
                               "This is fine.",
                               "Good Morning ... No Such Thing!"]        
        
        return {"required": {
                "image": ("IMAGE",),
                "preset": (simple_meme_presets,),   
                "text_top": ("STRING", {"multiline": True, "default": "text_top"}),
                "text_bottom": ("STRING", {"multiline": True, "default": "text_bottom"}),
                "font_name": (file_list,),
                "max_font_size": ("INT", {"default": 150, "min": 20, "max": 500}),
                "font_color": (colors,),
                "font_outline": (["none", "thin", "thick"],),
                "bar_color": (colors,),
                "bar_options": (bar_opts,),
                }        
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_meme"
    CATEGORY = "Comfyroll/Image/Text"

    def make_meme(self, image, preset,
                  text_top, text_bottom,
                  font_name, max_font_size, font_color, font_outline,
                  bar_color, bar_options):

        text_color = color_mapping.get(font_color, (0, 0, 0))  # Default to black if the color is not found
        
        # Convert tensor images
        image_3d = image[0, :, :, :]

        # Calculate the height factor
        if bar_options == "top":
            height_factor = 1.2
        elif bar_options == "bottom":
            height_factor = 1.2
        elif bar_options == "top and bottom":
            height_factor = 1.4
        else:
            height_factor = 1.0
        
        if preset == "One Does Not Simply ... MEME IN COMFY":
            text_top = "One Does Not Simply"
            text_bottom = "MEME IN COMFY"
        if preset == "This is fine.":
            text_top = "This is fine."
            text_bottom = ""            
        if preset == "Good Morning ... No Such Thing!":
            text_top = "Good Morning"
            text_bottom = "\"No Such Thing!\""  
        
        # Create PIL images for the image and text bars
        back_image = tensor2pil(image_3d)   
        size = back_image.width, int(back_image.height * height_factor)
        result_image = Image.new("RGB", size)

        # Define font settings
        #font_file = "fonts\\" + str(font_name)
        font_file = os.path.join("fonts", font_name)
        resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    
        # Create the drawing context
        draw = ImageDraw.Draw(result_image)
 
        # Create two color bars at the top and bottom
        bar_width = back_image.width
        bar_height = back_image.height // 5    ### add parameter for this in adv node
        top_bar = Image.new("RGB", (bar_width, bar_height), bar_color)
        bottom_bar = Image.new("RGB", (bar_width, bar_height), bar_color)

        # Composite the result image onto the input image
        if bar_options == "top" or bar_options == "top and bottom":
            image_out = result_image.paste(back_image, (0, bar_height))
        else:
            image_out = result_image.paste(back_image, (0, 0))
        
        # Get the font size and draw the text
        if bar_options == "top" or bar_options == "top and bottom":
            result_image.paste(top_bar, (0, 0))
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, font_outline)
            
        if bar_options == "bottom" or bar_options == "top and bottom":
            result_image.paste(bottom_bar, (0, (result_image.height - bar_height)))
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            if bar_options == "bottom":
                y_position = back_image.height
            else:
                y_position = bar_height + back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, font_outline)

        # Overlay text on image
        if bar_options == "bottom" and text_top > "":
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, font_outline)

        if (bar_options == "top" or bar_options == "none") and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, font_outline)

        if bar_options == "no bars" and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height - bar_height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, font_outline)

        if bar_options == "no bars" and text_top > "":
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, font_outline)
 
        show_help = """Help:
        
        The two text entry boxes are for the top and bottom text.
        these can be added either on a color bar or as an overlay.
        Both top and bottom text are optional.
        
        Only the first two lines will be used for top and bottom text.
        If you enter more than two lines any additional lines will be ignored.
        
        If you enter both top and bottom text and select a single bar (top or bottom),
        then one of texts will be ouput as overlay text.
        
        If you enter both top and bottom text and select no bars,
        then both texts will be ouput as overlay text."""
        
        image_out = np.array(result_image).astype(np.float32) / 255.0
        image_out = torch.from_numpy(image_out).unsqueeze(0)          
        
        # Convert the PIL image back to a torch tensor
        #return (pil2tensor(image_out), show_help, )
        return (image_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Overlay Text":CR_OverlayText,
    "CR Draw Text":CR_DrawText, 
    "CR Mask Text":CR_MaskText,
    "CR Composite Text":CR_CompositeText,
    "CR Draw Perspective Text":CR_DrawPerspectiveText,
    "CR Simple Meme Template":CR_SimpleMemeTemplate,
}
'''

