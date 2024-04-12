# PromptMove AI User Manual

Project README [link](https://github.com/revanthsenthil/promptmove-ai/blob/main/README.md).

This user manual is an all-in-one guide to use PromptMove AI.

## What is PromptMove AI

PromptMove AI is essentially an extension of the [VirtualHome](http://virtual-home.org/) simulation platform. It allows for natural language commands to be given to VirtualHome in order to instruct agents to complete certain tasks. The goal of PromptMove AI is to allow researchers, corporations, or robotics enthusiasts a simple way to see how their agents will respond to certain commands. 

PromptMove AI consists of a web app where users can log in and create prompts to make tasks in the environment with simulated agents. With the usage of VirtualHome, users can train multiple agents in the environment with high-level instructions and human-like activities. This is useful as we would like to make it easier for users to use language input to control agents in the simulator.


## How to use PromptMove AI

The README that mentions installing and getting PromptMove AI setup is [here](https://github.com/revanthsenthil/promptmove-ai/blob/main/README.md). There are steps that differ based on your operating system, and the current support extends to Windows and Linux. Specific requirements are listed in the respective `requirements.txt` and `setup.py` files. The applicaiton is run using streamlit, which will locally host the user interface in your browser. In the `src` directory, run the application with `streamlit run assistants.py`.

Once open in the browser, you have two sources of input. You may use the microphone to speak a request to the AI assistant, or you may type a request to the AI assistant. These requests should be situated around a home environment, and should be based on the status of certain items of the house, or a request for the AI assistant to do something in the house. There are a wide variety of requests that may be asked, due to the LLM involved in interpreting your request. The response to your request may be a text based response from the assistant, error or success information involved with the simulator, or video generation from the simulator. Currently, video and error response is still in development. Many additional features will be added soon to enhance the virtual AI house assistant experience.


## Why you should use PromptMove AI

PromptMove AI should be used by anyone interested in understanding how agents will respond to tasks in a simulated household environment. If proven to work well with simulated agents, PromptMove AI can be applied to real-life environments where users will be able to use robots and automated agents setup in a domestic setting to perform tasks automatically. 


## How to extend and collaborate on PromptMove AI

If you would like to improve on PromptMove AI and make changes that make it more viable to the community, we would highly recommend creating a Pull Request [here](https://github.com/revanthsenthil/promptmove-ai/pulls). If you would like to make suggestions, please send feedback on the issues page [here](https://github.com/revanthsenthil/promptmove-ai/issues). We are eager to develop PromptMove AI to make it an easy-to-use and viable product for the developer community.


## How to integrate with PromptMove AI

The easiest way to integrate with PromptMove AI is to include it as a dependency within your repository. Additionally, our repository can be forked or cloned if those methods are more relevant to your project.

PromptMove AI can be used as a submodule, but the `--recursive` flag must be used during installation as `VirtualHome` is used as a submodule within PrompMove AI.


## Sending feedback to PromptMove AI

Any feedback regarding updates to PromptMove AI or trouble running the program can be resolved by creating an issue within the GitHub repository [here](https://github.com/revanthsenthil/promptmove-ai/issues).

