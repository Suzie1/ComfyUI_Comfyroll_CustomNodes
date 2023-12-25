#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import os 
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter
from ..categories import icons
from ..config import color_mapping, COLORS
from .graphics_functions import (hex_to_rgb,
                                 get_color_values,
                                 text_panel,
                                 combine_images,
                                 apply_outline_and_border,
                                 get_font_size,
                                 draw_text_on_image) 

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
class CR_PageLayout:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

        layout_options = ["header", "footer", "header and footer", "no header or footer"]               
        
        return {"required": {
                "layout_options": (layout_options,),
                "image_panel": ("IMAGE",),
                "header_height": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "header_text": ("STRING", {"multiline": True, "default": "text"}),
                "header_align": (JUSTIFY_OPTIONS, ),
                "footer_height": ("INT", {"default": 0, "min": 0, "max": 1024}), 
                "footer_text": ("STRING", {"multiline": True, "default": "text"}),
                "footer_align": (JUSTIFY_OPTIONS, ),
                "font_name": (file_list,),
                "font_color": (COLORS,),
                "header_font_size": ("INT", {"default": 150, "min": 0, "max": 1024}),
                "footer_font_size": ("INT", {"default": 50, "min": 0, "max": 1024}),
                "border_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "border_color": (COLORS,),                
                "background_color": (COLORS,),
               },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def layout(self, layout_options, image_panel,
               border_thickness, border_color, background_color,
               header_height, header_text, header_align,
               footer_height, footer_text, footer_align,
               font_name, font_color,
               header_font_size, footer_font_size,
               font_color_hex='#000000', border_color_hex='#000000', bg_color_hex='#000000'):

        # Get RGB values for the text and background colors    
        font_color = get_color_values(font_color, font_color_hex, color_mapping)
        border_color = get_color_values(border_color, border_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)
                    
        main_panel = tensor2pil(image_panel)
        
        # Get image width and height        
        image_width = main_panel.width
        image_height = main_panel.height 

        # Set defaults
        margins = 50
        line_spacing = 0
        position_x = 0
        position_y = 0
        align = "center"
        rotation_angle = 0
        rotation_options = "image center"
        font_outline_thickness = 0
        font_outline_color = "black"
        
        images = []
        
        ### Create text panels and add to images array       
        if layout_options == "header" or layout_options == "header and footer":
            header_panel = text_panel(image_width, header_height, header_text,
                                      font_name, header_font_size, font_color,
                                      font_outline_thickness, font_outline_color,
                                      bg_color,
                                      margins, line_spacing,
                                      position_x, position_y,
                                      align, header_align,
                                      rotation_angle, rotation_options)
            images.append(header_panel)
        
        images.append(main_panel)
               
        if layout_options == "footer" or layout_options == "header and footer":        
            footer_panel = text_panel(image_width, footer_height, footer_text,
                                      font_name, footer_font_size, font_color,
                                      font_outline_thickness, font_outline_color,
                                      bg_color,
                                      margins, line_spacing,
                                      position_x, position_y,
                                      align, footer_align,
                                      rotation_angle, rotation_options)
            images.append(footer_panel)                                                           
       
        combined_image = combine_images(images, 'vertical')

        # Add a border to the combined image
        if border_thickness > 0:
            combined_image = ImageOps.expand(combined_image, border_thickness, border_color)
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-page-layout"

        return (pil2tensor(combined_image), show_help, )    

#---------------------------------------------------------------------------------------------------------------------#    
class CR_SimpleTitles:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

        layout_options = ["header", "footer", "header and footer", "no header or footer"]               
        
        return {"required": {
                "image": ("IMAGE",),
                "header_text": ("STRING", {"multiline": True, "default": "text"}),
                "header_height": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "header_font_size": ("INT", {"default": 150, "min": 0, "max": 1024}),                
                "header_align": (JUSTIFY_OPTIONS, ),
                "footer_text": ("STRING", {"multiline": True, "default": "text"}),
                "footer_height": ("INT", {"default": 0, "min": 0, "max": 1024}),  
                "footer_font_size": ("INT", {"default": 50, "min": 0, "max": 1024}),                
                "footer_align": (JUSTIFY_OPTIONS, ),
                "font_name": (file_list,),
                "font_color": (COLORS,),
                "background_color": (COLORS,),
               },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def layout(self, image,
               header_height, header_text, header_align, header_font_size, 
               footer_height, footer_text, footer_align, footer_font_size,
               font_name, font_color, background_color,
               font_color_hex='#000000', bg_color_hex='#000000',):

        # Get RGB values for the text and background colors    
        font_color = get_color_values(font_color, font_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)
        
        main_panel = tensor2pil(image)
        
        # Get image width and height        
        image_width = main_panel.width
        image_height = main_panel.height 

        # Set defaults
        margins = 50
        line_spacing = 0
        position_x = 0
        position_y = 0
        align = "center"
        rotation_angle = 0
        rotation_options = "image center"
        font_outline_thickness = 0
        font_outline_color = "black"
        
        images = []
        
        ### Create text panels and add to images array       
        if header_height >0:
            header_panel = text_panel(image_width, header_height, header_text,
                                      font_name, header_font_size, font_color,
                                      font_outline_thickness, font_outline_color,
                                      bg_color,
                                      margins, line_spacing,
                                      position_x, position_y,
                                      align, header_align,
                                      rotation_angle, rotation_options)
            images.append(header_panel)
        
        images.append(main_panel)
               
        if footer_height >0:       
            footer_panel = text_panel(image_width, footer_height, footer_text,
                                      font_name, footer_font_size, font_color,
                                      font_outline_thickness, font_outline_color,
                                      bg_color,
                                      margins, line_spacing,
                                      position_x, position_y,
                                      align, footer_align,
                                      rotation_angle, rotation_options)
            images.append(footer_panel)                                                           
       
        combined_image = combine_images(images, 'vertical')
          
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-simple_titles"

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
                "outline_color": (COLORS[1:],),
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

        border_color = get_color_values(border_color, border_color_hex, color_mapping)

        # Convert PIL images to NumPy arrays
        images = []
        #image_1 = image_1[0, :, :, :]
        images.append(tensor2pil(image_1))
        if image_2 is not None:
            #image_2 = image_2[0, :, :, :]
            images.append(tensor2pil(image_2))
        if image_3 is not None:
            #image_3 = image_3[0, :, :, :]
            images.append(tensor2pil(image_3))
        if image_4 is not None:
            #image_4 = image_4[0, :, :, :]
            images.append(tensor2pil(image_4))
            
        # Apply borders and outlines to each image        
        images = apply_outline_and_border(images, outline_thickness, outline_color, border_thickness, border_color)

        combined_image = combine_images(images, layout_direction)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-image-panel"

        return (pil2tensor(combined_image), show_help, )   

#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageGridPanel:

    @classmethod
    def INPUT_TYPES(s):

        directions = ["horizontal", "vertical"]               
        
        return {"required": {
                    "images": ("IMAGE",),
                    "border_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                    "border_color": (COLORS,),
                    "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                    "outline_color": (COLORS[1:],),
                    "max_columns": ("INT", {"default": 5, "min": 0, "max": 256}), 
                },
                "optional": {
                    "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, images,
                   border_thickness, border_color,
                   outline_thickness, outline_color, 
                   max_columns, border_color_hex='#000000'):

        border_color = get_color_values(border_color, border_color_hex, color_mapping)

        # Convert PIL images to NumPy arrays
        images = [tensor2pil(image) for image in images]
            
        # Apply borders and outlines to each image
        images = apply_outline_and_border(images, outline_thickness, outline_color, border_thickness, border_color)

        # Calculate dimensions for the grid
        num_images = len(images)
        num_rows = (num_images - 1) // max_columns + 1
        combined_width = max(image.width for image in images) * min(max_columns, num_images)
        combined_height = max(image.height for image in images) * num_rows

        combined_image = Image.new('RGB', (combined_width, combined_height))

        x_offset, y_offset = 0, 0  # Initialize offsets
        for image in images:
            combined_image.paste(image, (x_offset, y_offset))
            x_offset += image.width
            if x_offset >= max_columns * image.width:
                x_offset = 0
                y_offset += image.height

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-image-grid-panel"

        return (pil2tensor(combined_image), show_help, )   

#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageBorder:

    @classmethod
    def INPUT_TYPES(s):
                    
        return {"required": {
                    "image": ("IMAGE",),
                    "top_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "bottom_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "left_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "right_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "border_color": (COLORS,),
                    "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                    "outline_color": (COLORS[1:],),
                },
                "optional": {
                    "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, image,
                   top_thickness, bottom_thickness,
                   left_thickness, right_thickness, border_color,
                   outline_thickness, outline_color, 
                   border_color_hex='#000000'):

        images = []

        border_color = get_color_values(border_color, border_color_hex, color_mapping)

        for img in image:
            img = tensor2pil(img)
            
            # Apply the outline
            if outline_thickness > 0:
                img = ImageOps.expand(img, outline_thickness, fill=outline_color)
            
            # Apply the borders
            if left_thickness > 0 or right_thickness > 0 or top_thickness > 0 or bottom_thickness > 0:
                img = ImageOps.expand(img, (left_thickness, top_thickness, right_thickness, bottom_thickness), fill=border_color)
                
            images.append(pil2tensor(img))
        
        images = torch.cat(images, dim=0)                

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-image-border"

        return (images, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ColorPanel:

    @classmethod
    def INPUT_TYPES(s):
                    
        return {"required": {
                    "panel_width": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "panel_height": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "fill_color": (COLORS,),
                },
                "optional": {
                    "fill_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, panel_width, panel_height,
                   fill_color, fill_color_hex='#000000'):

        fill_color = get_color_values(fill_color, fill_color_hex, color_mapping)

        size = (panel_width, panel_height)
        panel = Image.new('RGB', size, fill_color)
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-color-panel"

        return (pil2tensor(panel), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleTextPanel:

    @classmethod
    def INPUT_TYPES(s):
    
        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

        return {"required": {
                "panel_width": ("INT", {"default": 512, "min": 8, "max": 4096}),
                "panel_height": ("INT", {"default": 512, "min": 8, "max": 4096}),
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_color": (COLORS,),
                "font_size": ("INT", {"default": 100, "min": 0, "max": 1024}),
                "font_outline_thickness": ("INT", {"default": 0, "min": 0, "max": 50}),
                "font_outline_color": (COLORS,),                
                "background_color": (COLORS,),                
                "align": (ALIGN_OPTIONS, ),
                "justify": (JUSTIFY_OPTIONS, ),
               },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
               }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def layout(self, panel_width, panel_height,
               text, align, justify,
               font_name, font_color, font_size,
               font_outline_thickness, font_outline_color,
               background_color, 
               font_color_hex='#000000', font_outline_color_hex='#000000', bg_color_hex='#000000'):

        # Get RGB values for the text and background colors    
        font_color = get_color_values(font_color, font_color_hex, color_mapping)
        outline_color = get_color_values(font_outline_color, font_outline_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)
        
        # Set defaults
        margins = 50
        line_spacing = 0
        position_x = 0
        position_y = 0
        rotation_angle = 0
        rotation_options = "image center"
        
        ### Create text panels
        
        panel = text_panel(panel_width, panel_height, text,
                           font_name, font_size, font_color, 
                           font_outline_thickness, outline_color,
                           bg_color,
                           margins, line_spacing,
                           position_x, position_y,
                           align, justify,
                           rotation_angle, rotation_options)
                                                       
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-simple-text-panel"

        return (pil2tensor(panel), show_help, )  

#---------------------------------------------------------------------------------------------------------------------#
class CR_OverlayTransparentImage:
    
    @classmethod
    def INPUT_TYPES(s):
                  
        return {"required": {
                "back_image": ("IMAGE",),
                "overlay_image": ("IMAGE",),
                "transparency": ("FLOAT", {"default": 0, "min": 0, "max": 1, "step": 0.1}),
                "offset_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "offset_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                "overlay_scale_factor": ("FLOAT", {"default": 1.0, "min": -0.1, "max": 100.0, "step": 0.1}),
                }        
        }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "overlay_image"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")

    def overlay_image(self, back_image, overlay_image, 
                      transparency, offset_x, offset_y, rotation_angle, overlay_scale_factor=1.0):

        """
        Overlay an image onto another image with transparency, rotation, and scaling.

        Args:
            back_image (torch.Tensor): Background image tensor.
            overlay_image (torch.Tensor): Overlay image tensor.
            transparency (float): Transparency level for the overlay image (0.0 to 1.0).
            offset_x (int): X-coordinate relative to the center of the back image.
            offset_y (int): Y-coordinate relative to the center of the back image.
            rotation_angle (float): Rotation angle in degrees.
            scale_factor (float): Scaling factor for the overlay image.

        Returns:
            torch.Tensor: Resulting image tensor.
        """
        
        # Convert tensor images
        #back_image = back_image[0, :, :, :]
        #overlay_image = overlay_image[0, :, :, :]

        # Create PIL images for the text and background layers and text mask
        back_image = tensor2pil(back_image)
        overlay_image = tensor2pil(overlay_image)

        # Apply transparency to overlay image
        overlay_image.putalpha(int(255 * (1 - transparency)))

        # Rotate overlay image
        overlay_image = overlay_image.rotate(rotation_angle, expand=True)

        # Scale overlay image
        overlay_width, overlay_height = overlay_image.size
        new_size = (int(overlay_width * overlay_scale_factor), int(overlay_height * overlay_scale_factor))
        overlay_image = overlay_image.resize(new_size, Image.ANTIALIAS)

        # Calculate centered position relative to the center of the background image
        center_x = back_image.width // 2
        center_y = back_image.height // 2
        position_x = center_x - overlay_image.width // 2 + offset_x
        position_y = center_y - overlay_image.height // 2 + offset_y

        # Paste the rotated overlay image onto the new back image at the specified position
        back_image.paste(overlay_image, (position_x, position_y), overlay_image)

        # Convert the PIL image back to a torch tensor
        return pil2tensor(back_image),

#---------------------------------------------------------------------------------------------------------------------#
class CR_FeatheredBorder:

    @classmethod
    def INPUT_TYPES(s):
                    
        return {"required": {
                    "image": ("IMAGE",),
                    "top_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "bottom_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "left_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "right_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "border_color": (COLORS,),
                    "feather_amount": ("INT", {"default": 0, "min": 0, "max": 1024}),
                },
                "optional": {
                    "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_border"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_border(self, image,
                   top_thickness, bottom_thickness,
                   left_thickness, right_thickness, border_color,
                   feather_amount,
                   border_color_hex='#000000'):

        images = []

        border_color = get_color_values(border_color, border_color_hex, color_mapping)

        for img in image:
            im = tensor2pil(img)
            
            RADIUS = feather_amount
                         
            # Paste image on white background
            diam = 2*RADIUS
            back = Image.new('RGB', (im.size[0]+diam, im.size[1]+diam), border_color)
            back.paste(im, (RADIUS, RADIUS))

            # Create paste mask
            mask = Image.new('L', back.size, 0)
            draw = ImageDraw.Draw(mask)
            x0, y0 = 0, 0
            x1, y1 = back.size
            for d in range(diam+RADIUS):
                x1, y1 = x1-1, y1-1
                alpha = 255 if d<RADIUS else int(255*(diam+RADIUS-d)/diam)
                draw.rectangle([x0, y0, x1, y1], outline=alpha)
                x0, y0 = x0+1, y0+1

            # Blur image and paste blurred edge according to mask
            blur = back.filter(ImageFilter.GaussianBlur(RADIUS/2))
            back.paste(blur, mask=mask)

            # Apply the borders
            if left_thickness > 0 or right_thickness > 0 or top_thickness > 0 or bottom_thickness > 0:
                img = ImageOps.expand(back, (left_thickness, top_thickness, right_thickness, bottom_thickness), fill=border_color)
            else:
                img = back

            images.append(pil2tensor(img))
        
        images = torch.cat(images, dim=0)                

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-feathered-border"

        return (images, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Page Layout": CR_PageLayout,
    "CR Image Grid Panel": CR_ImageGridPanel,
    "CR Image XY Panel": CR_ImageXYPanel,
    "CR Image Border": CR_ImageBorder,
    "CR Feathered Border": CR_FeatheredBorder,
    "CR Color Panel": CR_ColorPanel,
    "CR Simple Text Panel": CR_SimpleTextPanel,
    "CR Overlay Transparent Image": CR_OverlayTransparentImage,
    "CR Simple Titles": CR_SimpleTitles,
}
'''

