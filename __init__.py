from .Comfyroll_Nodes import *
from .Comfyroll_Pipe_Nodes import *
#from .Comfyroll_Animation_Nodes import *
#from .Comfyroll_Test_Nodes import *

NODE_CLASS_MAPPINGS = {
    "CR Module Pipe Loader": module_pipe_loader,
    "CR Module Input": module_input,
    "CR Module Output": module_output,
    "CR Image Pipe In": image_pipe_in,
    "CR Image Pipe Edit": image_pipe_edit,
    "CR Image Pipe Out": image_pipe_out,
    "CR Pipe Switch": input_switch_pipe,
    "CR Image Input Switch": ComfyRoll_InputImages,
    "CR Image Input Switch (4 way)": ComfyRoll_InputImages_4way,
    "CR Latent Input Switch": ComfyRoll_InputLatents,
    "CR Conditioning Input Switch": ComfyRoll_InputConditioning,
    "CR Clip Input Switch": ComfyRoll_InputClip,
    "CR Model Input Switch": ComfyRoll_InputModel,
    "CR ControlNet Input Switch": ComfyRoll_InputControlNet,
    "CR Load LoRA": ComfyRoll_LoraLoader,
    "CR Apply ControlNet": ComfyRoll_ApplyControlNet,
    "CR Image Size": ComfyRoll_ImageSize_Float,
    "CR Image Output": ComfyRoll_ImageOutput,
    "CR Integer Multiple": CR_Int_Multiple_Of,
    "CR Aspect Ratio": ComfyRoll_AspectRatio,
    "CR Aspect Ratio SDXL": ComfyRoll_AspectRatio_SDXL,
    "CR Seed to Int": ComfyRoll_SeedToInt,
    "CR Color Tint": Comfyroll_Color_Tint,
    "CR SDXL Prompt Mixer": ComfyRoll_prompt_mixer,
    "CR SDXL Style Text": Comfyroll_SDXLStyleText,
    "CR SDXL Base Prompt Encoder": Comfyroll_SDXLBasePromptEncoder, 
    "CR Img2Img Process Switch": ComfyRoll_InputLatentsText,
    "CR Hires Fix Process Switch": ComfyRoll_HiResFixSwitch,
    "CR Halftone Grid" : Comfyroll_Halftone_Grid,
    "CR Latent Batch Size": Comfyroll_LatentBatchSize,
    "CR LoRA Stack":Comfyroll_LoRA_Stack,
    "CR Apply LoRA Stack":Comfyroll_ApplyLoRA_Stack,
    "CR SDXL Aspect Ratio":Comfyroll_SDXL_AspectRatio_v2,
    "CR SD1.5 Aspect Ratio":Comfyroll_AspectRatio_v2,
    "CR Batch Process Switch": Comfyroll_BatchProcessSwitch,
    "CR Multi-ControlNet Stack":Comfyroll_ControlNetStack,
    "CR Apply Multi-ControlNet":Comfyroll_ApplyControlNetStack,
    "CR SDXL Prompt Mix Presets": Comfyroll_prompt_mixer_v2,
    "CR Seed": Comfyroll_Seed,
    ### Animation Nodes
    "CR Load Animation Frames":Comfyroll_LoadAnimationFrames,
    #"CR Animation Stack":Comfyroll_AnimationStack,
    #"CR Prompt List":Comfyroll_PromptList,
    #"CR Animation List":Comfyroll_AnimationList,
    #"CR Prompt List Scheduler":Comfyroll_PromptListScheduler,
    #"CR Animation Stack Scheduler":Comfyroll_AnimationStackScheduler,
    #"CR Advanced Prompt Scheduler":Comfyroll_AdvancedPromptScheduler,
    #"CR LoRA Scheduler":Comfyroll_LoraScheduler,
    ### test nodes
    "CR Apply Model Merge":Comfyroll_ApplyModelMerge,
    "CR Model Stack":Comfyroll_ModelStack,
    #"CR ModelMergeSimple": Comfyroll_SDXLCheckpointLoader,
    #"CR Latent Upscale (Iterative)":Comfyroll_LatentUpscaleIterative,
    #"CR KSampler (Iterative)":Comfyroll_Iterative_KSampler,
    #"CR Load Image Sequence":Comfyroll_LoadImageSequence,
    #"CR Switch": Comfyroll_Comfyroll_Switch_Test,
    #"CR Halftone Image":Comfyroll_ConvertImageToHalftone,
}

__all__ = ['NODE_CLASS_MAPPINGS']

print("\033[34mComfyroll Custom Nodes: \033[92mLoaded\033[0m")
