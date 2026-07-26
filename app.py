import streamlit as st
from brain.brain import JarvisBrain
from services.llm_service import LLMService
from datetime import datetime
import json
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="JARVIS AI",
    page_icon="🤖",
    layout="wide"
)

# =========================
# HIDE STREAMLIT ICONS
# =========================

st.markdown("""
<style>

/* BACKGROUND */

html, body, [class*="css"] {
    background: linear-gradient(135deg,#020617,#020617,#031b4e);
    color: white;
    font-family: 'Segoe UI';
}

/* REMOVE STREAMLIT DEFAULT UI */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stDeployButton {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}

.viewerBadge_container__1QSob {
    display: none !important;
}

.viewerBadge_link__1S137 {
    display: none !important;
}

.viewerBadge_text__1JaDK {
    display: none !important;
}

a[href*="github"] {
    display: none !important;
}

/* TITLES */

.main-title {
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#38bdf8;
    margin-top:20px;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
}

/* CHAT */

.chat-box{
    padding:18px;
    border-radius:18px;
    margin-top:15px;
    margin-bottom:15px;
    font-size:17px;
    line-height:1.7;
}

.user{
    background:#1e293b;
    border-left:5px solid #ef4444;
}

.bot{
    background:#111827;
    border-left:5px solid #38bdf8;
}

/* INPUT */

.stChatInput input{
    background:#111827 !important;
    color:white !important;
    border:1px solid #334155 !important;
}

/* SIDEBAR */

.sidebar-box{
    background:#111827;
    padding:15px;
    border-radius:15px;
    margin-bottom:15px;
}

/* LOGIN */

.login-box{
    max-width:450px;
    margin:auto;
    background:#111827;
    padding:40px;
    border-radius:20px;
    margin-top:80px;
}

.stTextInput input{
    background:#1e293b !important;
    color:white !important;
}

/* BUTTONS */

.stButton button{
    border-radius:10px !important;
    background:#0f172a !important;
    color:white !important;
    border:1px solid #334155 !important;
}

.stButton button:hover{
    border:1px solid #38bdf8 !important;
    color:#38bdf8 !important;
}

/* FOOTER */

.footer{
    text-align:center;
    color:#94a3b8;
    margin-top:40px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GROQ API
# =========================

brain = JarvisBrain()
llm = LLMService()
# =========================
# USERS FILE
# =========================

USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

with open(USERS_FILE, "r") as f:
    users = json.load(f)

# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# LOGIN PAGE
# =========================

if not st.session_state.logged_in:

    st.markdown("""
    <div class='main-title'>🤖 JARVIS AI</div>
    <div class='sub-title'>
    Futuristic AI Assistant created by Akash
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.subheader("🔐 Login / Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    # LOGIN

    with col1:

        if st.button("Login"):

            if username in users and users[username] == password:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login Successful ✅")
                st.rerun()

            else:
                st.error("Invalid Username or Password")

    # SIGNUP

    with col2:

        if st.button("Signup"):

            if username in users:

                st.warning("Username already exists")

            elif username == "" or password == "":

                st.warning("Enter username and password")

            else:

                users[username] = password

                with open(USERS_FILE, "w") as f:
                    json.dump(users, f)

                st.success("Account Created Successfully ✅")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("# 🤖 JARVIS AI")

    st.write(f"Welcome, {st.session_state.username}")

    st.write("Created by Akash")

    st.write("Powered by Groq + Llama3")

    st.markdown("---")

    st.markdown(f"""
    <div class='sidebar-box'>
    <h4>Total Messages</h4>
    <h2>{len(st.session_state.messages)}</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.rerun()

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.messages = []

        st.rerun()

# =========================
# TITLE
# =========================

st.markdown("""
<div class='main-title'>🤖 JARVIS AI</div>
<div class='sub-title'>
Futuristic AI Assistant created by Akash
</div>
""", unsafe_allow_html=True)

# =========================
# SHOW CHAT HISTORY
# =========================

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(f"""
        <div class="chat-box user">
        <b>🧑 You:</b><br><br>
        {msg["content"]}
        <br><br>
        <small>{msg["time"]}</small>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="chat-box bot">
        <b>🤖 JARVIS AI:</b><br><br>
        {msg["content"]}
        <br><br>
        <small>{msg["time"]}</small>
        </div>
        """, unsafe_allow_html=True)

# =========================
# CHAT INPUT
# =========================

user_input = st.chat_input("Ask JARVIS anything...")

# =========================
# WHEN USER SENDS MESSAGE
# =========================

if user_input:

    current_time = datetime.now().strftime("%I:%M %p")

    # SAVE USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": current_time
    })

    # SHOW USER MESSAGE IMMEDIATELY

    st.markdown(f"""
    <div class="chat-box user">
    <b>🧑 You:</b><br><br>
    {user_input}
    <br><br>
    <small>{current_time}</small>
    </div>
    """, unsafe_allow_html=True)

    # THINKING MESSAGE

    thinking = st.empty()

    thinking.markdown("""
    <div style='padding:10px; color:white;'>
    🤖 JARVIS is thinking...
    </div>
    """, unsafe_allow_html=True)
    try:

        # Build conversation history
        history = []

        for msg in st.session_state.messages:
            history.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Create messages using the Brain
        messages = brain.create_messages(
            history=history,
            user_message=user_input
        )

        # Ask the LLM
        bot_reply = llm.chat(messages)

    except Exception as e:

        bot_reply = f"Error: {str(e)}"

    thinking.empty()

    # SAVE BOT MESSAGE

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "time": current_time
    })

    st.rerun()

# =========================
# FOOTER
# =========================

st.markdown("""
<div class='footer'>
Generated by JARVIS AI
</div>
""", unsafe_allow_html=True)