#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from ..config import color_mapping

font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

def align_text(align, img_height, text_height, text_pos_y, margins):
    if align == "center":
        text_plot_y = img_height / 2 - text_height / 2 + text_pos_y
    elif align == "top":
        text_plot_y = text_pos_y + margins                       
    elif align == "bottom":
        text_plot_y = img_height - text_height + text_pos_y - margins 
    return text_plot_y        

def justify_text(justify, img_width, line_width, margins):
    if justify == "left":
        text_plot_x = 0 + margins
    elif justify == "right":
        text_plot_x = img_width - line_width - margins
    elif justify == "center":
        text_plot_x = img_width/2 - line_width/2
    return text_plot_x   

def draw_masked_text(text_mask, text,
                     font_name, font_size,
                     margins, line_spacing,
                     position_x, position_y, 
                     align, justify,
                     rotation_angle, rotation_options):
    
    # Create the drawing context        
    draw = ImageDraw.Draw(text_mask)

    # Define font settings
    font_folder = "fonts"
    font_file = os.path.join(font_folder, font_name)
    resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

     # Split the input text into lines
    text_lines = text.split('\n')

    # Calculate the size of the text plus padding for the tallest line
    max_text_width = 0
    max_text_height = 0

    for line in text_lines:
        line_width, line_height = draw.textsize(line, font=font)
        line_width = line_width 
        line_height = line_height + line_spacing ###
        max_text_width = max(max_text_width, line_width)
        max_text_height = max(max_text_height, line_height)
    
    # Get the image width and height
    image_width, image_height = text_mask.size
    image_center_x = image_width / 2
    image_center_y = image_height / 2

    text_pos_y = position_y
    sum_text_plot_y = 0
    text_height = max_text_height * len(text_lines)

    for line in text_lines:
        # Calculate the width of the current line
        line_width, _ = draw.textsize(line, font=font)
        line_width = line_width
                            
        # Get the text x and y positions for each line                                     
        text_plot_x = position_x + justify_text(justify, image_width, line_width, margins)
        text_plot_y = align_text(align, image_height, text_height, text_pos_y, margins)
        
        # Add the current line to the text mask
        draw.text((text_plot_x, text_plot_y), line, fill=255, font=font)

        text_pos_y += max_text_height  # Move down for the next line
        sum_text_plot_y += text_plot_y     # Sum the y positions

    text_center_x = text_plot_x + max_text_width / 2
    text_center_y = sum_text_plot_y / len(text_lines)

    if rotation_options == "text center":
        rotated_text_mask = text_mask.rotate(rotation_angle, center=(text_center_x, text_center_y))
    elif rotation_options == "image center":    
        rotated_text_mask = text_mask.rotate(rotation_angle, center=(image_center_x, image_center_y))
        
    return rotated_text_mask        

def draw_masked_text_v2(text_mask, text,
                     font_name, font_size,
                     margins, line_spacing,
                     position_x, position_y, 
                     align, justify,
                     perspective_factor, perspective_direction):
    
    # Create a drawing context        
    draw = ImageDraw.Draw(text_mask)

    # Define font settings
    font_folder = "fonts"
    font_file = os.path.join(font_folder, font_name)    
    resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

     # Split the input text into lines
    text_lines = text.split('\n')

    # Calculate the size of the text plus padding for the tallest line
    max_text_width = 0
    max_text_height = 0

    for line in text_lines:
        line_width, line_height = draw.textsize(line, font=font)
        line_width = line_width 
        line_height = line_height + line_spacing ###
        max_text_width = max(max_text_width, line_width)
        max_text_height = max(max_text_height, line_height)

    # Get the image width and height
    image_width, image_height = text_mask.size
    image_center_x = image_width / 2
    image_center_y = image_height / 2

    text_pos_y = position_y
    sum_text_plot_y = 0
    text_height = max_text_height * len(text_lines)

    for line in text_lines:
        # Calculate the width of the current line
        line_width, _ = draw.textsize(line, font=font)
        line_width = line_width
                            
        # Get the text x and y positions for each line                                     
        text_plot_x = position_x + justify_text(justify, image_width, line_width, margins)
        text_plot_y = align_text(align, image_height, text_height, text_pos_y, margins)
        
        # Add the current line to the text mask
        draw.text((text_plot_x, text_plot_y), line, fill=255, font=font)

        text_pos_y += max_text_height  # Move down for the next line
        sum_text_plot_y += text_plot_y     # Sum the y positions

    text_center_x = text_plot_x + max_text_width / 2
    text_center_y = sum_text_plot_y / len(text_lines)
        
    return text_mask
   
def draw_text_on_image(draw, y_position, bar_width, bar_height, text, font, text_color, font_outline):

        text_width, text_height = draw.textsize(text, font=font)
       
        if font_outline == "thin":
            outline_thickness = text_height // 40
        elif font_outline == "thick":
            outline_thickness = text_height // 20
            
        outline_color = (0, 0, 0)
        
        text_lines = text.split('\n')
        
        if len(text_lines) == 1:
            x = (bar_width - text_width) // 2
            y = y_position + (bar_height - text_height) // 2 - (bar_height * 0.06)
            if font_outline == "none":
                draw.text((x, y), text, fill=text_color, font=font)
            else:    
                draw.text((x, y), text, fill=text_color, font=font, stroke_width=outline_thickness, stroke_fill='black')
        elif len(text_lines) > 1:
            text_width, text_height = draw.textsize(text_lines[0], font=font)
            x = (bar_width - text_width) // 2
            y = y_position + (bar_height - text_height * 2) // 2 - (bar_height * 0.06)
            if font_outline == "none":
                draw.text((x, y), text_lines[0], fill=text_color, font=font)
            else:    
                draw.text((x, y), text_lines[0], fill=text_color, font=font, stroke_width=outline_thickness, stroke_fill='black')   
            text_width, text_height = draw.textsize(text_lines[1], font=font)
            x = (bar_width - text_width) // 2
            y = y_position + (bar_height - text_height * 2) // 2 + text_height  - (bar_height * 0.06)         
            if font_outline == "none":
                draw.text((x, y), text_lines[1], fill=text_color, font=font)
            else:    
                draw.text((x, y), text_lines[1], fill=text_color, font=font, stroke_width=outline_thickness, stroke_fill='black')

def get_font_size(draw, text, max_width, max_height, font_path, max_font_size):

    # Adjust the max-width to allow for start and end padding
    max_width = max_width * 0.9
    
    # Start with the maximum font size
    font_size = max_font_size
    font = ImageFont.truetype(str(font_path), size=font_size)

     # Get the first two lines
    text_lines = text.split('\n')[:2]
    
    if len(text_lines) == 2:
        font_size = min(max_height//2, max_font_size)        
        font = ImageFont.truetype(str(font_path), size=font_size)
        
    # Calculate max text width and height with the current font
    max_text_width = 0
    longest_line = text_lines[0]
    for line in text_lines:
        line_width, line_height = draw.textsize(line, font=font)
        if line_width > max_text_width:
            longest_line = line
        max_text_width = max(max_text_width, line_width)             
    
    # Calculate text height with the current font
    text_width, text_height = font.getsize(text)
    
    # Decrease the font size until it fits within the bounds
    while max_text_width > max_width or text_height > 0.88 * max_height / len(text_lines):
        font_size -= 1
        font = ImageFont.truetype(str(font_path), size=font_size)
        max_text_width, text_height = font.getsize(longest_line)
    
    return font

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Remove the '#' character, if present
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)
    
def text_panel(image_width, image_height, text,
              font_name, font_size, font_color, background_color,
              margins, line_spacing,
              position_x, position_y,
              align, justify,
              rotation_angle, rotation_options,
              font_color_hex='#000000', bg_color_hex='#000000'):

    """
    Create an image with text overlaid on a background.
    
    Returns:
    PIL.Image.Image: Image with text overlaid on the background.
    """

    # Get RGB values for the text and background colors
    text_color = get_color_values(font_color, font_color_hex, color_mapping)
    bg_color = get_color_values(background_color, bg_color_hex, color_mapping)
    
    # Create PIL images for the text and background layers and text mask
    size = (image_width, image_height)
    panel = Image.new('RGB', size, bg_color)

    # Draw the text on the text mask
    image_out = draw_text(panel, text,
                          font_name, font_size, 
                          font_color, bg_color,
                          margins, line_spacing,
                          position_x, position_y,
                          align, justify,
                          rotation_angle, rotation_options)
  
    return image_out     

def draw_text(panel, text,
              font_name, font_size,
              font_color, bg_color,
              margins, line_spacing,
              position_x, position_y, 
              align, justify,
              rotation_angle, rotation_options):
    
    # Create the drawing context        
    draw = ImageDraw.Draw(panel)

    # Define font settings
    font_folder = "fonts"
    font_file = os.path.join(font_folder, font_name)
    resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

     # Split the input text into lines
    text_lines = text.split('\n')

    # Calculate the size of the text plus padding for the tallest line
    max_text_width = 0
    max_text_height = 0

    for line in text_lines:
        line_width, line_height = draw.textsize(line, font=font)
        line_width = line_width 
        line_height = line_height + line_spacing ###
        max_text_width = max(max_text_width, line_width)
        max_text_height = max(max_text_height, line_height)
    
    # Get the image center
    image_center_x = panel.width / 2
    image_center_y = panel.height / 2

    text_pos_y = position_y
    sum_text_plot_y = 0
    text_height = max_text_height * len(text_lines)

    for line in text_lines:
        # Calculate the width of the current line
        line_width, _ = draw.textsize(line, font=font)
        line_width = line_width
                            
        # Get the text x and y positions for each line                                     
        text_plot_x = position_x + justify_text(justify, panel.width, line_width, margins)
        text_plot_y = align_text(align, panel.height, text_height, text_pos_y, margins)
        
        # Add the current line to the text mask
        draw.text((text_plot_x, text_plot_y), line, fill=font_color, font=font)

        text_pos_y += max_text_height  # Move down for the next line
        sum_text_plot_y += text_plot_y     # Sum the y positions

    text_center_x = text_plot_x + max_text_width / 2
    text_center_y = sum_text_plot_y / len(text_lines)

    if rotation_options == "text center":
        rotated_panel = panel.rotate(rotation_angle, center=(text_center_x, text_center_y), resample=Image.BILINEAR)
    elif rotation_options == "image center":    
        rotated_panel = panel.rotate(rotation_angle, center=(image_center_x, image_center_y), resample=Image.BILINEAR)
        
    return rotated_panel

def combine_images(images, layout_direction='horizontal'):
    """
    Combine a list of PIL Image objects either horizontally or vertically.

    Args:
    images (list of PIL.Image.Image): List of PIL Image objects to combine.
    layout_direction (str): 'horizontal' for horizontal layout, 'vertical' for vertical layout.

    Returns:
    PIL.Image.Image: Combined image.
    """

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

    return combined_image

def apply_outline_and_border(images, outline_thickness, outline_color, border_thickness, border_color):
    for i, image in enumerate(images):
        # Apply the outline
        if outline_thickness > 0:
            image = ImageOps.expand(image, outline_thickness, fill=outline_color)
        
        # Apply the border
        if border_thickness > 0:
            image = ImageOps.expand(image, border_thickness, fill=border_color)

        images[i] = image
    
    return images
    
def get_color_values(color, color_hex, color_mapping):
    """
    Get RGB values for the text and background colors.

    Returns:
        tuple: A tuple containing (font_color_rgb, background_color_rgb).
    """
    if color == "custom":
        color_rgb = hex_to_rgb(color_hex)
    else:
        color_rgb = color_mapping.get(color, (0, 0, 0))  # Default to black if the color is not found

    return color_rgb 
    
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Remove the '#' character, if present
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)
        