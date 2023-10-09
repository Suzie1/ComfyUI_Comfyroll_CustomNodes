from .Comfyroll_Nodes import *
from .Comfyroll_Pipe_Nodes import *
from .Comfyroll_SDXL_Nodes import *
from .nodes.upscale import *
from .nodes.xygrid import *
from .nodes.utils import *

NODE_CLASS_MAPPINGS = {
    "CR Image Input Switch": Comfyroll_ImageInputSwitch,
    "CR Image Input Switch (4 way)": Comfyroll_ImageInputSwitch_4way,
    "CR Latent Input Switch": Comfyroll_LatentInputSwitch,
    "CR Conditioning Input Switch": Comfyroll_ConditioningInputSwitch,
    "CR Clip Input Switch": Comfyroll_ClipInputSwitch,
    "CR Model Input Switch": Comfyroll_ModelInputSwitch,
    "CR ControlNet Input Switch": Comfyroll_ControlNetInputSwitch,
    "CR Text Input Switch": Comfyroll_TextInputSwitch,
    "CR Text Input Switch (4 way)": Comfyroll_TextInputSwitch_4way,
    "CR Switch Model and CLIP":Comfyroll_ModelAndCLIPInputSwitch,
    "CR Load LoRA": Comfyroll_LoraLoader,
    "CR Apply ControlNet": Comfyroll_ApplyControlNet,
    "CR Image Size": Comfyroll_ImageSize_Float,
    "CR Image Output": Comfyroll_ImageOutput,
    "CR Integer Multiple": Comfyroll_Int_Multiple_Of,
    "CR Aspect Ratio": Comfyroll_AspectRatio,
    "CR Seed to Int": Comfyroll_SeedToInt,
    "CR Integer To String":CR_IntegerToString,
    "CR Float To String":CR_FloatToString,
    "CR Color Tint": Comfyroll_Color_Tint,
    "CR Img2Img Process Switch": Comfyroll_InputLatentsText,
    "CR Hires Fix Process Switch": Comfyroll_HiResFixSwitch,
    "CR Halftone Grid" : Comfyroll_Halftone_Grid,
    "CR Latent Batch Size": Comfyroll_LatentBatchSize,
    "CR LoRA Stack":Comfyroll_LoRA_Stack,
    "CR Apply LoRA Stack":Comfyroll_ApplyLoRA_Stack,    
    "CR SD1.5 Aspect Ratio":Comfyroll_AspectRatio_v2,
    "CR Batch Process Switch": Comfyroll_BatchProcessSwitch,
    "CR Multi-ControlNet Stack":Comfyroll_ControlNetStack,
    "CR Apply Multi-ControlNet":Comfyroll_ApplyControlNetStack,    
    "CR Seed": Comfyroll_Seed,
    "CR Apply Model Merge":Comfyroll_ApplyModelMerge,
    "CR Model Merge Stack":Comfyroll_ModelMergeStack,
    ##Prompt
    "CR Prompt Text":CR_PromptText,
    ### Pipe Nodes
    "CR Module Pipe Loader": CR_module_pipe_loader,
    "CR Module Input": CR_module_input,
    "CR Module Output": CR_module_output,
    "CR Image Pipe In": CR_image_pipe_in,
    "CR Image Pipe Edit": CR_image_pipe_edit,
    "CR Image Pipe Out": CR_image_pipe_out,
    "CR Pipe Switch": CR_input_switch_pipe,
    ### SDXL Nodes
    "CR SDXL Prompt Mix Presets": Comfyroll_prompt_mixer_v2,
    "CR SDXL Aspect Ratio":Comfyroll_SDXL_AspectRatio_v2,
    "CR SDXL Prompt Mixer": Comfyroll_prompt_mixer,
    "CR SDXL Style Text": Comfyroll_SDXLStyleText,
    "CR SDXL Base Prompt Encoder": Comfyroll_SDXLBasePromptEncoder, 
    "CR Aspect Ratio SDXL": Comfyroll_AspectRatio_SDXL,
    ### Upscale Nodes
    "CR Multi Upscale Stack":CR_MultiUpscaleStack,
    "CR Upscale Image":CR_UpscaleImage,
    "CR Apply Multi Upscale":CR_ApplyMultiUpscale,
    ### XY Gid Nodes    
    "CR XY List":CR_XYList,
    "CR XY Interpolate":CR_XYInterpolate,
    "CR XY Index":CR_XYIndex,
    #"CR XYZ Index":CR_XYZIndex,
    "CR XY From Folder":CR_XYFromFolder,
    #"CR Load XY Annotation From File":CR_LoadXYAnnotationFromFile,
    #"CR XY Grid":CR_XYGrid,
    "CR XY Save Grid Image":CR_XYSaveGridImage,
    ### Utils
    "CR Index":CR_Index,    
    "CR Index Increment":CR_IncrementIndex,
    "CR Index Multiply":CR_MultiplyIndex,
    "CR Index Reset":CR_IndexReset,
    "CR Trigger":CR_Trigger,
    "CR String To Number":CR_StringToNumber,
    "CR Split String":CR_SplitString,
    "CR Float To Integer":CR_FloatToInteger, 
    "CR Text List To String":CR_TextListToString,
    "CR String To Combo":CR_StringToCombo, 
}

__all__ = ['NODE_CLASS_MAPPINGS']

print("\033[34mComfyroll Custom Nodes: \033[92mLoaded\033[0m")
