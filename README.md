# 🧩 Comfyroll Custom Nodes for SDXL and SD1.5

Co-authored by Suzie1 and RockOfFire

These nodes can be used in any ComfyUI workflow.  

# Installation

1. cd custom_nodes
2. git clone https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes.git
3. Restart ComfyUI

You can also install the nodes using the following methods:
* install using [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
* download from [CivitAI](https://civitai.com/models/87609/comfyroll-custom-nodes-for-comfyui)

# Patch Notes

https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/blob/main/Patch_Notes.md


# Wiki

https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki

# List of Custom Nodes

__🔳 Aspect Ratio__
* CR SDXL Aspect Ratio
* CR SD1.5 Aspect Ratio
* CR Aspect Ratio (new 27/11/2023)

__🌟 SDXL__
* CR SDXL Prompt Mix Presets
* CR SDXL Style Text
* CR SDXL Base Prompt Encoder

__💊 LoRA__
* CR Load LoRA
* CR LoRA Stack
* CR Apply LoRA Stack

__🕹️ ControlNet__
* CR Apply ControlNet
* CR Multi-ControlNet Stack
* CR Apply Multi-ControlNet Stack

__🔂 Process__
* CR Img2Img Process Switch
* CR Hires Fix Process Switch
* CR Batch Process Switch

__👓 Graphics - Filter__
* CR Color Tint

__🌈 Graphics - Pattern__
* CR Halftone Grid
* CR Color Bars
* CR Style Bars   
* CR Checker Pattern
* CR Polygons
* CR Color Gradient
* CR Radial Gradiant
* CR Starburst Lines
* CR Starburst Colors

__🔤 Graphics - Text__
* CR Overlay Text
* CR Draw Text
* CR Mask Text
* CR Composite Text

__👽 Graphics - Template__
* CR Simple Meme Template

__🌁 Graphics - Layout__
* CR Image Panel
* CR Page Layout
* CR Image Grid Panel
* CR Image Border
* CR Color Panel
* CR Simple Text Panel

__✈️ Module__
* CR Module Pipe Loader
* CR Module Input
* CR Module Output

__🛩️ Pipe__
* CR Image Pipe In
* CR Image Pipe Edit
* CR Image Pipe Out
* CR Pipe Switch

__⛏️ Model Merge__
* CR Model Stack
* CR Apply Model Merge

__🔍 Upscale__
* CR Multi Upscale Stack
* CR Upscale Image
* CR Apply Multi Upscale

__📉 XY Grid__
* CR XY List
* CR XY Interpolate   
* CR XY Index
* CR XY From Folder
* CR XY Save Grid Image
* CR Image Output

__🔢 Index__
* CR Index
* CR Index Increment
* CR Index Multiply
* CR Index Reset
* CR Trigger

__🔧 Conversion__    
* CR String To Number
* CR String To Combo    
* CR Float To String
* CR Float To Integer
* CR Integer To String    
* CR Text List To String
* CR Seed to Int

__🔀 Logic__
* CR Image Input Switch
* CR Image Input Switch (4 way)
* CR Latent Input Switch
* CR Conditioning Input Switch
* CR Clip Input Switch
* CR Model Input Switch
* CR ControlNet Input Switch
* CR VAE Input Switch
* CR Text Input Switch
* CR Text Input Switch (4 way)
* CR Switch Model and CLIP
  
__📦 Other__
* CR Latent Batch Size
* CR Prompt Text
* CR Split String
* CR Integer Multiple
* CR Seed
* CR Value
* CR Conditioning Mixer (new 27/11/2023)
* CR Select Model (new 27/11/2023)

__Deleted Nodes__
* CR Aspect Ratio SDXL replaced by CR SDXL Aspect Ratio
* CR SDXL Prompt Mixer replaced by CR SDXL Prompt Mix Presets

# CR Animation Nodes

CR Animation Nodes are now included in the Comfyroll Custom Nodes pack.

[Animation Nodes](https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/blob/suzie_dev/Animation_Nodes.md)

# Multi-ControlNet methodology

The method used in CR Apply Multi-ControlNet is to chain the conditioning so that the output from the first Controlnet becomes the input to the second.

For an example of this method see this link:

https://comfyanonymous.github.io/ComfyUI_examples/controlnet/#mixing-controlnets

# Multi-ControlNet compatability with Efficiency nodes

![Custom Nodes](/images/Efficiency_Compability.JPG)

CR LoRA Stack and CR Multi-ControlNet Stack are both compatible with the Efficient Loader node, in Efficiency nodes by LucianoCirino.

CR Apply Multi-ControlNet Stack can accept inputs from the Control Net Stacker node in the Efficiency nodes (see diagram in Node Images below).

# SDXL Prompt Mix Presets

Preset mappings can be found in this CivitAI article:

https://civitai.com/articles/1835

# Comfyroll Workflow Templates

The nodes were originally made for use in the Comfyroll Template Workflows.

[Comfyroll Template Workflows](https://civitai.com/models/59806/comfyroll-template-workflows)

[Comfyroll Pro Templates](https://civitai.com/models/85619/comfyroll-pro-template)

[Comfyroll SDXL Workflow Templates](https://civitai.com/models/118005/comfyroll-sdxl-workflow-templates)

[SDXL Workflow for ComfyUI with Multi-ControlNet](https://civitai.com/models/129858/sdxl-workflow-for-comfyui-with-multi-controlnet)

[SDXL and SD1.5 Model Merge Templates for ComfyUI](https://civitai.com/models/123125/sdxl-and-sd15-model-merge-templates-for-comfyui)

# Credits

comfyanonymous/[ComfyUI](https://github.com/comfyanonymous/ComfyUI) - A powerful and modular stable diffusion GUI.

WASasquatch/[was-node-suite-comfyui](https://github.com/WASasquatch/was-node-suite-comfyui) - A powerful custom node extensions of ComfyUI.

TinyTerra/[ComfyUI_tinyterraNodes](https://github.com/TinyTerra/ComfyUI_tinyterraNodes) - A selection of nodes for Stable Diffusion ComfyUI

hnmr293/[ComfyUI-nodes-hnmr](https://github.com/hnmr293/ComfyUI-nodes-hnmr) - ComfyUI custom nodes - merge, grid (aka xyz-plot) and others

SeargeDP/[SeargeSDXL](https://github.com/SeargeDP) - ComfyUI custom nodes - Prompt nodes and Conditioning nodes

LucianoCirino/[efficiency-nodes-comfyui](https://github.com/LucianoCirino/efficiency-nodes-comfyui) - A collection of ComfyUI custom nodes.

SLAPaper/[ComfyUI-Image-Selector](https://github.com/SLAPaper/ComfyUI-Image-Selector) - Select one or some of images from a batch
