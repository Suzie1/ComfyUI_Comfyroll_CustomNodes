"""
@author: RockOfFire
@title: Comfyroll Custom Nodes
@nickname: Comfyroll Custom Nodes
@description: Custom nodes for SDXL and SD1.5 including Multi-ControlNet, LoRA, Aspect Ratio, Process Switches, and many more nodes.
"""

from .nodes.nodes import *
from .nodes.legacy_nodes import *
from .nodes.lora import *
from .nodes.controlnet import *
from .nodes.pipe import *
from .nodes.sdxl import *
from .nodes.logic import *
from .nodes.model_merge import *
from .nodes.upscale import *
from .nodes.xygrid import *
from .nodes.index import *
from .nodes.conversion import *
from .nodes.matplot import *
from .nodes.pil_text import *
from .nodes.pil_layout import *
from .nodes.pil_filter import *
from .nodes.pil_template import *
from .nodes.pil_pattern import *
from .nodes.nodes_random import *

from .animation_nodes.interpolation import *
from .animation_nodes.io import *
from .animation_nodes.prompt import *
from .animation_nodes.schedulers import *
from .animation_nodes.schedules import *
from .animation_nodes.lists import *
from .animation_nodes.utils import *
from .animation_nodes.cyclers import *

LIVE_NODE_CLASS_MAPPINGS = {
    ### Misc Nodes
    "CR Image Output": CR_ImageOutput,
    "CR Integer Multiple": CR_IntegerMultipleOf,
    "CR Latent Batch Size": CR_LatentBatchSize,   
    "CR Seed": CR_Seed,
    "CR Prompt Text":CR_PromptText,
    "CR Split String":CR_SplitString,
    "CR Value": CR_Value,
    "CR Conditioning Mixer":CR_ConditioningMixer,
    "CR Select Model": CR_SelectModel,
    ### List Nodes
    "CR Font File List": CR_FontFileList,
    "CR Text List": CR_TextList,     
    ### Aspect Ratio Nodes
    "CR SD1.5 Aspect Ratio":CR_AspectRatioSD15,
    "CR SDXL Aspect Ratio":CR_SDXLAspectRatio,
    "CR Aspect Ratio": CR_AspectRatio,
    "CR Aspect Ratio Banners": CR_AspectRatioBanners,      
    ### Legacy Nodes
    "CR Image Size": CR_ImageSize,
    "CR Aspect Ratio SDXL": CR_AspectRatio_SDXL,    
    ### ControlNet Nodes
    "CR Apply ControlNet": CR_ApplyControlNet,    
    "CR Multi-ControlNet Stack": CR_ControlNetStack,
    "CR Apply Multi-ControlNet": CR_ApplyControlNetStack,   
    ### LoRA Nodes    
    "CR Load LoRA": CR_LoraLoader,    
    "CR LoRA Stack": CR_LoRAStack,
    "CR Random LoRA Stack": CR_RandomLoRAStack,
    "CR Random Weight LoRA": CR_RandomWeightLoRA,
    "CR Apply LoRA Stack": CR_ApplyLoRAStack,  
    ### Model Merge Nodes
    "CR Apply Model Merge": CR_ApplyModelMerge,
    "CR Model Merge Stack": CR_ModelMergeStack,
    ### Pipe Nodes
    "CR Module Pipe Loader": CR_ModulePipeLoader,
    "CR Module Input": CR_ModuleInput,
    "CR Module Output": CR_ModuleOutput,
    "CR Image Pipe In": CR_ImagePipeIn,
    "CR Image Pipe Edit": CR_ImagePipeEdit,
    "CR Image Pipe Out": CR_ImagePipeOut,
    "CR Pipe Switch": CR_InputSwitchPipe,
    ### SDXL Nodes
    "CR SDXL Prompt Mix Presets": CR_PromptMixPresets,
    "CR SDXL Style Text": CR_SDXLStyleText,
    "CR SDXL Base Prompt Encoder": CR_SDXLBasePromptEncoder, 
    ### Upscale Nodes
    "CR Multi Upscale Stack": CR_MultiUpscaleStack,
    "CR Upscale Image": CR_UpscaleImage,
    "CR Apply Multi Upscale": CR_ApplyMultiUpscale,
    ### XY Grid Nodes    
    "CR XY List": CR_XYList,  
    "CR XY Interpolate": CR_XYInterpolate,   
    "CR XY From Folder": CR_XYFromFolder,
    "CR XY Save Grid Image": CR_XYSaveGridImage,
    "CR XY Index": CR_XYIndex,
    #"CR XYZ Index": CR_XYZIndex,
    ### Graphics Pattern
    "CR Halftone Grid": CR_HalftoneGrid,    
    "CR Color Bars": CR_ColorBars,
    "CR Style Bars": CR_StyleBars,    
    "CR Checker Pattern": CR_CheckerPattern,
    "CR Polygons": CR_Polygons,
    "CR Color Gradient": CR_ColorGradient,
    "CR Radial Gradient": CR_RadialGradient,    
    "CR Starburst Lines": CR_StarburstLines,
    "CR Starburst Colors": CR_StarburstColors,
    "CR Simple Binary Pattern": CR_BinaryPatternSimple,     
    "CR Binary Pattern": CR_BinaryPattern,
    ### Graphics Text
    "CR Overlay Text": CR_OverlayText,
    "CR Draw Text": CR_DrawText,
    "CR Mask Text": CR_MaskText,
    "CR Composite Text": CR_CompositeText, 
    #"CR Arabic Text RTL": CR_ArabicTextRTL,
    "CR Simple Text Watermark": CR_SimpleTextWatermark,
    ### Graphics Filter
    "CR Halftone Filter": CR_HalftoneFilter,
    "CR Color Tint": CR_ColorTint,
    "CR Vignette Filter": CR_VignetteFilter,    
    ### Graphics Layout 
    "CR Page Layout": CR_PageLayout,
    "CR Image Panel": CR_ImagePanel,
    "CR Image Grid Panel": CR_ImageGridPanel,
    "CR Image Border": CR_ImageBorder,
    "CR Feathered Border": CR_FeatheredBorder,    
    "CR Simple Text Panel": CR_SimpleTextPanel,    
    "CR Color Panel": CR_ColorPanel,
    "CR Overlay Transparent Image": CR_OverlayTransparentImage,
    #"CR Simple Titles": CR_SimpleTitles,    
    ### Graphics Template
    "CR Simple Meme Template": CR_SimpleMemeTemplate,
    "CR Simple Banner": CR_SimpleBanner,    
    "CR Comic Panel Templates": CR_ComicPanelTemplates,
    "CR Simple Image Compare": CR_SimpleImageCompare,
    ### Utils Logic Nodes
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
    "CR Switch Model and CLIP": CR_ModelAndCLIPInputSwitch,  
    ### Utils Process Nodes
    "CR Batch Process Switch": CR_BatchProcessSwitch,    
    "CR Img2Img Process Switch": CR_Img2ImgProcessSwitch,
    "CR Hires Fix Process Switch": CR_HiResFixProcessSwitch,    
    ### Utils Index Nodes
    "CR Index": CR_Index,    
    "CR Index Increment": CR_IncrementIndex,
    "CR Index Multiply": CR_MultiplyIndex,
    "CR Index Reset": CR_IndexReset,
    "CR Trigger": CR_Trigger,
    ### Utils Conversion Nodes  
    "CR String To Number": CR_StringToNumber,
    "CR String To Combo": CR_StringToCombo,    
    "CR Float To String": CR_FloatToString,
    "CR Float To Integer": CR_FloatToInteger,
    "CR Integer To String": CR_IntegerToString,    
    "CR Text List To String": CR_TextListToString,
    "CR Seed to Int": CR_SeedToInt,
    ### Utils Random Nodes
    "CR Random Hex Color": CR_RandomHexColor, 
    "CR Random RGB": CR_RandomRGB,
    "CR Random Multiline Values": CR_RandomMultilineValues,
    "CR Random RGB Gradient": CR_RandomRGBGradient,    
    #------------------------------------------------------
    ### Animation Nodes
    # Schedules  
    "CR Simple Schedule": CR_SimpleSchedule,
    "CR Central Schedule": CR_CentralSchedule, 
    "CR Combine Schedules": CR_CombineSchedules,  
    "CR Output Schedule To File": CR_OutputScheduleToFile,
    "CR Load Schedule From File": CR_LoadScheduleFromFile, 
    "CR Schedule Input Switch": Comfyroll_ScheduleInputSwitch,      
    # Schedulers
    "CR Simple Value Scheduler": CR_SimpleValueScheduler,
    "CR Simple Text Scheduler": CR_SimpleTextScheduler,
    "CR Value Scheduler": CR_ValueScheduler,
    "CR Text Scheduler": CR_TextScheduler,  
    "CR Load Scheduled Models": CR_LoadScheduledModels,
    "CR Load Scheduled LoRAs": CR_LoadScheduledLoRAs,
    "CR Prompt Scheduler": CR_PromptScheduler,
    "CR Simple Prompt Scheduler": CR_SimplePromptScheduler,      
    # Prompt
    "CR Prompt List": CR_PromptList,
    "CR Prompt List Keyframes": CR_PromptListKeyframes,
    "CR Simple Prompt List": CR_SimplePromptList,    
    "CR Simple Prompt List Keyframes": CR_SimplePromptListKeyframes,
    "CR Keyframe List": CR_KeyframeList,    
    "CR Prompt Text": CR_PromptText,
    #"CR Load Prompt Style": CR_LoadPromptStyle,
    "CR Encode Scheduled Prompts": CR_EncodeScheduledPrompts,      
    # Interpolation
    "CR Gradient Float": CR_GradientFloat,
    "CR Gradient Integer": CR_GradientInteger,
    "CR Increment Float": CR_IncrementFloat,    
    "CR Increment Integer": CR_IncrementInteger,
    "CR Interpolate Latents": CR_InterpolateLatents,    
    # Lists
    "CR Model List": CR_ModelList,
    "CR LoRA List": CR_LoRAList,
    #"CR Text List": CR_TextList,
    "CR Text List Simple": CR_TextListSimple,
    "CR Image List": CR_ImageList,
    "CR Image List Simple": CR_ImageListSimple,     
    # Cyclers
    "CR Cycle Models": CR_CycleModels,    
    "CR Cycle LoRAs": CR_CycleLoRAs,
    "CR Cycle Text": CR_CycleText,
    "CR Cycle Text Simple": CR_CycleTextSimple,
    "CR Cycle Images": CR_CycleImages,
    "CR Cycle Images Simple": CR_CycleImagesSimple,        
    # Utils   
    "CR Debatch Frames": CR_DebatchFrames,    
    "CR Current Frame": CR_CurrentFrame,
    #"CR Input Text List": CR_InputTextList,   
    # IO
    "CR Load Animation Frames": CR_LoadAnimationFrames,
    "CR Load Flow Frames": CR_LoadFlowFrames,
    "CR Output Flow Frames": CR_OutputFlowFrames,       
}

LIVE_NODE_DISPLAY_NAME_MAPPINGS = {
    ### Misc Nodes
    "CR Image Output": "💾 CR Image Output",
    "CR Integer Multiple": "⚙️ CR Integer Multiple",
    "CR Latent Batch Size": "⚙️ CR Latent Batch Size", 
    "CR Seed": "🌱 CR Seed",
    "CR Prompt Text": "📝 CR Prompt Text",
    "CR Split String": "⚙️ CR Split String",
    "CR Value": "⚙️ CR Value",
    "CR Conditioning Mixer": "⚙️ CR Conditioning Mixer",
    "CR Select Model": "🔮 CR Select Model",
    ### List Nodes
    "CR Font File List": "📜 CR Font File List",
    "CR Text List": "📜 CR Text List",     
    ### Aspect Ratio Nodes
    "CR SD1.5 Aspect Ratio": "🔳 CR SD1.5 Aspect Ratio",
    "CR SDXL Aspect Ratio": "🔳 CR SDXL Aspect Ratio",    
    "CR Aspect Ratio": "🔳 CR Aspect Ratio",
    "CR Aspect Ratio Banners": "🔳 CR Aspect Ratio Banners",
    ### Legacy Nodes
    "CR Image Size": "CR Image Size (Legacy)",
    "CR Aspect Ratio SDXL": "CR Aspect Ratio SDXL (Legacy)",     
    ### ControlNet Nodes
    "CR Apply ControlNet": "🕹️ CR Apply ControlNet",    
    "CR Multi-ControlNet Stack": "🕹️ CR Multi-ControlNet Stack",
    "CR Apply Multi-ControlNet": "🕹️ CR Apply Multi-ControlNet",   
    ### LoRA Nodes    
    "CR Load LoRA": "💊 CR Load LoRA",    
    "CR LoRA Stack": "💊 CR LoRA Stack",
    "CR Random LoRA Stack": "💊 CR Random LoRA Stack",
    "CR Random Weight LoRA": "💊 CR Random Weight LoRA",
    "CR Apply LoRA Stack": "💊 CR Apply LoRA Stack",
    ### Model Merge Nodes
    "CR Apply Model Merge": "⛏️ CR Apply Model Merge",
    "CR Model Merge Stack": "⛏️ CR Model Merge Stack",
    ### Pipe Nodes
    "CR Module Pipe Loader": "✈️ CR Module Pipe Loader",
    "CR Module Input": "✈️ CR Module Input",
    "CR Module Output": "✈️ CR Module Output",
    "CR Image Pipe In": "🛩 CR Image Pipe In",
    "CR Image Pipe Edit": "🛩️ CR Image Pipe Edit",
    "CR Image Pipe Out": "🛩️ CR Image Pipe Out",
    "CR Pipe Switch": "🔀️ CR Pipe Switch",    
    ### SDXL Nodes
    "CR SDXL Prompt Mix Presets": "🌟 CR SDXL Prompt Mix Presets",
    "CR SDXL Style Text": "🌟 CR SDXL Style Text",
    "CR SDXL Base Prompt Encoder": "🌟 CR SDXL Base Prompt Encoder", 
    ### Upscale Nodes
    "CR Multi Upscale Stack": "🔍 CR Multi Upscale Stack",
    "CR Upscale Image": "🔍 CR Upscale Image",
    "CR Apply Multi Upscale": "🔍 CR Apply Multi Upscale",
    ### XY Grid Nodes    
    "CR XY List": "📉 CR XY List",  
    "CR XY Interpolate": "📉 CR XY Interpolate", 
    "CR XY Index": "📉 CR XY Index",
    "CR XY From Folder": "📉 CR XY From Folder",
    "CR XY Save Grid Image": "📉 CR XY Save Grid Image",
    #"CR XYZ Index": "📉 CR XYZ Index",
    ### Graphics Pattern
    "CR Halftone Grid" : "🟫 CR Halftone Grid",    
    "CR Color Bars" : "🟫 CR Color Bars",
    "CR Style Bars" : "🟪 CR Style Bars",    
    "CR Checker Pattern": "🟦 CR Checker Pattern",
    "CR Polygons": "🟩 CR Polygons",
    "CR Color Gradient": "🟨 CR Color Gradient",
    "CR Radial Gradient": "🟨 CR Radial Gradient",    
    "CR Starburst Lines": "🟧 CR Starburst Lines",
    "CR Starburst Colors": "🟥 CR Starburst Colors",
    "CR Simple Binary Pattern": "🟥 CR Simple Binary Pattern",
    "CR Binary Pattern": "🟥 CR Binary Pattern",
    ### Graphics Text
    "CR Overlay Text": "🔤 CR Overlay Text",
    "CR Draw Text": "🔤️ CR Draw Text",
    "CR Mask Text": "🔤️ CR Mask Text",
    "CR Composite Text": "🔤️ CR Composite Text",
    #"CR Arabic Text RTL": "🔤️ CR Arabic Text RTL",
    "CR Simple Text Watermark": "🔤️ CR Simple Text Watermark",
    "CR Font File List": "🔤️ CR Font File List",
    ### Graphics Filter
    "CR Halftone Filter": "🎨 Halftone Filter",
    "CR Color Tint": "🎨 CR Color Tint", 
    "CR Vignette Filter": "🎨 CR Vignette Filter",   
    ### Graphics Layout
    "CR Image Panel": "🌁 CR Image Panel",
    "CR Image Grid Panel": "🌁 CR Image Grid Panel",
    "CR Simple Text Panel": "🌁 CR Simple Text Panel",
    "CR Color Panel": "🌁 CR Color Panel",
    "CR Page Layout": "🌁 CR Page Layout",
    "CR Image Border": "🌁 CR Image Border",
    "CR Feathered Border": "🌁 CR Feathered Border",    
    "CR Overlay Transparent Image": "🌁 CR Overlay Transparent Image",
    #"CR Simple Titles": "🌁 CR Simple Titles",    
    ### Graphics Template
    "CR Simple Meme Template": "👽 CR Simple Meme Template",
    "CR Simple Banner": "👽 CR Simple Banner",     
    "CR Comic Panel Templates": "👽 CR Comic Panel Templates",
    "CR Simple Image Compare": "👽 CR Simple Image Compare",
    ### Utils Logic Nodes
    "CR Image Input Switch": "🔀 CR Image Input Switch",
    "CR Image Input Switch (4 way)": "🔀 CR Image Input Switch (4 way)",
    "CR Latent Input Switch": "🔀 CR Latent Input Switch",
    "CR Conditioning Input Switch": "🔀 CR Conditioning Input Switch",
    "CR Clip Input Switch": "🔀 CR Clip Input Switch",
    "CR Model Input Switch": "🔀 CR Model Input Switch",
    "CR ControlNet Input Switch": "🔀 CR ControlNet Input Switch",
    "CR VAE Input Switch": "🔀 CR VAE Input Switch",     
    "CR Text Input Switch": "🔀 CR Text Input Switch",
    "CR Text Input Switch (4 way)": "🔀 CR Text Input Switch (4 way)",
    "CR Switch Model and CLIP": "🔀 CR Switch Model and CLIP",
    ### Utils Process Nodes
    "CR Batch Process Switch": "🔂 CR Batch Process Switch",    
    "CR Img2Img Process Switch": "🔂 CR Img2Img Process Switch",
    "CR Hires Fix Process Switch": "🔂 CR Hires Fix Process Switch",    
    ### Utils Index Nodes
    "CR Index":"🔢 CR Index",    
    "CR Index Increment": "🔢 CR Index Increment",
    "CR Index Multiply": "🔢 CR Index Multiply",
    "CR Index Reset": "🔢 CR Index Reset",
    "CR Trigger": "🔢 CR Trigger",
    ### Utils Conversion Nodes
    "CR String To Number": "🔧 CR String To Number",
    "CR String To Combo": "🔧 CR String To Combo",    
    "CR Float To String": "🔧 CR Float To String",
    "CR Float To Integer": "🔧 CR Float To Integer",
    "CR Integer To String": "🔧 CR Integer To String",    
    "CR Text List To String": "🔧 CR Text List To String",
    "CR Seed to Int": "🔧 CR Seed to Int",
    ### Utils Random Nodes
    "CR Random Hex Color": "🎲 CR Random Hex Color", 
    "CR Random RGB": "🎲 CR Random RGB",
    "CR Random Multiline Values": "🎲 CR Random Multiline Values",
    "CR Random RGB Gradient": "🎲 CR Random RGB Gradient", 
    #------------------------------------------------------
    ### Animation Nodes
    # Schedules  
    "CR Simple Schedule": "📋 CR Simple Schedule",
    "CR Central Schedule": "📋 CR Central Schedule", 
    "CR Combine Schedules": "📋 CR Combine Schedules",  
    "CR Output Schedule To File": "📋 CR Output Schedule To File",
    "CR Load Schedule From File": "📋 CR Load Schedule From File", 
    "CR Schedule Input Switch": "📋 CR Schedule Input Switch",      
    # Schedulers
    "CR Simple Value Scheduler": "📑 CR Simple Value Scheduler",
    "CR Simple Text Scheduler": "📑 CR Simple Text Scheduler",
    "CR Value Scheduler": "📑 CR Value Scheduler",
    "CR Text Scheduler": "📑 CR Text Scheduler",  
    "CR Load Scheduled Models": "📑 CR Load Scheduled Models",
    "CR Load Scheduled LoRAs": "📑 CR Load Scheduled LoRAs",
    "CR Prompt Scheduler": "📑 CR Prompt Scheduler",
    "CR Simple Prompt Scheduler": "📑 CR Simple Prompt Scheduler",      
    # Prompt
    "CR Prompt List": "📝 CR Prompt List",
    "CR Prompt List Keyframes": "📝 CR Prompt List Keyframes",
    "CR Simple Prompt List": "📝 CR Simple Prompt List",    
    "CR Simple Prompt List Keyframes": "📝 CR Simple Prompt List Keyframes",
    "CR Keyframe List": "📝 CR Keyframe List",    
    "CR Prompt Text": "📝 CR Prompt Text",
    #"CR Load Prompt Style": "📝 CR Load Prompt Style",
    "CR Encode Scheduled Prompts": "📝 CR Encode Scheduled Prompts",      
    # Interpolation
    "CR Gradient Float": "🔢 CR Gradient Float",
    "CR Gradient Integer": "🔢 CR Gradient Integer",
    "CR Increment Float": "🔢 CR Increment Float",    
    "CR Increment Integer": "🔢 CR Increment Integer",
    "CR Interpolate Latents": "🔢 CR Interpolate Latents",    
    # Lists
    "CR Model List": "📃 CR Model List",
    "CR LoRA List": "📃 CR LoRA List",
    #"CR Text List": "📃 CR Text List",
    "CR Text List Simple": "📃 CR Text List Simple",
    "CR Image List": "📃 CR Image List",
    "CR Image List Simple": "📃 CR Image List Simple", 
    "CR Input Text List": "📃 CR Input Text List", 
    # Cyclers
    "CR Cycle Models": "♻️ CR Cycle Models",    
    "CR Cycle LoRAs": "♻️ CR Cycle LoRAs",
    "CR Cycle Text": "♻️ CR Cycle Text",
    "CR Cycle Text Simple": "♻️ CR Cycle Text Simple",
    "CR Cycle Images": "♻️ CR Cycle Images",
    "CR Cycle Images Simple": "♻️ CR Cycle Images Simple",        
    # Utils   
    "CR Debatch Frames": "🛠️ CR Debatch Frames",    
    "CR Current Frame": "🛠️ CR Current Frame",
    # IO
    "CR Load Animation Frames": "⌨️ CR Load Animation Frames",
    "CR Load Flow Frames": "⌨️ CR Load Flow Frames",
    "CR Output Flow Frames": "⌨️ CR Output Flow Frames",  
}

INCLUDE_DEV_NODES = False

try:
    from .dev_node_mappings import DEV_NODE_CLASS_MAPPINGS, DEV_NODE_DISPLAY_NAME_MAPPINGS
    if INCLUDE_DEV_NODES:
        NODE_CLASS_MAPPINGS = {**DEV_NODE_CLASS_MAPPINGS, **LIVE_NODE_CLASS_MAPPINGS}
        NODE_DISPLAY_NAME_MAPPINGS = {**DEV_NODE_DISPLAY_NAME_MAPPINGS, **LIVE_NODE_DISPLAY_NAME_MAPPINGS}
        print("\033[34mComfyroll Custom Nodes: \033[92mDev Nodes Loaded\033[0m")
    else:
        NODE_CLASS_MAPPINGS = LIVE_NODE_CLASS_MAPPINGS
        NODE_DISPLAY_NAME_MAPPINGS = LIVE_NODE_DISPLAY_NAME_MAPPINGS
except ImportError:
    NODE_CLASS_MAPPINGS = LIVE_NODE_CLASS_MAPPINGS
    NODE_DISPLAY_NAME_MAPPINGS = LIVE_NODE_DISPLAY_NAME_MAPPINGS

print("----------------------------------------")    
print("\033[34mComfyroll Custom Nodes:\033[92m 148 Nodes Loaded\033[0m")
print("----------------------------------------")

import shutil
import folder_paths
import os

comfy_path = os.path.dirname(folder_paths.__file__)
comfyroll_nodes_path = os.path.join(os.path.dirname(__file__))

js_dest_path = os.path.join(comfy_path, "web", "extensions", "Comfyroll")
os.makedirs(js_dest_path, exist_ok=True)

files_to_copy = ["test.js"]

for file in files_to_copy:
    js_src_path = os.path.join(comfyroll_nodes_path, "js", file)
    shutil.copy(js_src_path, js_dest_path)

