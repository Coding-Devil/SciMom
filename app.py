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
    "Zephyr-7B": "HuggingFaceH4/zephyr-7b-beta"
}

# Pull info about the model to display
model_info = {
    "Zephyr-7B-β": {
        'description': """The **Zephyr 7B β** is a next-gen **GPT-like Large Language Model (LLM)** fine-tuned from Mistral-7B-v0.1, containing 7 billion parameters. This model is optimized for educational tasks and excels at science-related Q&A with high accuracy and performance.\n"""
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
st.sidebar.write("Built for my mom, with love ❤️.")

st.sidebar.markdown(model_info["Zephyr-7B-β"]['description'])
st.sidebar.markdown("""
### Zephyr 7B β 🤖
Your personal science assistant, built with **7 billion parameters** to help with all your science Q&As.

- **Trained using Ultrachat Feedbacks**!
- **Quick & Smart**: Handles easy to tough topics like a pro.
- **Accurate**: Reliable answers every time.

Need help with science? Zephyr’s got your back! 🔬📘
""")


st.sidebar.markdown("By Gokulnath ♔")

# If model selection was needed (now removed)
selected_model = "Zephyr-7B"  # Only one model remains

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
