#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import os
import sys
import comfy.sd
import comfy.utils
import folder_paths
import hashlib
from random import random, uniform
from ..categories import icons

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

#---------------------------------------------------------------------------------------------------------------------#
# LoRA Nodes
#---------------------------------------------------------------------------------------------------------------------#
# This is a load lora node with an added switch to turn on or off.  On will add the lora and off will skip the node.
class CR_LoraLoader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
    
        file_list = folder_paths.get_filename_list("loras")
        file_list.insert(0, "None")
        
        return {"required": { "model": ("MODEL",),
                              "clip": ("CLIP", ),
                              "switch": (["On","Off"],),
                              "lora_name": (file_list, ),
                              "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                              "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "show_help", )
    FUNCTION = "load_lora"
    CATEGORY = icons.get("Comfyroll/LoRA")

    def load_lora(self, model, clip, switch, lora_name, strength_model, strength_clip):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/LoRA-Nodes#cr-load-lora"
        if strength_model == 0 and strength_clip == 0:
            return (model, clip, show_help, )

        if switch == "Off" or  lora_name == "None":
            return (model, clip, show_help, )

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                del self.loaded_lora

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        return (model_lora, clip_lora, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# Based on Efficiency Nodes
# This is a lora stack where a single node has 3 different loras each with their own switch
class CR_LoRAStack:

    @classmethod
    def INPUT_TYPES(cls):
    
        loras = ["None"] + folder_paths.get_filename_list("loras")
        
        return {"required": {
                    "switch_1": (["Off","On"],),
                    "lora_name_1": (loras,),
                    "model_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "switch_2": (["Off","On"],),
                    "lora_name_2": (loras,),
                    "model_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "switch_3": (["Off","On"],),
                    "lora_name_3": (loras,),
                    "model_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                },
                "optional": {"lora_stack": ("LORA_STACK",)
                },
        }

    RETURN_TYPES = ("LORA_STACK", "STRING", )
    RETURN_NAMES = ("LORA_STACK", "show_help", )
    FUNCTION = "lora_stacker"
    CATEGORY = icons.get("Comfyroll/LoRA")

    def lora_stacker(self, lora_name_1, model_weight_1, clip_weight_1, switch_1, lora_name_2, model_weight_2, clip_weight_2, switch_2, lora_name_3, model_weight_3, clip_weight_3, switch_3, lora_stack=None):

        # Initialise the list
        lora_list=list()
        
        if lora_stack is not None:
            lora_list.extend([l for l in lora_stack if l[0] != "None"])
        
        if lora_name_1 != "None" and  switch_1 == "On":
            lora_list.extend([(lora_name_1, model_weight_1, clip_weight_1)]),

        if lora_name_2 != "None" and  switch_2 == "On":
            lora_list.extend([(lora_name_2, model_weight_2, clip_weight_2)]),

        if lora_name_3 != "None" and  switch_3 == "On":
            lora_list.extend([(lora_name_3, model_weight_3, clip_weight_3)]),
           
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/LoRA-Nodes#cr-lora-stack"           

        return (lora_list, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# This applies the lora stack.
class CR_ApplyLoRAStack:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"model": ("MODEL",),
                            "clip": ("CLIP", ),
                            "lora_stack": ("LORA_STACK", ),
                            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "show_help", )
    FUNCTION = "apply_lora_stack"
    CATEGORY = icons.get("Comfyroll/LoRA")

    def apply_lora_stack(self, model, clip, lora_stack=None,):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/LoRA-Nodes#cr-apply-lora-stack"

        # Initialise the list
        lora_params = list()
 
        # Extend lora_params with lora-stack items 
        if lora_stack:
            lora_params.extend(lora_stack)
        else:
            return (model, clip, show_help,)

        # Initialise the model and clip
        model_lora = model
        clip_lora = clip

        # Loop through the list
        for tup in lora_params:
            lora_name, strength_model, strength_clip = tup
            
            lora_path = folder_paths.get_full_path("loras", lora_name)
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            
            model_lora, clip_lora = comfy.sd.load_lora_for_models(model_lora, clip_lora, lora, strength_model, strength_clip)  

        return (model_lora, clip_lora, show_help,)

#---------------------------------------------------------------------------------------------------------------------#
# This is adds to a LoRA stack chain, which produces a LoRA instance with a randomized weight within a range.
# Stride sets the number of iterations before weight is re-randomized.
class CR_RandomWeightLoRA:

    @classmethod
    def INPUT_TYPES(cls):

        loras = ["None"] + folder_paths.get_filename_list("loras")

        return {"required": {
                    "stride": (("INT", {"default": 1, "min": 1, "max": 1000})),
                    "force_randomize_after_stride": (["Off","On"],),
                    "lora_name": (loras,),
                    "switch": (["Off","On"],),
                    "weight_min": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "weight_max": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                },
                "optional": {"lora_stack": ("LORA_STACK",)
                },
        }

    RETURN_TYPES = ("LORA_STACK",)
    FUNCTION = "random_weight_lora"
    CATEGORY = icons.get("Comfyroll/LoRA")

    LastWeightMap = {}
    StridesMap = {}
    LastHashMap = {}

    @staticmethod
    def getIdHash(lora_name: str, force_randomize_after_stride, stride, weight_min, weight_max, clip_weight) -> int:
        fl_str = f"{lora_name}_{force_randomize_after_stride}_{stride}_{weight_min:.2f}_{weight_max:.2f}_{clip_weight:.2f}"
        return hashlib.sha256(fl_str.encode('utf-8')).hexdigest()

    @classmethod
    def IS_CHANGED(cls, stride, force_randomize_after_stride, lora_name, switch, weight_min, weight_max, clip_weight, lora_stack=None):     
        id_hash = CR_RandomWeightLoRA.getIdHash(lora_name, force_randomize_after_stride, stride, weight_min, weight_max, clip_weight)

        if switch == "Off":
            return id_hash + "_Off"
        if lora_name == "None":
            return id_hash

        if id_hash not in CR_RandomWeightLoRA.StridesMap:
            CR_RandomWeightLoRA.StridesMap[id_hash] = 0

        CR_RandomWeightLoRA.StridesMap[id_hash] += 1

        if stride > 1 and CR_RandomWeightLoRA.StridesMap[id_hash] < stride and id_hash in CR_RandomWeightLoRA.LastHashMap:
            return CR_RandomWeightLoRA.LastHashMap[id_hash]
        else:
            CR_RandomWeightLoRA.StridesMap[id_hash] = 0

        last_weight = CR_RandomWeightLoRA.LastWeightMap.get(id_hash, None)
        weight = uniform(weight_min, weight_max)

        if last_weight is not None:
            while weight == last_weight:
                weight = uniform(weight_min, weight_max)

        CR_RandomWeightLoRA.LastWeightMap[id_hash] = weight 

        hash_str = f"{id_hash}_{weight:.3f}"
        CR_RandomWeightLoRA.LastHashMap[id_hash] = hash_str
        return hash_str

    def random_weight_lora(self, stride, force_randomize_after_stride, lora_name, switch, weight_min, weight_max, clip_weight, lora_stack=None):
        id_hash = CR_RandomWeightLoRA.getIdHash(lora_name, force_randomize_after_stride, stride, weight_min, weight_max, clip_weight)

        # Initialise the list
        lora_list=list()

        if lora_stack is not None:
            lora_list.extend([l for l in lora_stack if l[0] != "None"])

        weight = CR_RandomWeightLoRA.LastWeightMap.get(id_hash, 0.0)

        if lora_name != "None" and switch == "On":
            lora_list.extend([(lora_name, weight, clip_weight)]),

        return (lora_list,)

#---------------------------------------------------------------------------------------------------------------------#
# This is a lora stack where a single node has 3 different loras which can be applied randomly. Exclusive mode causes only one lora to be applied.
# If exclusive mode is on, each LoRA's chance of being applied is evaluated, and the lora with the highest chance is applied
# Stride sets the minimum number of cycles before a re-randomization is performed.
class CR_RandomLoRAStack:

    @classmethod
    def INPUT_TYPES(cls):

        loras = ["None"] + folder_paths.get_filename_list("loras")

        return {"required": {
                    "exclusive_mode": (["Off","On"],),
                    "stride": (("INT", {"default": 1, "min": 1, "max": 1000})),
                    "force_randomize_after_stride": (["Off","On"],),
                    "lora_name_1": (loras,),
                    "switch_1": (["Off","On"],),
                    "chance_1": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                    "model_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "lora_name_2": (loras,),
                    "switch_2": (["Off","On"],),
                    "chance_2": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                    "model_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "lora_name_3": (loras,),
                    "switch_3": (["Off","On"],),
                    "chance_3": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                    "model_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                    "clip_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                },
                "optional": {"lora_stack": ("LORA_STACK",)
                },
        }

    RETURN_TYPES = ("LORA_STACK",)
    FUNCTION = "random_lora_stacker"
    CATEGORY = icons.get("Comfyroll/LoRA")

    UsedLorasMap = {}
    StridesMap = {}
    LastHashMap = {}

    @staticmethod
    def getIdHash(lora_name_1: str, lora_name_2: str, lora_name_3: str) -> int:
        id_set = set([lora_name_1, lora_name_2, lora_name_3])
        id_hash = hash(frozenset(id_set))
        return id_hash

    @staticmethod
    def deduplicateLoraNames(lora_name_1: str, lora_name_2: str, lora_name_3: str):
        is_same_1 = False
        is_same_2 = False
        is_same_3 = False

        if lora_name_1 == lora_name_2:
            is_same_1 = True
            is_same_2 = True
        if lora_name_1 == lora_name_3:
            is_same_1 = True
            is_same_3 = True
        if lora_name_2 == lora_name_3:
            is_same_2 = True
            is_same_3 = True

        if is_same_1:
            lora_name_1 = lora_name_1 + "CR_RandomLoRAStack_1"
        if is_same_2:
            lora_name_2 = lora_name_2 + "CR_RandomLoRAStack_2"
        if is_same_3:
            lora_name_3 = lora_name_3 + "CR_RandomLoRAStack_3"

        return lora_name_1, lora_name_2, lora_name_3

    @staticmethod
    def cleanLoraName(lora_name) -> str:
        if "CR_RandomLoRAStack_1" in lora_name:
            lora_name = lora_name.replace("CR_RandomLoRAStack_1", "")
        elif "CR_RandomLoRAStack_2" in lora_name:
            lora_name = lora_name.replace("CR_RandomLoRAStack_2", "")
        elif "CR_RandomLoRAStack_3" in lora_name:
            lora_name = lora_name.replace("CR_RandomLoRAStack_3", "")
        return lora_name


    @classmethod
    def IS_CHANGED(cls, exclusive_mode, stride, force_randomize_after_stride, lora_name_1, model_weight_1, clip_weight_1, switch_1, chance_1, lora_name_2,
                    model_weight_2, clip_weight_2, switch_2, chance_2, lora_name_3, model_weight_3, clip_weight_3, switch_3, chance_3, lora_stack=None):     
        lora_set = set()

        lora_name_1, lora_name_2, lora_name_3 = CR_RandomLoRAStack.deduplicateLoraNames(lora_name_1, lora_name_2, lora_name_3)        
        id_hash = CR_RandomLoRAStack.getIdHash(lora_name_1, lora_name_2, lora_name_3)

        if id_hash not in CR_RandomLoRAStack.StridesMap:
            CR_RandomLoRAStack.StridesMap[id_hash] = 0

        CR_RandomLoRAStack.StridesMap[id_hash] += 1

        if stride > 1 and CR_RandomLoRAStack.StridesMap[id_hash] < stride and id_hash in CR_RandomLoRAStack.LastHashMap:
            return CR_RandomLoRAStack.LastHashMap[id_hash]
        else:
            CR_RandomLoRAStack.StridesMap[id_hash] = 0

        total_on = 0
        if lora_name_1 != "None" and switch_1 == "On" and chance_1 > 0.0: total_on += 1
        if lora_name_2 != "None" and switch_2 == "On" and chance_2 > 0.0: total_on += 1
        if lora_name_3 != "None" and switch_3 == "On" and chance_3 > 0.0: total_on += 1

        def perform_randomization() -> set:    
            _lora_set = set()

            rand_1 = random()
            rand_2 = random()
            rand_3 = random()

            apply_1 = True if (rand_1 <= chance_1 and switch_1 == "On") else False
            apply_2 = True if (rand_2 <= chance_2 and switch_2 == "On") else False
            apply_3 = True if (rand_3 <= chance_3 and switch_3 == "On") else False

            num_to_apply = sum([apply_1, apply_2, apply_3])

            if exclusive_mode == "On" and num_to_apply > 1:
                rand_dict = {}
                if apply_1: rand_dict[1] = rand_1
                if apply_2: rand_dict[2] = rand_2
                if apply_3: rand_dict[3] = rand_3
                sorted_rands = sorted(rand_dict.keys(), key=lambda k: rand_dict[k])
                if sorted_rands[0] == 1:
                    apply_2 = False
                    apply_3 = False
                elif sorted_rands[0] == 2:
                    apply_1 = False
                    apply_3 = False
                elif sorted_rands[0] == 3:
                    apply_1 = False
                    apply_2 = False

            if lora_name_1 != "None" and switch_1 == "On" and apply_1:
                _lora_set.add(lora_name_1)
            if lora_name_2 != "None" and switch_2 == "On" and apply_2:
                _lora_set.add(lora_name_2)
            if lora_name_3 != "None" and switch_3 == "On" and apply_3:
                _lora_set.add(lora_name_3)
            return _lora_set

        last_lora_set = CR_RandomLoRAStack.UsedLorasMap.get(id_hash, set())
        lora_set = perform_randomization()

        if force_randomize_after_stride == "On" and len(last_lora_set) > 0 and total_on > 1:
            while lora_set == last_lora_set:
                lora_set = perform_randomization()

        CR_RandomLoRAStack.UsedLorasMap[id_hash] = lora_set        

        hash_str = str(hash(frozenset(lora_set)))
        CR_RandomLoRAStack.LastHashMap[id_hash] = hash_str
        return hash_str

    def random_lora_stacker(self, exclusive_mode, stride, force_randomize_after_stride, lora_name_1, model_weight_1, clip_weight_1, switch_1, chance_1, lora_name_2,
                    model_weight_2, clip_weight_2, switch_2, chance_2, lora_name_3, model_weight_3, clip_weight_3, switch_3, chance_3, lora_stack=None):

        # Initialise the list
        lora_list=list()

        if lora_stack is not None:
            lora_list.extend([l for l in lora_stack if l[0] != "None"])

        lora_name_1, lora_name_2, lora_name_3 = CR_RandomLoRAStack.deduplicateLoraNames(lora_name_1, lora_name_2, lora_name_3)
        id_hash = CR_RandomLoRAStack.getIdHash(lora_name_1, lora_name_2, lora_name_3)

        used_loras = CR_RandomLoRAStack.UsedLorasMap.get(id_hash, set())

        if lora_name_1 != "None" and switch_1 == "On" and lora_name_1 in used_loras:
            lora_list.extend([(CR_RandomLoRAStack.cleanLoraName(lora_name_1), model_weight_1, clip_weight_1)]),

        if lora_name_2 != "None" and switch_2 == "On" and lora_name_2 in used_loras:
            lora_list.extend([(CR_RandomLoRAStack.cleanLoraName(lora_name_2), model_weight_2, clip_weight_2)]),

        if lora_name_3 != "None" and switch_3 == "On" and lora_name_3 in used_loras:
            lora_list.extend([(CR_RandomLoRAStack.cleanLoraName(lora_name_3), model_weight_3, clip_weight_3)]),

        return (lora_list,)

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Load LoRA": CR_LoraLoader,
    "CR LoRA Stack":CR_LoRAStack,
    "CR Apply LoRA Stack":CR_ApplyLoRAStack,
    "CR Random LoRA Stack":CR_RandomLoRAStack,
    "CR Random Weight LoRA":CR_RandomWeightLoRA,    
}
'''
