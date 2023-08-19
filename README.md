# Comfyroll Custom Nodes for SDXL and SD1.5

These nodes were originally made for use in the Comfyroll Template Workflows.

[Comfyroll Template Workflows](https://civitai.com/models/59806/comfyroll-template-workflows)

[Comfyroll Pro Templates](https://civitai.com/models/85619/comfyroll-pro-template)

[Comfyroll SDXL Workflow Templates](https://civitai.com/models/118005/comfyroll-sdxl-workflow-templates)

[SDXL Workflow for ComfyUI with Multi-ControlNet](https://civitai.com/models/129858/sdxl-workflow-for-comfyui-with-multi-controlnet)

<p style="color: yellow;">The nodes can be used in any ComfyUI workflow.</p>

# Installation

If you have a previous version of the Comfyroll nodes from the Comfyroll Worflow Templates download, please delete this before installing these nodes.

1. cd custom_nodes
2. git clone https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes.git
3. Restart ComfyUI

You can also install the nodes using the following methods:
* install using [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
* download from [CivitAI](https://civitai.com/models/87609/comfyroll-custom-nodes-for-comfyui)

# List of Custom Nodes

__Logic__
* CR Image Input Switch
* CR Image Input Switch (4 way)
* CR Latent Input Switch
* CR Conditioning Input Switch
* CR Clip Input Switch
* CR Model Input Switch
* CR ControlNet Input Switch

__Process__
* CR Img2Img Process Switch
* CR Hires Fix Process Switch
* CR Batch Process Switch

__IO__
* CR Load LoRA
* CR LoRA Stack
* CR Apply LoRA Stack

__Maths__
* CR Integer Multiple

__Number__
* CR Seed to Int
* CR Seed

__Image__
* CR Image Size
* CR SD1.5 Aspect Ratio
* CR Color Tint
* CR Halftone Grid

__Conditioning__
* CR Apply ControlNet
* CR Multi-ControlNet Stack
* CR Apply Multi-ControlNet Stack

__SDXL__
* CR SDXL Aspect Ratio
* CR SDXL Prompt Mix Presets
* CR SDXL Style Text
* CR SDXL Base Prompt Encoder

__Module__
* CR Module Pipe Loader
* CR Module Input
* CR Module Output
* CR Image Pipe In
* CR Image Pipe Edit
* CR Image Pipe Out
* CR Pipe Switch

__Latent__
* CR Latent Batch Size

__Legacy__
* CR Image Output
* CR Aspect Ratio SDXL
* CR Aspect Ratio
* CR SDXL Prompt Mixer

# Multi-ControlNet methodology

The method used in CR Apply Multi-ControlNet is to chain the conditioning so that the output from the first Controlnet becomes the input to the second.

For an example of this method see this link:

https://comfyanonymous.github.io/ComfyUI_examples/controlnet/#mixing-controlnets

# Node Images

In the images below, the black nodes are the CR nodes and the grey nodes are other nodes shown for context.

![Custom Nodes](/images/custom_nodes_image8a.JPG)

![Custom Nodes](/images/custom_nodes_image5a.JPG)

![Custom Nodes](/images/custom_nodes_image4b.JPG)

![Custom Nodes](/images/custom_nodes_image6.JPG)

![Custom Nodes](/images/custom_nodes_image7.JPG)

![Custom Nodes](/images/custom_nodes_image7b.JPG)

![Custom Nodes](/images/custom_nodes_image12.JPG)

![Custom Nodes](/images/custom_nodes_image13.JPG)

![Custom Nodes](/images/custom_nodes_image10.JPG)

![Custom Nodes](/images/custom_nodes_image9.JPG)

![Custom Nodes](/images/custom_nodes_image11.JPG)

# Credits

comfyanonymous/[ComfyUI](https://github.com/comfyanonymous/ComfyUI) - A powerful and modular stable diffusion GUI.

WASasquatch/[was-node-suite-comfyui](https://github.com/WASasquatch/was-node-suite-comfyui) - A powerful custom node extensions of ComfyUI.

TinyTerra/[ComfyUI_tinyterraNodes](https://github.com/TinyTerra/ComfyUI_tinyterraNodes) - A selection of nodes for Stable Diffusion ComfyUI

hnmr293/[ComfyUI-nodes-hnmr](https://github.com/hnmr293/ComfyUI-nodes-hnmr) - ComfyUI custom nodes - merge, grid (aka xyz-plot) and others

SeargeDP/[SeargeSDXL](https://github.com/SeargeDP) - ComfyUI custom nodes - Prompt nodes and Conditioning nodes

LucianoCirino/[efficiency-nodes-comfyui](https://github.com/LucianoCirino/efficiency-nodes-comfyui) - A collection of ComfyUI custom nodes.

SLAPaper/[ComfyUI-Image-Selector](https://github.com/SLAPaper/ComfyUI-Image-Selector) - Select one or some of images from a batch
