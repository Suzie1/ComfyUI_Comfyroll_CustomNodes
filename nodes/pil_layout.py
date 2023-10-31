#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import os 
from PIL import Image, ImageDraw, ImageOps, ImageFont
from ..categories import icons
from .pil_text_functions import (draw_masked_text,
                                 draw_text_on_image,
                                 get_font_size)

font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

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
class CR_SimpleMemeTemplate:
    
    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
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
    CATEGORY = icons.get("Comfyroll/Graphics/Template")

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
class CR_SimpleAnnotations:

    @classmethod
    def INPUT_TYPES(s):

        bar_opts = ["top", "bottom", "top and bottom", "no bars"]      
        
        return {"required": {
                "image": ("IMAGE",),  
                "text_top": ("STRING", {"multiline": True, "default": "text_top"}),
                "text_bottom": ("STRING", {"multiline": True, "default": "text_bottom"}),
                "font_name": (file_list,),
                "max_font_size": ("INT", {"default": 100, "min": 50, "max": 150}),
                "font_color": (COLORS,),
                "bar_color": (COLORS,),
                "bar_options": (bar_opts,),
                "bar_scaling_factor": ("FLOAT", {"default": 0.2, "min": 0.1, "max": 2, "step": 0.1}),
                },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bar_color_hex": ("STRING", {"multiline": False, "default": "#000000"})
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_meme"
    CATEGORY = icons.get("Comfyroll/Graphics/Text")

    def make_meme(self, image,
                  text_top, text_bottom,
                  font_name, max_font_size,
                  font_color, bar_color, bar_options, bar_scaling_factor,
                  font_color_hex='#000000',
                  bar_color_hex='#000000'):

        if font_color == "custom":
            text_color = hex_to_rgb(font_color_hex)
        else:
            text_color = color_mapping.get(font_color, (0, 0, 0))  # Default to black if the color is not found
                 
        if bar_color == "custom":
            bar_color = hex_to_rgb(bar_color_hex)

        # Convert tensor images
        image_3d = image[0, :, :, :]

        # Calculate the height factor
        if bar_options == "top":
            height_factor = 1 + bar_scaling_factor
        elif bar_options == "bottom":
            height_factor = 1 + bar_scaling_factor
        elif bar_options == "top and bottom":
            height_factor = 1 + 2 * bar_scaling_factor
        else:
            height_factor = 1.0

        # Create PIL images for the image and text bars
        back_image = tensor2pil(image_3d)   
        size = back_image.width, int(back_image.height * height_factor)
        result_image = Image.new("RGB", size)

        # Define font settings
        font_file = "fonts\\" + str(font_name)
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
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, "No")
            
        if bar_options == "bottom" or bar_options == "top and bottom":
            result_image.paste(bottom_bar, (0, (result_image.height - bar_height)))
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            if bar_options == "bottom":
                y_position = back_image.height
            else:
                y_position = bar_height + back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, "No")

        # Overlay text on image
        if bar_options == "bottom" and text_top > "":
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, "No")

        if (bar_options == "top" or bar_options == "none") and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, "No")

        if bar_options == "none" and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height - bar_height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, "No")
 
        show_help = "example help text"
        
        image_out = np.array(result_image).astype(np.float32) / 255.0
        image_out = torch.from_numpy(image_out).unsqueeze(0)          
        
        # Convert the PIL image back to a torch tensor
        #return (pil2tensor(image_out), show_help, )
        return (image_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ApplyAnnotations:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        bar_opts = ["no bars", "top", "bottom", "top and bottom"]      
        
        return {"required": {
                "image": ("IMAGE", ),  
                "annotation_stack": ("ANNOTATION_STACK", ),
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "apply_annotations"
    CATEGORY = icons.get("Comfyroll/Graphics/Text")

    def apply_annotations(self, image, annotation_stack):

        show_help = "example help text"

        return (image_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_AddAnnotation:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        bar_opts = ["no bars", "top", "bottom", "top and bottom"]      
        
        return {"required": {
                "text": ("STRING", {"multiline": True, "default": "text_top"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 100, "min": 20, "max": 150}),
                "font_color": (COLORS,),
                "position_x": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "justify": (JUSTIFY_OPTIONS,),
                },
                "optional": {
                "annotation_stack": ("ANNOTATION_STACK",),
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                }
    }

    RETURN_TYPES = ("ANNOTATION_STACK", "STRING", )
    RETURN_NAMES = ("ANNOTATION_STACK", "show_help", )
    FUNCTION = "add_annotation"
    CATEGORY = icons.get("Comfyroll/Graphics/Text")

    def add_annotation(self, image, 
                       font_name, font_size, font_color,
                       position_x, position_y, justify,
                       annotation_stack=None, font_color_hex='#000000'):
 
        show_help = "example help text"
 
        return (annotation_stack, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_MultiPanelMemeTemplate:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        templates = ["vertical - 2 image + 2 text",
                     "vertical - 3 image + 3 text",
                     "vertical - 4 image + 4 text",
                     "horizontal - 2 image + 2 text",
                     "horizontal - text bar + 2 image",
                     "text bar + 1 image with overlay text",
                     "text bar + 4 image",
                     "text bar + 4 image with overlay text"] 
        colors = COLORS[1:]                     
        
        return {"required": {
                "template": (templates,),
                "image_1": ("IMAGE",),
                "text_1": ("STRING", {"multiline": True, "default": "text_1"}),
                "text_2": ("STRING", {"multiline": True, "default": "text_2"}),
                "text_3": ("STRING", {"multiline": True, "default": "text_3"}),
                "text_4": ("STRING", {"multiline": True, "default": "text_4"}),              
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (colors,),
                "bar_color": (colors,),
                "reverse_panels": (["No", "Yes"],),
               },
                "optional": {
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                }        
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "draw_text"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")

    def draw_text(self, template, image_1, text_1, text_2, text_3, text_4,
                  font_name, font_size, font_color, bar_color, reverse_panels, image_2 = None, image_3 = None, image_4 = None):
        
        show_help = "example help text"
        
        # Convert the PIL image back to a torch tensor
        return image_1, show_help,

#---------------------------------------------------------------------------------------------------------------------#
class CR_PopularMemeTemplates:

    @classmethod
    def INPUT_TYPES(s):

        templates = ["Expanding brain",
                     "My honest reaction",
                     "The GF I want",
                     "Who would win?",
                     "I have 4 sides",
                     "This is Fine",
                     "Is This a Pigeon?",
                     "Drake hotline bling"]
        colors = COLORS[1:]                
        
        return {"required": {
                "meme": (templates,),
                "image_1": ("IMAGE",),
                        
                "text_1": ("STRING", {"multiline": True, "default": "text_1"}),
                "text_2": ("STRING", {"multiline": True, "default": "text_2"}),
                "text_3": ("STRING", {"multiline": True, "default": "text_3"}),
                "text_4": ("STRING", {"multiline": True, "default": "text_4"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (colors,),
               },
                "optional": {
                "image_2": ("IMAGE",), 
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "draw_text"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")

    def draw_text(self, meme, image_1, text_1, text_2, text_3, text_4,
                  font_name, font_size, font_color, image_2 = None, image_3 = None, image_4 = None):

        show_help = "example help text"
        
        # Convert the PIL image back to a torch tensor
        return image_1, show_help,

#---------------------------------------------------------------------------------------------------------------------#
class CR_PageLayout:

    @classmethod
    def INPUT_TYPES(s):

        directions = ["horizontal", "vertical"]               
        
        return {"required": {
                "title_bar": ("IMAGE",),
                "image_1": ("IMAGE",),
                "border_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "border_color": (COLORS,),
                "background_color": (COLORS,),
                "layout_direction": (directions,),
               },
                "optional": {
                "image_2": ("IMAGE",), 
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "image_5": ("IMAGE",),
                "footer": ("IMAGE",),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def layout(self, title_bar, image_1, layout_direction,
               border_thickness, border_color, background_color,
               image_2 = None, image_3 = None, image_4 = None,
               image_5 = None, footer = None):

        images = []
        images.append(tensor2pil(image_1))
        if image_2 is not None:
            images.append(tensor2pil(image_2))
        if image_3 is not None:
            images.append(tensor2pil(image_3))
        if image_4 is not None:
            images.append(tensor2pil(image_4))
        if image_5 is not None:
            images.append(tensor2pil(image_5))
        
        # Determine the final image size based on layout direction
        if layout_direction == 'horizontal':
            total_width = sum(image.size[0] for image in images)
            max_height = max(image.size[1] for image in images)
            combined_image = Image.new('RGB', (total_width, max_height), background_color)
            x_offset = 0
            for image in images:
                combined_image.paste(image, (x_offset, 0))
                x_offset += image.size[0]
        else:
            max_width = max(image.size[0] for image in images)
            total_height = sum(image.size[1] for image in images)
            combined_image = Image.new('RGB', (max_width, total_height), background_color)
            y_offset = 0
            for image in images:
                combined_image.paste(image, (0, y_offset))
                y_offset += image.size[1]

        # Add a border to the combined image
        if border_thickness > 0:
            combined_image = ImageOps.expand(combined_image, border_thickness, border_color)
            
        show_help = "example help text"

        return (pil2tensor(combined_image), show_help, )    
 
#---------------------------------------------------------------------------------------------------------------------#    
class CR_ImagePanel:

    @classmethod
    def INPUT_TYPES(s):

        directions = ["horizontal", "vertical"]               
        
        return {"required": {
                "image_1": ("IMAGE",),
                "border_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "border_color": (COLORS,),
                "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "outline_color": (COLORS,),
                "layout_direction": (directions,),
               },
                "optional": {
                "image_2": ("IMAGE",), 
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, image_1,
                   border_thickness, border_color,
                   outline_thickness, outline_color, 
                   layout_direction, image_2=None, image_3=None, image_4=None,
                   border_color_hex='#000000'):

        if border_color == "custom":
            border_color = hex_to_rgb(border_color_hex)
        else:
            border_color = color_mapping.get(border_color, (0, 0, 0))  # Default to black if the color is not found

        # Convert PIL images to NumPy arrays
        images = []
        image_1 = image_1[0, :, :, :]
        images.append(tensor2pil(image_1))
        if image_2 is not None:
            image_2 = image_2[0, :, :, :]
            images.append(tensor2pil(image_2))
        if image_3 is not None:
            image_3 = image_3[0, :, :, :]
            images.append(tensor2pil(image_3))
        if image_4 is not None:
            image_4 = image_4[0, :, :, :]
            images.append(tensor2pil(image_4))
            
        # Apply borders and outlines to each image
        for i, image in enumerate(images):

            # Apply the outline
            if outline_thickness > 0:
                image = ImageOps.expand(image, outline_thickness, fill=outline_color)
            
            # Apply the border
            if border_thickness > 0:
                image = ImageOps.expand(image, border_thickness, fill=border_color)

            images[i] = image

        # Combine images horizontally or vertically
        if layout_direction == 'horizontal':
            combined_width = sum(image.width for image in images)
            combined_height = max(image.height for image in images)
        else:
            combined_width = max(image.width for image in images)
            combined_height = sum(image.height for image in images)

        combined_image = Image.new('RGB', (combined_width, combined_height))

        x_offset = 0
        y_offset = 0  # Initialize y_offset for vertical layout
        for image in images:
            combined_image.paste(image, (x_offset, y_offset))
            if layout_direction == 'horizontal':
                x_offset += image.width
            else:
                y_offset += image.height

        show_help = "example help text"

        return (pil2tensor(combined_image), show_help, )   

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Simple Meme Template":CR_SimpleMemeTemplate,
    #"CR Multi-Panel Meme Template":CR_MultiPanelMemeTemplate,
    #"CR Popular Meme Templates":CR_PopularMemeTemplates,
    #"CR Simple Annotations":CR_SimpleAnnotations,
    #"CR Apply Annotations":CR_ApplyAnnotations,
    #"CR Add Annotation":CR_AddAnnotation,
    "CR Page Layout":CR_PageLayout,
    "CR Image Panel":CR_ImagePanel, 
}
'''

