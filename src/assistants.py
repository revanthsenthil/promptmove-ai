"""
FUNCTION CALLING EXAMPLES
https://platform.openai.com/docs/assistants/tools/function-calling

App inspired by blogpost: https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/
"""

from openai import OpenAI
import openai
import streamlit as st

import src.audio.transcribe as transcribe
from src.functions import perform_action_on_object, run_script
from src.log import log

import os
import json
import datetime

def create_assistant():

    # gets the environment variable OPENAI_API_KEY
    try:
        client = OpenAI(api_key=st.session_state.openai_key)
    except openai.OpenAIError as e:
        st.error("Error creating client instance. Please check your credentials.")
        log(f"Error creating client instance. Please check your credentials: {e}")
        return None
    
    # Get possible objects and actions
    with open('../config/objs_env4.json') as f:
        object_info = json.load(f)
        objects = list(object_info.keys())
        actions = set([action for obj in object_info for action in object_info[obj]])
        actions.add('walk')
        actions.add('find')
        actions.add('run')
        actions.add('open')
        actions.add('close')
        actions = list(actions)

    # Add the files to the assistant
    try:
        assistant = client.beta.assistants.create(
            instructions=f"You are a personal house assistant for assisting in the VirtualHome simulated environment \
                to help with tasks around the house, such as cooking, cleaning, organizing, retrieving items, and general knowledge about the state of the house. \
                You can ask me to perform actions on objects in the house. For example, you can ask me to 'walk to the kitchen' or 'find the microwave'. \
                Every possible object and action is listed as follows: {str(json.dumps(object_info))}. \
                The action of 'walk', 'find', and 'run' are also acceptable for each object. Actions of 'open' and 'close' are acceptable if 'CAN_OPEN' is an action for that object. \
                If an action is in all caps, this tells specific information about the object, however, it is not an acceptable action to perform on that object. \
                The function you have access to is 'perform_action_on_object'. \
                If the user references an object or action that is not in the list, but is similar to an object or action in the list, the assistant will attempt to \
                perform the action on the similar object. \
                The user exists on the sofa in the livingroom, and so if they request an object be brought to them, it should be brought to the 'sofa' object. \
                If they request an object you must first 'grab' that object before 'walk' to the 'sofa'.",
            model="gpt-4-turbo",
            tools=
            [
                {
                "type": "function",
                    "function": {
                        "name": "perform_action_on_object",
                        "description": "Perform an action to an object in the house",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "description": f"the action to represent doing something with an object or location. Possible actions are: {', '.join(actions)}",
                                },
                                "object": {
                                    "type": "string", 
                                    "description": f"the object or location to perform the action on. Possible objects are: {', '.join(objects)}",
                                },
                            },
                            "required": ["object", "action"],
                        },
                    },
                }
            ]
        )
    except openai.OpenAIError as e:
        st.error("Error creating assistant. Please check your credentials.")
        log(f"Error creating assistant. Please check your credentials: {e}")
        return None
    
    # Create one thread per user
    thread = client.beta.threads.create()

    return client, assistant, thread


def run_assistant(client, assistant, thread, run):
    # If no tool calls are required, return the assistant's response
    if run.status == 'completed':
        log(f"run status: {run.status}")

        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        log(messages)
        return messages.data[0].content[0].text.value
    
    # If the assistant requires action, perform the required action
    elif run.status == 'requires_action':
        log(f"run status: {run.status}")

        # Define the list to store tool outputs
        tool_outputs = []

        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        log(f'Tool calls: {tool_calls}')

        if tool_calls:
            available_functions = {
                'perform_action_on_object': perform_action_on_object
            }
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                log(f'Function args: {function_args}')
                function_response = function_to_call(**function_args)
                tool_outputs.append(
                    {
                        "tool_call_id": tool_call.id,
                        "output": function_response,
                    }
                )
        else:
            # No tool calls
            log("No tool calls.")
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            log(messages)
            return messages.data[0].content[0].text.value
        
        # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                log("Tool outputs submitted successfully.")
            except Exception as e:
                log(f"Failed to submit tool outputs: {e}")

            # recursively call run_assistant to check the status of the run
            return run_assistant(client, assistant, thread, run)
           
        else:
            log("No tool outputs.")
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            log(messages)
            return messages.data[0].content[0].text.value

    # If the run is not completed or requires action, return the status
    else:
        log(f"Error: {run.status}")
        return f"Error: {run.status}. Please try again."


# Function for generating LLM response
def generate_response(user_input):
    log(f"Running generate_response({user_input})")

    if user_input in [None, ""] or not isinstance(user_input, str):
        return "Invalid input. Please try again."

    # load session's assistant
    client, assistant, thread = st.session_state.assistant

    _ = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    return run_assistant(client, assistant, thread, run)

def click_button():
    st.session_state.clicked = True

def check_key():
    try:
        client = OpenAI(api_key=st.session_state.openai_key)
    except Exception:
        st.session_state.correct_key = False
    try:
        _ = client.beta.assistants.create(
            instructions="You are a personal house assistant for assisting in the VirtualHome simulated environment \
            to help with tasks around the house, such as cooking, cleaning, organizing, retrieving items, and general knowledge about the state of the house.",
            model="gpt-4-turbo",
            tools=[{"type": "file_search"}]
        )
        st.session_state.correct_key = True
    except Exception:
        st.session_state.correct_key = False

def main():

    # Set up Streamlit app
    st.set_page_config(page_title="PromptMove-AI")
    st.title(":blue[PromptMove-AI]")
    st.write("This is a virtual assistant to help with tasks around the house, such as \
            cooking, cleaning, retrieving items, and general assistance.")	
    
    if "log" not in st.session_state.keys():
        num = 0
        while os.path.exists(f"logs/log{num}.txt"):
            num += 1
        st.session_state.log = f"logs/log{num}.txt"
    
    # Set up sidebar for OpenAI API key credentials
    with st.sidebar:
        st.title('Credentials')

        # if key is already provided 
        if 'openai_key' in st.session_state.keys():
            check_key()
            if st.session_state.correct_key:
                st.success('OpenAI API Key Already Accepted!', icon='✅')
            else:
                st.session_state.openai_key = st.text_input('Enter OpenAI API Key:', type='password')
                check_key()

        # if key is provided in environment variables
        elif 'OPENAI_API_KEY' in os.environ:
            st.session_state.openai_key = os.environ['OPENAI_API_KEY']
            check_key()
            if st.session_state.correct_key:
                st.success('OpenAI API Key Accepted!', icon='✅')
            else:
                st.session_state.openai_key = st.text_input('Enter OpenAI API Key:', type='password')
                check_key()
        else:
            st.warning('Please enter your OpenAI API Key!', icon='⚠️')
            st.session_state.openai_key = st.text_input('Enter OpenAI API Key:', type='password')
            check_key()

        st.title('Video Controls')
        st.session_state.framerate = st.slider('Framerate', min_value=1, max_value=30, value=10, step=1)
        st.session_state.width = st.slider('Video Width', min_value=10, max_value=1920, value=320, step=10)
        st.session_state.height = st.slider('Video Height', min_value=10, max_value=1080, value=240, step=10)   
        
        st.markdown('[GitHub repo](https://github.com/revanthsenthil/promptmove-ai)')

    if not st.session_state.correct_key:
        return

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    # Get assistant if not already created
    if "assistant" not in st.session_state.keys():
        client, assistant, thread = create_assistant()
        assistant_info = client, assistant, thread
        st.session_state.assistant = assistant_info

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "video" in message:
                date = message["video"]
                if date in os.listdir('video_output') and 'video_normal.mp4' in os.listdir(f'video_output/{date}'): 
                    st.video(f'video_output/{date}/video_normal.mp4', format="video/mp4", start_time=0, subtitles=None, end_time=None, loop=False)

    # User-provided input
    if user_input := st.chat_input():
        if st.session_state.messages[-1]["role"] == "assistant":
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

    # Record and transcribe user speech on button click
    if st.session_state.clicked:
        audio = transcribe.record_5_sec()
        user_input = transcribe.transcribe_speech(audio)
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.clicked = False

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] == "user" and st.session_state.messages[-2]["role"] == "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = generate_response(user_input)
                except openai.BadRequestError as e:
                    response = f"Error: {e}"
                log(f'Response: {response}')
                if 'Error: Error code: 400' in response:
                    response = "Please Restart the Program."
                date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                run_script(date, st.session_state.framerate, st.session_state.width, st.session_state.height) 
                st.write(response)
                if date in os.listdir('video_output') and 'video_normal.mp4' in os.listdir(f'video_output/{date}'): 
                    st.video(f'video_output/{date}/video_normal.mp4', format="video/mp4", start_time=0, subtitles=None, end_time=None, loop=False)
                with st.sidebar:
                    if os.path.isfile(st.session_state.log):
                        with open(st.session_state.log, 'r') as f:
                            logs = '\n'.join(f.readlines())
                        st.text_area('Log', value=logs, height=500, label_visibility='hidden')
        message = {"role": "assistant", "content": response, "video": date}
        st.session_state.messages.append(message)

    # Display button
    st.button(":studio_microphone:", help="Click to use microphone", type='primary', use_container_width=True, on_click=click_button)


if __name__ == "__main__":		

    # run the app
    # streamlit run assistants.py

    main()

