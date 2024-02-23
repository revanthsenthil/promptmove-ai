"""
FUNCTION CALLING EXAMPLES
https://platform.openai.com/docs/assistants/tools/function-calling

"""
from openai import OpenAI
import streamlit as st

def create_assistant():
    
	# gets the environment variable OPENAI_API_KEY
	client = OpenAI()

	# Upload files with an "assistants" purpose
	house_info_file = client.files.create(
			file=open("house_information.json", "rb"),
			purpose='assistants'
		)

	example_functions = client.files.create(
			file=open("example_virtualhome_functions.py", "rb"),
			purpose='assistants'
		)

	# Add the files to the assistant
	assistant = client.beta.assistants.create(
			instructions="You are a personal house assistant. Write and run virtualhome simulator code \
					to help with tasks around the house, such as cooking, cleaning, organizing, and retrieving items.",
			model="gpt-3.5-turbo-0125",
			tools=[{"type": "retrieval"}],
			file_ids=[house_info_file.id, example_functions.id]
		)
    
	# Create one thread per user
	thread = client.beta.threads.create()

	return client, assistant, thread


def main():

	# Set up Streamlit app
	st.set_page_config(page_title="PromptMove-AI")
	st.title(":blue[PromptMove-AI]")
	st.write("This is a virtual assistant to help with tasks around the house, such as \
		  	cooking, cleaning, retrieving items, and general assistance.")	
	with st.sidebar:
		st.title('Credentials')

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

	# Function for generating LLM response
	def generate_response(user_input):
		if user_input in [None, ""] or type(user_input) != str:
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

		return messages.data[0].content[0].text.value

	# User-provided input
	if user_input := st.chat_input():
		st.session_state.messages.append({"role": "user", "content": user_input})
		with st.chat_message("user"):
			st.write(user_input)

	# Generate a new response if last message is not from assistant
	if st.session_state.messages[-1]["role"] != "assistant":
		with st.chat_message("assistant"):
			with st.spinner("Thinking..."):
				response = generate_response(user_input) 
				st.write(response) 
		message = {"role": "assistant", "content": response}
		st.session_state.messages.append(message)


if __name__ == "__main__":		
	
	# run the app
	main()
		
