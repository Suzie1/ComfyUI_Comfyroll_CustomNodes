# By Suzie1 and RockOfFire
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to
# deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
@author: Suzie1
@title: Comfyroll Studio
@nickname: Comfyroll Studio
@description: 162 custom nodes for Graphics, Animation, IO, Aspect Ratio, Model Merge, ControlNet, LoRA, XY Grid, and Utilities.
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

print("------------------------------------------------")    
print("\033[34mComfyroll Custom Nodes v1.54 : \033[92m 162 Nodes Loaded\033[0m")
print("------------------------------------------------")  

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

