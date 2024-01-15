#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi   https://github.com/Suzie1/CR-Animation-Nodes              
# for ComfyUI                                     https://github.com/comfyanonymous/ComfyUI 
#---------------------------------------------------------------------------------------------------------------------#

import torch
from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
# NODES
#---------------------------------------------------------------------------------------------------------------------#
class CR_GradientInteger:

    @classmethod
    def INPUT_TYPES(s):
        gradient_profiles = ["Lerp"]
       
        return {"required": {"start_value": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "end_value": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "gradient_profile": (gradient_profiles,) 
                },
        }
    
    RETURN_TYPES = ("INT", "STRING", )
    RETURN_NAMES = ("INT", "show_help", )
    FUNCTION = "gradient"
    CATEGORY = icons.get("Comfyroll/Animation/Interpolate")

    def gradient(self, start_value, end_value, start_frame, frame_duration, current_frame, gradient_profile):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Interpolation-Nodes#cr-gradient-integer"

        if current_frame < start_frame:
            return (start_value, show_help, )

        if current_frame > start_frame + frame_duration:
            return (end_value, show_help, )
            
        step = (end_value - start_value) / frame_duration
        
        current_step = current_frame - start_frame
        
        int_out = start_value + int(current_step * step)
        
        return (int_out, show_help, )
    
#---------------------------------------------------------------------------------------------------------------------#
class CR_GradientFloat:

    @classmethod
    def INPUT_TYPES(s):
        gradient_profiles = ["Lerp"]    
    
        return {"required": {"start_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.01,}),
                             "end_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.01,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "gradient_profile": (gradient_profiles,)                              
                },
        }
    
    RETURN_TYPES = ("FLOAT", "STRING", )
    RETURN_NAMES = ("FLOAT", "show_help", )    
    FUNCTION = "gradient"
    CATEGORY = icons.get("Comfyroll/Animation/Interpolate")

    def gradient(self, start_value, end_value, start_frame, frame_duration, current_frame, gradient_profile):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Interpolation-Nodes#cr-gradient-float"

        if current_frame < start_frame:
            return (start_value, show_help, )

        if current_frame > start_frame + frame_duration:
            return (end_value, show_help, )
            
        step = (end_value - start_value) / frame_duration
        
        current_step = current_frame - start_frame        
        
        float_out = start_value + current_step * step
        
        return (float_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_IncrementFloat:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {"start_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.001,}),
                             "step": ("FLOAT", {"default": 0.1, "min": -9999.0, "max": 9999.0, "step": 0.001,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.00,}),
                             "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("FLOAT", "STRING", )
    RETURN_NAMES = ("FLOAT", "show_help", )
    OUTPUT_NODE = True    
    FUNCTION = "increment"
    CATEGORY = icons.get("Comfyroll/Animation/Interpolate")

    def increment(self, start_value, step, start_frame, frame_duration, current_frame):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Interpolation-Nodes#cr-increment-float"

        #print(f"current frame {current_frame}")
        if current_frame < start_frame:
            return (start_value, show_help, )
  
        current_value = start_value + (current_frame - start_frame) * step
        if current_frame <= start_frame + frame_duration:
            current_value += step
            #print(f"<current value {current_value}")    
            return (current_value, show_help, )
                
        return (current_value, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_IncrementInteger:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {"start_value": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "step": ("INT", {"default": 1.0, "min": -9999.0, "max": 9999.0, "step": 1.0,}),
                             "start_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "frame_duration": ("INT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "current_frame": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                },
        }
    
    RETURN_TYPES = ("INT", "STRING", )
    RETURN_NAMES = ("INT", "show_help", )
    OUTPUT_NODE = True    
    FUNCTION = "increment"
    CATEGORY = icons.get("Comfyroll/Animation/Interpolate")

    def increment(self, start_value, step, start_frame, frame_duration, current_frame):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Interpolation-Nodes#cr-increment-integer"

        #print(f"current frame {current_frame}")
        if current_frame < start_frame:
            return (start_value, show_help, )
  
        current_value = start_value + (current_frame - start_frame) * step
        if current_frame <= start_frame + frame_duration:
            current_value += step
            #print(f"<current value {current_value}")    
            return (current_value, show_help, )
                
        return (current_value, show_help, )
         
#---------------------------------------------------------------------------------------------------------------------#
class CR_InterpolateLatents:

    @classmethod
    def INPUT_TYPES(cls):
    
        #interpolation_methods = ["lerp", "slerp"]
        interpolation_methods = ["lerp"]
        
        return {
            "required": {
                "latent1": ("LATENT",),
                "latent2": ("LATENT",),
                "weight": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "method": (interpolation_methods,),
            }
        }

    RETURN_TYPES = ("LATENT", "STRING", )
    RETURN_NAMES = ("LATENT", "show_help", )
    FUNCTION = "interpolate"
    CATEGORY = icons.get("Comfyroll/Animation/Interpolate")

    def interpolate(self, latent1, latent2, weight, method):
        a = latent1.copy()
        b = latent2.copy()
        c = {}
        
        if method == "lerp":
        
            torch.lerp(a["samples"], b["samples"], weight, out=a["samples"])
            
        elif method == "slerp":
            
            dot_products = torch.sum(latent1["samples"] * latent2["samples"], dim=(2, 3))
            dot_products = torch.clamp(dot_products, -1, 1)  # Ensure dot products are within valid range

            angles = torch.acos(dot_products)
            sin_angles = torch.sin(angles)

            weight1 = torch.sin((1 - weight) * angles) / sin_angles
            weight2 = torch.sin(weight * angles) / sin_angles

            # Broadcast weights to match latent samples dimensions
            weight1 = weight1.unsqueeze(-1).unsqueeze(-1)
            weight2 = weight2.unsqueeze(-1).unsqueeze(-1)

            interpolated_samples = weight1 * latent1["samples"] + weight2 * latent2["samples"]
            a["samples"] = interpolated_samples
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Interpolation-Nodes#cr-interpolate-latents"

        return (a, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
    # Interpolate Anything
    "CR Gradient Float":CR_GradientFloat,
    "CR Gradient Integer":CR_GradientInteger,
    "CR Increment Float":CR_IncrementFloat,        
    "CR Increment Integer":CR_IncrementInteger,
    # Latent
    "CR Interpolate Latents":CR_InterpolateLatents,
}
'''

