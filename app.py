import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the model and tokenizer
model_name = "HuggingFaceH4/zephyr-7b-beta"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define function to generate responses
def generate_response(prompt, max_length=150):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=max_length)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Streamlit app UI
st.set_page_config(page_title="SciMom - Your Science Guide", page_icon="🧬", layout="centered")

st.title("SciMom - Your Science Guide")
st.write("A chatbot to assist with Science NCERT content, built for my mom ❤️")

# User input
user_input = st.text_area("Ask a Science question:", placeholder="Type your question here...")

if st.button("Get Answer"):
    if user_input:
        with st.spinner("Thinking..."):
            response = generate_response(user_input)
        st.write("### Answer:")
        st.write(response)
    else:
        st.warning("Please enter a question to get an answer.")

# Sidebar for options
st.sidebar.title("Options")
st.sidebar.markdown("Adjust the chatbot settings:")
max_length = st.sidebar.slider("Max Response Length", min_value=50, max_value=500, value=150)
