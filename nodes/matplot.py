#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import os
import sys
import io
import folder_paths
from PIL import Image

try:
    import matplotlib.pyplot as plt
except ImportError:
    import pip
    pip.main(['install', 'matplotlib'])
    import matplotlib.pyplot as plt
    
from matplotlib.patches import RegularPolygon

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

#---------------------------------------------------------------------------------------------------------------------#

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
    CATEGORY = "Comfyroll/Graphics/Patterns"

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
    
        modes = ["2-color"]
        
        return {"required": {
                    "mode": (modes,),
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "color1": (COLORS,),
                    "color2": (COLORS,),
                    "orientation": (["vertical", "horizontal", "diagonal", "alt_diagonal"],), #added 135 angle for diagonals
                    "bar_frequency": ("INT", {"default": 5, "min": 1, "max":200, "step": 1}),
                    "offset": ("FLOAT", {"default": 0, "min": 0, "max":20, "step": 0.05}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "Comfyroll/Graphics/Patterns"

    def draw(self, mode, width, height, color1, color2, orientation, bar_frequency, offset=0):

        color1_rgb = color_mapping.get(color1, (255, 255, 255))  # Default to white if the color is not found
        color2_rgb = color_mapping.get(color2, (0, 0, 0))  # Default to black if the color is not found

        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        
        bar_width = width / bar_frequency
        bar_height = height / bar_frequency
        offset_pixels = int(offset * max(width, height))

        if orientation == "vertical":
            for j in range(height):
                for i in range(width):
                    if ((i + offset_pixels) // bar_width) % 2 == 0:  # Check for even index
                        canvas[j, i] = color1_rgb
                    else:
                        canvas[j, i] = color2_rgb
        elif orientation == "horizontal":
            for j in range(height):
                for i in range(width):
                    if ((j + offset_pixels) // bar_height) % 2 == 0:  # Check for even index
                        canvas[j, i] = color1_rgb
                    else:
                        canvas[j, i] = color2_rgb                
        elif orientation == "diagonal":
            # Calculate the bar width based on a 45 degree angle 
            bar_width = int(bar_height / np.tan(np.pi / 4)) * 2
            for j in range(height): 
                for i in range(width):
                     # Calculate which diagonal bar the pixel belongs to with the offset
                    bar_number = (i + j + offset_pixels) // bar_width
                    if bar_number % 2 == 0:  # Check for even bar number
                        canvas[j, i] = color1_rgb
                    else:
                        canvas[j, i] = color2_rgb
        elif orientation == "alt_diagonal":
            bar_width = int(bar_height / np.tan(np.pi / 4)) * 2
            for j in range(height): 
                for i in range(width):
                    # Calculate which diagonal bar the pixel belongs to with the offset
                    bar_number = (i - j + width + offset_pixels) // bar_width
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
    CATEGORY = "Comfyroll/Graphics/Patterns"

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
    
        modes = ["linear", "radial"]
        
        return {"required": {
                    "mode": (modes,),
                    "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                    "start_color": (COLORS,),
                    "end_color": (COLORS,),
                    "gradient_distance": ("FLOAT", {"default": 1, "min": 0, "max": 2, "step": 0.05}),
                    "transition_point": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": 0.05}),
                    "rad_center_x": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": 0.05}),
                    "rad_center_y": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": 0.05}),
                    "orientation": (["vertical", "horizontal", ],),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "Comfyroll/Graphics/Patterns"

    def draw(self, mode, width, height, start_color, end_color, orientation, transition_point=0.5, rad_center_x=0.5, rad_center_y=0.5, gradient_distance=1): # Default to .5 if the value is not found
    
        color1_rgb = color_mapping.get(start_color, (255, 255, 255))  # Default to white if the color is not found
        color2_rgb = color_mapping.get(end_color, (0, 0, 0))  # Default to black if the color is not found

        # Create a blank canvas
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        transition_pixel = int(transition_point * (width if orientation == 'horizontal' else height)) #getting center point for gradient
        
        def get_gradient_value(pos, length, transition_point, gradient_distance): #getting the distance we use to apply gradient
            # Calculate the start and end of the transition
            transition_length = length * gradient_distance
            transition_start = transition_point * length - transition_length / 2
            transition_end = transition_point * length + transition_length / 2
            
            # Return the gradient value based on position
            if pos < transition_start:
                return 0
            elif pos > transition_end:
                return 1
            else:
                return (pos - transition_start) / transition_length

        if mode == "linear":  #changed the approach here to use numpy since we have it anyway, makes the new code way easier to apply
            if orientation == 'horizontal':
                # Define the x-values for interpolation
                x = [0, width * transition_point - 0.5 * width * gradient_distance, width * transition_point + 0.5 * width * gradient_distance, width]
                # Define the y-values for interpolation (t-values)
                y = [0, 0, 1, 1]
                # Interpolate
                t_values = np.interp(np.arange(width), x, y)
                for i, t in enumerate(t_values):
                    interpolated_color = [int(c1 * (1 - t) + c2 * t) for c1, c2 in zip(color1_rgb, color2_rgb)]
                    canvas[:, i] = interpolated_color

            elif orientation == 'vertical':
                # Define the x-values for interpolation
                x = [0, height * transition_point - 0.5 * height * gradient_distance, height * transition_point + 0.5 * height * gradient_distance, height]
                # Define the y-values for interpolation (t-values)
                y = [0, 0, 1, 1]
                # Interpolate
                t_values = np.interp(np.arange(height), x, y)
                for j, t in enumerate(t_values):
                    interpolated_color = [int(c1 * (1 - t) + c2 * t) for c1, c2 in zip(color1_rgb, color2_rgb)]
                    canvas[j, :] = interpolated_color
                    
        elif mode == "radial":        
                center_x = int(rad_center_x * width)
                center_y = int(rad_center_y * height)
                # Corrected computation for max_distance
                max_distance = (np.sqrt(max(center_x, width - center_x)**2 + max(center_y, height - center_y)**2))*gradient_distance

                for i in range(width):
                    for j in range(height):
                        distance_to_center = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                        t = distance_to_center / max_distance
                        # Ensure t is between 0 and 1
                        t = max(0, min(t, 1))
                        interpolated_color = [int(c1 * (1 - t) + c2 * t) for c1, c2 in zip(color1_rgb, color2_rgb)]
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
    
        modes = ["regular", "stepped"]          
        
        return {"required": {
            "mode": (modes,),
            "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "color1": (COLORS,),
            "color2": (COLORS,), 
            "grid_frequency": ("INT", {"default": 8, "min": 1, "max": 200, "step": 1}),
            "step": ("INT", {"default": 2, "min": 2, "max": 200, "step": 1}),
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "Comfyroll/Graphics/Patterns"

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
        
        modes = ["hexagons", "triangles"]          
        
        return {"required": {
            "mode": (modes,),
            "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "height": ("INT", {"default": 512, "min": 64, "max": 2048}),         
            "rows": ("INT", {"default": 5, "min": 1, "max": 512}),          
            "columns": ("INT", {"default": 5, "min": 1, "max": 512}),
            "face_color": (COLORS,),
            "line_color": (COLORS,),            
            "line_width": ("INT", {"default": 2, "min": 0, "max": 512}),
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "Comfyroll/Graphics/Patterns"

    def draw(self, mode, width, height, rows, columns, face_color, line_color, line_width):
    
        fig, ax = plt.subplots(figsize=(width/100, height/100))
        plt.xlim(0, width/100)
        plt.ylim(0, height/100)
        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(False)         
        
        face_color_rgb = color_mapping.get(face_color, (255, 255, 255))  # Default to white if the color is not found
        face_color_hex = rgb_to_hex(face_color_rgb)
        
        if mode == "hexagons":
            vertices = 6
        elif mode == "triangles":
            vertices = 3      
        
        # Define the height and width of a hexagon
        cell_width = (width/100) / columns
        print(cell_width)
    
        cell_height = (width/height) * np.sqrt(3) * (height/100) / (2 * columns)
        print(cell_height)
        
        for row in range(rows + 2):
            for col in range(columns + 2):
                x = col * cell_width
                y = row * cell_height

                # Shift every other row
                if row % 2 == 1:
                    x += cell_width / 2
                #    hex_color = hex_color2
                #else:
                #    hex_color = hex_color1
                    
                # Create a hexagon as a polygon patch
                hexagon = RegularPolygon((x, y), numVertices=vertices, radius=cell_width/1.732, edgecolor=line_color, linewidth=line_width, facecolor=face_color)
                ax.add_patch(hexagon)
                 
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)

        return pil2tensor(img),   

#---------------------------------------------------------------------------------------------------------------------#
class CR_StarburstLines:

    @classmethod
    def INPUT_TYPES(s):
      
        return {"required": {
            "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "height": ("INT", {"default": 512, "min": 64, "max": 2048}),              
            "num_lines": ("INT", {"default": 6, "min": 1, "max": 2048}),      
            "line_length": ("INT", {"default": 256, "min": 1, "max": 512}), 
            "line_width": ("INT", {"default": 5, "min": 1, "max": 512}),
            "line_color": (COLORS,),
            "background_color": (COLORS,),
            "center_x": ("INT", {"default": 0, "min": 0, "max": 1024}),
            "center_y": ("INT", {"default": 0, "min": 0, "max": 1024}),
            "rotation": ("FLOAT", {"default": 0, "min": 0, "max": 720}),            
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "Comfyroll/Graphics/Patterns"
    
    def draw(self, width, height, num_lines, line_length, line_width, line_color, background_color, center_x, center_y, rotation=0):
             
        bgc = background_color        
        
        # Define the angle for the spokes in the starburst
        angle = 360 / num_lines

        # Set up the plot
        fig, ax = plt.subplots(figsize=(width/100,height/100))
        plt.xlim(-width/100, width/100)
        plt.ylim(-height/100, height/100)
        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(False)        

        # Coordinates of the central point
        center_x = center_x/100
        center_y = center_y/100

        # Draw the starburst lines
        for i in range(num_lines):
            # Calculate the endpoint of each line
            x_unrotated = center_x + line_length * np.cos(np.radians(i * angle))
            y_unrotated = center_y + line_length * np.sin(np.radians(i * angle))
        
            # Apply rotation transformation
            x = center_x + x_unrotated * np.cos(np.radians(rotation)) - y_unrotated * np.sin(np.radians(rotation))
            y = center_y + x_unrotated * np.sin(np.radians(rotation)) + y_unrotated * np.cos(np.radians(rotation))
        
            # Plot the line
            fig.patch.set_facecolor(bgc)
            ax.plot([center_x, x], [center_y, y], color=line_color, linewidth=line_width)
   
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img = Image.open(img_buf)

        return pil2tensor(img), 
        
#---------------------------------------------------------------------------------------------------------------------#
class CR_StarburstColors:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {
            #"mode": (modes,),
            "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "height": ("INT", {"default": 512, "min": 64, "max": 2048}),             
            "num_triangles": ("INT", {"default": 6, "min": 1, "max": 512}),                      
            "color_1": (COLORS,),
            "color_2": (COLORS,),
            "center_x": ("INT", {"default": 0, "min": 0, "max": 512}),
            "center_y": ("INT", {"default": 0, "min": 0, "max": 512}),
            "rotation": ("FLOAT", {"default": 0, "min": 0, "max": 720}),
            "bbox_factor": ("FLOAT", {"default": 2, "min": 0, "max": 2, "step": .01}),
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = "Comfyroll/Graphics/Patterns"        
        
    def draw(self, width, height, num_triangles, color_1, color_2, center_x, center_y, bbox_factor, rotation=0): 

        # Set up the plot
        fig, ax = plt.subplots()
        
        x = width/100
        y = height/100

        fig, ax = plt.subplots(figsize=(x,y))  
        plt.xlim(-x/2, x/2)
        plt.ylim(-y/2, y/2)
        
        plt.axis('off')
        plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.autoscale(False)
        
        # Set the size of the starburst bounding box in x and y dimensions
        box_width = bbox_factor * x
        box_height = bbox_factor * y
        
        # Initialize a color list for alternating colors
        colors = [color_1, color_2]
        
        tri = num_triangles
        
        # Draw the starburst triangles with alternating colors and square pattern
        for i in range(tri):
            # Calculate the endpoints of the triangle with varying length
            x1 = center_x/100
            y1 = center_y/100
            x2_unrotated = (box_width / 2) * np.cos(np.radians(i * 360 / tri))
            y2_unrotated = (box_height / 2) * np.sin(np.radians(i * 360 / tri))
            x3_unrotated = (box_width / 2) * np.cos(np.radians((i + 1) * 360 / tri))
            y3_unrotated = (box_height / 2) * np.sin(np.radians((i + 1) * 360 / tri))
            
            #apply rotation transform
            x2 = x2_unrotated * np.cos(np.radians(rotation)) - y2_unrotated * np.sin(np.radians(rotation))
            y2 = x2_unrotated * np.sin(np.radians(rotation)) + y2_unrotated * np.cos(np.radians(rotation))
            x3 = x3_unrotated * np.cos(np.radians(rotation)) - y3_unrotated * np.sin(np.radians(rotation))
            y3 = x3_unrotated * np.sin(np.radians(rotation)) + y3_unrotated * np.cos(np.radians(rotation))
            
            # Plot the triangle with alternating colors
            ax.fill([x1, x2, x3, x1], [y1, y2, y3, y1], color=colors[i % 2])

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
    "CR Overlay Text":CR_OverlayText,
    "CR Starburst Lines":CR_StarburstLines,
    "CR Starburst Colors":CR_StarburstColors,
}
'''

