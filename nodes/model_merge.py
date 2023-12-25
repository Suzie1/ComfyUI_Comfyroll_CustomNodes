#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import comfy.sd
import comfy.model_management
import folder_paths
from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#                        
# Model Merge Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_ModelMergeStack:
    
    @classmethod
    def INPUT_TYPES(cls):
    
        checkpoint_files = ["None"] + folder_paths.get_filename_list("checkpoints")
        
        return {"required": {"switch_1": (["Off","On"],),
                             "ckpt_name1": (checkpoint_files,),
                             "model_ratio1": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                             "clip_ratio1": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                             #
                             "switch_2": (["Off","On"],),
                             "ckpt_name2": (checkpoint_files,),
                             "model_ratio2": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                             "clip_ratio2": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                             #
                             "switch_3": (["Off","On"],),
                             "ckpt_name3": (checkpoint_files,),
                             "model_ratio3": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                             "clip_ratio3": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                            },      
                "optional":{
                             "model_stack": ("MODEL_STACK",),
                },
        }

    RETURN_TYPES = ("MODEL_STACK", "STRING", )
    RETURN_NAMES = ("MODEL_STACK", "show_help", )
    FUNCTION = "list_checkpoints"
    CATEGORY = icons.get("Comfyroll/Model Merge")

    def list_checkpoints(self, switch_1, ckpt_name1, model_ratio1, clip_ratio1, switch_2, ckpt_name2, model_ratio2, clip_ratio2, switch_3, ckpt_name3, model_ratio3, clip_ratio3, model_stack=None):
    
        # Initialise the list
        model_list = list()
    
        if model_stack is not None:
            model_list.extend([l for l in model_stack if l[0] != "None"])
        
        if ckpt_name1 != "None" and  switch_1 == "On":
            model_list.extend([(ckpt_name1, model_ratio1, clip_ratio1)]),

        if ckpt_name2 != "None" and  switch_2 == "On":
            model_list.extend([(ckpt_name2, model_ratio2, clip_ratio2)]),

        if ckpt_name3 != "None" and  switch_3 == "On":
            model_list.extend([(ckpt_name3, model_ratio3, clip_ratio3)]),

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Model-Merge-Nodes#cr-model-stack"
        
        return (model_list, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ApplyModelMerge:

    @classmethod
    def INPUT_TYPES(s):
    
        merge_methods = ["Recursive", "Weighted"]
        
        return {"required": {"model_stack": ("MODEL_STACK",),
                             "merge_method": (merge_methods,),
                             "normalise_ratios": (["Yes","No"],),
                             "weight_factor":("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                            }
        }
        
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", )
    RETURN_NAMES = ("MODEL", "CLIP", "model_mix_info", "show_help", )
    FUNCTION = "merge"
    CATEGORY = icons.get("Comfyroll/Model Merge")

    def merge(self, model_stack, merge_method, normalise_ratios, weight_factor):
    
        # Initialise
        sum_clip_ratio = 0
        sum_model_ratio = 0
        model_mix_info = str("Merge Info:\n")
             
        # If no models
        if len(model_stack) == 0:
            print(f"[Warning] Apply Model Merge: No active models selected in the model merge stack")
            return()

        # If only one model
        if len(model_stack) == 1:
            print(f"[Warning] Apply Model Merge: Only one active model found in the model merge stack. At least 2 models are normally needed for merging. The active model will be output.")
            model_name, model_ratio, clip_ratio = model_stack[0]
            ckpt_path = folder_paths.get_full_path("checkpoints", model_name)
            return comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
        
        # Calculate ratio sums for normalisation        
        for i, model_tuple in enumerate(model_stack):
            model_name, model_ratio, clip_ratio = model_tuple
            sum_model_ratio += model_ratio                
            sum_clip_ratio += clip_ratio
   
        # Do recursive merge loops
        model_mix_info = model_mix_info + "Ratios are applied using the Recursive method\n\n"
        
        # Loop through the models and compile the merged model
        for i, model_tuple in enumerate(model_stack):
            model_name, model_ratio, clip_ratio = model_tuple
            ckpt_path = folder_paths.get_full_path("checkpoints", model_name)
            merge_model = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
            print(f"Apply Model Merge: Model Name {model_name}, Model Ratio {model_ratio}, CLIP Ratio {clip_ratio}")

            if sum_model_ratio != 1 and normalise_ratios == "Yes":
                print(f"[Warning] Apply Model Merge: Sum of model ratios != 1. Ratios will be normalised")
                # Normalise the ratios  
                model_ratio = round(model_ratio / sum_model_ratio, 2)
                clip_ratio = round(clip_ratio / sum_clip_ratio, 2)
            
            # Weighted merge method
            if merge_method == "Weighted":
                if i == 1:
                    # Reassign extra weight to the second model
                    model_ratio = 1 - weight_factor + (weight_factor * model_ratio)
                    clip_ratio = 1 - weight_factor + (weight_factor * clip_ratio)
                      
            #Clone the first model
            if i == 0: 
                model1 = merge_model[0].clone()
                clip1 = merge_model[1].clone()
                
                model_mix_info = model_mix_info + "Base Model Name: " + model_name
            else:
                # Merge next model
                # Comfy merge logic is flipped for stacked nodes. This is because the first model is effectively model1 and all subsequent models are model2. 
                model2 = merge_model[0].clone()
                kp = model2.get_key_patches("diffusion_model.")
                for k in kp:
                    #model1.add_patches({k: kp[k]}, 1.0 - model_ratio, model_ratio) #original logic
                    model1.add_patches({k: kp[k]}, model_ratio, 1.0 - model_ratio) #flipped logic
                # Merge next clip
                clip2 = merge_model[1].clone()          
                kp = clip2.get_key_patches()
                for k in kp:
                    if k.endswith(".position_ids") or k.endswith(".logit_scale"):
                        continue
                    #clip1.add_patches({k: kp[k]}, 1.0 - clip_ratio, clip_ratio) #original logic
                    clip1.add_patches({k: kp[k]}, clip_ratio, 1.0 - clip_ratio) #flipped logic
            
            # Update model info                
                model_mix_info = model_mix_info + "\nModel Name: " + model_name + "\nModel Ratio: " + str(model_ratio) + "\nCLIP Ratio: " + str(clip_ratio) + "\n"

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Model-Merge-Nodes#cr-apply-model-merge"
                
        return (model1, clip1, model_mix_info, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Apply Model Merge": CR_ApplyModelMerge,
    "CR Model Merge Stack": CR_ModelMergeStack,
}
'''


