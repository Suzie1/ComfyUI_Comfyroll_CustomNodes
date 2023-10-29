from .Comfyroll_Nodes import *
from .nodes.pipe import *
from .nodes.sdxl import *
from .nodes.upscale import *
from .nodes.xygrid import *
from .nodes.utils import *
from .nodes.matplot import *
from .nodes.pil_text import *

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
    "CR Prompt Text":CR_PromptText,
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
    "CR Starburst Lines":CR_StarburstLines,
    "CR Starburst Colors":CR_StarburstColors, 
    ### PIL Text
    "CR Overlay Text":CR_OverlayText,
    "CR Draw Text":CR_DrawText,
    "CR Mask Text":CR_MaskText,
    "CR Composite Text":CR_CompositeText,
    "CR Simple Meme Template":CR_SimpleMemeTemplate, 
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
