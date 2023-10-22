#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import math
import torch
import os 
from PIL import Image, ImageDraw, ImageFont, ImageOps

#try:
#    import Markdown
#except ImportError:
#    import pip
#    pip.main(['install', 'Markdown'])

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

COLORS = ["white", "black", "red", "green", "blue", "yellow",
          "cyan", "magenta", "orange", "purple", "pink", "brown", "gray",
          "lightgray", "darkgray", "olive", "lime", "teal", "navy", "maroon",
          "fuchsia", "aqua", "silver", "gold", "turquoise", "lavender",
          "violet", "coral", "indigo"]
          
ALIGN_OPTIONS = ["center", "top left", "top right", "top center", 
                 "bottom left", "bottom right", "bottom center"]
                 
ROTATE_OPTIONS = ["text center", "image center"]

JUSTIFY_OPTIONS = ["tbd"]

#---------------------------------------------------------------------------------------------------------------------#

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def align_text(align_txt, img_center_x, img_center_y, img_width, img_height, pos_x, pos_y, txt_width, txt_height, txt_padding):
    if align_txt == "center":
        txt_center_x = img_center_x + pos_x - txt_width / 2
        txt_center_y = img_center_y + pos_y - txt_height / 2
    elif align_txt == "top left":
        txt_center_x = pos_x + txt_padding
        txt_center_y = pos_y + txt_padding            
    if align_txt == "top right":
        txt_center_x = img_width + pos_x - txt_width - txt_padding
        txt_center_y = pos_y + txt_padding
    elif align_txt == "top center":
        txt_center_x = img_width/2 + pos_x - txt_width/2 - txt_padding
        txt_center_y = pos_y + txt_padding               
    elif align_txt == "bottom left":
        txt_center_x = pos_x + txt_padding
        txt_center_y = img_height + pos_y - txt_height - txt_padding
    elif align_txt == "bottom right":
        txt_center_x = img_width + pos_x - txt_width - txt_padding
        txt_center_y = img_height + pos_y - txt_height - txt_padding
    elif align_txt == "bottom center":
        txt_center_x = img_width/2 + pos_x - txt_width/2 - txt_padding
        txt_center_y = img_height + pos_y - txt_height - txt_padding
    return (txt_center_x, txt_center_y, )     

#---------------------------------------------------------------------------------------------------------------------#
class CR_OverlayText:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
                        
        return {"required": {
            "image": ("IMAGE",),
            "text": ("STRING", {"multiline": True, "default": "text"}),
            "font_name": (file_list,),
            "font_size": ("INT", {"default": 50, "min": 1, "max": 256}),
            "font_color": (COLORS,),
            "alignment_options": (ALIGN_OPTIONS,),
            "justify": (JUSTIFY_OPTIONS,),
            "text_padding": ("INT", {"default": 0, "min": 0, "max": 1024}),
            "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "rotation_angle": ("INT", {"default": 0, "min": 0, "max": 0}),
            "rotation_options": (["tbd"],),
        }       
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "overlay_text"
    CATEGORY = "Comfyroll/Image"

    def overlay_text(self, image, text, font_name, font_size, font_color, 
                     text_padding, position_x, position_y, alignment_options, justify,
                     rotation_angle, rotation_options):
    
        text_color = color_mapping.get(font_color, (0, 0, 0))  # Default to black if the color is not found
        
        image_3d = image[0, :, :, :]
            
        # Create a PIL image from the NumPy array
        pil_image = tensor2pil(image_3d)

        # Create a drawing context        
        draw = ImageDraw.Draw(pil_image)

        # Define font settings
        font_file = "fonts\\" + str(font_name)
        resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
        font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

        # Calculate the size of the text plus padding
        text_width, text_height = draw.textsize(text, font=font)
        text_width = text_width + 2 * text_padding
        text_height = text_height + 2 * text_padding

        # Get the image width and height
        image_width, image_height = pil_image.size
        image_center_x = image_width / 2
        image_center_y = image_height / 2
               
        # Get the text centers             
        text_center_x, text_center_y = align_text(alignment_options, image_center_x, image_center_y, image_width, image_height, 
            position_x, position_y, text_width, text_height, text_padding)
        
        draw.text((text_center_x, text_center_y), text, font=font, fill=text_color)             

        # Convert the PIL image back to a torch tensor
        return pil2tensor(pil_image), 

#---------------------------------------------------------------------------------------------------------------------#
class CR_DrawText:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
                        
        return {"required": {
            "image_width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "image_height": ("INT", {"default": 512, "min": 64, "max": 2048}),  
            "text": ("STRING", {"multiline": True, "default": "text"}),
            "font_name": (file_list,),
            "font_size": ("INT", {"default": 50, "min": 1, "max": 256}),
            "font_color": (COLORS,),
            "background_color": (COLORS,),
            "alignment_options": (ALIGN_OPTIONS,),
            "justify": (["tbd"],),
            "text_padding": ("INT", {"default": 0, "min": 0, "max": 1024}),
            "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "rotation_angle": ("INT", {"default": 0, "min": 0, "max": 0}),
            "rotation_options": (["tbd"],),             
        },        
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw_text"
    CATEGORY = "Comfyroll/Image"

    def draw_text(self, image_width, image_height, text,
                  font_name, font_size, font_color, background_color,
                  text_padding, position_x, position_y,
                  alignment_options, justify,
                  rotation_angle, rotation_options):
    
        text_color = color_mapping.get(font_color, (0, 0, 0))  # Default to black if the color is not found
        background_color = color_mapping.get(background_color, (255, 255, 255))  # Default to white if the color is not found
        
        # Create a blank canvas
        size = (image_height, image_width)
        pil_image = Image.new("RGB", size, background_color)

        # Create a drawing context        
        draw = ImageDraw.Draw(pil_image)

        # Define font settings
        font_file = "fonts\\" + str(font_name)
        resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
        font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

        # Calculate the size of the text plus padding
        text_width, text_height = draw.textsize(text, font=font)
        text_width = text_width + 2 * text_padding
        text_height = text_height + 2 * text_padding

        # Get the image width and height
        image_width, image_height = pil_image.size
        image_center_x = image_width / 2
        image_center_y = image_height / 2
           
        # Get the text centers             
        text_center_x, text_center_y = align_text(alignment_options, image_center_x, image_center_y, image_width, image_height, 
            position_x, position_y, text_width, text_height, text_padding)

        draw.text((text_center_x, text_center_y), text, font=font, fill=text_color)            

        # Convert the PIL image back to a torch tensor
        return pil2tensor(pil_image), 
    
#---------------------------------------------------------------------------------------------------------------------#
class CR_MaskText:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
                        
        return {"required": {
            "image": ("IMAGE",),
            "text": ("STRING", {"multiline": True, "default": "text"}),
            "font_name": (file_list,),
            "font_size": ("INT", {"default": 50, "min": 1, "max": 256}),
            "background_color": (COLORS,),
            "alignment_options": (ALIGN_OPTIONS,),
            "justify": (["tbd"],),
            "text_padding": ("INT", {"default": 0, "min": 0, "max": 1024}),
            "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "rotation_angle": ("INT", {"default": 0, "min": -360, "max": 360}),
            "rotation_options": (ROTATE_OPTIONS,),             
        }        
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "mask_text"
    CATEGORY = "Comfyroll/Image"
    
    def mask_text(self, image, text, font_name, font_size, text_padding, 
                     position_x, position_y, background_color,
                     alignment_options, justify,
                     rotation_angle, rotation_options):

        background_color = color_mapping.get(background_color, (255, 255, 255))  # Default to white if the color is not found 

        image_3d = image[0, :, :, :]
            
        # Create a PIL image from the NumPy array
        text_image = tensor2pil(image_3d)
        #text_image = text_image.convert("RGB")

        # Create a blank canvas with the same size as the text image
        text_mask = Image.new('L', text_image.size)

        # Create a drawing context for the text mask        
        draw = ImageDraw.Draw(text_mask)

        # Define font settings
        font_file = "fonts\\" + str(font_name)
        resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
        font = ImageFont.truetype(resolved_font_path, size=font_size)

        # Calculate the size of the text plus padding
        text_width, text_height = draw.textsize(text, font=font)
        text_width = text_width + 2 * text_padding
        text_height = text_height + 2 * text_padding

        # Get the image width and height
        image_width, image_height = text_mask.size
        image_center_x = image_width / 2
        image_center_y = image_height / 2

        # Get the text centers             
        text_center_x, text_center_y = align_text(alignment_options, image_center_x, image_center_y, image_width, image_height, 
            position_x, position_y, text_width, text_height, text_padding)

        # Add the text to the text mask
        draw.text((text_center_x, text_center_y), text, fill=255, font=font)
        
        # Rotate the text about the text center
        if rotation_options == "text center":
            rotated_text_mask = text_mask.rotate(rotation_angle, center=(text_center_x, text_center_y))
        elif rotation_options == "image center":    
            rotated_text_mask = text_mask.rotate(rotation_angle, center=(image_center_x, image_center_y))         
        
        # Invert the text mask (so the text is white and the background is black)
        text_mask = ImageOps.invert(rotated_text_mask)
        
        background_image = Image.new('RGB', text_mask.size, background_color)
        
        image_out = Image.composite(background_image, text_image, text_mask)
        
        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out),

#---------------------------------------------------------------------------------------------------------------------#
class CR_CompositeText:

    @classmethod
    def INPUT_TYPES(s):
     
        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
                        
        return {"required": {
            "image_text": ("IMAGE",),
            "image_background": ("IMAGE",),
            "text": ("STRING", {"multiline": True, "default": "text"}),
            "font_name": (file_list,),
            "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
            "alignment_options": (ALIGN_OPTIONS,),
            "justify": (JUSTIFY_OPTIONS,),
            "text_padding": ("INT", {"default": 0, "min": 0, "max": 1024}),
            "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
            "rotation_angle": ("INT", {"default": 0, "min": -360, "max": 360}),
            "rotation_options": (ROTATE_OPTIONS,),            
        }        
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "composite_text"
    CATEGORY = "Comfyroll/Image"
    
    def composite_text(self, image_text, image_background, text, font_name, font_size, 
                     text_padding, position_x, position_y,
                     alignment_options, justify,
                     rotation_angle, rotation_options):

        image_text_3d = image_text[0, :, :, :]
        image_back_3d = image_background[0, :, :, :]
            
        # Create a PIL image from the NumPy array
        text_image = tensor2pil(image_text_3d)
        back_image = tensor2pil(image_back_3d)

        # Create a blank canvas with the same size as the text image
        text_mask = Image.new('L', back_image.size)

        # Create a drawing context for the text mask        
        draw = ImageDraw.Draw(text_mask)

        # Define font settings
        font_file = "fonts\\" + str(font_name)
        resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
        font = ImageFont.truetype(resolved_font_path, size=font_size)

        # Calculate the size of the text plus padding
        text_width, text_height = draw.textsize(text, font=font)
        text_width = text_width + 2 * text_padding
        text_height = text_height + 2 * text_padding

        # Get the image width and height
        image_width, image_height = text_mask.size
        image_center_x = image_width / 2
        image_center_y = image_height / 2

        # Get the text centers             
        text_center_x, text_center_y = align_text(alignment_options, image_center_x, image_center_y, image_width, image_height, 
            position_x, position_y, text_width, text_height, text_padding)
            
        # Add the text to the text mask
        draw.text((text_center_x, text_center_y), text, fill=255, font=font)
        
        # Rotate the text about the text center
        if rotation_options == "text center":
            rotated_text_mask = text_mask.rotate(rotation_angle, center=(text_center_x, text_center_y))
        elif rotation_options == "image center":    
            rotated_text_mask = text_mask.rotate(rotation_angle, center=(image_center_x, image_center_y))         
        
        # Invert the text mask (so the text is white and the background is black)
        text_mask = ImageOps.invert(rotated_text_mask)
        
        image_out = Image.composite(text_image, back_image, rotated_text_mask)
        
        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out),
   
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
}
'''

