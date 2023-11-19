from .animation_nodes.prompt import *
from .dev_nodes.DT_Pixel_Sort import *

from .dev_nodes.dev_nodes import *
from .dev_nodes.graphics_dev_nodes import *
from .dev_nodes.dev_pil_3D import *
from .dev_nodes.dev_workflow import *
from .dev_nodes.animation_dev_nodes import *
from .dev_nodes.dev_schedulers import *
from .dev_nodes.dev_xygrid import *

DEV_NODE_CLASS_MAPPINGS = {
    ### Dev Nodes
    "CR XYZ List": CR_XYZList,    
    "CR XYZ Interpolate": CR_XYZInterpolate,    
    "CR XYZ Index": CR_XYZIndex,
    "CR Conditioning Mixer": CR_ConditioningMixer,  
    "CR Pixel Sort": Pixel_Sort,
    ### Graphics_Dev Nodes
    "CR Overlay Transparent Image": CR_OverlayTransparentImage,
    "CR Multi-Panel Meme Template": CR_MultiPanelMemeTemplate,
    "CR Popular Meme Templates": CR_PopularMemeTemplates,    
    "CR Draw Perspective Text": CR_DrawPerspectiveText,
    "CR Simple Annotations": CR_SimpleAnnotations,
    "CR Apply Annotations": CR_ApplyAnnotations,
    "CR Add Annotation": CR_AddAnnotation,    
    "CR 3D Polygon": CR_3DPolygon,
    "CR 3D Solids": CR_3DSolids,
    ### Workflow
    "CR Job List": CR_JobList,
    "CR Job Scheduler": CR_JobScheduler,
    "CR Check Job Complete": CR_CheckJobComplete,
    "CR Spawn Workflow Instance": CR_SpawnWorkflowInstance,    
    "CR Job Current Frame": CR_JobCurrentFrame,
    "CR Load Workflow": CR_LoadWorkflow,
    ### Animation Dev Nodes   
    "CR Prompt Weight Scheduler": CR_PromptWeightScheduler,    
    "CR Load Scheduled ControlNets": CR_LoadScheduledControlNets,
    "CR Interpolate Prompt Weights": CR_InterpolatePromptWeights,    
    "CR Text List Cross Join": CR_TextListCrossJoin,   
    "CR Schedule Camera Movements": CR_ScheduleCameraMovements,
    "CR Schedule Styles": CR_ScheduleStyles,      
    "CR Style List": CR_StyleList,       
    "CR Cycle Styles": CR_CycleStyles,
    "CR Image Transition": CR_ImageTransition,
    "CR Strobe Images": CR_StrobeImages,      
    "CR Alternate Latents": CR_AlternateLatents,
    "CR 3D Camera Drone": CR_DroneCamera3D,
    "CR 3D Camera Static": CR_StaticCamera3D, 
    "CR Interpolate Zoom": CR_InterpolateZoom,
    "CR Interpolate Rotation": CR_InterpolateRotation,
    "CR Interpolate Track": CR_InterpolateTrack,    
    "CR Continuous Zoom": CR_ContinuousZoom,
    "CR Continuous Rotation": CR_ContinuousRotation,
    "CR Continuous Track": CR_ContinuousTrack,    
}

DEV_NODE_DISPLAY_NAME_MAPPINGS = {
    # Dev Nodes
    "CR XYZ List": "CR XYZ List (Dev)",    
    "CR XYZ Interpolate": "CR XYZ Interpolate (Dev)",    
    "CR XYZ Index": "CR XYZ Index (Dev)",    
    "CR Overlay Transparent Image": "CR Overlay Transparent Image (Dev)",
    "CR Multi-Panel Meme Template": "CR Multi-Panel Meme Template (Dev)",
    "CR Popular Meme Templates": "CR Popular Meme Templates (Dev)",    
    "CR Draw Perspective Text": "CR Draw Perspective Text (Dev)",
    "CR Simple Annotations": "CR Simple Annotations (Dev)",
    "CR Apply Annotations": "CR Apply Annotations (Prototype)",
    "CR Add Annotation": "CR Add Annotation (Prototype)",    
    "CR 3D Polygon": "CR 3D Polygon (Dev)",
    "CR 3D Solids": "CR 3D Solids (Dev)",    
    "CR Job List": "CR Job List (Prototype)",
    "CR Job Scheduler": "CR Job Scheduler (Prototype)",
    "CR Check Job Complete": "CR Check Job Complete (Prototype)",
    "CR Spawn Workflow Instance": "CR Spawn Workflow Instance (Prototype)",    
    "CR Job Current Frame": "CR Job Current Frame (Prototype)",
    "CR Load Workflow": "CR Load Workflow (Prototype)",
    "CR Conditioning Mixer": "CR Conditioning Mixer (Dev)",
    ### Animation Dev Nodes
    "CR Prompt Weight Scheduler": "CR Prompt Weight Scheduler (Dev)",    
    "CR Load Scheduled ControlNets": "CR Load Scheduled ControlNets (Dev)",
    "CR Interpolate Prompt Weights": "CR Interpolate Prompt Weights (Dev)",    
    "CR Text List Cross Join": "CR Text List Cross Join (Dev)",   
    "CR Schedule Camera Movements": "CR Schedule Camera Movements (Prototype)",
    "CR Schedule Styles": "CR Schedule Styles (Prototype)",      
    "CR Style List": "CR Style List (Prototype)",       
    "CR Cycle Styles": "CR Cycle Styles (Prototype)",
    "CR Image Transition": "CR Image Transition (Prototype)",
    "CR Strobe Images": "CR Strobe Images (Prototype)",      
    "CR Alternate Latents": "CR Alternate Latents (Prototype)",
    "CR 3D Camera Drone": "CR 3D Camera Drone (Prototype)",
    "CR 3D Camera Static": "CR 3D Camera Static (Prototype)", 
    "CR Interpolate Zoom": "CR Interpolate Zoom (Prototype)",
    "CR Interpolate Rotation": "CR Interpolate Rotation (Prototype)",
    "CR Interpolate Track": "CR Interpolate Track (Prototype)",    
    "CR Continuous Zoom": "CR Continuous Zoom (Prototype)",
    "CR Continuous Rotation": "CR Continuous Rotation (Prototype)",
    "CR Continuous Track": "CR Continuous Track (Prototype)",    
}