from virtualhome.simulation.unity_simulator import UnityCommunication
from virtualhome.simulation.unity_simulator import utils_viz

import matplotlib.pyplot as plt
from tqdm import tqdm

from utils_demo import get_scene_cameras,display_scene_cameras,display_grid_img,find_nodes,add_node,add_edge


file_name = "../src/linux_exec.v2.3.0.x86_64" 

comm = UnityCommunication(file_name=file_name, port="8082", x_display="1", timeout_wait=120)

views = []
for scene_id in tqdm(range(10)):
    comm.reset(scene_id)
    
    # We will go over the line below later
    comm.remove_terrain()
    top_view = get_scene_cameras(comm, [-1])
    views += top_view

comm.reset(0)

indices = [3, 32, -5, -1, -20, 15, 48, -8, 50, 17]
img_final = display_scene_cameras(comm, indices, nrows=2)
plt.imshow(img_final)
plt.axis('off')
plt.show()

# specify the position and rotation of the camera
comm.add_camera(position=[-3,1.8,-4], rotation=[20, 120, 0], field_view=60)

# Get the last camera
s, c = comm.camera_count()
img_final = display_scene_cameras(comm, [c-1], nrows=1)
plt.imshow(img_final)
plt.axis('off')
plt.show()

s, graph = comm.environment_graph()
print(graph['nodes'][140])
print(graph['edges'][:5])

comm.reset(4)

imgs_prev = get_scene_cameras(comm, [-4])
plt.imshow(display_grid_img(imgs_prev, nrows=1))
plt.axis('off')
plt.show()

success, graph = comm.environment_graph()
sofa = find_nodes(graph, class_name='sofa')[-2]
print(sofa)

add_node(graph, {'class_name': 'cat', 
                   'category': 'Animals', 
                   'id': 1000, 
                   'properties': [], 
                   'states': []})
add_edge(graph, 1000, 'ON', sofa['id'])

success, message = comm.expand_scene(graph)

imgs_final = get_scene_cameras(comm, [-4])
plt.imshow(display_grid_img(imgs_prev+imgs_final, nrows=1))
plt.axis('off')
plt.show()

imgs_prev = imgs_final

success, graph = comm.environment_graph()

fridge = find_nodes(graph, class_name='fridge')[0]
fridge['states'] = ['OPEN']

success = comm.expand_scene(graph)

imgs_final = get_scene_cameras(comm, [-4])
plt.imshow(display_grid_img(imgs_prev+imgs_final, nrows=1))
plt.axis('off')
plt.show()

indices = [0]
imgs_prev = get_scene_cameras(comm, indices)
plt.imshow(display_grid_img(imgs_prev, nrows=1))
plt.axis('off')
plt.show()

success, graph = comm.environment_graph()
prev_graph = graph
tv_node = [x for x in graph['nodes'] if x['class_name'] == 'tv'][0]
light_node = [x for x in graph['nodes'] if x['class_name'] == 'lightswitch'][0]

tv_node['states'] = ['ON']
light_node['states'] = ['OFF']
_ = comm.expand_scene(graph)
last_graph = graph

imgs_final = get_scene_cameras(comm, indices)
plt.imshow(display_grid_img(imgs_prev+imgs_final, nrows=1))
plt.axis('off')
plt.show()

comm.reset(2)

views = []
s, message = comm.add_camera(position=[-9.2,1.3,-3], rotation=[15, 130, 0], field_view=60)
cam_id = int(message.split(':')[1])
# Set time to 05:30 
comm.set_time(hours=10, minutes=30, seconds=0)
morning_view = get_scene_cameras(comm, [cam_id])
views += morning_view

# Set time to 8:30 
comm.set_time(hours=15, minutes=30, seconds=0)
day_view = get_scene_cameras(comm, [cam_id])
views += day_view

# Set time to 21:00 
comm.set_time(hours=21, minutes=0, seconds=0)
night_view = get_scene_cameras(comm, [cam_id])
views += night_view
    
plt.imshow(display_grid_img(views, nrows=1))
plt.axis('off')
plt.show()

comm.reset(0)
comm.remove_terrain()
no_day_view = get_scene_cameras(comm, [17])
plt.imshow(display_grid_img(no_day_view, nrows=1)) 
plt.axis('off')
plt.show()

# Generating Scripts

comm.reset(4)
tv_node['states'] = ['OFF']
comm.expand_scene(prev_graph)
comm.add_character('chars/Female2', initial_room='kitchen')
s, g = comm.environment_graph()
cat_id = [node['id'] for node in g['nodes'] if node['class_name'] == 'cat'][0]

s, nc = comm.camera_count()
indices = range(nc - 6, nc)
imgs_prev = get_scene_cameras(comm, indices)
plt.imshow(display_grid_img(imgs_prev, nrows=2))
plt.axis('off')
plt.show()

script = ['<char0> [Walk] <sofa> ({})'.format(sofa['id']),
          '<char0> [Find] <cat> ({})'.format(cat_id),
          '<char0> [Grab] <cat> ({})'.format(cat_id),
          '<char0> [Sit] <sofa> ({})'.format(sofa['id'])]

success, message = comm.render_script(script=script,
                                      processing_time_limit=60,
                                      find_solution=False,
                                      image_width=320,
                                      image_height=240,  
                                      skip_animation=False,
                                      recording=True,
                                      save_pose_data=True,
                                      file_name_prefix='relax')

path_video = "./Output/"
utils_viz.generate_video(input_path=path_video, prefix='relax', output_path='.')