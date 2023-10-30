from .nodes.nodes import *
from .nodes.lora import *
from .nodes.controlnet import *  
from .nodes.logic import *
from .nodes.index import *
from .nodes.conversion import *
from .nodes.pipe import *
from .nodes.sdxl import *
from .nodes.model_merge import *
from .nodes.upscale import *
from .nodes.xygrid import *
from .nodes.matplot import *
from .nodes.pil_text import *

NODE_CLASS_MAPPINGS = {
    "CR Image Output": CR_ImageOutput,
    "CR Integer Multiple": CR_IntegerMultipleOf,
    "CR Color Tint": CR_ColorTint,
    "CR Latent Batch Size": CR_LatentBatchSize, 
    "CR SD1.5 Aspect Ratio":CR_AspectRatioSD15,
    "CR Seed": CR_Seed,
    "CR Prompt Text":CR_PromptText,
    "CR Split String":CR_SplitString, 
    ### ControlNet Nodes
    "CR Apply ControlNet": CR_ApplyControlNet,    
    "CR Multi-ControlNet Stack":CR_ControlNetStack,
    "CR Apply Multi-ControlNet":CR_ApplyControlNetStack,   
    ### LoRA Nodes    
    "CR Load LoRA": CR_LoraLoader,    
    "CR LoRA Stack":CR_LoRAStack,
    "CR Apply LoRA Stack":CR_ApplyLoRAStack,  
    ### Logic Nodes
    "CR Image Input Switch": CR_ImageInputSwitch,
    "CR Image Input Switch (4 way)": CR_ImageInputSwitch4way,
    "CR Latent Input Switch": CR_LatentInputSwitch,
    "CR Conditioning Input Switch": CR_ConditioningInputSwitch,
    "CR Clip Input Switch": CR_ClipInputSwitch,
    "CR Model Input Switch": CR_ModelInputSwitch,
    "CR ControlNet Input Switch": CR_ControlNetInputSwitch,
    "CR VAE Input Switch": CR_VAEInputSwitch,
    "CR Text Input Switch": CR_TextInputSwitch,
    "CR Text Input Switch (4 way)": CR_TextInputSwitch4way,
    "CR Switch Model and CLIP":CR_ModelAndCLIPInputSwitch,    
    "CR Batch Process Switch": CR_BatchProcessSwitch,    
    "CR Img2Img Process Switch": CR_Img2ImgProcessSwitch,
    "CR Hires Fix Process Switch": CR_HiResFixProcessSwitch, 
    ### Model Merge
    "CR Apply Model Merge":CR_ApplyModelMerge,
    "CR Model Merge Stack":CR_ModelMergeStack,
    ### Pipe Nodes
    "CR Module Pipe Loader":CR_ModulePipeLoader,
    "CR Module Input":CR_ModuleInput,
    "CR Module Output":CR_ModuleOutput,
    "CR Image Pipe In":CR_ImagePipeIn,
    "CR Image Pipe Edit":CR_ImagePipeEdit,
    "CR Image Pipe Out":CR_ImagePipeOut,
    "CR Pipe Switch":CR_InputSwitchPipe,  
    ### SDXL Nodes
    "CR SDXL Prompt Mix Presets": CR_PromptMixPresets,
    "CR SDXL Aspect Ratio":CR_SDXLAspectRatio,
    "CR SDXL Style Text": CR_SDXLStyleText,
    "CR SDXL Base Prompt Encoder": CR_SDXLBasePromptEncoder, 
    ### Upscale Nodes
    "CR Multi Upscale Stack":CR_MultiUpscaleStack,
    "CR Upscale Image":CR_UpscaleImage,
    "CR Apply Multi Upscale":CR_ApplyMultiUpscale,
    ### XY Grid Nodes    
    "CR XY List":CR_XYList,
    "CR XY Interpolate":CR_XYInterpolate,
    "CR XY Index":CR_XYIndex,
    "CR XY From Folder":CR_XYFromFolder,
    "CR XY Save Grid Image":CR_XYSaveGridImage,
    ### Matplot Nodes
    "CR Halftone Grid":CR_HalftoneGrid,
    "CR Color Bars":CR_ColorBars,
    "CR Style Bars":CR_StyleBars,    
    "CR Checker Pattern":CR_CheckerPattern,
    "CR Polygons":CR_Polygons,
    "CR Color Gradient":CR_ColorGradient,
    "CR Radial Gradient": CR_RadialGradient,
    "CR Starburst Lines":CR_StarburstLines,
    "CR Starburst Colors":CR_StarburstColors, 
    ### PIL Text
    "CR Overlay Text":CR_OverlayText,
    "CR Draw Text":CR_DrawText,
    "CR Mask Text":CR_MaskText,
    "CR Composite Text":CR_CompositeText,
    "CR Simple Meme Template":CR_SimpleMemeTemplate,
    "CR Image Panel":CR_ImagePanel, 
    ### Conversion    
    "CR String To Number":CR_StringToNumber,
    "CR String To Combo":CR_StringToCombo,    
    "CR Float To String":CR_FloatToString,
    "CR Float To Integer":CR_FloatToInteger,
    "CR Integer To String":CR_IntegerToString,    
    "CR Text List To String":CR_TextListToString,
    "CR Seed to Int": CR_SeedToInt,    
    ### Index
    "CR Index":CR_Index,    
    "CR Index Increment":CR_IncrementIndex,
    "CR Index Multiply":CR_MultiplyIndex,
    "CR Index Reset":CR_IndexReset,
    "CR Trigger":CR_Trigger,
}

__all__ = ['NODE_CLASS_MAPPINGS']

print("\033[34mComfyroll Custom Nodes: \033[92mLoaded\033[0m")
