"""
@author: Suzie1
@title: Comfyroll Custom Nodes
@nickname: Comfyroll Custom Nodes
@description: 148 custom nodes for Graphics, Animation, IO, Aspect Ratio, Model Merge, ControlNet, LoRA, XY Grid, and Utilities.
"""

from .live_node_mappings import LIVE_NODE_CLASS_MAPPINGS, LIVE_NODE_DISPLAY_NAME_MAPPINGS

INCLUDE_DEV_NODES = False

try:
    if INCLUDE_DEV_NODES:
        from .dev_node_mappings import DEV_NODE_CLASS_MAPPINGS, DEV_NODE_DISPLAY_NAME_MAPPINGS
        NODE_CLASS_MAPPINGS = {**DEV_NODE_CLASS_MAPPINGS, **LIVE_NODE_CLASS_MAPPINGS}
        NODE_DISPLAY_NAME_MAPPINGS = {**DEV_NODE_DISPLAY_NAME_MAPPINGS, **LIVE_NODE_DISPLAY_NAME_MAPPINGS}
        print("\033[34mComfyroll Custom Nodes: \033[92mDev Nodes Loaded\033[0m")
    else:
        NODE_CLASS_MAPPINGS = LIVE_NODE_CLASS_MAPPINGS
        NODE_DISPLAY_NAME_MAPPINGS = LIVE_NODE_DISPLAY_NAME_MAPPINGS
except ImportError:
    NODE_CLASS_MAPPINGS = LIVE_NODE_CLASS_MAPPINGS
    NODE_DISPLAY_NAME_MAPPINGS = LIVE_NODE_DISPLAY_NAME_MAPPINGS

print("-----------------------------------------------")    
print("\033[34mComfyroll Custom Nodes v1.47 : \033[92m 148 Nodes Loaded\033[0m")
print("-----------------------------------------------")  

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

