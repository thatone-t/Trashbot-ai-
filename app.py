import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="My Pocket AI", page_icon="🤖", layout="wide")

# 2. Sidebar Settings & Security
with st.sidebar:
    st.title("⚙️ Settings")
    # Using 'password' type hides the key characters
    api_key = st.text_input("Enter Google API Key:", type="password", help="Get your key at aistudio.google.com")
    
    st.divider()
    
    # NEW FEATURE: Model Selection & Creativity Control
    model_choice = st.selectbox("Choose Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    temp = st.slider("Creativity (Temperature):", 0.0, 2.0, 1.0)
    
    # NEW FEATURE: Clear Chat Button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 3. AI Logic Setup
if api_key:
    try:
        genai.configure(api_key=api_key)
        # We define generation config for better control
        generation_config = {
            "temperature": temp,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }
        model = genai.GenerativeModel(model_name=model_choice, generation_config=generation_config)

        # 4. Initialize Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 5. Display Chat History (using standard chat UI)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 6. Chat Input Logic
        if prompt := st.chat_input("What's on your mind?"):
            # Display user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # NEW FEATURE: Real Contextual Memory
            # We convert our history into the format Gemini expects
            history = [
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1] # Exclude current prompt
            ]
            
            chat_session = model.start_chat(history=history)

            # Generate AI response with a loading spinner
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_session.send_message(prompt)
                    st.markdown(response.text)
            
            # Add AI response to history
            st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("👈 Please enter your API Key in the sidebar to begin.")
    st.info("Tip: Gemini 1.5 Flash is faster, while Pro is smarter for complex tasks.")
