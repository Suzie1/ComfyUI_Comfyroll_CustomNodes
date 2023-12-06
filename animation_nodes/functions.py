#-----------------------------------------------------------------------------------------------------------#
# CR Animation Nodes by RockOfFire and Akatsuzi     https://github.com/Suzie1/CR-Animation-Nodes
# for ComfyUI                                       https://github.com/comfyanonymous/ComfyUI
#-----------------------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------------------#
# FUNCTIONS
#-----------------------------------------------------------------------------------------------------------#

def keyframe_scheduler(schedule, schedule_alias, current_frame):

    # Initialise
    schedule_lines = list()
    previous_params = ""
    
    # Loop through the schedule to find lines with matching schedule_alias
    for item in schedule:   
        alias = item[0]
        if alias == schedule_alias:
            schedule_lines.extend([(item)])

    # Loop through the filtered lines
    for i, item in enumerate(schedule_lines):
        # Get alias and schedule line
        alias, line = item
        
        # Skip empty lines
        if not line.strip():
            print(f"[Warning] Skipped blank line at line {i}")
            continue
            
        # Get parameters from the tuples
        frame_str, params = line.split(',', 1)
        frame = int(frame_str)
        
        # Strip spaces at start of params
        params = params.lstrip()
        
        # Return the params
        if frame < current_frame:
            previous_params = params
            continue
        if frame == current_frame:
            previous_params = params
        else:
            params = previous_params
        return params
            
    # Continue using the final params after the last schedule line has been evaluated     
    return previous_params
    
def prompt_scheduler(schedule, schedule_alias, current_frame):

    # Initialise
    schedule_lines = list()
    previous_prompt = ""
    previous_keyframe = 0
    
    #print(schedule, schedule_alias, current_frame) 
    
    # Loop through the schedule to find lines with matching schedule_alias
    for item in schedule:   
        alias = item[0]
        if alias == schedule_alias:
            schedule_lines.extend([(item)])

    # Loop through the filtered lines
    for i, item in enumerate(schedule_lines):
        # Get alias and schedule line
        alias, line = item
            
        # Get parameters from the tuples 
        frame_str, prompt = line.split(',', 1)
        frame_str = frame_str.strip('\"')
        frame = int(frame_str)
        
        # Strip leading spaces and quotes
        prompt = prompt.lstrip()
        prompt = prompt.replace('"', '')        
        
        # Return the parameters
        if frame < current_frame:
            previous_prompt = prompt
            previous_keyframe = frame
            #print(f"[Debug] frame < current_frame, frame {frame}, current frame {current_frame}")
            #print(f"[Debug] frame < current_frame, prompt {prompt}")
            continue
        if frame == current_frame:
            next_prompt = prompt
            next_keyframe = frame             
            previous_prompt = prompt
            previous_keyframe = frame
            #print(f"[Debug] frame = current_frame, frame {frame}, current frame {current_frame}, next keyframe {next_keyframe}")
            #print(f"[Debug] frame = current_frame, prompt {prompt}")            
        else:
            next_prompt = prompt
            next_keyframe = frame            
            prompt = previous_prompt
            #print(f"[Debug] frame > current_frame, frame {frame}, current frame {current_frame}, next keyframe {next_keyframe}")
            #print(f"[Debug] frame > current_frame, next prompt {next_prompt}")                
            
        return prompt, next_prompt, previous_keyframe, next_keyframe
            
    # Continue using the final params after the last schedule line has been evaluated     
    return previous_prompt, previous_prompt, previous_keyframe, previous_keyframe