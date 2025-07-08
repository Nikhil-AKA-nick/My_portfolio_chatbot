import os
# use the pure‑Python protobuf parser (avoids the “Descriptors cannot be created directly” error)
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"


import streamlit as st
from mychatbot import get_response
import time

st.set_page_config(page_title="AI Chatbot", layout="centered")

# Session setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False


# ---------- CSS Styling ----------
# ---------- CSS Styling (Purple Theme) ----------


st.markdown("""
    <style>
        .main {
            background-color: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: auto;
        }
        .chat-message {
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
        }
        .bot .bubble {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            padding: 12px 18px;
            border-radius: 16px 16px 16px 0;
            max-width: 75%;
            font-size: 16px;
        }
        .user {
            justify-content: flex-end;
        }
        .user .bubble {
            background: #f0f0f0;
            color: black;
            padding: 12px 18px;
            border-radius: 16px 16px 0 16px;
            max-width: 75%;
            font-size: 16px;
        }
        .bot-avatar, .user-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            margin: 0 10px;
        }
        .bot-avatar {
            background: url('https://cdn-icons-png.flaticon.com/512/4712/4712034.png');
            background-size: cover;
        }
        .user-avatar {
            background: url('https://cdn-icons-png.flaticon.com/512/4140/4140048.png');
            background-size: cover;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Typing effect ----------
def display_typing_response(text, delay=0.03):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(f'<div class="chat-message bot"><div class="bot-avatar"></div><div class="bubble">{output}</div></div>', unsafe_allow_html=True)
        time.sleep(delay)

# ---------- Header ----------
st.markdown("<h2 style='text-align:center;'>🤖 Hi, I’m Nikhil, Let’s Chat About My Work</h2>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 15px; margin-top: -10px; margin-bottom: 20px;'>
📄 <a href='https://drive.google.com/file/d/1HXZx6b-3EUGq6U8iOGS99C-VhmRpQKao/view?usp=sharing' target='_blank'>Resume</a> &nbsp;|&nbsp;
💼 <a href='https://linkedin.com/in/nikhil-sonone' target='_blank'>LinkedIn</a> &nbsp;|&nbsp;
💻 <a href='https://github.com/Nikhil-AKA-nick' target='_blank'>GitHub</a> &nbsp;|&nbsp;
📧 <a href='mailto:nikhilsonone12345@gmail.com'>Email</a>
</div>
""", unsafe_allow_html=True)



# ---------- Main Container ----------
st.markdown('<div class="main">', unsafe_allow_html=True)

# ---------- Message Storage ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Render Message History ----------
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="bubble">{content}</div>
            <div class="user-avatar"></div>
        </div>
        """, unsafe_allow_html=True)
    elif role == "bot":
        st.markdown(f"""
        <div class="chat-message bot">
            <div class="bot-avatar"></div>
            <div class="bubble">{content}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- Chat Input (Clean Style) ----------
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message immediately
    st.markdown(f"""
    <div class="chat-message user">
        <div class="bubble">{user_input}</div>
        <div class="user-avatar"></div>
    </div>
    """, unsafe_allow_html=True)

    # Get response
    with st.spinner("🤖 Typing..."):
        response = get_response(user_input)

    display_typing_response(response)
    st.session_state.messages.append({"role": "bot", "content": response})

# ---------- Response Phase ----------
elif st.session_state.waiting_for_response:
    user_input = st.session_state.last_input

    # Get response
    with st.spinner("🤖 Typing..."):
        response = get_response(user_input)

    # Typing animation
    display_typing_response(response)

    # Save response
    st.session_state.messages.append({"role": "bot", "content": response})
    st.session_state.waiting_for_response = False
    st.rerun()
