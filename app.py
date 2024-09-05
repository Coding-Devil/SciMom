import numpy as np
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(
  base_url="https://api-inference.huggingface.co/v1",
  api_key=os.environ.get('HUGGINGFACEHUB_API_TOKEN')  # Replace with your token
)

# Create supported model
model_links = {
    "Meta-Llama-3-8B": "meta-llama/Meta-Llama-3-8B-Instruct"
}

# Pull info about the model to display
model_info = {
    "Meta-Llama-3-8B": {
        'description': """The Llama (3) model is a **Large Language Model (LLM)** designed to assist with question and answer interactions.\n
        \nThis model was created by Meta's AI team and has over 8 billion parameters.\n
        **Training**: The model was fine-tuned on science textbooks from the NCERT curriculum using Docker AutoTrain to ensure it can provide relevant and accurate responses in the education domain.\n
        **Purpose**: This version of Llama has been trained specifically for educational purposes, focusing on answering science-related queries in a clear and simple manner to help students and teachers alike.\n"""
    }
}

# Reset the conversation
def reset_conversation():
    st.session_state.conversation = []
    st.session_state.messages = []
    return None

# App title and description
st.title("Sci-Mom 👩‍🏫 ")
st.subheader("AI chatbot for Solving your doubts 📚 :)")

# Custom description for SciMom in the sidebar
st.sidebar.write("Built for my mom, with love ❤️. This model is pretrained with textbooks of Science NCERT.")
st.sidebar.write("Base-Model used: Meta Llama, trained using: Docker AutoTrain.")

# Add technical details in the sidebar
st.sidebar.markdown(model_info["Meta-Llama-3-8B"]['description'])
st.sidebar.markdown("*By Gokulnath ♔ *")

# If model selection was needed (now removed)
selected_model = "Meta-Llama-3-8B"  # Only one model remains

if "prev_option" not in st.session_state:
    st.session_state.prev_option = selected_model

if st.session_state.prev_option != selected_model:
    st.session_state.messages = []
    st.session_state.prev_option = selected_model
    reset_conversation()

# Pull in the model we want to use
repo_id = model_links[selected_model]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask Scimom!"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model_links[selected_model],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.5,  # Default temperature setting
                stream=True,
                max_tokens=3000,
            )
            response = st.write_stream(stream)

        except Exception as e:
            response = "😵‍💫 Something went wrong. Please try again later."
            st.write(response)
            st.write("This was the error message:")
            st.write(e)

    st.session_state.messages.append({"role": "assistant", "content": response})
