#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
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
            },
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),            
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, image1=None, image2=None):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-image-input-switch"
        
        if Input == 1:
            return (image1, show_help, )
        else:
            return (image2, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LatentInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
            },
            "optional": {
                "latent1": ("LATENT",),
                "latent2": ("LATENT",)          
            }
        }

    RETURN_TYPES = ("LATENT", "STRING", )
    RETURN_NAMES = ("LATENT", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, latent1=None, latent2=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-latent-input-switch"
        if Input == 1:
            return (latent1, show_help, )
        else:
            return (latent2, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ConditioningInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
            },
            "optional": {
                "conditioning1": ("CONDITIONING",),
                "conditioning2": ("CONDITIONING",),        
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING", )
    RETURN_NAMES = ("CONDITIONING", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, conditioning1=None, conditioning2=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-conditioning-input-switch"
        if Input == 1:
            return (conditioning1, show_help, )
        else:
            return (conditioning2, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ClipInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
            },
            "optional": {
                "clip1": ("CLIP",),
                "clip2": ("CLIP",),      
            }
        }

    RETURN_TYPES = ("CLIP", "STRING", )
    RETURN_NAMES = ("CLIP", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, clip1=None, clip2=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-clip-input-switch"
        if Input == 1:
            return (clip1, show_help, )
        else:
            return (clip2, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ModelInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
            },
            "optional": {
                "model1": ("MODEL",),
                "model2": ("MODEL",),   
            }
        }

    RETURN_TYPES = ("MODEL", "STRING", )
    RETURN_NAMES = ("MODEL", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, model1=None, model2=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-model-input-switch"
        if Input == 1:
            return (model1, show_help, )
        else:
            return (model2, show_help, )

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
            },
            "optional": {
                "control_net1": ("CONTROL_NET",),
                "control_net2": ("CONTROL_NET",),   
            }
        }
        
    RETURN_TYPES = ("CONTROL_NET", "STRING", )
    RETURN_NAMES = ("CONTROL_NET", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, control_net1=None, control_net2=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-controlnet-input-switch"
        if Input == 1:
            return (control_net1, show_help, )
        else:
            return (control_net2, show_help, )

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
            },
            "optional": {
                "text1": ("STRING", {"forceInput": True}),
                "text2": ("STRING", {"forceInput": True}), 
            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, text1=None, text2=None,):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-text-input-switch"
        if Input == 1:
            return (text1, show_help, )
        else:
            return (text2, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_VAEInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),            
            },
            "optional": {
                "VAE1": ("VAE", {"forceInput": True}),
                "VAE2": ("VAE", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("VAE", "STRING", )   
    RETURN_NAMES = ("VAE", "show_help", ) 
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, VAE1=None, VAE2=None,):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-vae-input-switch"
        if Input == 1:
            return (VAE1, show_help, )
        else:
            return (VAE2, show_help, )
            
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageInputSwitch4way:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 4}),
            },
            "optional": {
                "image1": ("IMAGE",),            
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, image1=None, image2=None, image3=None, image4=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-text-input-switch-4-way"
        if Input == 1:
            return (image1, show_help, )
        elif Input == 2:
            return (image2, show_help, )
        elif Input == 3:
            return (image3, show_help, )
        else:
            return (image4, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextInputSwitch4way:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 4}),
            },
            "optional": {
                "text1": ("STRING", {"forceInput": True}),
                "text2": ("STRING", {"forceInput": True}),
                "text3": ("STRING", {"forceInput": True}),
                "text4": ("STRING", {"forceInput": True}),  
            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, text1=None, text2=None, text3=None, text4=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-text-input-switch-4-way"
        if Input == 1:
            return (text1, show_help, )
        elif Input == 2:
            return (text2, show_help, )
        elif Input == 3:
            return (text3, show_help, )
        else:
            return (text4, show_help, )            

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

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Logic")

    def switch(self, Input, clip1, clip2, model1, model2):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Logic-Nodes#cr-switch-model-and-clip"
        if Input == 1:
            return (model1, clip1, show_help, )
        else:
            return (model2, clip2, show_help, )

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
            },
            "optional": {
                "txt2img": ("LATENT",),
                "img2img": ("LATENT",),
            }
        }

    RETURN_TYPES = ("LATENT", "STRING", )
    RETURN_NAMES = ("LATENT", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Process")

    def switch(self, Input, txt2img=None, img2img=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Process-Nodes#cr-img2img-process-switch"
        if Input == "txt2img":
            return (txt2img, show_help, )
        else:
            return (img2img, show_help, )            

#---------------------------------------------------------------------------------------------------------------------#
class CR_HiResFixProcessSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["latent_upscale", "image_upscale"],),
            },
            "optional": {
                "latent_upscale": ("LATENT",),
                "image_upscale": ("LATENT",),
            }
        }

    RETURN_TYPES = ("LATENT", "STRING", )
    RETURN_NAMES = ("LATENT", "STRING", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Process")

    def switch(self, Input, latent_upscale=None, image_upscale=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Process-Nodes#cr-hires-fix-process-switch"
        if Input == "latent_upscale":
            return (latent_upscale, show_help, )
        else:
            return (image_upscale, show_help, )  

#---------------------------------------------------------------------------------------------------------------------#
class CR_BatchProcessSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": (["image", "image batch"],),
            },
            "optional": {
                "image": ("IMAGE", ),
                "image_batch": ("IMAGE", )
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "switch"
    CATEGORY = icons.get("Comfyroll/Utils/Process")

    def switch(self, Input, image=None, image_batch=None):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Process-Nodes#cr-batch-process-switch"
        if Input == "image":
            return (image, show_help, )
        else:
            return (image_batch, show_help, ) 
            
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

    
