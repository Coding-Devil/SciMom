import streamlit as st
import os

# Create supported models
model_links = {
    "Zephyr-7B-β": "HuggingFaceH4/zephyr-7b-beta",
    "Meta-Llama-3-8B": "meta-llama/Meta-Llama-3-8B-Instruct"
}

# Pull info about the model to display
model_info = {
    "Zephyr-7B-β": {
        'description': "Zephyr is a **Large Language Model (LLM)** trained to act as a helpful assistant. "
                       "[Zephyr-7B-β](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta) is a fine-tuned version "
                       "of mistralai/Mistral-7B-v0.1, trained using Direct Preference Optimization (DPO).",
    },
    "Meta-Llama-3-8B": {
        'description': "Llama (3) is a **Large Language Model (LLM)** designed for question and answer interactions, "
                       "created by [Meta's AI](https://llama.meta.com/), with over **8 billion parameters.**"
    }
}

# Sidebar details
st.sidebar.title("SciMom - Your Science Guide")
st.sidebar.markdown("A chatbot to assist with Science NCERT content, built for my mom ❤️")
st.sidebar.markdown("### Options")

# Define the available models
models = ["Zephyr-7B-β", "Meta-Llama-3-8B"]

# Model selection dropdown
selected_model = st.sidebar.selectbox("Select Model", models)

# Display selected model info
st.sidebar.markdown(f"You're now chatting with **{selected_model}**")
st.sidebar.markdown(model_info[selected_model]['description'])
st.sidebar.image(model_info[selected_model]['logo'])

# Temperature slider
temp_values = st.sidebar.slider('Select a temperature value', 0.0, 1.0, 0.5)

# Reset button to clear conversation
def reset_conversation():
    st.session_state.messages = []
st.sidebar.button('Reset Chat', on_click=reset_conversation)

# Conversation management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update session state if model changes
if "prev_option" not in st.session_state:
    st.session_state.prev_option = selected_model

if st.session_state.prev_option != selected_model:
    st.session_state.messages = []
    st.session_state.prev_option = selected_model
    reset_conversation()

# Streamlit main interface
st.title(f'Chat with {selected_model}')
st.subheader("Ask any Science question:")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(f"Hi I'm {selected_model}, ask me a question"):

    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model_links[selected_model],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=temp_values,
                stream=True,
                max_tokens=3000,
            )
            response = st.write_stream(stream)
        except Exception as e:
            response = "😵‍💫 Something went wrong! Please try again later."
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
