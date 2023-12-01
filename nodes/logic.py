#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi         https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes
# for ComfyUI                                               https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
# Logic Switches
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "image1": ("IMAGE",),
                "image2": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, image1, image2):
        if Input == 1:
            return (image1, )
        else:
            return (image2, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LatentInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "latent1": ("LATENT",),
                "latent2": ("LATENT",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, latent1, latent2):
        if Input == 1:
            return (latent1, )
        else:
            return (latent2, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ConditioningInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "conditioning1": ("CONDITIONING",),
                "conditioning2": ("CONDITIONING",)
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, conditioning1, conditioning2):
        if Input == 1:
            return (conditioning1, )
        else:
            return (conditioning2, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ClipInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "clip1": ("CLIP",),
                "clip2": ("CLIP",)
            }
        }

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, clip1, clip2):
        if Input == 1:
            return (clip1, )
        else:
            return (clip2, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ModelInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "model1": ("MODEL",),
                "model2": ("MODEL",)
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, model1, model2):
        if Input == 1:
            return (model1, )
        else:
            return (model2, )

#---------------------------------------------------------------------------------------------------------------------#
#This is an input switch for controlNet.  Can pick an input and that image will be the one picked for the workflow.
class CR_ControlNetInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "control_net1": ("CONTROL_NET",),
                "control_net2": ("CONTROL_NET",)
            }
        }
        
    RETURN_TYPES = ("CONTROL_NET",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, control_net1, control_net2):
        if Input == 1:
            return (control_net1, )
        else:
            return (control_net2, )

#---------------------------------------------------------------------------------------------------------------------#
#This is an input switch for text.  Can pick an input and that image will be the one picked for the workflow.
class CR_TextInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),            
                "text1": ("STRING", {"forceInput": True}),
                "text2": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, text1, text2,):

        if Input == 1:
            return (text1, )
        else:
            return (text2, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_VAEInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),            
                "VAE1": ("VAE", {"forceInput": True}),
                "VAE2": ("VAE", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("VAE",)   
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, VAE1, VAE2,):

        if Input == 1:
            return (VAE1, )
        else:
            return (VAE2, )
            
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageInputSwitch4way:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 4}),
                "image1": ("IMAGE",),
            },
            "optional": {
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, image1, image2=None, image3=None, image4=None):
        if Input == 1:
            return (image1, )
        elif Input == 2:
            return (image2, )
        elif Input == 3:
            return (image3, )
        else:
            return (image4, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextInputSwitch4way:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 4}),            
                "text1": ("STRING", {"forceInput": True}),               
            },
            "optional": {
                "text2": ("STRING", {"forceInput": True}),
                "text3": ("STRING", {"forceInput": True}),
                "text4": ("STRING", {"forceInput": True}),   
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, text1, text2=None, text3=None, text4=None):

        if Input == 1:
            return (text1, )
        elif Input == 2:
            return (text2, )
        elif Input == 3:
            return (text3, )
        else:
            return (text4, )            

#---------------------------------------------------------------------------------------------------------------------#
class CR_ModelAndCLIPInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "model1": ("MODEL",),
                "clip1": ("CLIP",),                
                "model2": ("MODEL",),               
                "clip2": ("CLIP",)
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, clip1, clip2, model1, model2):
        if Input == 1:
            return (model1, clip1, )
        else:
            return (model2, clip2, )

#---------------------------------------------------------------------------------------------------------------------#
# Process switches
#---------------------------------------------------------------------------------------------------------------------#
class CR_Img2ImgProcessSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["txt2img", "img2img"],),
                "txt2img": ("LATENT",),
                "img2img": ("LATENT",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Process")

    def switch(self, Input, txt2img, img2img):
        if Input == "txt2img":
            return (txt2img, )
        else:
            return (img2img, )            

#---------------------------------------------------------------------------------------------------------------------#
class CR_HiResFixProcessSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["latent_upscale", "image_upscale"],),
                "latent_upscale": ("LATENT",),
                "image_upscale": ("LATENT",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Process")

    def switch(self, Input, latent_upscale, image_upscale):
        if Input == "latent_upscale":
            return (latent_upscale, )
        else:
            return (image_upscale, )  

#---------------------------------------------------------------------------------------------------------------------#
class CR_BatchProcessSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["image", "image batch"],),
                "image": ("IMAGE", ),
                "image_batch": ("IMAGE", )
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Process")

    def switch(self, Input, image, image_batch):
        if Input == "image":
            return (image, )
        else:
            return (image_batch, ) 
            
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = { 
    # Logic switches        
    "CR Image Input Switch": CR_ImageInputSwitch,
    "CR Latent Input Switch": CR_LatentInputSwitch,
    "CR Conditioning Input Switch": CR_ConditioningInputSwitch,
    "CR Clip Input Switch": CR_ClipInputSwitch,
    "CR Model Input Switch": CR_ModelInputSwitch,
    "CR ControlNet Input Switch": CR_ControlNetInputSwitch,
    "CR Text Input Switch": CR_TextInputSwitch,
    "CR VAE Input Switch": CR_VAEInputSwitch,
    "CR Switch Model and CLIP":CR_ModelAndCLIPInputSwitch,
    # 4-way switches
    "CR Image Input Switch (4 way)": CR_InputImages4way, 
    "CR Text Input Switch (4 way)": CR_TextInputSwitch4way,    
    # Process switches
    "CR Img2Img Process Switch": CR_Img2ImgProcessSwitch:,
    "CR Hires Fix Process Switch": CR_HiResFixProcessSwitch,
    "CR Batch Process Switch": CR_BatchProcessSwitch,   
}
'''    

    
