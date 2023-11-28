# 🧩 Comfyroll Custom Nodes - Patch Notes

## PR40 Nov 27, 2023

__Added nodes__

    CR Select Model

    * allows selection of model from one of 5 presets 

__Changed Nodes__

    CR Simple Text Watermark

    * added batch support
    * added custom font hex color

    CR Aspect Ratio

    * changed descriptions in aspect_ratios for issue 24

__Other Changes__

    - changed preset RGB for brown to 160, 85, 15  

## PR39 Nov 26, 2023

__Changed Nodes__

    CR Halftone Filter

    * changed handling for RGBA inputs 

## PR38 Nov 26, 2023

 __Added nodes__

    CR Aspect Ratio

    * combines aspect ratio options for both SD1.5 and SDXL
    * includes empty_latent output

__Changed Nodes__

    CR Halftone Filter

    * added resolution options 
    * modified antialias_scale parameters

    CR SDXL Aspect Ratio

    * added empty_latent output  

    CR SD1.5 Aspect Ratio

    * added empty_latent output  

## PR37 Nov 19, 2023

__Added Nodes__

    CR Simple Text Watermark

    * adds a text watermark to an image

__Other Changes__

    * Merged CR Animation Nodes into Comfyroll custom Nodes
    * added CR Animation Nodes demo workflows
    * added reduce_opacity function in graphics_functions

