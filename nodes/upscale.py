#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Nodes by RockOfFire and Akatsuzi      https://github.com/RockOfFire/CR-Animation-Nodes
# for ComfyUI                                     https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import folder_paths
from PIL import Image

from .upscale_functions import load_model, upscale_with_model, apply_resize_image

#MAX_RESOLUTION=8192

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

#---------------------------------------------------------------------------------------------------------------------
# NODES
#---------------------------------------------------------------------------------------------------------------------
# These nodes are based on WAS nodes Image Resize and the Comfy Extras upscale with model nodes
#---------------------------------------------------------------------------------------------------------------------
class CR_UpscaleImage:

    @classmethod
    def INPUT_TYPES(s):

        resampling_methods = ["lanczos", "nearest", "bilinear", "bicubic"]
       
        return {"required":
                    {"image": ("IMAGE",),
                     "upscale_model": (folder_paths.get_filename_list("upscale_models"), ),
                     "mode": (["rescale", "resize"],),
                     "rescale_factor": ("FLOAT", {"default": 2, "min": 0.01, "max": 16.0, "step": 0.01}),
                     "resize_width": ("INT", {"default": 1024, "min": 1, "max": 48000, "step": 1}),
                     "resampling_method": (resampling_methods,),                     
                     "supersample": (["true", "false"],),   
                     "rounding_modulus": ("INT", {"default": 8, "min": 8, "max": 1024, "step": 8}),
                     }
                }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "upscale"
    CATEGORY = "Comfyroll/Upscale"
    
    def upscale(self, image, upscale_model, rounding_modulus=8, loops=1, mode="rescale", supersample='true', resampling_method="lanczos", rescale_factor=2, resize_width=1024):

        pil_img = tensor2pil(image)
        original_width, original_height = pil_img.size
        
        # Load upscale model 
        up_model = load_model(upscale_model)

        # Upscale with model
        up_image = upscale_with_model(up_model, image)            
        
        # Get new size
        pil_img = tensor2pil(up_image)
        upscaled_width, upscaled_height = pil_img.size

        # Return if no rescale needed
        if upscaled_width == original_width and rescale_factor == 1:
            return (up_image, )
              
        # Image resize
        scaled_images = []
        
        for img in up_image:
            scaled_images.append(pil2tensor(apply_resize_image(tensor2pil(img), original_width, original_height, rounding_modulus, mode, supersample, rescale_factor, resize_width, resampling_method)))
        images_out = torch.cat(scaled_images, dim=0)
            
        return (images_out, )
 
#---------------------------------------------------------------------------------------------------------------------
class CR_MultiUpscaleStack:

    @classmethod
    def INPUT_TYPES(s):
    
        mix_methods = ["Combine", "Average", "Concatenate"]
        up_models = ["None"] + folder_paths.get_filename_list("upscale_models")
        
        return {"required":
                    {
                     "switch_1": (["On","Off"],),              
                     "upscale_model_1": (up_models, ),
                     "rescale_factor_1": ("FLOAT", {"default": 2, "min": 0.01, "max": 16.0, "step": 0.01}),
                     "switch_2": (["On","Off"],),                          
                     "upscale_model_2": (up_models, ),
                     "rescale_factor_2": ("FLOAT", {"default": 2, "min": 0.01, "max": 16.0, "step": 0.01}),
                     "switch_3": (["On","Off"],),                        
                     "upscale_model_3": (up_models, ),
                     "rescale_factor_3": ("FLOAT", {"default": 2, "min": 0.01, "max": 16.0, "step": 0.01}),
                     },
                "optional": {"upscale_stack": ("UPSCALE_STACK",),
                }
        }

    RETURN_TYPES = ("UPSCALE_STACK", )
    FUNCTION = "stack"
    CATEGORY = "Comfyroll/Upscale"
    
    def stack(self, switch_1, upscale_model_1, rescale_factor_1, switch_2, upscale_model_2, rescale_factor_2, switch_3, upscale_model_3, rescale_factor_3, upscale_stack=None):
    
        # Initialise the list
        upscale_list=list()
        
        if upscale_stack is not None:
            upscale_list.extend([l for l in upscale_stack if l[0] != "None"])
        
        if upscale_model_1 != "None" and  switch_1 == "On":
            upscale_list.extend([(upscale_model_1, rescale_factor_1)]),

        if upscale_model_2 != "None" and  switch_2 == "On":
            upscale_list.extend([(upscale_model_2, rescale_factor_2)]),

        if upscale_model_3 != "None" and  switch_3 == "On":
            upscale_list.extend([(upscale_model_3, rescale_factor_3)]),

        return (upscale_list,)

#---------------------------------------------------------------------------------------------------------------------
class CR_ApplyMultiUpscale:

    @classmethod
    def INPUT_TYPES(s):
    
        resampling_methods = ["lanczos", "nearest", "bilinear", "bicubic"]
        
        return {"required": {"image": ("IMAGE",),
                             "resampling_method": (resampling_methods,),
                             "supersample": (["true", "false"],),                     
                             "rounding_modulus": ("INT", {"default": 8, "min": 8, "max": 1024, "step": 8}),                   
                             "upscale_stack": ("UPSCALE_STACK",),
                            }
        }
    
    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "image"
    FUNCTION = "apply"

    CATEGORY = "Comfyroll/Upscale"

    def apply(self, image, resampling_method, supersample, rounding_modulus, upscale_stack):

        # Get original size
        pil_img = tensor2pil(image)
        original_width, original_height = pil_img.size
    
        # Extend params with upscale-stack items 
        params = list()
        params.extend(upscale_stack)

        # Loop through the list
        for tup in params:
            upscale_model, rescale_factor = tup
            print(f"[Info] CR Apply Multi Upscale: Applying {upscale_model} and rescaling by factor {rescale_factor}")
            # Load upscale model 
            up_model = load_model(upscale_model)

            # Upscale with model
            up_image = upscale_with_model(up_model, image)

            # Get new size
            pil_img = tensor2pil(up_image)
            upscaled_width, upscaled_height = pil_img.size

            # Return if no rescale needed
            if upscaled_width == original_width and rescale_factor == 1:
                image = up_image           
            else:      
                # Image resize
                scaled_images = []
                mode = "rescale"
                resize_width = 1024 
                
                for img in up_image:
                    scaled_images.append(pil2tensor(apply_resize_image(tensor2pil(img), original_width, original_height, rounding_modulus, mode, supersample, rescale_factor, resize_width, resampling_method)))
                image = torch.cat(scaled_images, dim=0)
            
        return (image, )
   
#---------------------------------------------------------------------------------------------------------------------
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 0 nodes released
'''
NODE_CLASS_MAPPINGS = {
    # Conditioning
    "CR Multi Upscale Stack":CR_MultiUpscaleStack,
    "CR Upscale Image":CR_UpscaleImage,
    "CR Apply Multi Upscale":CR_ApplyMultiUpscale,
}
'''

    
     
