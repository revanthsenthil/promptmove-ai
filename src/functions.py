
import json

ACTIONS = []
OBJECTS = []

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    print(f"Running get_current_weather({location})")

    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
    
def perform_action_on_object(action, object):
    """Perform an action on an object in a virtual home environment"""
    print(f"Running perform_action_on_object({action}, {object})")
    global ACTIONS, OBJECTS

    with open('../config/all_object_info.json') as f:
        object_info = json.load(f)

    object = object.lower()
    action = action.lower()

    acceptable_actions = ['walk']

    # check if object and action are acceptable
    if object not in object_info:
        print(f"failed to find {object}")
        return json.dumps({"action": action, "object": object, "status": f"failed to find {object}"})
    elif action not in object_info[object] and action not in acceptable_actions:
        print(f"failed to find {action} for {object}")
        return json.dumps({"action": action, "object": object, "status": f"failed to perform {action} on {object}"})

    # Append objects and actions to list for the script
    ACTIONS.append(action)
    OBJECTS.append(object)
    print(f"Appended {action} on {object} to the list")
    return json.dumps({"action": action, "object": object, "status": "success"})

def run_script():
    """Run the scrupt for performing actions on objects in a virtual home environment"""
    global ACTIONS, OBJECTS
    print(f"Running run_script({ACTIONS}, {OBJECTS})")

    from virtualhome.simulation.unity_simulator import UnityCommunication
    from virtualhome.simulation.unity_simulator import utils_viz

    import matplotlib.pyplot as plt
    import datetime
    from tqdm import tqdm
    import os

    from scripts.utils_demo import get_scene_cameras,display_scene_cameras,display_grid_img,find_nodes,add_node,add_edge


    file_name = "linux_exec/linux_exec.v2.3.0.x86_64" # path to executable

    comm = UnityCommunication(file_name=file_name, port="8081", x_display='0', timeout_wait=120)

    # Generating Scripts

    comm.reset(4)
    comm.add_character('chars/Female2', initial_room='kitchen')
    s, g = comm.environment_graph()

    script = []
    
    for obj, act in zip(OBJECTS, ACTIONS):
        object = find_nodes(g, class_name=obj)[0]
        script.append('<char0> [{}] <{}> ({})'.format(act, obj, object['id']))
        

    success, message = comm.render_script(script=script,
                                        frame_rate=10,
                                        processing_time_limit=60,
                                        find_solution=False,
                                        image_width=320,
                                        image_height=240,  
                                        skip_animation=False,
                                        recording=True,
                                        save_pose_data=True,
                                        file_name_prefix='relax')

    directory = './Output/relax/0'

    print(os.listdir(directory))

    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            file_path = directory + filename
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    pass
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
                

    path_video = f"./Output"

    if os.path.exists('video_normal.mp4'):
        os.remove('video_normal.mp4')

    utils_viz.generate_video(input_path=path_video, prefix='relax', output_path='.')

    # reset everything
    comm.close()
    acts = ACTIONS
    objs = OBJECTS
    ACTIONS = []
    OBJECTS = []
    return json.dumps({"actions": acts, "object": objs})

if __name__ == "__main__":
    run_script()