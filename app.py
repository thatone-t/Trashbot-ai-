import streamlit as st
import google.generativeai as genai

# 1. Setup the Page Title and Icon
st.set_page_config(page_title="My Pocket AI", page_icon="🤖")
st.title("📱 My Custom ChatGPT")

# 2. Configuration (You can get a free API key at aistudio.google.com)
# For now, this code will ask you for the key in the sidebar
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 4. Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Chat Input Logic
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
        # Add AI response to history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("Please enter your API Key in the sidebar to start chatting! You can get one for free at Google AI Studio.")
