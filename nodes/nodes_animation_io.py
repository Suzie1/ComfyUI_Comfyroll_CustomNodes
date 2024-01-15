#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi   https://github.com/Suzie1/CR-Animation-Nodes
# for ComfyUI                                     https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

from PIL import Image, ImageSequence
import comfy.sd
import re
import torch
import numpy as np
import os
import sys
import folder_paths
import math
import json
import csv
from typing import List
from PIL.PngImagePlugin import PngInfo
from nodes import SaveImage
import glob
from ..categories import icons

#MAX_RESOLUTION=8192
ALLOWED_EXT = ('.jpeg', '.jpg', '.png', '.tiff', '.gif', '.bmp', '.webp')

def resolve_pattern(pattern):
    folder_path, file_pattern = os.path.split(pattern)
    frame_pattern = re.sub(r"#+", "*", file_pattern)
    matching_files = glob.glob(os.path.join(folder_path, frame_pattern))
    #print(f"[Debug] Found {len(matching_files)} matching files for frame pattern {frame_pattern}")
    return matching_files

def get_files(image_path, sort_by="Index", pattern=None):
    if pattern is not None:
        matching_files = resolve_pattern(os.path.join(image_path, pattern))
    else:
        matching_files = os.listdir(image_path)

    if sort_by == "Index":
        sorted_files = sorted(matching_files, key=lambda s: sum(((s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)), ()))
    elif sort_by == "Alphabetic":
        sorted_files = sorted(matching_files, key=lambda s: (re.split(r'(\d+)', s), s))
    else:
        raise ValueError("Invalid sort_by value. Use 'Index' or 'Alphabetic'.")

    return sorted_files
    
#---------------------------------------------------------------------------------------------------------------------#
# NODES
#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadAnimationFrames:
    #input_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'input')
    input_dir = folder_paths.input_directory
    #print(f"CR_LoadAnimationFrames: input directory {input_dir}")
    @classmethod
    def INPUT_TYPES(s):
        #if not os.path.exists(s.input_dir):
            #os.makedirs(s.input_dir)
        image_folder = [name for name in os.listdir(s.input_dir) if os.path.isdir(os.path.join(s.input_dir,name)) and len(os.listdir(os.path.join(s.input_dir,name))) != 0]
        return {"required":
                    {"image_sequence_folder": (sorted(image_folder), ),
                     "start_index": ("INT", {"default": 1, "min": 1, "max": 10000}),
                     "max_frames": ("INT", {"default": 1, "min": 1, "max": 10000})
                     }
                }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    FUNCTION = "load_image_sequence"
    CATEGORY = icons.get("Comfyroll/Animation/IO")

    def load_image_sequence(self, image_sequence_folder, start_index, max_frames):
        image_path = os.path.join(self.input_dir, image_sequence_folder)
        file_list = sorted(os.listdir(image_path), key=lambda s: sum(((s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)), ()))
        sample_frames = []
        sample_frames_mask = []
        sample_index = list(range(start_index-1, len(file_list), 1))[:max_frames]
        for num in sample_index:
            i = Image.open(os.path.join(image_path, file_list[num]))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            image = image.squeeze()
            sample_frames.append(image)
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/IO-Nodes#cr-load-animation-frames"                        
        return (torch.stack(sample_frames), show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadFlowFrames:
# based on Load Image Sequence in vid2vid and mtb
    @classmethod
    def INPUT_TYPES(s):
    
        sort_methods = ["Index", "Alphabetic"]
        #sort_methods = ["Date modified", "Alphabetic", "Index"]
        input_dir = folder_paths.input_directory

        input_folders = [name for name in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,name)) and len(os.listdir(os.path.join(input_dir,name))) != 0]

        return {"required":
                    {"input_folder": (sorted(input_folders), ),
                     "sort_by": (sort_methods, ),
                     "current_frame": ("INT", {"default": 0, "min": 0, "max": 10000, "forceInput": True}),
                     "skip_start_frames": ("INT", {"default": 0, "min": 0, "max": 10000}),
                     },
                "optional":
                    {"input_path": ("STRING", {"default": '', "multiline": False}),
                     "file_pattern": ("STRING", {"default": '*.png', "multiline": False}),
                    } 
                }

    CATEGORY = icons.get("Comfyroll/Animation/IO")

    RETURN_TYPES = ("IMAGE", "IMAGE", "INT", "STRING", )
    RETURN_NAMES = ("current_image", "previous_image", "current_frame", "show_help", )
    FUNCTION = "load_images"

    def load_images(self, file_pattern, skip_start_frames, input_folder, sort_by, current_frame, input_path=''):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/IO-Nodes#cr-load-flow-frames"

        input_dir = folder_paths.input_directory
        
        current_frame = current_frame + skip_start_frames
        print(f"[Info] CR Load Flow Frames: current_frame {current_frame}")
            
        if input_path != '':
            if not os.path.exists(input_path):
                print(f"[Warning] CR Load Flow Frames: The input_path `{input_path}` does not exist")
                return ("", )
            image_path = os.path.join('', input_path)
        else:
            image_path = os.path.join(input_dir, input_folder)

        print(f"[Info] CR Load Flow Frames: ComfyUI Input directory is `{image_path}`")
        
        file_list = get_files(image_path, sort_by, file_pattern) 
         
        if os.path.exists(image_path + '.DS_Store'):
            file_list.remove('.DS_Store') # For Mac users
            
        if len(file_list) == 0:
            print(f"[Warning] CR Load Flow Frames: No matching files found for loading")
            return ()
         
        remaining_files = len(file_list) - current_frame   
        print(f"[Info] CR Load Flow Frames: {remaining_files} input files remaining for processing")

        img = Image.open(os.path.join(image_path, file_list[current_frame]))
        cur_image = img.convert("RGB")
        cur_image = np.array(cur_image).astype(np.float32) / 255.0
        cur_image = torch.from_numpy(cur_image)[None,]
        print(f"[Debug] CR Load Flow Frames: Current image {file_list[current_frame]}")        

        # Load first frame as previous frame if no frames skipped
        if current_frame == 0 and skip_start_frames == 0:
            img = Image.open(os.path.join(image_path, file_list[current_frame]))
            pre_image = img.convert("RGB")
            pre_image = np.array(pre_image).astype(np.float32) / 255.0
            pre_image = torch.from_numpy(pre_image)[None,] 
            print(f"[Debug] CR Load Flow Frames: Previous image {file_list[current_frame]}")               
        else:
            img = Image.open(os.path.join(image_path, file_list[current_frame - 1]))
            pre_image = img.convert("RGB")
            pre_image = np.array(pre_image).astype(np.float32) / 255.0
            pre_image = torch.from_numpy(pre_image)[None,] 
            print(f"[Debug] CR Load Flow Frames: Previous image {file_list[current_frame - 1]}")            

        return (cur_image, pre_image, current_frame, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_OutputFlowFrames:
# based on SaveImageSequence by mtb

    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
    
        output_dir = folder_paths.output_directory
        output_folders = [name for name in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir,name)) and len(os.listdir(os.path.join(output_dir,name))) != 0]
    
        return {
            "required": {"output_folder": (sorted(output_folders), ),
                         "current_image": ("IMAGE", ),
                         "filename_prefix": ("STRING", {"default": "CR"}),
                         "current_frame": ("INT", {"default": 0, "min": 0, "max": 9999999, "forceInput": True}),
            },
            "optional": {"interpolated_img": ("IMAGE", ),
                         "output_path": ("STRING", {"default": '', "multiline": False}),           
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = icons.get("Comfyroll/Animation/IO")

    def save_images(self, output_folder, current_image, current_frame, output_path='', filename_prefix="CR", interpolated_img=None):
    
        output_dir = folder_paths.get_output_directory()  
        out_folder = os.path.join(output_dir, output_folder)
        
        if output_path != '':
            if not os.path.exists(output_path):
                print(f"[Warning] CR Output Flow Frames: The input_path `{output_path}` does not exist")
                return ("",)
            out_path = output_path     # os.path.join("", output_path)
        else:
            out_path = os.path.join(output_dir, out_folder)
        print(f"[Info] CR Output Flow Frames: Output path is `{out_path}`")
        
        if interpolated_img is not None:
        
            output_image0 = current_image[0].cpu().numpy()
            output_image1 = interpolated_img[0].cpu().numpy()
        
            img0 = Image.fromarray(np.clip(output_image0 * 255.0, 0, 255).astype(np.uint8))
            img1 = Image.fromarray(np.clip(output_image1 * 255.0, 0, 255).astype(np.uint8))
        
            output_filename0 = f"{filename_prefix}_{current_frame:05}_0.png"
            output_filename1 = f"{filename_prefix}_{current_frame:05}_1.png"
            print(f"[Warning] CR Output Flow Frames: Saved {filename_prefix}_{current_frame:05}_0.png")
            print(f"[Warning] CR Output Flow Frames: Saved {filename_prefix}_{current_frame:05}_1.png")
            
            resolved_image_path0 = out_path + "/" + output_filename0
            resolved_image_path1 = out_path + "/" + output_filename1

            img0.save(resolved_image_path0, pnginfo="", compress_level=4)
            img1.save(resolved_image_path1, pnginfo="", compress_level=4)            
        else:
            output_image0 = current_image[0].cpu().numpy()
            img0 = Image.fromarray(np.clip(output_image0 * 255.0, 0, 255).astype(np.uint8))
            output_filename0 = f"{filename_prefix}_{current_frame:05}.png"
            resolved_image_path0 = out_path + "/" + output_filename0
            img0.save(resolved_image_path0, pnginfo="", compress_level=4)
            print(f"[Info] CR Output Flow Frames: Saved {filename_prefix}_{current_frame:05}.png")

        result = {"ui": {"images": [{"filename": output_filename0,"subfolder": out_path,"type": self.type,}]}}
        
        return result

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 3 nodes released
'''
NODE_CLASS_MAPPINGS = {
    # IO
    "CR Load Animation Frames":CR_LoadAnimationFrames,
    "CR Load Flow Frames":CR_LoadFlowFrames,
    "CR Output Flow Frames":CR_OutputFlowFrames,
}
'''

