#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
from PIL import Image, ImageDraw, ImageStat, ImageFilter

from .functions_graphics import get_color_values
from ..config import color_mapping, COLORS
from ..categories import icons

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

#---------------------------------------------------------------------------------------------------------------------#
# Based on Color Tint node by hnmr293
class CR_ColorTint:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
    
        #tints = COLORS.append('sepia')
        
        tints = ["custom", "white", "black", "sepia", "red", "green", "blue",
            "cyan", "magenta", "yellow", "purple", "orange", "warm",
            "cool",  "lime", "navy", "vintage", "rose", "teal",
            "maroon", "peach", "lavender", "olive"]
           
        return {
            "required": {"image": ("IMAGE",),
                         "strength": ("FLOAT", {"default": 1.0,"min": 0.1,"max": 1.0,"step": 0.1}),
                         "mode": (tints,),
                        },
            "optional": {"tint_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),} 
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )    
    FUNCTION = "color_tint"
    CATEGORY = icons.get("Comfyroll/Graphics/Filter")

    def color_tint(self, image: torch.Tensor, strength, mode: str="sepia", tint_color_hex='#000000'):
    
        if strength == 0:
            return (image,)
            
        # Get RGB values for the tint color  
        tint_color = get_color_values(mode, tint_color_hex, color_mapping)    
        color_rgb = tuple([value / 255 for value in tint_color])
        
        sepia_weights = torch.tensor([0.2989, 0.5870, 0.1140]).view(1, 1, 1, 3).to(image.device)
        
        mode_filters = {
            "custom": torch.tensor([color_rgb[0], color_rgb[1], color_rgb[2]]),
            "white": torch.tensor([1, 1, 1]),
            "black": torch.tensor([0, 0, 0]),
            "sepia": torch.tensor([1.0, 0.8, 0.6]),
            "red": torch.tensor([1.0, 0.6, 0.6]),
            "green": torch.tensor([0.6, 1.0, 0.6]),
            "blue": torch.tensor([0.6, 0.8, 1.0]),
            "cyan": torch.tensor([0.6, 1.0, 1.0]),
            "magenta": torch.tensor([1.0, 0.6, 1.0]),
            "yellow": torch.tensor([1.0, 1.0, 0.6]),
            "purple": torch.tensor([0.8, 0.6, 1.0]),
            "orange": torch.tensor([1.0, 0.7, 0.3]),
            "warm": torch.tensor([1.0, 0.9, 0.7]),
            "cool": torch.tensor([0.7, 0.9, 1.0]),
            "lime": torch.tensor([0.7, 1.0, 0.3]),
            "navy": torch.tensor([0.3, 0.4, 0.7]),
            "vintage": torch.tensor([0.9, 0.85, 0.7]),
            "rose": torch.tensor([1.0, 0.8, 0.9]),
            "teal": torch.tensor([0.3, 0.8, 0.8]),
            "maroon": torch.tensor([0.7, 0.3, 0.5]),
            "peach": torch.tensor([1.0, 0.8, 0.6]),
            "lavender": torch.tensor([0.8, 0.6, 1.0]),
            "olive": torch.tensor([0.6, 0.7, 0.4]),
        }

        scale_filter = mode_filters[mode].view(1, 1, 1, 3).to(image.device)

        grayscale = torch.sum(image * sepia_weights, dim=-1, keepdim=True)
        tinted = grayscale * scale_filter

        result = tinted * strength + image * (1 - strength)
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Filter-Nodes#cr-color-tint"
        
        return (result, show_help, ) 

#---------------------------------------------------------------------------------------------------------------------#
class CR_HalftoneFilter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
    
        shapes = ["ellipse", "rectangle"]
        rez = ["normal", "hi-res (2x output size)"]
    
        return {
            "required": {
                "image": ("IMAGE",),
                "dot_size": ("INT", {"default": 5, "min": 1, "max": 30, "step": 1}),
                "dot_shape": (shapes, {"default": "ellipse"}),
                #"scale": ("INT", {"default": 1, "min": 1, "max": 8, "step": 1}),
                "resolution": (rez, {"default": "normal"}),
                "angle_c": ("INT", {"default": 75, "min": 0, "max": 360, "step": 1}),
                "angle_m": ("INT", {"default": 45, "min": 0, "max": 360, "step": 1}),
                "angle_y": ("INT", {"default": 15, "min": 0, "max": 360, "step": 1}),
                "angle_k": ("INT", {"default": 0, "min": 0, "max": 360, "step": 1}),
                "greyscale": ("BOOLEAN", {"default": True}),
                "antialias": ("BOOLEAN", {"default": True}),
                "antialias_scale": ("INT", {"default": 2, "min": 1, "max": 4, "step": 1}),
                "border_blending":  ("BOOLEAN", {"default": False}),                       
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "halftone_effect"
    CATEGORY = icons.get("Comfyroll/Graphics/Filter")
                 
    def tensor_to_pil(self, tensor):
        if tensor.ndim == 4 and tensor.shape[0] == 1:  # Check for batch dimension
            tensor = tensor.squeeze(0)  # Remove batch dimension
        if tensor.dtype == torch.float32:  # Check for float tensors
            tensor = tensor.mul(255).byte()  # Convert to range [0, 255] and change to byte type
        elif tensor.dtype != torch.uint8:  # If not float and not uint8, conversion is needed
            tensor = tensor.byte()  # Convert to byte type

        numpy_image = tensor.cpu().numpy()

        # Determine the correct mode based on the number of channels
        if tensor.ndim == 3:
            if tensor.shape[2] == 1:
                mode = 'L'  # Grayscale
            elif tensor.shape[2] == 3:
                mode = 'RGB'  # RGB
            elif tensor.shape[2] == 4:
                mode = 'RGBA'  # RGBA
            else:
                raise ValueError(f"Unsupported channel number: {tensor.shape[2]}")
        else:
            raise ValueError(f"Unexpected tensor shape: {tensor.shape}")

        pil_image = Image.fromarray(numpy_image, mode)
        return pil_image

    def pil_to_tensor(self, pil_image):
        numpy_image = np.array(pil_image)
        tensor = torch.from_numpy(numpy_image).float().div(255)  # Convert to range [0, 1]
        tensor = tensor.unsqueeze(0)  # Add batch dimension
        return tensor
        
    def halftone_effect(self, image, dot_size, dot_shape, resolution, angle_c, angle_m, angle_y, angle_k, greyscale, antialias, border_blending, antialias_scale):
        
        sample = dot_size
        shape = dot_shape
        
        # Map resolution to scale
        resolution_to_scale = {
            "normal": 1,
            "hi-res (2x output size)": 2,
        }
        scale = resolution_to_scale.get(resolution, 1)  # Default to 1 if resolution is not recognized
             
         # If the input is a PyTorch tensor, convert to PIL Image
        if isinstance(image, torch.Tensor):
            image = self.tensor_to_pil(image)
        
        # Ensure the image is a PIL Image
        if not isinstance(image, Image.Image):
            raise TypeError("The provided image is neither a PIL Image nor a PyTorch tensor.")

        pil_image = image  # Now we are sure pil_image is defined

        # Convert to greyscale or CMYK
        if greyscale:
            pil_image = pil_image.convert("L")
            channel_images = [pil_image]
            angles = [angle_k]
        else:
            pil_image = pil_image.convert("CMYK")
            channel_images = list(pil_image.split())
            angles = [angle_c, angle_m, angle_y, angle_k]

        # Apply the halftone effect using PIL
        halftone_images = self._halftone_pil(pil_image, channel_images, sample, scale, angles, antialias, border_blending, antialias_scale, shape)

        # Merge channels and convert to RGB
        if greyscale:
            new_image = halftone_images[0].convert("RGB")  # Convert the greyscale image to RGB
        else:
            new_image = Image.merge("CMYK", halftone_images).convert("RGB")
        
        result_tensor = self.pil_to_tensor(new_image)

        # Debug print to check the final tensor shape
        print("Final tensor shape:", result_tensor.shape)

        return (result_tensor, show_help, ) 

    def _halftone_pil(self, im, cmyk, sample, scale, angles, antialias, border_blending, antialias_scale, shape):
        # If we're antialiasing, we'll multiply the size of the image by this
        # scale while drawing, and then scale it back down again afterwards.
        antialias_res = antialias_scale if antialias else 1
        scale = scale * antialias_res

        dots = []

        for channel_index, (channel, angle) in enumerate(zip(cmyk, angles)):
            channel = channel.rotate(angle, expand=1)
            size = channel.size[0] * scale, channel.size[1] * scale
            half_tone = Image.new("L", size)
            draw = ImageDraw.Draw(half_tone)

            # Cycle through one sample point at a time, drawing a circle for
            # each one:
            for x in range(0, channel.size[0], sample):
                for y in range(0, channel.size[1], sample):

                    # Adjust the sampling near the borders for non-square angles
                    if border_blending and angle % 90 != 0 and (x < sample or y < sample or x > channel.size[0] - sample or y > channel.size[1] - sample):
                        # Get a weighted average of the neighboring pixels
                        neighboring_pixels = channel.crop((max(x - 1, 0), max(y - 1, 0), min(x + 2, channel.size[0]), min(y + 2, channel.size[1])))
                        pixels = list(neighboring_pixels.getdata())
                        weights = [0.5 if i in [0, len(pixels)-1] else 1 for i in range(len(pixels))]
                        weighted_mean = sum(p * w for p, w in zip(pixels, weights)) / sum(weights)
                        mean = weighted_mean
                    else:
                        # Area we sample to get the level:
                        box = channel.crop((x, y, x + sample, y + sample))
                        # The average level for that box (0-255):
                        mean = ImageStat.Stat(box).mean[0]

                    # The diameter or side length of the shape to draw based on the mean (0-1):
                    size = (mean / 255) ** 0.5

                    # Size of the box we'll draw the circle in:
                    box_size = sample * scale

                    # Diameter or side length of shape we'll draw:
                    draw_size = size * box_size

                    # Position of top-left of box we'll draw the circle in:
                    box_x, box_y = (x * scale), (y * scale)

                    # Positioned of top-left and bottom-right of circle:
                    x1 = box_x + ((box_size - draw_size) / 2)
                    y1 = box_y + ((box_size - draw_size) / 2)
                    x2 = x1 + draw_size
                    y2 = y1 + draw_size

                    # Draw the shape based on the variable passed
                    draw_method = getattr(draw, shape, None)
                    if draw_method:
                        draw_method([(x1, y1), (x2, y2)], fill=255)

            half_tone = half_tone.rotate(-angle, expand=1)
            width_half, height_half = half_tone.size

            # Top-left and bottom-right of the image to crop to:
            xx1 = (width_half - im.size[0] * scale) / 2
            yy1 = (height_half - im.size[1] * scale) / 2
            xx2 = xx1 + im.size[0] * scale
            yy2 = yy1 + im.size[1] * scale

            half_tone = half_tone.crop((xx1, yy1, xx2, yy2))

            if antialias:
                # Scale it back down to antialias the image.
                w = int((xx2 - xx1) / antialias_scale)
                h = int((yy2 - yy1) / antialias_scale)
                half_tone = half_tone.resize((w, h), resample=Image.LANCZOS)

            dots.append(half_tone)
            
            show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Filter-Nodes#cr-halftone-filter"

        return (dots, show_help, )  
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_VignetteFilter:

    @classmethod
    def INPUT_TYPES(s):
                    
        return {"required": {
                    "image": ("IMAGE",),
                    "vignette_shape": (["circle","oval","square","diamond"],),                    
                    "feather_amount": ("INT", {"default": 100, "min": 0, "max": 1024}),
                    "x_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "y_offset": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                    "zoom": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                    "reverse": (["no","yes"],), 
               }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", )
    RETURN_NAMES = ("IMAGE", "MASK", "show_help", )
    FUNCTION = "make_vignette"
    CATEGORY = icons.get("Comfyroll/Graphics/Filter")
    
    def make_vignette(self, image, feather_amount, reverse,
                      vignette_shape='circle',
                      x_offset=0, y_offset=0, zoom=1.0):
    
        images = []
        masks = []

        vignette_color = "black"

        for img in image:
            im = tensor2pil(img)

            RADIUS = feather_amount

            # Create an alpha mask for the vignette effect
            alpha_mask = Image.new('L', im.size, 255)
            draw = ImageDraw.Draw(alpha_mask)

            center_x = im.size[0] // 2 + x_offset
            center_y = im.size[1] // 2 + y_offset         
            radius = min(center_x, center_y) * zoom
            size_x = (im.size[0] - RADIUS) * zoom
            size_y = (im.size[1] - RADIUS) * zoom               
                    
            if vignette_shape == 'circle':
                if reverse == 'no':
                    # Calculate the position to center the circular mask with offsets and zoom
                    draw.ellipse([(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)], fill=0)
                elif reverse == 'yes':
                    draw.rectangle([(0, 0), im.size], fill=0)
                    draw.ellipse([(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)], fill=255)             
                else:
                    raise ValueError("Invalid value for reverse. Use 'yes' or 'no'.")
            elif vignette_shape == 'oval':
                if reverse == 'no':
                    draw.ellipse([(center_x - size_x / 2, center_y - size_y / 2),
                        (center_x + size_x / 2, center_y + size_y / 2)], fill=0)
                elif reverse == 'yes':
                    draw.rectangle([(0, 0), im.size], fill=0)
                    draw.ellipse([(center_x - size_x / 2, center_y - size_y / 2),
                        (center_x + size_x / 2, center_y + size_y / 2)], fill=255)                                                             
            elif vignette_shape == 'diamond':
                if reverse == 'no':
                    # Calculate the position and size to center the diamond mask with offsets and zoom
                    size = min(im.size[0] - x_offset, im.size[1] - y_offset) * zoom
                    draw.polygon([(center_x, center_y - size / 2),
                                  (center_x + size / 2, center_y),
                                  (center_x, center_y + size / 2),
                                  (center_x - size / 2, center_y)],
                                 fill=0)
                elif reverse == 'yes':
                    size = min(im.size[0] - x_offset, im.size[1] - y_offset) * zoom
                    draw.rectangle([(0, 0), im.size], fill=0)
                    draw.polygon([(center_x, center_y - size / 2),
                                  (center_x + size / 2, center_y),
                                  (center_x, center_y + size / 2),
                                  (center_x - size / 2, center_y)],
                                 fill=255)                                    
            elif vignette_shape == 'square':
                if reverse == 'no':
                    # Calculate the position to center the square mask with offsets and zoom
                    size = min(im.size[0] - x_offset, im.size[1] - y_offset) * zoom
                    draw.rectangle([(center_x - size / 2, center_y - size / 2),
                        (center_x + size / 2, center_y + size / 2)], fill=0)
                elif reverse == 'yes':
                    size = min(im.size[0] - x_offset, im.size[1] - y_offset) * zoom
                    draw.rectangle([(0, 0), im.size], fill=0)
                    draw.rectangle([(center_x - size / 2, center_y - size / 2),
                        (center_x + size / 2, center_y + size / 2)], fill=255)                      
                else:
                    raise ValueError("Invalid value for reverse. Use 'yes' or 'no'.")
            else:
                raise ValueError("Invalid vignette_shape. Use 'circle', 'oval', or 'square'.")

            # Apply GaussianBlur to the alpha mask for feathering
            alpha_mask = alpha_mask.filter(ImageFilter.GaussianBlur(RADIUS))
            
            # Append the alpha mask to the masks list
            masks.append(pil2tensor(alpha_mask).unsqueeze(0))

            # Create a new image with the vignette effect
            vignette_img = Image.new('RGBA', im.size, vignette_color)
            vignette_img.putalpha(alpha_mask)

            # Composite the original image with the vignette effect
            result_img = Image.alpha_composite(im.convert('RGBA'), vignette_img)

            images.append(pil2tensor(result_img.convert("RGB")))

        images = torch.cat(images, dim=0)
        masks = torch.cat(masks, dim=0)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Layout-Nodes#cr-vignette-filter"

        return (images, masks, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
        "CR Halftone Filter": "CR HalftoneFilter",
        "CR Color Tint": CR_ColorTint,
        "CR Vignette Filter": CR_VignetteFilter,        
}
'''

