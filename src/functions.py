from virtualhome.simulation.unity_simulator import UnityCommunication
from virtualhome.simulation.unity_simulator import utils_viz
from src.utils import find_nodes
from src.log import log

import os
import json

ACTIONS = []
OBJECTS = []
    
def perform_action_on_object(action, object):
    """Perform an action on an object in a virtual home environment"""
    log(f"Running perform_action_on_object({action}, {object})")
    global ACTIONS, OBJECTS

    with open('../config/objs_env4.json') as f:
        object_info = json.load(f)

    object = object.lower().replace(" ", "")

    acceptable_actions = ['walk', 'find']

    # check if object and action are acceptable
    if object not in object_info:
        log(f"failed to find {object}")
        return json.dumps({"action": action, "object": object, "status": f"failed to find {object}"})
    elif action not in object_info[object] and action not in acceptable_actions:
        log(f"failed to find {action} for {object}")
        return json.dumps({"action": action, "object": object, "status": f"failed to perform {action} on {object}"})

    # Append objects and actions to list for the script
    ACTIONS.append(action)
    OBJECTS.append(object)
    log(f"Appended {action} on {object} to the list")
    return json.dumps({"action": action, "object": object, "status": "success"})

def run_script(date : str):
    """Run the scrupt for performing actions on objects in a virtual home environment"""
    global ACTIONS, OBJECTS
    log(f"Running run_script({ACTIONS}, {OBJECTS})")

    if len(ACTIONS) == 0 and len(OBJECTS) == 0:
        return json.dumps({"success_actions": [], "success_objects": [], 'failed_actions': [], 'failed_objects': []})
    
    # Initialize Unity Communication
    file_name = "linux_exec/linux_exec.v2.3.0.x86_64" # path to executable
    comm = UnityCommunication(file_name=file_name, port="8081", x_display='0', timeout_wait=120)

    # Base Environment Setup
    comm.reset(4)
    comm.add_character('chars/Female2', initial_room='kitchen')
    _, g = comm.environment_graph()

    # Find the nodes for the objects and actions
    script = []
    success_actions = []
    success_objects = []
    for obj, act in zip(OBJECTS, ACTIONS):
        try:
            object = find_nodes(g, class_name=obj)[0]
        except IndexError:
            log(f"Object {obj} not found in the environment")
            continue
        script.append('<char0> [{}] <{}> ({})'.format(act, obj, object['id']))
        success_actions.append(act)
        success_objects.append(obj)

    log(f'script: {script}')

    # if the script is empty, return the list of successful and failed actions and objects
    if len(script) == 0:
        return json.dumps({"success_actions": success_actions, "success_objects": success_objects, 'failed_actions': ACTIONS, 'failed_objects': OBJECTS})

    # render the images from the script
    _, _ = comm.render_script(script=script,
                                        frame_rate=10,
                                        processing_time_limit=60,
                                        find_solution=False,
                                        image_width=320,
                                        image_height=240,  
                                        skip_animation=False,
                                        recording=True,
                                        save_pose_data=True,
                                        file_name_prefix=date)
    

    path_video = "./Output"
    video_output_path = f'video_output/{date}'

    try:
        os.mkdir(video_output_path)
    except OSError:
        pass

    if os.path.exists(os.path.join(video_output_path, 'video_normal.mp4')):
        os.remove(os.path.join(video_output_path, 'video_normal.mp4'))

    utils_viz.generate_video(input_path=path_video, prefix=date, output_path=video_output_path)

    # reset everything
    comm.close()
    failed_actions = [act for act in ACTIONS if act not in success_actions]
    failed_objects = [obj for obj in OBJECTS if obj not in success_objects]
    ACTIONS = []
    OBJECTS = []
    return json.dumps({"success_actions": success_actions, "success_objects": success_objects, 'failed_actions': failed_actions, 'failed_objects': failed_objects})

if __name__ == "__main__":
    import datetime
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    perform_action_on_object("walk", "box")
    run_script(date)