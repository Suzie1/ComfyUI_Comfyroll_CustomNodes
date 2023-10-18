#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import os
import sys
import io
from PIL import Image, ImageDraw

import folder_paths

try:
    import matplotlib.pyplot as plt
except ImportError:
    import pip
    pip.main(['install', 'matplotlib'])
    import matplotlib.pyplot as plt
    
from matplotlib.patches import RegularPolygon

# Define a dictionary to map color names to RGB values
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

def rgb_to_hex(rgb):
    r, g, b = rgb
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

#---------------------------------------------------------------------------------------------------------------------#
class CR_HalftoneGrid:
    @classmethod
    def INPUT_TYPES(s):
    
        dot_styles = ["Accent","afmhot","autumn","binary","Blues","bone","BrBG","brg",
            "BuGn","BuPu","bwr","cividis","CMRmap","cool","coolwarm","copper","cubehelix","Dark2","flag",
            "gist_earth","gist_gray","gist_heat","gist_rainbow","gist_stern","gist_yarg","GnBu","gnuplot","gnuplot2","gray","Greens",
            "Greys","hot","hsv","inferno","jet","magma","nipy_spectral","ocean","Oranges","OrRd",
            "Paired","Pastel1","Pastel2","pink","PiYG","plasma","PRGn","prism","PuBu","PuBuGn",
            "PuOr","PuRd","Purples","rainbow","RdBu","RdGy","RdPu","RdYlBu","RdYlGn","Reds","seismic",
            "Set1","Set2","Set3","Spectral","spring","summer","tab10","tab20","tab20b","tab20c","terrain",
            "turbo","twilight","twilight_shifted","viridis","winter","Wistia","YlGn","YlGnBu","YlOrBr","YlOrRd"]
            
        return {"required": {
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "dot_style": (dot_styles,),
                    "reverse_dot_style": (["No", "Yes"],),
                    "dot_frequency": ("INT", {"default": 50, "min": 1, "max":200, "step": 1}),
                    "background_color": (["custom", "white", "black", "red", "green", "blue", "cyan", "magenta", "yellow", "purple", "orange", "lime", "navy", "teal", "maroon", "lavender", "olive"],),
                    "background_R": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                    "background_G": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                    "background_B": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                    "x_pos": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": .01}),
                    "y_pos": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": .01}),                    
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "halftone"
    CATEGORY = "Comfyroll/Image"

    def halftone(self, width, height, dot_style, reverse_dot_style, dot_frequency, background_color, background_R, background_G, background_B, x_pos, y_pos):
    
        if background_color == "custom":
            bgc = (background_R/255, background_G/255, background_B/255)
        else:
            bgc = background_color
            
        reverse = ""
        
        if reverse_dot_style == "Yes":
            reverse = "_r"
        
        fig, ax = plt.subplots(figsize=(width/100,height/100))
           
        dotsx = np.linspace(0, 1, dot_frequency)
        dotsy = np.linspace(0, 1, dot_frequency)
    
        X, Y = np.meshgrid(dotsx, dotsy)
    
        dist = np.sqrt((X - x_pos)**2 + (Y - y_pos)**2)
    
        fig.patch.set_facecolor(bgc)
        ax.scatter(X, Y, c=dist, cmap=dot_style+reverse)
        
        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(tight=True)
      
        
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)
        
        return(pil2tensor(img),)

#---------------------------------------------------------------------------------------------------------------------#
class CR_ColorBars:
    @classmethod
    def INPUT_TYPES(s):
    
        colors = ["white", "black", "red", "green", "blue", "yellow",
            "cyan", "magenta", "orange", "purple", "pink", "brown", "gray",
            "lightgray", "darkgray", "olive", "lime", "teal", "navy", "maroon",
            "fuchsia", "aqua", "silver", "gold", "turquoise", "lavender",
            "violet", "coral", "indigo"]
        modes = ["2-color"]
        
        return {"required": {
                    "mode": (modes,),
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "color1": (colors,),
                    "color2": (colors,),
                    "orientation": (["vertical", "horizontal", "diagonal"],),
                    "bar_frequency": ("INT", {"default": 5, "min": 1, "max":200, "step": 1}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "CR 3D"

    def draw(self, mode, width, height, color1, color2, orientation, bar_frequency):

        color1_rgb = color_mapping.get(color1, (255, 255, 255))  # Default to white if the color is not found
        color2_rgb = color_mapping.get(color2, (0, 0, 0))  # Default to black if the color is not found

        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        
        bar_width = width / bar_frequency
        bar_height = height / bar_frequency

        if orientation == "vertical":
            for j in range(height):
                for i in range(width):
                    if (i // bar_width) % 2 == 0:  # Check for even index
                        canvas[j, i] = color1_rgb
                    else:
                        canvas[j, i] = color2_rgb
        elif orientation == "horizontal":
            for j in range(height):
                for i in range(width):
                    if (j // bar_height) % 2 == 0:  # Check for even index
                        canvas[j, i] = color1_rgb
                    else:
                        canvas[j, i] = color2_rgb                
        elif orientation == "diagonal":
            # Calculate the bar width based on a 45 degree angle 
            bar_width = int(bar_height / np.tan(np.pi / 4)) * 2
            for j in range(height): 
                for i in range(width):
                    # Calculate which diagonal bar the pixel belongs to
                    bar_number = (i + j) // bar_width
                    if bar_number % 2 == 0:  # Check for even bar number
                        canvas[j, i] = color1_rgb
                    else:
                        canvas[j, i] = color2_rgb
                
        fig, ax = plt.subplots(figsize=(width/100, height/100))

        ax.imshow(canvas)

        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(tight=True)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)

        return pil2tensor(img),

#---------------------------------------------------------------------------------------------------------------------#
class CR_StyleBars:
    @classmethod
    def INPUT_TYPES(s):
    
        bar_styles = ["Accent","afmhot","autumn","binary","Blues","bone","BrBG","brg",
            "BuGn","BuPu","bwr","cividis","CMRmap","cool","coolwarm","copper","cubehelix","Dark2","flag",
            "gist_earth","gist_gray","gist_heat","gist_rainbow","gist_stern","gist_yarg","GnBu","gnuplot","gnuplot2","gray",
            "Greens","Greys","hot","hsv","inferno","jet","magma","nipy_spectral","ocean","Oranges","OrRd",
            "Paired","Pastel1","Pastel2","pink","PiYG","plasma","PRGn","prism","PuBu","PuBuGn",
            "PuOr","PuRd","Purples","rainbow","RdBu","RdGy","RdPu","RdYlBu","RdYlGn","Reds","seismic",
            "Set1","Set2","Set3","Spectral","spring","summer","tab10","tab20","tab20b","tab20c","terrain",
            "turbo","twilight","twilight_shifted","viridis","winter","Wistia","YlGn","YlGnBu","YlOrBr","YlOrRd"]
        modes = ["color bars", "sin wave", "gradient bars"]
        
        return {"required": {
                    "mode": (modes,),
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "bar_style": (bar_styles,),
                    "orientation": (["vertical", "horizontal", ],),
                    "bar_frequency": ("INT", {"default": 5, "min": 1, "max":200, "step": 1}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "CR 3D"

    def draw(self, mode, width, height, bar_style, orientation, bar_frequency):

        # Create a horizontal or vertical bar depending on the orientation
        if orientation == "vertical":
            x = np.linspace(0, 1, width)
            y = np.zeros((height, width))
        elif orientation == "horizontal":
            x = np.zeros((height, width))
            y = np.linspace(0, 1, height)

        # Create a grid of colors for the bar
        X, Y = np.meshgrid(x, y)

        if mode == "color bars":
            bar_width = 1 / bar_frequency
            if orientation == "vertical":
                colors = (X // bar_width) % 2
            elif orientation == "horizontal":
                colors = (Y // bar_width) % 2 
        elif mode == "sin wave":    
            if orientation == "vertical":
                colors = np.sin(2 * np.pi * bar_frequency * X)
            elif orientation == "horizontal":
                colors = np.sin(2 * np.pi * bar_frequency * Y) 
        elif mode == "gradient bars":
            if orientation == "vertical":
                colors = (X * bar_frequency * 2) % 2
            elif orientation == "horizontal":
                colors = (Y * bar_frequency * 2) % 2
            
        fig, ax = plt.subplots(figsize=(width/100, height/100))

        ax.imshow(colors, cmap=bar_style, aspect='auto')

        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(tight=True)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)

        return pil2tensor(img),

#---------------------------------------------------------------------------------------------------------------------#
class CR_ColorGradient:
    @classmethod
    def INPUT_TYPES(s):
    
        colors = ["white", "black", "red", "green", "blue", "yellow",
            "cyan", "magenta", "orange", "purple", "pink", "brown", "gray",
            "lightgray", "darkgray", "olive", "lime", "teal", "navy", "maroon",
            "fuchsia", "aqua", "silver", "gold", "turquoise", "lavender",
            "violet", "coral", "indigo"]
        modes = ["linear", "radial"]
        
        return {"required": {
                    "mode": (modes,),
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "start_color": (colors,),
                    "end_color": (colors,),
                    "orientation": (["vertical", "horizontal", ],),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "CR 3D"

    def draw(self, mode, width, height, start_color, end_color, orientation):
    
        color1_rgb = color_mapping.get(start_color, (255, 255, 255))  # Default to white if the color is not found
        color2_rgb = color_mapping.get(end_color, (0, 0, 0))  # Default to black if the color is not found

        # Create a blank canvas
        canvas = np.zeros((height, width, 3), dtype=np.uint8)

        if mode == "linear": 
            if orientation == 'horizontal':
                # Create a smooth horizontal gradient
                for i in range(width):
                    t = i / (width - 1)
                    interpolated_color = [int((1 - t) * c1 + t * c2) for c1, c2 in zip(color1_rgb, color2_rgb)]
                    canvas[:, i] = interpolated_color
            elif orientation == 'vertical':
                # Create a smooth vertical gradient
                for j in range(height):
                    t = j / (height - 1)
                    interpolated_color = [int((1 - t) * c1 + t * c2) for c1, c2 in zip(color1_rgb, color2_rgb)]
                    canvas[j, :] = interpolated_color
        elif mode == "radial":        
            center_x = width // 2
            center_y = height // 2

            for i in range(width):
                for j in range(height):
                    distance_to_center = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                    t = distance_to_center / np.sqrt(center_x ** 2 + center_y ** 2)

                    interpolated_color = [
                        int((1 - t) * c1 + t * c2)
                        for c1, c2 in zip(color1_rgb, color2_rgb)
                    ]
                    canvas[j, i] = interpolated_color      

        fig, ax = plt.subplots(figsize=(width / 100, height / 100))

        ax.imshow(canvas)
        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(tight=True)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)

        return pil2tensor(img),

#---------------------------------------------------------------------------------------------------------------------#
class CR_CheckerPattern:

    @classmethod
    def INPUT_TYPES(s):
    
        colors = ["white", "black", "red", "green", "blue", "yellow",
            "cyan", "magenta", "orange", "purple", "pink", "brown", "gray",
            "lightgray", "darkgray", "olive", "lime", "teal", "navy", "maroon",
            "fuchsia", "aqua", "silver", "gold", "turquoise", "lavender",
            "violet", "coral", "indigo"]
        modes = ["regular", "stepped"]          
        
        return {"required": {
            "mode": (modes,),
            "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "color1": (colors,),
            "color2": (colors,), 
            "grid_frequency": ("INT", {"default": 8, "min": 1, "max": 200, "step": 1}),
            "step": ("INT", {"default": 2, "min": 2, "max": 200, "step": 1}),
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "CR 3D"

    def draw(self, mode, width, height, color1, color2, grid_frequency, step):

        color1_rgb = color_mapping.get(color1, (255, 255, 255))  # Default to white if the color is not found
        color2_rgb = color_mapping.get(color2, (0, 0, 0))  # Default to black if the color is not found

        # Create a blank canvas
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        
        grid_size = width / grid_frequency

        for i in range(width):
            for j in range(height):
            
                if mode == "regular":
                    if (i // grid_size) % 2 == (j // grid_size) % 2:    
                        canvas[j, i] = color1_rgb
                    else:
                        canvas[j, i] = color2_rgb
                elif mode == "stepped":
                    if (i // grid_size) % step != (j // grid_size) % step:    
                        canvas[j, i] = color1_rgb            
                    else:
                        canvas[j, i] = color2_rgb  

        fig, ax = plt.subplots(figsize=(width/100, height/100))

        ax.imshow(canvas)

        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(tight=True)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)

        return pil2tensor(img),
       
#---------------------------------------------------------------------------------------------------------------------#
class CR_Polygons:

    @classmethod
    def INPUT_TYPES(s):
    
        colors = ["white", "black", "red", "green", "blue", "yellow",
            "cyan", "magenta", "orange", "purple", "pink", "brown", "gray",
            "lightgray", "darkgray", "olive", "lime", "teal", "navy", "maroon",
            "fuchsia", "aqua", "silver", "gold", "turquoise", "lavender",
            "violet", "coral", "indigo"]
    
        modes = ["hexagons", "triangles"]          
        
        return {"required": {
            "mode": (modes,),
            "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "height": ("INT", {"default": 512, "min": 64, "max": 2048}),         
            "rows": ("INT", {"default": 5, "min": 2, "max": 512}),          
            "cols": ("INT", {"default": 5, "min": 2, "max": 512}),
            "color1": (colors,),
            "color2": (colors,),              
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "CR 3D"

    def draw(self, width, height, rows, cols, color1, color2, mode):
    
        fig, ax = plt.subplots(figsize=(width/100, height/100))
        
        color1_rgb = color_mapping.get(color1, (255, 255, 255))  # Default to white if the color is not found
        color2_rgb = color_mapping.get(color2, (255, 255, 255)) 
        hex_color1 = rgb_to_hex(color1_rgb)
        hex_color2 = rgb_to_hex(color2_rgb)
        
        if mode == "hexagons":
            vertices = 6
        elif mode == "triangles":
            vertices = 3      
        
        # Define the height and width of a hexagon
        hex_width = width // cols
        hex_height = np.sqrt(3) * hex_width / 2

        fig_width = cols * hex_width
        fig_height = (rows + 0.5) * hex_height
        
        for row in range(rows):
            for col in range(cols):
                x = col * hex_width
                y = row * hex_height

                # Shift every other row
                if row % 2 == 1:
                    x += hex_width / 2
                    hex_color = hex_color2
                else:
                    hex_color = hex_color1
                    
                # Create a hexagon as a polygon patch
                hexagon = RegularPolygon((x, y), numVertices=vertices, radius=hex_width/1.732, edgecolor='k', facecolor=hex_color)
                ax.add_patch(hexagon)
                 
        ax.set_xlim(0, fig_width)
        ax.set_ylim(0, fig_height)
         
        #ax.autoscale_view()
        
        plt.axis('off')
    
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(tight=True)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)

        return pil2tensor(img),   

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Color Bars" :CR_ColorBars,
    "CR Style Bars" :CR_StyleBars,
    "CR Checker Pattern" :CR_CheckerPattern,
    "CR Polygons" :CR_Polygons,
    "CR Halftone Grid" :CR_HalftoneGrid,
    "CR Color Gradient":CR_ColorGradient,
}
'''

