# promptmove-ai

Last updated 04/27/2024.

This project was created as a collaborative effort between Revanth Krishna Senthilkumaran, Calvin Madsen and Usman Chaudhary. 

User Manual: https://github.com/revanthsenthil/promptmove-ai/blob/main/docs/USERMANUAL.md

Example virtualhome video generation
![]( https://github.com/revanthsenthil/promptmove-ai/blob/main/docs/assets/video_normal.gif)

## Setup and Installation

Make sure your environment is set up correctly with python 3.9
```bash
conda create -n promptmove python=3.9
conda activate promptmove
```

You will have to clone this repository onto your local computer.

```bash
git clone https://github.com/revanthsenthil/promptmove-ai.git
```

### Install PromptMove-AI

Make sure you properly install PromptMove-AI
```bash
cd promptmove-ai
pip install -e .
```

The current version of promptmove-ai has been tested on Unity Simulator for Linux 

### Linux
Download the executable from [http://virtual-home.org//release/simulator/v2.0/v2.3.0/linux_exec.zip]
The commands below can be followed to download the executable and extract it into the proper directory.
```bash
cd src
wget http://virtual-home.org//release/simulator/v2.0/v2.3.0/linux_exec.zip
unzip linux_exec.zip -d linux_exec
```

### Testing
In the `/promptmove-ai` directory, you may run our tests to ensure promptmove-ai was setup and installed correctly. If you have pytest installed you may run our test suite.
```bash
cd ..
pip install pytest
pytest tests
```

### Running PromptMove-AI

You must have an OpenAI API key to utilize promptmove-ai. It can be set as an environment variable called `OPENAI_API_KEY`.
Alternatively, this key mey be imported into the application while running ours treamlit app.
```bash
export OPENAI_API_KEY=your_key_here
```

Navigate to the `/src` directory and run the assistants.py streamlit app.
```bash
cd src
streamlit run assistants.py
```

This should open a new window in your browser to interact with the promptmove-ai user interface.

View the [User Manual](https://github.com/revanthsenthil/promptmove-ai/blob/main/docs/USERMANUAL.md) for further instruction.