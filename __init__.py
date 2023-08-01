from .Comfyroll_Nodes import *
from .Comfyroll_Pipe_Nodes import *

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
}

__all__ = ['NODE_CLASS_MAPPINGS']

print("\033[34mComfyroll Custom Nodes: \033[92mLoaded\033[0m")

