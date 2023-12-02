# 🧩 Comfyroll Custom Nodes - Patch Notes

## PR54 Dec 2, 2023

__Other Changes__
	
	- added show-help outputs on animation nodes with links to wiki
	
## PR51, PR52 Dec 2, 2023	

__Added Nodes__

	CR Random RGB

## PR50 Dec 1, 2023

__Other Changes__
	
	- added show-help outputs with links to wiki

## PR48 Nov 30, 2023

__Other Changes__

	- disabled CR Load Prompt Style
	- rename classes on logic nodes
	- increased max sizes on Aspect Ratio nodes

## PR45 Nov 29, 2023

__Added Nodes__

	CR Random Hex Color

__Changed Nodes__

    CR Color Tint 

    - added custom color
	
	CR Simple Text Panel
	
	- added outline text
	
__Other Changes__
	
	- added demo workflows
	
## PR44 Nov 28, 2023

__Changed Nodes__

    CR Select Model

    - added ckpt_name output
	
__Other Changes__

    - added new Patch Notes page 	

## PR40 Nov 27, 2023

__Added Nodes__

    CR Select Model

    - allows selection of model from one of 5 preset models 

__Changed Nodes__

    CR Simple Text Watermark

    - added batch support
    - added custom font hex color

    CR Aspect Ratio

    - changed descriptions in aspect_ratios for issue 24
	
	CR Upscale Image

    - fixed issue with batched images

__Other Changes__

    - changed preset RGB for brown to 160, 85, 15  


## PR39 Nov 26, 2023

__Changed Nodes__

    CR Halftone Filter

    - changed handling for RGBA inputs 


## PR38 Nov 26, 2023

 __Added Nodes__

    CR Aspect Ratio

    - combines aspect ratio options for both SD1.5 and SDXL
    - includes empty_latent output

__Changed Nodes__

    CR Halftone Filter

    - added resolution options 
    - modified antialias_scale parameters

    CR SDXL Aspect Ratio

    - added empty_latent output  

    CR SD1.5 Aspect Ratio

    - added empty_latent output  


## PR37 Nov 19, 2023

__Added Nodes__

    CR Simple Text Watermark

    - adds a text watermark to an image

__Other Changes__

    - merged CR Animation Nodes into Comfyroll custom Nodes
    - added CR Animation Nodes demo workflows
    - added reduce_opacity function in graphics_functions

