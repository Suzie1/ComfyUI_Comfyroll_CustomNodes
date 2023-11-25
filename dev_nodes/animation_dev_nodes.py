#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi
# for ComfyUI                                    https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

from PIL import Image
import torch
import numpy as np
import folder_paths
from math import sqrt, ceil
from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
# Interpolation Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_InterpolatePromptWeights:

    @classmethod
    def INPUT_TYPES(cls):
    
        #interpolation_methods = ["lerp", "slerp"]
        interpolation_methods = ["lerp"]
        
        return {
            "required": {
                "weight1": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "weight2": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "method": (interpolation_methods,),
            },
            #"optional": {"schedule": ("SCHEDULE",),
            #}
            
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("weight",)
    FUNCTION = "interpolate"

    CATEGORY = icons.get("Comfyroll/Animation/Interpolate")

    def interpolate(self, weight1, weight2, method):
    
        weight = 0.5
        return (weight,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageTransition:
    @classmethod
    def INPUT_TYPES(s):
        transition_types = ["Morph", "Dissolve", "Cross-Fade", "Jump Cut",
            "Swipe-Left", "Swipe-Right", "Fade to Black"]
            
        return {"required": {
                    "image1": ("IMAGE",),
                    "image2": ("IMAGE",),
                    "transition_type": (transition_types,),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "start_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "end_keyframe": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "get_image"
    CATEGORY = icons.get("Comfyroll/Animation/Other")

    def get_image(self, image1, image2, transition_type, current_frame, start_keyframe, end_keyframe):
    
        image_out = image1
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------#       
class CR_AlternateLatents:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent1": ("LATENT",),
                "latent2": ("LATENT",),          
                "frame_interval": ("INT", {"default": 1, "min": 1, "max": 999}),
                "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),               
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "InputLatents"
    CATEGORY = icons.get("Comfyroll/Animation/Other")

    def InputLatents(self, latent1, latent2, frame_interval, current_frame):

        if current_frame == 0:
            return latent1  # Start with the first latent

        frame_mod = (current_frame // frame_interval) % 2
        
        if frame_mod == 0:
            return latent1
        else:
            return latent2
            
#---------------------------------------------------------------------------------------------------------------------#       
class CR_StrobeImages:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "animationframes1": ("IMAGE",),
                "animation frames2": ("IMAGE",),          
                "frame_interval": ("INT", {"default": 1, "min": 1, "max": 999}),
                "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),               
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "strobe"
    CATEGORY = icons.get("Comfyroll/Animation/Other")

    def strobe(self, image1, image2, frame_interval, current_frame):

        if current_frame == 0:
            return image1  # Start with the first image

        frame_mod = (current_frame // frame_interval) % 2
        
        if frame_mod == 0:
            return image1
        else:
            return image2

#---------------------------------------------------------------------------------------------------------------------#
# Camera Nodes
#---------------------------------------------------------------------------------------------------------------------# 
# add more camera types and motions, including
#   hand held, steadycam
#   crane/boom camera
#   dolly/track
#   pov
#   static camera
#---------------------------------------------------------------------------------------------------------------------# 

class CR_StaticCamera3D:
    @classmethod
    def INPUT_TYPES(s):
        rotation_types = ["Tilt Up", "Tilt Down", "Pan Left", "Pan Right"]
        
        return {"required": {
                    "image": ("IMAGE",),
                    "x_position": ("FLOAT", {"default": 0.0}),
                    "y_position": ("FLOAT", {"default": 0.0}),                   
                    "pan_rotation": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                    "tilt_rotation": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                    "zoom_factor": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.1}),                      
                    "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),                    
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "static3d"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def static3d(self, image, x_position, y_position, pan_rotation, tilt_rotation, zoom_factor, start_frame, current_frame, frame_duration):
    
        if current_frame < start_frame:
            return (image,)

        if current_frame >= start_frame + frame_duration:
            return (image,)

        if rotation_type == "Tilt Up":
            rotation_angle = start_angle - (tilt_rotation * ((current_frame - start_frame) / frame_duration))
        elif rotation_type == "Tilt Down":
            rotation_angle = start_angle + (tilt_rotation * ((current_frame - start_frame) / frame_duration))
        elif rotation_type == "Pan Left":
            rotation_angle = start_angle - (pan_rotation * ((current_frame - start_frame) / frame_duration))
        elif rotation_type == "Pan Right":
            rotation_angle = start_angle + (pan_rotation * ((current_frame - start_frame) / frame_duration))
        else:
            rotation_angle = start_angle

        # Apply rotation to the image using your rotation logic here
        # You should apply the rotation angle to transform the image accordingly
        
        # image_out = apply_rotation(image, rotation_angle)  # Replace this with your actual rotation logic
        image_out = image
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------# 
class CR_DroneCamera3D:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                    "image": ("IMAGE",),        
                    "x_position": ("FLOAT", {"default": 0.0}),
                    "y_position": ("FLOAT", {"default": 0.0}),
                    "yaw_angle": ("FLOAT", {"default": 0.0}),
                    "pitch_angle": ("FLOAT", {"default": 0.0}),
                    "roll_angle": ("FLOAT", {"default": 0.0}),
                    "zoom_factor": ("FLOAT", {"default": 0.0}),                    
                    "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                }
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "drone3d"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def drone3d(self, x_position, y_position, z_position, yaw_angle, pitch_angle,
                roll_angle, zoom_factor, start_frame, current_frame, frame_duration):
        """
        Create an animation of aerial camera movements.

        Args:
            x_position (float): The camera's x-coordinate in 3D space.
            y_position (float): The camera's y-coordinate in 3D space.
            z_position (float): The camera's z-coordinate in 3D space.
            yaw_angle (float): The camera's rotation around the vertical axis (yaw).
            pitch_angle (float): The camera's rotation around the lateral axis (pitch).
            roll_angle (float): The camera's rotation around the longitudinal axis (roll).
            fov (float): The camera's field of view angle.
            zoom_factor (float): The zoom factor affecting FOV or object size.
            frame_rate (int): The number of frames per second for the animation.
            animation_duration (float): The total duration of the animation in seconds.
            image_width (int): The width of the output image in pixels.
            image_height (int): The height of the output image in pixels.

        Returns:
            List[PIL.Image.Image]: A list of image.
        """
        # Your animation generation logic here
        # Combine camera movements, FOV changes, and zoom effects
        # Generate image based on the provided parameters
        
        #animation_frames = []  # List to store image
        
        # Implement your animation generation logic here
        image_out = image
        
        return image_out

#---------------------------------------------------------------------------------------------------------------------#
class CR_InterpolateZoom:
    @classmethod
    def INPUT_TYPES(s):
        zoom_types = ["Zoom In", "Zoom Out",]
        return {"required": {
                    "image": ("IMAGE",),
                    "zoom_type": (zoom_types,),
                    "start_factor": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "step_factor": ("INT", {"default": 1.0, "min": -9999.0, "max": 9999.0, "step": 1.0,}),
                    "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "zoom"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def zoom(self, image, zoom_type, current_frame, zoom_factor):
    
        if current_frame < start_frame:
            return (image,)

        if current_frame >= start_frame + frame_duration:
            return (image,)

        if zoom_type == "Zoom In":
            zoom_factor = 1.0 + (zoom_amount - 1.0) * ((current_frame - start_frame) / frame_duration)
        elif zoom_type == "Zoom Out":
            zoom_factor = 1.0 - (zoom_amount - 1.0) * ((current_frame - start_frame) / frame_duration)
        else:
            zoom_factor = 1.0

        # Apply zoom to the image using your zoom logic here
        # You should apply the zoom factor to resize the image accordingly
        
        # image_out = apply_zoom(image, zoom_factor)  # Replace this with your actual zoom logic
        image_out = image
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
class CR_InterpolateRotation:
    @classmethod
    def INPUT_TYPES(s):
        rotation_types = ["Tilt Up", "Tilt Down", "Pan Left", "Pan Right"]
        
        return {"required": {
                    "image": ("IMAGE",),
                    "rotation_type": (rotation_types,),
                    "pan_rotation": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                    "tilt_rotation": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.1}),                    
                    "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),                    
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "rotate"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def rotate(self, image, rotation_type, current_frame, rotation_angle):
    
        if current_frame < start_frame:
            return (image,)

        if current_frame >= start_frame + frame_duration:
            return (image,)

        if rotation_type == "Tilt Up":
            rotation_angle = start_angle - (tilt_rotation * ((current_frame - start_frame) / frame_duration))
        elif rotation_type == "Tilt Down":
            rotation_angle = start_angle + (tilt_rotation * ((current_frame - start_frame) / frame_duration))
        elif rotation_type == "Pan Left":
            rotation_angle = start_angle - (pan_rotation * ((current_frame - start_frame) / frame_duration))
        elif rotation_type == "Pan Right":
            rotation_angle = start_angle + (pan_rotation * ((current_frame - start_frame) / frame_duration))
        else:
            rotation_angle = start_angle

        # Apply rotation to the image using your rotation logic here
        # You should apply the rotation angle to transform the image accordingly
        
        # image_out = apply_rotation(image, rotation_angle)  # Replace this with your actual rotation logic
        image_out = image
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
class CR_InterpolateTrack:
    @classmethod
    def INPUT_TYPES(s):
        track_types = ["Track Left", "Track Left", "Track Up", "Track Down"]
        
        return {"required": {
                    "image": ("IMAGE",),
                    "track_type": (track_types,),
                    "track_speed": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),                    
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "track"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def track(self, image, rotation_type, current_frame, rotation_angle):

        if current_frame < start_frame:
            return (image,)

        if current_frame >= start_frame + frame_duration:
            return (image,)

        if track_type == "Track Left":
            track_distance = track_speed * ((current_frame - start_frame) / frame_duration)
        elif track_type == "Track Right":
            track_distance = track_speed * ((current_frame - start_frame) / frame_duration)
        elif track_type == "Track Up":
            track_distance = track_speed * ((current_frame - start_frame) / frame_duration)
        elif track_type == "Track Down":
            track_distance = track_speed * ((current_frame - start_frame) / frame_duration)
        else:
            track_distance = 0.0

        # Apply tracking motion to the image using your tracking logic here
        # You should apply the track_distance to translate the image accordingly
        
        # image_out = apply_tracking(image, track_distance)  # Replace this with your actual tracking logic
        image_out = image
           
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_ContinuousZoom:
    @classmethod
    def INPUT_TYPES(s):
        zoom_types = ["Zoom In", "Zoom Out",]
        
        return {"required": {
                    "image": ("IMAGE",),
                    "zoom_type": (zoom_types,),
                    "zoom_factor": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "zoom"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def zoom(self, image, zoom_type, current_frame, zoom_factor):
        """
        Apply continuous zoom to the input image based on the zoom type and factor.

        Args:
            image (PIL.Image.Image): The input image.
            zoom_type (str): Either "Zoom In" or "Zoom Out" to specify the zoom direction.
            zoom_factor (float): The factor by which to zoom the image.

        Returns:
            PIL.Image.Image: The zoomed image.
        """    
        width, height = image.size

        if zoom_type == "Zoom In":
            new_width = int(width / zoom_factor)
            new_height = int(height / zoom_factor)
        else:
            new_width = int(width * zoom_factor)
            new_height = int(height * zoom_factor)

        # Perform image resizing using the specified resampling method (LANCZOS)
        image_out = image.resize((new_width, new_height), resample=Image.LANCZOS)
        
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_ContinuousRotation:
    @classmethod
    def INPUT_TYPES(s):
        rotation_types = ["Tilt Up", "Tilt Down", "Pan Left", "Pan Right"]
        return {"required": {
                    "image": ("IMAGE",),
                    "rotation_type": (rotation_types,),
                    "rotation_angle": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "get_image"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def get_image(self, image, rotation_type, current_frame, rotation_angle):
    
        """
        Apply continuous camera rotation to the input image.

        Args:
            image (PIL.Image.Image): The input image.
            rotation_type (str): One of "Tilt Up", "Tilt Down", "Pan Left", or "Pan Right" to specify the rotation type.
            rotation_angle (float): The angle by which to rotate the camera.

        Returns:
            PIL.Image.Image: The rotated image.
        """
        if rotation_type == "Tilt Up":
            rotated_image = image.rotate(-rotation_angle, resample=Image.LANCZOS, expand=True)
        elif rotation_type == "Tilt Down":
            rotated_image = image.rotate(rotation_angle, resample=Image.LANCZOS, expand=True)
        elif rotation_type == "Pan Left":
            rotated_image = image.rotate(rotation_angle, resample=Image.LANCZOS, expand=True)
        elif rotation_type == "Pan Right":
            rotated_image = image.rotate(-rotation_angle, resample=Image.LANCZOS, expand=True)
        else:
            rotated_image = image  # No rotation
            
        image_out = image    
            
        return (image_out,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_ContinuousTrack:
    @classmethod
    def INPUT_TYPES(s):
        track_types = ["Track Left", "Track Left", "Track Up", "Track Down"]
        return {"required": {
                    "image": ("IMAGE",),
                    "track_type": (track_types,),
                    "track_speed": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                    },
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "get_image"
    CATEGORY = icons.get("Comfyroll/Animation/Camera")

    def get_image(self, image, rotation_type, current_frame, rotation_angle):
        """
        Apply continuous tracking to the input image based on the tracking type and speed.

        Args:
            image (PIL.Image.Image): The input image.
            track_type (str): One of "Track Left", "Track Right", "Track Up", or "Track Down" to specify tracking direction.
            track_speed (float): The speed of the tracking operation.

        Returns:
            PIL.Image.Image: The tracked image.
        """
        # Placeholder for tracking logic based on the provided track_type and track_speed
        # Replace with actual tracking implementation
        
        # In this example, we're just returning the original image
        image_out = image  
        
        return (image_out,)
 
#---------------------------------------------------------------------------------------------------------------------#   
class CR_TextListCrossJoin:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "text_list_simple1": ("TEXT_LIST_SIMPLE", {"default": 1, "min": 0, "max": 10000}),
                    "text_list_simple2": ("TEXT_LIST_SIMPLE", {"default": 1, "min": 0, "max": 10000}),
                    }
        }

    RETURN_TYPES = ("TEXT_LIST_SIMPLE", )
    RETURN_NAMES = ("TEXT_LIST_SIMPLE", )
    FUNCTION = "cross_join"
    CATEGORY = icons.get("Comfyroll/Animation/List")
    
    def cross_join(self, current_frame, max_frames):

        lines = list()
    
        for line1 in list1:
            for line2 in list2:
                concat_line = line1 + ',' + line2
                lines.append(concat_line)
                
        list = list1
        return (lines, ) 

#---------------------------------------------------------------------------------------------------------------------#
# Load From List
#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadModelFromList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model_list": ("MODEL_LIST",),                          
                             "model_ID": ("STRING", {"default": "", "multiline": False}),
                },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    RETURN_NAMES = ("MODEL", "CLIP", "VAE")
    FUNCTION = "loadmodel"
    CATEGORY = icons.get("Comfyroll/Animation/List")

    def loadmodel(self, model_list, model_ID,):

        print(model_list)
        #get modelname from ID
        #try GPT for this
        model_name = "SD1_5\CounterfeitV25_25.safetensors"
        ckpt_path = folder_paths.get_full_path("checkpoints", model_name)
        out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, 
        embedding_directory=folder_paths.get_folder_paths("embeddings"))
        return out
        
#---------------------------------------------------------------------------------------------------------------------#  
class CR_LoadLoRAFromList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model": ("MODEL",),
                             "clip": ("CLIP",),
                             "lora_list": ("LORA_LIST",),
                             "lora_ID": ("STRING", {"default": "", "multiline": False}),
                },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", )
    RETURN_NAMES = ("MODEL", "CLIP", )
    FUNCTION = "loadlora"
    CATEGORY = icons.get("Comfyroll/Animation/List")

    def loadlora(self, model, clip, lora_ID, lora_list,):

        print(lora_list)
        #if lora_list == None:
 
        #pick lora by ID
        #load lora

        return (model, clip,)

#---------------------------------------------------------------------------------------------------------------------#  
class CR_LoadStyleFromList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"style_list": ("STYLE_LIST",),
                             "style_ID": ("STRING", {"default": "", "multiline": False}),
                },
        }
    
    RETURN_TYPES = ("STYLE", )
    RETURN_NAMES = ("STYLE", )
    FUNCTION = "loadstyle"
    CATEGORY = icons.get("Comfyroll/Animation/List")

    def loadstyle(self, style_ID, style_list,):

        print(style_list)
        #if style_list == None:
 
        #pick style by ID
        #load style

        return (style_ID,)
              
#--------------------------------------------------------------------------------------------------------------------#  
class CR_StyleList:

    @classmethod
    def INPUT_TYPES(cls):

        #current_directory = os.path.dirname(os.path.realpath(__file__))
        #self.json_data, style_files = load_styles_from_directory(current_directory)
        
        style_files = ["None"] + folder_paths.get_filename_list("loras")
    
        return {"required": {
                    "style_name1": (style_files,),
                    "alias1": ("STRING", {"multiline": False, "default": ""}),
                    "style_name2": (style_files,),
                    "alias2": ("STRING", {"multiline": False, "default": ""}),
                    "style_name3": (style_files,),
                    "alias3": ("STRING", {"multiline": False, "default": ""}),
                    "style_name4": (style_files,),
                    "alias4": ("STRING", {"multiline": False, "default": ""}),                    
                    "style_name5": (style_files,),
                    "alias5": ("STRING", {"multiline": False, "default": ""}),                    
                },
                "optional": {"style_list": ("style_LIST",)
                },
        }

    RETURN_TYPES = ("STYLE_LIST", "STRING", )
    RETURN_NAMES = ("STYLE_LIST", "show_text", )
    FUNCTION = "style_list"
    CATEGORY = icons.get("Comfyroll/Animation/List")

    def style_list(self, style_name1, alias1, style_name2, alias2, style_name3, alias3, style_name4, alias4, 
        style_name5, alias5, style_list=None):

        # Initialise the list
        styles = list()
        
        # Extend the list for each style in the stack
        if style_list is not None:
            styles.extend([l for l in style_list])
        
        if style_name1 != "None":
            styles.extend([(alias1 + "," + style_name1 + "\n")]),

        if style_name2 != "None":
            styles.extend([(alias2 + "," + style_name2 + "\n")]),

        if style_name3 != "None":
            styles.extend([(alias3 + "," + style_name3 + "\n")]),

        if style_name4 != "None":
            styles.extend([(alias4 + "," + style_name4 + "\n")]),
            
        if style_name5 != "None":
            styles.extend([(alias5 + "," + style_name5 + "\n")]),
            
        #print(f"[TEST] CR style List: {styles}")

        show_text = "".join(styles)
            
        return (styles, show_text, )            

#---------------------------------------------------------------------------------------------------------------------#
class CR_CycleStyles:

    @classmethod
    def INPUT_TYPES(s):
    
        cycle_methods = ["Sequential", "Random"]
    
        return {"required": {"switch": ([
                                "Off",
                                "On"],),
                             "style_list": ("STYLE_LIST",),
                             "frame_interval": ("INT", {"default": 30, "min": 0, "max": 999, "step": 1,}),         
                             "loops": ("INT", {"default": 1, "min": 1, "max": 1000}),
                             "cycle_method": (cycle_methods,),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("STYLE", )
    FUNCTION = "cycle"
    CATEGORY = icons.get("Comfyroll/Animation/Other")

    def cycle(self, switch, style_list, frame_interval, loops, cycle_method, current_frame,):
    
        if switch == "Off":
            return (None, )

        print(style_list)
        #loop through style names
        
        style_ID = 1

        return (style_ID, ) 
  
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
    #
    "CR Interpolate Prompt Weights":CR_InterpolatePromptWeights,
    "CR Alternate Latents":CR_AlternateLatents,
    "CR Image Transition":CR_ImageTransition,      
    "CR Strobe Images": CR_StrobeImages,
    #
    "CR 3D Camera Drone":CR_DroneCamera3D,
    "CR 3D Camera Static":CR_StaticCamera3D, 
    "CR Interpolate Zoom":CR_InterpolateZoom,
    "CR Interpolate Rotation":CR_InterpolateRotation,
    "CR Interpolate Track":CR_InterpolateTrack,
    "CR Continuous Zoom":CR_ContinuousZoom,
    "CR Continuous Rotation":CR_ContinuousRotation,
    "CR Continuous Track":CR_ContinuousTrack,
    #
    "CR Text List Cross Join":CR_TextListCrossJoin,
    "CR Style List":CR_StyleList, 
    #
    "CR Load Model From List":CR_LoadModelFromList,
    "CR Load LoRA From List":CR_LoadLoRAFromList,
    "CR Load Style From List":CR_LoadStyleFromList,
    "CR Load Image From List":CR_LoadImageFromList,
    "CR Load Text From List":CR_LoadTextFromList, 
    #
    "CR Cycle Styles":CR_CycleStyles, 
}
'''

