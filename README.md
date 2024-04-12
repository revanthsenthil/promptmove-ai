# promptmove-ai

Last updated 04/12/2024.

This project was created as a collaborative effort between Revanth Krishna Senthilkumaran, Calvin Madsen and Usman Chaudhary. 

User Manual: https://github.com/revanthsenthil/promptmove-ai/blob/main/docs/USERMANUAL.md

## Setup and Installation

Make sure your environment is set up correctly with python 3.9
```bash
conda create -n promptmove python=3.9
```

You will have to clone this repository onto your local computer.

```bash
git clone https://github.com/revanthsenthil/promptmove-ai.git
```

Make sure to setup the VirtualHome repository which has been placed as a submodule in this repository.

```bash
cd promptmove-ai
git submodule update --init --recursive
```

### Install Virtualhome

Make sure you properly install virtualhome.
```bash
cd virtualhome
pip install virtualhome
```

### Install PromptMove-AI

Make sure you properly install PromptMove-AI
```bash
cd ..
pip install -e .
```

The current version of promptmove-ai has been tested on Unity Simulator for Linux and Windows 

## Windows
Download the executable from [http://virtual-home.org//release/simulator/last_release/windows_exec.zip].

### Linux
Download the executable from [http://virtual-home.org//release/simulator/last_release/linux_exec.zip]

### Testing
Once downloaded, extract the executable into the `virtualhome/simulation` directory. 

In the `virtualhome_test.py` script inside of `promptmove-ai/scripts`, change `file_name` to the path of your saved executable. 

Run `virtualhome_test.py`. This should run a simple simulated motion on the simulator and generate a stream of images as output to a newly created directory inside `virtualhome/virtualhome/Output/`.

If these images are generated, the installation was successful.
