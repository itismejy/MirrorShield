import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# 1. Load environment variables
load_dotenv()

# 2. Configure your Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("No API key found. Please check your .env file.")
    st.stop()
genai.configure(api_key=api_key)

# 3. Choose your Gemini model
MODEL = "models/gemini-1.5-flash"   # free Flash model

# 4. Create the Gemini model object
model = genai.GenerativeModel(model_name=MODEL)

# 5. Set up Streamlit page
st.set_page_config(
    page_title="MirrorShield - NPD Interaction Simulator",
    page_icon="🛡️",
    layout="centered"
)

# 6. Sidebar with your Red Flag Guide
with st.sidebar:
    st.header("🚩 Red Flag Guide")
    st.markdown("""
    ### Common Manipulation Tactics:

    1. **Gaslighting**  
       - Making you question your reality  
       - Denying things that happened  
       - "You're too sensitive"

    2. **Love Bombing**  
       - Excessive affection  
       - Over-the-top compliments  
       - Moving too fast

    3. **Blame-Shifting**  
       - Never taking responsibility  
       - Always the victim  
       - Turning situations around

    Pay attention to these patterns in the conversation!
    """)

# 7. Initialize or retrieve a single chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
    # Send the system prompt once at the very start
    system_prompt = (
        "You are simulating someone with narcissistic personality disorder traits. "
        "Your responses should subtly demonstrate gaslighting, love‑bombing, "
        "and blame‑shifting, while remaining realistic and conversational."
    )
    st.session_state.chat.send_message(system_prompt)

# 8. Initialize chat history storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# 9. Page header and instructions
st.title("🛡️ MirrorShield")
st.markdown("""
This interactive simulation helps you recognize and understand manipulative behaviors 
associated with narcissistic personality disorder (NPD).

Type a message below to start the conversation.
""")

# 10. Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 11. Handle new user input
if user_input := st.chat_input("Type your message here..."):
    # a) Display & save the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # b) Send the user message to Gemini
    try:
        response = st.session_state.chat.send_message(user_input)
        assistant_text = response.text

        # c) Display & save Gemini's reply
        st.session_state.messages.append({"role": "assistant", "content": assistant_text})
        with st.chat_message("assistant"):
            st.markdown(assistant_text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        if "quota" in str(e).lower():
            st.error("API quota exceeded. Please check your API key limits.")
