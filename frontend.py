# Step1: Setup Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Send user message to backend
    try:
        fixed_dummy_response_from_backend = requests.post(BACKEND_URL, json={"message": user_input})
        if fixed_dummy_response_from_backend.status_code == 200:
            response_data = fixed_dummy_response_from_backend.json()
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f'{response_data["response"]} WITH TOOL: [{response_data["tool_called"]}]'
            })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Sorry, I’m having trouble reaching the backend service."
            })
    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"An error occurred: {e}"
        })

# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
