#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#
# based on Tiny Terra nodes

from ..categories import icons

class AnyType(str):
    # Credit to pythongosssss    

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

#---------------------------------------------------------------------------------------------------------------------#
# MODULE NODES
#---------------------------------------------------------------------------------------------------------------------#
class CR_DataBusIn:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            },
            "optional": {
                "pipe": (any_type,),
                "any1": (any_type,),
                "any2": (any_type,),
                "any3": (any_type,),
                "any4": (any_type,),          
            },
        }

    RETURN_TYPES = ("PIPE_LINE", "STRING", )
    RETURN_NAMES = ("pipe", "show_help", )
    FUNCTION = "load_data"
    CATEGORY = icons.get("Comfyroll/Pipe/Bus")

    def load_data(self, any1=None, any2=None, any3=None, any4=None, pipe=None):
 
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-data-bus-in"

        # Initialize with default values
        new_any1, new_any2, new_any3, new_any4 = None, None, None, None
     
        if pipe is not None:
            new_any1, new_any2, new_any3, new_any4 = pipe

        new_any1 = any1 if any1 is not None else new_any1
        new_any2 = any2 if any2 is not None else new_any2
        new_any3 = any3 if any3 is not None else new_any3
        new_any4 = any4 if any4 is not None else new_any4

        new_pipe = new_any1, new_any2, new_any3, new_any4
              
        return (new_pipe, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_DataBusOut:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pipe": ("PIPE_LINE",)
            }
        }

    RETURN_TYPES = ("PIPE_LINE", any_type, any_type, any_type, any_type, "STRING", )
    RETURN_NAMES = ("pipe", "any1", "any2", "any3", "any4", "show_help", )
    FUNCTION = "data_out"
    CATEGORY = icons.get("Comfyroll/Pipe/Bus")

    def data_out(self, any1=None, any2=None, any3=None, any4=None, pipe=None):
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-data-bus-out"
            
        new_any1, new_any2, new_any3, new_any4 = pipe
        
        return (pipe, new_any1, new_any2, new_any3, new_any4, show_help, )

#---------------------------------------------------------------------------------------------------------------------#        
class CR_8ChannelIn:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            },
            "optional": {
                "pipe": (any_type,),
                "ch1": (any_type,),
                "ch2": (any_type,),
                "ch3": (any_type,),
                "ch4": (any_type,),
                "ch5": (any_type,),
                "ch6": (any_type,),
                "ch7": (any_type,),
                "ch8": (any_type,),                 
            },
        }

    RETURN_TYPES = ("PIPE_LINE", "STRING", )
    RETURN_NAMES = ("pipe", "show_help", )
    FUNCTION = "load_data"
    CATEGORY = icons.get("Comfyroll/Pipe/Bus")

    def load_data(self, ch1=None, ch2=None, ch3=None, ch4=None, ch5=None, ch6=None, ch7=None, ch8=None, pipe=None):
 
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-8-channel-in"

        # Initialize with default values
        new_ch1, new_ch2, new_ch3, new_ch4, new_ch5, new_ch6, new_ch7, new_ch8 = None, None, None, None, None, None, None, None
     
        if pipe is not None:
            new_ch1, new_ch2, new_ch3, new_ch4, new_ch5, new_ch6, new_ch7, new_ch8 = pipe

        new_ch1 = ch1 if ch1 is not None else new_ch1
        new_ch2 = ch2 if ch2 is not None else new_ch2
        new_ch3 = ch3 if ch3 is not None else new_ch3
        new_ch4 = ch4 if ch4 is not None else new_ch4
        new_ch5 = ch5 if ch5 is not None else new_ch5
        new_ch6 = ch6 if ch6 is not None else new_ch6
        new_ch7 = ch7 if ch7 is not None else new_ch7
        new_ch8 = ch8 if ch8 is not None else new_ch8        

        new_pipe = new_ch1, new_ch2, new_ch3, new_ch4, new_ch5, new_ch6, new_ch7, new_ch8
              
        return (new_pipe, show_help, )      

#---------------------------------------------------------------------------------------------------------------------#
class CR_8ChannelOut:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pipe": ("PIPE_LINE",)
            }
        }

    RETURN_TYPES = ("PIPE_LINE", any_type, any_type, any_type, any_type, any_type, any_type, any_type, any_type, "STRING", )
    RETURN_NAMES = ("pipe", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "show_help", )
    FUNCTION = "data_out"
    CATEGORY = icons.get("Comfyroll/Pipe/Bus")

    def data_out(self, ch1=None, ch2=None, ch3=None, ch4=None, ch5=None, ch6=None, ch7=None, ch8=None, pipe=None):
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-8-channel-out"
            
        new_ch1, new_ch2, new_ch3, new_ch4, new_ch5, new_ch6, new_ch7, new_ch8 = pipe
        
        return (pipe, new_ch1, new_ch2, new_ch3, new_ch4, new_ch5, new_ch6, new_ch7, new_ch8, show_help, ) 
        
#---------------------------------------------------------------------------------------------------------------------#
class CR_ModulePipeLoader:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            },
            "optional": {
                "model": ("MODEL",),
                "pos": ("CONDITIONING",),
                "neg": ("CONDITIONING",),
                "latent": ("LATENT",),
                "vae": ("VAE",),
                "clip": ("CLIP",),
                "controlnet": ("CONTROL_NET",),
                "image": ("IMAGE",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})            
            },
        }

    RETURN_TYPES = ("PIPE_LINE", "STRING", )
    RETURN_NAMES = ("pipe", "show_help", )
    FUNCTION = "pipe_input"
    CATEGORY = icons.get("Comfyroll/Pipe/Module")

    def pipe_input(self, model=0, pos=0, neg=0, latent=0, vae=0, clip=0, controlnet=0, image=0, seed=0):
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-module-pipe-loader"   
        
        pipe_line = (model, pos, neg, latent, vae, clip, controlnet, image, seed)

        return (pipe_line, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
class CR_ModuleInput:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"pipe": ("PIPE_LINE",)},
            }

    RETURN_TYPES = ("PIPE_LINE", "MODEL", "CONDITIONING", "CONDITIONING", "LATENT", "VAE", "CLIP", "CONTROL_NET", "IMAGE", "INT", "STRING", )
    RETURN_NAMES = ("pipe", "model", "pos", "neg", "latent", "vae", "clip", "controlnet", "image", "seed", "show_help", )
    FUNCTION = "flush"
    CATEGORY = icons.get("Comfyroll/Pipe/Module")
    
    def flush(self, pipe):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-module-input"

        model, pos, neg, latent, vae, clip, controlnet, image, seed = pipe
        
        return (pipe, model, pos, neg, latent, vae, clip, controlnet, image, seed, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ModuleOutput:
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"pipe": ("PIPE_LINE",)},
                "optional": {
                    "model": ("MODEL",),
                    "pos": ("CONDITIONING",),
                    "neg": ("CONDITIONING",),
                    "latent": ("LATENT",),
                    "vae": ("VAE",),
                    "clip": ("CLIP",),
                    "controlnet": ("CONTROL_NET",),
                    "image": ("IMAGE",),
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
                },
            }

    RETURN_TYPES = ("PIPE_LINE", "STRING", )
    RETURN_NAMES = ("pipe", "show_help", )
    FUNCTION = "pipe_output"
    CATEGORY = icons.get("Comfyroll/Pipe/Module")

    def pipe_output(self, pipe, model=None, pos=None, neg=None, latent=None, vae=None, clip=None, controlnet=None, image=None, seed=None):
       
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-module-output"   
    
        new_model, new_pos, new_neg, new_latent, new_vae, new_clip, new_controlnet, new_image, new_seed = pipe

        if model is not None:
            new_model = model
        
        if pos is not None:
            new_pos = pos

        if neg is not None:
            new_neg = neg

        if latent is not None:
            new_latent = latent

        if vae is not None:
            new_vae = vae

        if clip is not None:
            new_clip = clip
            
        if controlnet is not None:
            new_controlnet = controlnet
            
        if image is not None:
            new_image = image
            
        if seed is not None:
            new_seed = seed
       
        pipe = new_model, new_pos, new_neg, new_latent, new_vae, new_clip, new_controlnet, new_image, new_seed
       
        return (pipe, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
# PIPE NODES
#---------------------------------------------------------------------------------------------------------------------#
class CR_ImagePipeIn:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            },
            "optional": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000})
            },
        }

    RETURN_TYPES = ("PIPE_LINE", "STRING", )
    RETURN_NAMES = ("pipe", "show_help", )
    FUNCTION = "pipe_in"
    CATEGORY = icons.get("Comfyroll/Pipe/Image")

    def pipe_in(self, image=0, width=0, height=0, upscale_factor=0):
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-image-pipe-in"
        
        pipe_line = (image, width, height, upscale_factor)

        return (pipe_line, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ImagePipeEdit:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"pipe": ("PIPE_LINE",)
            },
            "optional": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 64, "max": 2048, "forceInput": True}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048, "forceInput": True}),
                "upscale_factor": ("FLOAT", {"default": 1, "min": 1, "max": 2000, "forceInput": True}),
            },
        }

    RETURN_TYPES = ("PIPE_LINE", "STRING", )
    RETURN_NAMES = ("pipe", "show_help", )
    FUNCTION = "pipe_edit"
    CATEGORY = icons.get("Comfyroll/Pipe/Image")

    def pipe_edit(self, pipe, image=None, width=None, height=None, upscale_factor=None):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-image-pipe-edit"
            
        new_image, new_width, new_height, new_upscale_factor = pipe

        if image is not None:
            new_image = image
            
        if width is not None:
            new_width = width
            
        if height is not None:
            new_height = height

        if upscale_factor is not None:
            new_upscale_factor = upscale_factor
            
        pipe = new_image, new_width, new_height, new_upscale_factor
        
        return (pipe, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ImagePipeOut:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"pipe": ("PIPE_LINE",)},
            }

    RETURN_TYPES = ("PIPE_LINE", "IMAGE", "INT", "INT", "FLOAT", "STRING", )
    RETURN_NAMES = ("pipe", "image", "width", "height", "upscale_factor", "show_help", )
    FUNCTION = "pipe_out"
    CATEGORY = icons.get("Comfyroll/Pipe/Image")
    
    def pipe_out(self, pipe):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-image-pipe-out"

        image, width, height, upscale_factor = pipe
        
        return (pipe, image, width, height, upscale_factor, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_InputSwitchPipe:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2}),
                "pipe1": ("PIPE_LINE",),
                "pipe2": ("PIPE_LINE",)
            }
        }
 
    RETURN_TYPES = ("PIPE_LINE", "STRING", )
    RETURN_NAMES = ("PIPE_LINE", "show_help", )
    OUTPUT_NODE = True
    FUNCTION = "switch_pipe"
    CATEGORY = icons.get("Comfyroll/Pipe")

    def switch_pipe(self, Input, pipe1, pipe2):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Pipe-Nodes#cr-pipe-switch"
        
        if Input == 1:
            return (pipe1, show_help, )
        else:
            return (pipe2, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS_2 = {
    "CR Data Bus In":CR_DataBusIn,
    "CR Data Bus Out":CR_DataBusOut,
    "CR 8 Channel In":CR_8ChannelIn,
    "CR 8 Channel Out":CR_8ChannelOut,
    "CR Module Pipe Loader":CR_ModulePipeLoader,
    "CR Module Input":CR_ModuleInput,
    "CR Module Output":CR_ModuleOutput,
    "CR Image Pipe In":CR_ImagePipeIn,
    "CR Image Pipe Edit":CR_ImagePipeEdit,
    "CR Image Pipe Out":CR_ImagePipeOut,
    "CR Pipe Switch":CR_InputSwitchPipe,
}
'''
