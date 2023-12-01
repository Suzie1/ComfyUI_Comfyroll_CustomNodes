#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import os 
from PIL import Image, ImageDraw, ImageOps, ImageFont
from ..categories import icons
from ..config import color_mapping, COLORS
from .graphics_functions import (hex_to_rgb,
                                 get_color_values,
                                 get_font_size,
                                 draw_text_on_image,
                                 crop_and_resize_image,
                                 create_and_paste_panel)                                                       

font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

#---------------------------------------------------------------------------------------------------------------------#
        
ALIGN_OPTIONS = ["top", "center", "bottom"]                 
ROTATE_OPTIONS = ["text center", "image center"]
JUSTIFY_OPTIONS = ["left", "center", "right"]
PERSPECTIVE_OPTIONS = ["top", "bottom", "left", "right"]

#---------------------------------------------------------------------------------------------------------------------#

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 
  
#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleMemeTemplate:
    
    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        bar_opts = ["no bars", "top", "bottom", "top and bottom"]
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
                    "font_color": (COLORS,),
                    "font_outline": (["none", "thin", "thick", "extra thick"],),
                    "bar_color": (COLORS,),
                    "bar_options": (bar_opts,),
                },
                "optional": {
                    "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "bar_color_hex": ("STRING", {"multiline": False, "default": "#000000"})
                }         
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_meme"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")

    def make_meme(self, image, preset,
                  text_top, text_bottom,
                  font_name, max_font_size, font_color, font_outline,
                  bar_color, bar_options,
                  font_color_hex='#000000', bar_color_hex='#000000'):

        # Get RGB values for the text and bar colors
        text_color = get_color_values(font_color, font_color_hex, color_mapping)
        bar_color = get_color_values(bar_color, bar_color_hex, color_mapping) 
        
        total_images = []
        
        for img in image:
        
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
            back_image = tensor2pil(img)   
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
            
            #image_out = np.array(result_image).astype(np.float32) / 255.0
            #image_out = torch.from_numpy(image_out).unsqueeze(0)          
            
            # Convert the PIL image back to a torch tensor
            #return (pil2tensor(image_out), show_help, )
            #return (image_out, show_help, )
        
            # convert to tensor
            out_image = np.array(result_image.convert("RGB")).astype(np.float32) / 255.0
            out_image = torch.from_numpy(out_image).unsqueeze(0)
            total_images.append(out_image)

        images_out = torch.cat(total_images, 0)
 
        # Convert the PIL image back to a torch tensor
        return (images_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ComicPanelTemplates:

    @classmethod
    def INPUT_TYPES(s):
    
        directions = ["left to right", "right to left"]

        templates = ["custom",
                     "G22", "G33",
                     "H2", "H3",
                     "H12", "H13",
                     "H21", "H23",
                     "H31", "H32",
                     "V2", "V3",
                     "V12", "V13",
                     "V21", "V23",
                     "V31", "V32"]                           
        
        return {"required": {
                    "page_width": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "page_height": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "template": (templates,),
                    "reading_direction": (directions,),
                    "border_thickness": ("INT", {"default": 5, "min": 0, "max": 1024}),
                    "outline_thickness": ("INT", {"default": 2, "min": 0, "max": 1024}),
                    "outline_color": (COLORS,), 
                    "panel_color": (COLORS,),
                    "background_color": (COLORS,),
               },
                "optional": {
                    "images": ("IMAGE",),
                    "custom_panel_layout": ("STRING", {"multiline": False, "default": "H123"}),
                    "outline_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "panel_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")
    
    def layout(self, page_width, page_height, template, reading_direction,
               border_thickness, outline_thickness, 
               outline_color, panel_color, background_color,
               images=None, custom_panel_layout='G44',
               outline_color_hex='#000000', panel_color_hex='#000000', bg_color_hex='#000000'):

        panels = []
        k = 0
        len_images = 0
        
        # Convert tensor images to PIL
        if images is not None:
            images = [tensor2pil(image) for image in images]
            len_images = len(images)
        
        # Get RGB values for the text and background colors    
        outline_color = get_color_values(outline_color, outline_color_hex, color_mapping)
        panel_color = get_color_values(panel_color, panel_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)                    

        # Create page and apply bg color
        size = (page_width - (2 * border_thickness), page_height - (2 * border_thickness))
        page = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(page)
 
        if template == "custom":
            template = custom_panel_layout
        
        # Calculate panel positions and add to bg image
        first_char = template[0]
        if first_char == "G":
            rows = int(template[1])
            columns = int(template[2])
            panel_width = (page.width - (2 * columns * (border_thickness + outline_thickness))) // columns
            panel_height = (page.height  - (2 * rows * (border_thickness + outline_thickness))) // rows
            # Row loop
            for i in range(rows):
                # Column Loop
                for j in range(columns):
                    # Draw the panel
                    create_and_paste_panel(page, border_thickness, outline_thickness,
                                           panel_width, panel_height, page.width,
                                           panel_color, bg_color, outline_color,
                                           images, i, j, k, len_images, reading_direction)
                    k += 1

        elif first_char == "H":
            rows = len(template) - 1
            panel_height = (page.height  - (2 * rows * (border_thickness + outline_thickness))) // rows
            for i in range(rows):
                columns = int(template[i+1])
                panel_width = (page.width - (2 * columns * (border_thickness + outline_thickness))) // columns
                for j in range(columns):
                    # Draw the panel
                    create_and_paste_panel(page, border_thickness, outline_thickness,
                                           panel_width, panel_height, page.width,
                                           panel_color, bg_color, outline_color,
                                           images, i, j, k, len_images, reading_direction)
                    k += 1
                    
        elif first_char == "V":
            columns = len(template) - 1
            panel_width = (page.width - (2 * columns * (border_thickness + outline_thickness))) // columns
            for j in range(columns):
                rows = int(template[j+1])
                panel_height = (page.height  - (2 * rows * (border_thickness + outline_thickness))) // rows
                for i in range(rows):
                    # Draw the panel
                    create_and_paste_panel(page, border_thickness, outline_thickness,
                                           panel_width, panel_height, page.width,
                                           panel_color, bg_color, outline_color,
                                           images, i, j, k, len_images, reading_direction)
                    k += 1 
        
        # Add a border to the page
        if border_thickness > 0:
            page = ImageOps.expand(page, border_thickness, bg_color)
            
        show_help = "example help text"

        return (pil2tensor(page), show_help, )   

        
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Simple Meme Template": CR_SimpleMemeTemplate,
    "CR Comic Panel Templates": CR_ComicPanelTemplates,
}
'''

