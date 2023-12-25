#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import math
import torch
import os 
from PIL import Image, ImageDraw
from ..categories import icons
from ..config import color_mapping, COLORS  
    
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
class CR_3DPolygon:

    @classmethod
    def INPUT_TYPES(s):
    
        shapes = ["cube","tetrahedron"]
        
        return {"required": {
            "shape": (shapes,),
            "image_width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "image_height": ("INT", {"default": 512, "min": 64, "max": 2048}),          
            "radius": ("INT", {"default": 100, "min": 2, "max": 2048}),          
            "distance": ("INT", {"default": 200, "min": 2, "max": 2048}), 
            "rotation_angle": ("FLOAT", {"default": 0, "min": 0, "max": 3600, "step": 0.5}),            
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw_cube"
    CATEGORY = icons.get("Comfyroll/Graphics/3D")
    
    def draw_cube(self, shape, image_width, image_height, radius, distance, rotation_angle=45):
        # Create a blank canvas
        size = (image_height, image_width)
        image = Image.new("RGB", size)
        draw = ImageDraw.Draw(image)

        if shape == "cube":
            vertices = [
                (-radius, -radius, -radius),
                (radius, -radius, -radius),
                (radius, radius, -radius),
                (-radius, radius, -radius),
                (-radius, -radius, radius),
                (radius, -radius, radius),
                (radius, radius, radius),
                (-radius, radius, radius)
            ]
            edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),
                (4, 5), (5, 6), (6, 7), (7, 4),
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]
        elif shape == "tetrahedron":
            vertices = [
                (0, radius, 0),
                (radius, -radius, -radius),
                (-radius, -radius, -radius),
                (0, -radius, radius)
            ]
            edges = [
                (0, 1), (0, 2), (0, 3),
                (1, 2), (2, 3), (3, 1)
            ]

        # Function to project 3D points to 2D
        def project_point(point):
            x, y, z = point
            x_2d = x * distance / (z + distance) + size[0] / 2
            y_2d = y * distance / (z + distance) + size[1] / 2
            return x_2d, y_2d

        # Rotate the cube
        rotated_vertices = []
        angle = math.radians(rotation_angle)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        for vertex in vertices:
            x, y, z = vertex
            new_x = x * cos_a - z * sin_a
            new_z = x * sin_a + z * cos_a
            rotated_vertices.append((new_x, y, new_z))

        # Project and draw the rotated cube
        for edge in edges:
            start_point = project_point(rotated_vertices[edge[0]])
            end_point = project_point(rotated_vertices[edge[1]])
            draw.line([start_point, end_point], fill=(255, 255, 255))

        # Convert the PIL image to a PyTorch tensor
        tensor_image = pil2tensor(image)

        return (tensor_image,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_3DSolids:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image_width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "image_height": ("INT", {"default": 512, "min": 64, "max": 2048}),          
            "radius": ("INT", {"default": 100, "min": 2, "max": 2048}),
            "height": ("INT", {"default": 100, "min": 2, "max": 2048}),
            "distance": ("INT", {"default": 200, "min": 2, "max": 2048}),            
            "rotation_angle": ("FLOAT", {"default": 0, "min": 0, "max": 3600, "step": 0.5}),           
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw"
    CATEGORY = icons.get("Comfyroll/Graphics/3D")

    def draw(self, image_width, image_height, radius, height, distance, rotation_angle=45):
    
        # Create a blank canvas
        size = (image_height, image_width)
        image = Image.new("RGB", size)
        draw = ImageDraw.Draw(image)

        # Define the cone's vertices
        vertices = [
            (0, height / 2, 0),
            (0, -height / 2, 0)
        ]

        num_points = 20  # Number of points to approximate the circular base
        base_points = [
            (radius * math.cos(2 * math.pi * i / num_points), -height / 2, radius * math.sin(2 * math.pi * i / num_points))
            for i in range(num_points)
        ]
        vertices = vertices + base_points

        # Define the cone's edges as pairs of vertices
        edges = []
        for i in range(num_points):
            edges.append((0, i + 2))
            edges.append((1, i + 2))
            edges.append((i + 2, (i + 3) if i < num_points - 1 else 2))

        # Function to project 3D points to 2D
        def project_point(point):
            x, y, z = point
            x_2d = x * distance / (z + distance) + size[0] / 2
            y_2d = y * distance / (z + distance) + size[1] / 2
            return x_2d, y_2d

        # Rotate the cone
        rotated_vertices = []
        angle = math.radians(rotation_angle)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        for vertex in vertices:
            x, y, z = vertex
            new_x = x * cos_a - z * sin_a
            new_z = x * sin_a + z * cos_a
            rotated_vertices.append((new_x, y, new_z))

        # Project and draw the rotated cone's faces with different colors
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Example colors
        for i in range(num_points):
            vertices_indices = [0, i + 2, (i + 3) if i < num_points - 1 else 2]
            face_vertices = [project_point(rotated_vertices[idx]) for idx in vertices_indices]
            fill_color = colors[i % 3]  # Cycle through colors for each face
            draw.polygon(face_vertices, fill=fill_color)

        # Draw the edges
        for edge in edges:
            start_point = project_point(rotated_vertices[edge[0]])
            end_point = project_point(rotated_vertices[edge[1]])
            draw.line([start_point, end_point], fill=(0, 0, 0))

        # Convert the PIL image to a PyTorch tensor
        tensor_image = pil2tensor(image)

        return (tensor_image,)

#---------------------------------------------------------------------------------------------------------------------#

class CR_DrawOBJ:

    @classmethod
    def INPUT_TYPES(s):
    
        obj_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "obj")
        file_list = [f for f in os.listdir(obj_dir) if os.path.isfile(os.path.join(obj_dir, f)) and f.lower().endswith(".obj")]      

    
        return {"required": {
            "image_width": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "image_height": ("INT", {"default": 512, "min": 64, "max": 2048}),
            "obj_name": (file_list,),            
            "line_color": (COLORS[1:],),           
        },
    }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "draw_wireframe"
    CATEGORY = icons.get("Comfyroll/Graphics/3D")
    
    def draw_wireframe(self, obj_name, image_width=800, image_height=800, line_color="black"):

        # Load the OBJ file
        obj_file = "obj\\" + str(obj_name)   
        resolved_obj_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), obj_file)
        scene = Wavefront(resolved_obj_path)

        # Create a blank image
        img = Image.new("RGB", (image_width, image_height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        for name, material in scene.materials.items():
            for face in material.mesh.faces:
                vertices = [scene.vertices[i] for i in face]

                # Draw lines between vertices to create wireframe
                for i in range(len(vertices)):
                    x1, y1, z1 = vertices[i]
                    x2, y2, z2 = vertices[(i + 1) % len(vertices)]

                    # Scale and translate vertices to fit the image
                    x1 = int((x1 + 1) * image_width / 2)
                    y1 = int((1 - y1) * image_height / 2)
                    x2 = int((x2 + 1) * image_width / 2)
                    y2 = int((1 - y2) * image_height / 2)

                    draw.line([(x1, y1), (x2, y2)], fill=line_color)

        # Convert the PIL image to a PyTorch tensor
        tensor_image = pil2tensor(img)

        return (tensor_image,)    

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR 3D Polygon":CR_3DPolygon,
    "CR 3D Solids":CR_3DSolids,
    "CR Draw OBJ":CR_DrawOBJ,
}
'''

