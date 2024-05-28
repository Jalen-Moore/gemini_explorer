import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "sample-gemini-424016"
vertexai.init(project=project)

config = generative_models.GenerationConfig(temperature=0.4)

# Load model with config
model = GenerativeModel('gemini-pro', generation_config=config)
chat = model.start_chat()

# Helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message('model'):
        st.markdown(output)

    st.session_state['messages'].append(
        {
            "role": "user",
            "content": query
        }
    )

    st.session_state['messages'].append(
        {
            "role": "assistant",
            "content": output
        }
    )

st.title("Gemini Explorer")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state['messages'] = []

# Display and load to chat history
for index, message in enumerate(st.session_state['messages']):
    content = Content(role=message['role'], parts=[Part.from_text(message['content'])])

    if index != 0:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    chat.history.append(content)

# For capturing user input
query = st.chat_input("Gemini Explorer")

# Implementation of the initial message logic
if len(st.session_state['messages']) == 0:

    # Get user's name and send it to the initial prompt
    user_name = st.text_input("Please enter your name")
    if st.button("Enter"):
        initial_prompt = "Greet " + user_name + ". Introduce yourself as ReX, an assistant powered by Google Gemini. Please make all of your responses reference the Harry Potter franchise in some way."
        llm_function(chat, initial_prompt)

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
