#---------------------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/CR-Animation-Nodes 
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#---------------------------------------------------------------------------------------------------------------------#

from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
class CR_JobList:

    @classmethod
    def INPUT_TYPES(s):
        job_types = ["Input", "Batch Process", "Output"] 
        return {"required":{
                    "job_desc1": ("STRING", {"default": "job description", "multiline": True}),
                    "job_type1": (job_types,),
                    "job_alias1": ("STRING", {"default": "", "multiline": False}),
                    "job_desc2": ("STRING", {"default": "job description", "multiline": True}),
                    "job_type2": (job_types,),
                    "job_alias2": ("STRING", {"default": "", "multiline": False}),
                    "job_desc3": ("STRING", {"default": "job description", "multiline": True}),
                    "job_type3": (job_types,),
                    "job_alias3": ("STRING", {"default": "", "multiline": False}),                    
                    },
                "optional": {"job": ("JOB",),
                }
        }

    RETURN_TYPES = ("JOB", )
    RETURN_NAMES = ("JOB", )
    FUNCTION = "increment"
    CATEGORY = icons.get("Comfyroll/Workflow")
    
    def increment(self, job_desc1, job_type1, job_alias1, job_desc2, job_type2, job_alias2, job_desc3, job_type3, job_alias3, job=None):
        job = list()
        return (job, )

#---------------------------------------------------------------------------------------------------------------------#   
class CR_JobScheduler:

    @classmethod
    def INPUT_TYPES(s):
    
        status = ["Asleep", "Awake"]     
        
        return {"required":{
                    "schedule": ("SCHEDULE", ),
                    "index": ("INT", {"default": 1, "min": -10000, "max": 10000}),
                    "schedule_alias": ("STRING", {"default": "", "multiline": False}),                    
                    "status": (status,),
                    }
        }

    RETURN_TYPES = ("JOB", "STRING", )
    RETURN_NAMES = ("JOB", "log", )
    FUNCTION = "listen"
    CATEGORY = icons.get("Comfyroll/Workflow")
    
    def listen(listen, index, schedule, schedule_alias, status):
        log = ""
        return (log, ) 
#---------------------------------------------------------------------------------------------------------------------# 
class CR_JobCurrentFrame:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required":{
                    "index": ("INT", {"default": 1, "min": -10000, "max": 10000}),
                    "max_frames": ("INT", {"default": 1, "min": 0, "max": 10000}),                    
                    "print_to_console": ([
                                "Yes",
                                "No"],),
                    }
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("current_frame", "max_frames",)
    FUNCTION = "to_console"
    CATEGORY = icons.get("Comfyroll/Workflow")
    
    def to_console(self, index, max_frames, print_to_console):
        if print_to_console == "Yes":
            print(f"[Info] CR Current Frame:{index}")
        current_frame = index
            
        return (current_frame, max_frames, )

#---------------------------------------------------------------------------------------------------------------------#   
class CR_CheckJobComplete:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "current_frame": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    "max_frames": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    }
        }

    RETURN_TYPES = ("BOOL", )
    RETURN_NAMES = ("BOOL", )
    FUNCTION = "reset"
    CATEGORY = icons.get("Comfyroll/Workflow")
    
    def reset(self, current_frame, max_frames):
        
        return (BOOL)    

#---------------------------------------------------------------------------------------------------------------------#   
class CR_SpawnWorkflowInstance:

    @classmethod
    def INPUT_TYPES(s):
    
        #mode = ["API"]
        
        return {"required":{
                    #"mode": (mode,),
                    "job": ("JOB", ),
                    #"job_alias": ("STRING", {"default": "", "multiline": False}),
                    "workflow_path": ("STRING", {"multiline": False, "default": ""}),
                    "workflow_name": ("STRING", {"multiline": False, "default": ""}),
                    }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True
    FUNCTION = "spawn"
    CATEGORY = icons.get("Comfyroll/Workflow")
    
    def spawn(self, job, workflow_path, workflow_name):

        return () 

#---------------------------------------------------------------------------------------------------------------------#   
class CR_LoadWorkflow:

    @classmethod
    def INPUT_TYPES(s):
        
        return {"required":{
                    "workflow_path": ("STRING", {"multiline": False, "default": ""}),
                    "workflow_name": ("STRING", {"multiline": False, "default": ""}),                   
                    }
        }

    RETURN_TYPES = ("WORKFLOW", )
    RETURN_NAMES = ("WORKFLOW", )
    FUNCTION = "workflow"
    CATEGORY = icons.get("Comfyroll/Workflow")
    
    def spawn(self, mode, job, schedule, workflow):
        workflow = ""
        return (workflow, ) 
               
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
# 3 nodes
'''
NODE_CLASS_MAPPINGS = {
    # Jobs
    "CR Job List": CR_JobList,
    "CR Job Scheduler": CR_JobScheduler,
    "CR Job Current Frame": CR_JobCurrentFrame,
    "CR Check Job Complete": CR_CheckJobComplete,
    "CR Spawn Workflow Instance": CR_SpawnWorkflowInstance,
    "CR Load Workflow": CR_LoadWorkflow,    
}
'''

