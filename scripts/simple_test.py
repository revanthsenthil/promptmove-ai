from virtualhome.simulation.unity_simulator import UnityCommunication
from virtualhome.simulation.unity_simulator import utils_viz

import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm
import os

from utils_demo import get_scene_cameras,display_scene_cameras,display_grid_img,find_nodes,add_node,add_edge


file_name = "../src/linux_exec.v2.3.0.x86_64" # path to executable

comm = UnityCommunication(file_name=file_name, port="8082", x_display="1", timeout_wait=120)


# Generating Scripts

comm.reset(4)
comm.add_character('chars/Female2', initial_room='kitchen')
s, g = comm.environment_graph()

# need to change to input from LLM
OBJECTS = ['sofa', 'sofa', 'computer', 'computer']
ACTIONS = ['walk', 'sit', 'find', 'walk']


script = []
 
for obj, act in zip(OBJECTS, ACTIONS):
    object = find_nodes(g, class_name=obj)[0]
    script.append('<char0> [{}] <{}> ({})'.format(act, obj, object['id']))
    

success, message = comm.render_script(script=script,
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
utils_viz.generate_video(input_path=path_video, prefix='relax', output_path='.')