# promptmove-ai

Last updated 02/22/2024.

This project was created as a collaborative effort between Revanth Krishna Senthilkumaran, Calvin Madsen and Usman Chaudhary. 

### Setup and Installation

First, you will have to clone this repository onto your local computer.

```bash
git clone https://github.com/revanthsenthil/promptmove-ai.git
```

Make sure to setup the VirtualHome repository which has been placed as a submodule in this repository.

```bash
cd promptmove-ai
git submodule update --init --recursive
```

The current version of promptmove-ai has been tested on Unity Simulator for Windows, and it should be downloadable from [http://virtual-home.org//release/simulator/last_release/windows_exec.zip].

Once you extract the directory, move the directory titled `windows_execv2.2.4` to `promptmove-ai/virtualhome/virtualhome/simulation`. To test that it's installed with no issues, navigate into that directory and open the Unity Simulator file `VirtualHome`. It should open a blank full screen Unity Simulator window.

Run the `test.py` script inside of `promptmove-ai/scripts`. This should run a simple simulated motion on the simulator and generate a stream of images as output to a newly created directory inside `virtualhome/virtualhome/Output/`.
