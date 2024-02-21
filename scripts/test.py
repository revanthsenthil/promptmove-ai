# cd into virtualhome repo
from simulation.unity_simulator import comm_unity

YOUR_FILE_NAME = "../virtualhome/virtualhome/simulation/windows_exec.v2.2.4/VirtualHome" # Your path to the simulator
port= "8080" # or your preferred port

comm = comm_unity.UnityCommunication(
    file_name=YOUR_FILE_NAME,
    port=port
)

env_id = 1 # env_id ranges from 0 to 6
comm.reset(env_id)

# Check the number of cameras
s, cam_count = comm.camera_count()
s, images = comm.camera_image([0, cam_count-1])

# Add a camera at the specified rotation and position
comm.add_camera(position=[-3, 2, -5], rotation=[10, 15, 0])

# View camera from different modes
modes = ['normal', 'seg_class', 'surf_normals']
images = []
for mode in modes:
    s, im = comm.camera_image([cam_count], mode=mode)
    images.append(im[0])

# # save images
# import matplotlib.pyplot as plt
# import numpy as np
# for i, im in enumerate(images):
#     plt.imsave('{}.png'.format(modes[i]), np.array(im))
    
# Reset the environment
comm.reset()

# Get graph
s, graph = comm.environment_graph()

# Get the fridge node
fridge_node = [node for node in graph['nodes'] if node['class_name'] == 'fridge'][0]

# Open it
fridge_node['states'] = ['OPEN']

# create a new node
new_node = {
    'id': 1000,
    'class_name': 'salmon',
    'states': []
}
# Add an edge
new_edge = {'from_id': 1000, 'to_id': fridge_node['id'], 'relation_type': 'INSIDE'}
graph['nodes'].append(new_node)
graph['edges'].append(new_edge)

# update the environment
comm.expand_scene(graph)

###############

# Reset the environment
# comm.reset(0)
# comm.add_character('Chars/Female2')

# # Get nodes for salmon and microwave
# salmon_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'salmon'][0]
# microwave_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'microwave'][0]

# # Put salmon in microwave
# script = [
#     '<char0> [walk] <salmon> ({})'.format(salmon_id),
#     '<char0> [grab] <salmon> ({})'.format(salmon_id),
#     '<char0> [open] <microwave> ({})'.format(microwave_id),
#     '<char0> [putin] <salmon> ({}) <microwave> ({})'.format(salmon_id, microwave_id),
#     '<char0> [close] <microwave> ({})'.format(microwave_id)
# ]
# comm.render_script(script, recording=True, frame_rate=10)

# Reset the environment
comm.reset(0)

# Add two agents this time
comm.add_character('Chars/Male2', initial_room='kitchen')
comm.add_character('Chars/Female4', initial_room='bedroom')

# Get nodes for salmon and microwave, glass, faucet and sink
salmon_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'salmon'][0]
microwave_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'microwave'][0]
glass_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'waterglass'][-1]
sink_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'sink'][0]
faucet_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'faucet'][-1]


# Put salmon in microwave
script = [
     '<char0> [walk] <salmon> ({}) | <char1> [walk] <glass> ({})'.format(salmon_id, glass_id),
     '<char0> [grab] <salmon> ({}) | <char1> [grab] <glass> ({})'.format(salmon_id, glass_id),
     '<char0> [open] <microwave> ({}) | <char1> [walk] <sink> ({})'.format(microwave_id, sink_id),
     '<char0> [putin] <salmon> ({}) <microwave> ({}) | <char1> [putback] <glass> ({}) <sink> ({})'.format(salmon_id, microwave_id, glass_id, sink_id),
     '<char0> [close] <microwave> ({}) | <char1> [switchon] <faucet> ({})'.format(microwave_id, faucet_id)
]
comm.render_script(script, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])