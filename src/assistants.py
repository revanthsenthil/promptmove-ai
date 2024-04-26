"""
FUNCTION CALLING EXAMPLES
https://platform.openai.com/docs/assistants/tools/function-calling

App inspired by blogpost: https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/
"""

from openai import OpenAI
import openai
import streamlit as st

import src.audio.transcribe as transcribe
from src.functions import get_current_weather, perform_action_on_object, run_script

import os
import re
import json

p = os.path.abspath("../config")

def create_assistant():

    # gets the environment variable OPENAI_API_KEY
    try:
        client = OpenAI(api_key=st.session_state.openai_key)
    except openai.OpenAIError:
        st.error("Error creating client instance. Please check your credentials.")
        return None

    # Add the files to the assistant
    try:
        assistant = client.beta.assistants.create(
            instructions="You are a personal house assistant for assisting in the VirtualHome simulated environment \
            to help with tasks around the house, such as cooking, cleaning, organizing, retrieving items, and general knowledge about the state of the house.",
            model="gpt-4-turbo",
            tools=
            [
                {"type": "file_search"},
                {
                "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "unit": {"type": "string", "enum": ["fahrenheit", "celsius"]},
                            },
                            "required": ["location"],
                        },
                    },
                },
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
                                    "description": "the action to represent doing something with an object or location. Eg. 'walk', 'sit', 'find', 'eat', 'move'",
                                },
                                "object": {
                                    "type": "string", 
                                    "description": "the object or location to perform the action on. Eg. 'sofa', 'kitchen', 'cat'",
                                },
                            },
                            "required": ["object"],
                        },
                    },
                }
            ]
        )
    except openai.OpenAIError:
        st.error("Error creating assistant. Please check your credentials.")
        return None
    
    # Create a vector store
    vector_store = client.beta.vector_stores.create(name="Simulated House Information")
    
    # Ready the files for upload to OpenAI 
    file_paths = [p +'/house_information.json']
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    _ = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id = vector_store.id, 
        files = file_streams
    )

    # update assistant to use new vector store
    assistant = client.beta.assistants.update(
        assistant_id = assistant.id,
        tool_resources = {"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # Create one thread per user
    thread = client.beta.threads.create()

    return client, assistant, thread

# Function for generating LLM response
def generate_response(user_input):
    if user_input in [None, ""] or not isinstance(user_input, str):
        return "Invalid input. Please try again."

    # load session's assistant
    client, assistant, thread = st.session_state.assistant

    _ = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    print(f"\nRunning generate_response({user_input})")

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    if run.status == 'completed':
        # No tool calls
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(messages)
        return messages.data[0].content[0].text.value
    else:
        print(run.status)

    # Define the list to store tool outputs
    tool_outputs = []

    # Loop through each tool in the required action section
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    print('Tool calls:', tool_calls)

    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
            'perform_action_on_object': perform_action_on_object
        }
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print(f'Function args: {function_args}')
            function_response = function_to_call(**function_args)
            tool_outputs.append(
                {
                    "tool_call_id": tool_call.id,
                    #"role": "tool",
                    #"name": function_name,
                    "output": function_response,
                }
            )
        run_script()
    else:
        # No tool calls
        print("No tool calls.")
        return messages.data[0].content[0].text.value


    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            print(messages)
        else:
            print(run.status)
        
        return messages.data[0].content[0].text.value

    else:
        # No tool outputs
        print('\nTHIS CODE RUNS\n')
        # create a message associated with the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # create a run associated with the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for run to complete
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status in ["failed", "cancelled", "cancelling", "expired"]:
                return f"Error: {run.status}"
            if run.status == "requires_action":
                return "Assistant requires action"

        # List the messages associated with the thread
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        return remove_brackets(messages.data[0].content[0].text.value)

def click_button():
    st.session_state.clicked = True

def remove_brackets(text):
    pattern = r'【.*?】'  # Matches text between "【" and "】" non-greedily
    return re.sub(pattern, '', text)

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
        print("Key is correct!")
    except Exception:
        st.session_state.correct_key = False

def main():

    # Set up Streamlit app
    st.set_page_config(page_title="PromptMove-AI")
    st.title(":blue[PromptMove-AI]")
    st.write("This is a virtual assistant to help with tasks around the house, such as \
            cooking, cleaning, retrieving items, and general assistance.")	
    
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

    # User-provided input
    if user_input := st.chat_input():
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
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(user_input) 
                st.write(response) 
                # st.video('video_normal.mp4', format="video/mp4", start_time=0, subtitles=None, end_time=None, loop=False)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

    # Display button
    st.button(":studio_microphone:", help="Click to use microphone", type='primary', use_container_width=True, on_click=click_button)


if __name__ == "__main__":		

    # run the app
    # streamlit run assistants.py

    main()

