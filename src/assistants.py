"""
FUNCTION CALLING EXAMPLES
https://platform.openai.com/docs/assistants/tools/function-calling

App inspired by blogpost: https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/
"""

from openai import OpenAI
import openai
import streamlit as st

import src.audio.transcribe as transcribe

import configparser
import os
import re

p = os.path.abspath("../config")

def create_assistant():

    # gets the environment variable OPENAI_API_KEY
    try:
        client = OpenAI()
    except openai.OpenAIError:
        config = configparser.ConfigParser()
        config.read('../.env')
        key = config['KEYS']['OPENAI_API_KEY']
        client = OpenAI(api_key=key)

    # Upload files with an "assistants" purpose
    house_info_file = client.files.create(
        file=open(p +'/house_information.json', "rb"),
        purpose='assistants'
    )

    example_functions = client.files.create(
        file=open(p + '/example_virtualhome_functions.py', "rb"),
        purpose='assistants'
    )

    # Add the files to the assistant
    assistant = client.beta.assistants.create(
        instructions="You are a personal house assistant for assisting in the VirtualHome simulated environment \
        to help with tasks around the house, such as cooking, cleaning, organizing, retrieving items, and general knowledge about the state of the house.",
        model="gpt-3.5-turbo-0125",
        tools=[{"type": "retrieval"}],
        file_ids=[house_info_file.id, example_functions.id]
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

def credentials():
    st.title('Credentials')
    if 'KEY' in st.secrets:
        st.success('OpenAI API Key already provided!', icon='✅')
        openai_key = st.secrets['KEY']
    else:
        openai_key = st.text_input('Enter OpenAI API Key:', type='password')
        if not openai_key:
            st.warning('Please enter your OpenAI API Key!', icon='⚠️')
        else:
            st.success('Thank You!', icon='✅')
    st.markdown('[GitHub repo](https://github.com/revanthsenthil/promptmove-ai)')
    return openai_key

def click_button():
    st.session_state.clicked = True

def remove_brackets(text):
    pattern = r'【.*?】'  # Matches text between "【" and "】" non-greedily
    return re.sub(pattern, '', text)

def main():

    # Set up Streamlit app
    st.set_page_config(page_title="PromptMove-AI")
    st.title(":blue[PromptMove-AI]")
    st.write("This is a virtual assistant to help with tasks around the house, such as \
            cooking, cleaning, retrieving items, and general assistance.")	
    
    # Set up siebar for OpenAI API key
    # with st.sidebar:
    #    key = credentials()

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    # get assistant if not already created
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
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

    # Display button
    st.button(":studio_microphone:", help="Click to use microphone", type='primary', use_container_width=True, on_click=click_button)


if __name__ == "__main__":		

    # run the app
    main()

