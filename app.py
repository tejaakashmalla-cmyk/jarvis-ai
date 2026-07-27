"""
JARVIS OS - app.py
==================
ChatGPT-style Streamlit chat UI wired to the existing project modules.
Only app.py has been modified. Brain, LLMService, MemoryDetector,
MemoryManager, and voice.tts are used exactly as they already exist -
no new methods, no renamed imports, no architecture changes.
"""

import json
import os
import threading
from datetime import datetime

import streamlit as st

# ---------------------------------------------------------------------------
# Existing project modules - imports kept EXACTLY as-is
# ---------------------------------------------------------------------------
from brain.brain import JarvisBrain
from services.llm_service import LLMService
from brain.memory_detector import MemoryDetector
from memory.memory_manager import MemoryManager
from voice.tts import JarvisTTS


# =============================================================================
# CONSTANTS
# =============================================================================
USERS_FILE = "users.json"
APP_TITLE = "JARVIS OS"


# =============================================================================
# AUTH LAYER (existing users.json login - kept exactly, no hashing, no SQLite)
# =============================================================================
def load_users() -> dict:
    """Load users.json. Returns an empty dict if the file doesn't exist yet."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users: dict) -> None:
    """Persist the users dict back to users.json."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def register_user(username: str, password: str) -> tuple:
    """Create a new user entry in users.json. Returns (success, message)."""
    username = (username or "").strip()
    if not username or not password:
        return False, "Username and password are required."

    users = load_users()
    if username in users:
        return False, "That username is already taken."

    users[username] = {
        "password": password,
        "created_at": datetime.now().isoformat(),
    }
    save_users(users)
    return True, "Account created successfully. You can now log in."


def authenticate_user(username: str, password: str) -> bool:
    username = (username or "").strip()

    if not username or not password:
        return False

    users = load_users()
    record = users.get(username)

    if record is None:
        return False

    # OLD FORMAT
    if isinstance(record, str):
        return record == password

    # NEW FORMAT
    if isinstance(record, dict):
        return record.get("password") == password

    return False

    return record.get("password") == password


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
def init_session_state() -> None:
    """Ensure every session_state key the app relies on exists."""
    defaults = {
        "authenticated": False,
        "username": None,
        "messages": [],  # list of {"role": ..., "content": ..., "time": ...}
        "auth_error": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =============================================================================
# STYLING (existing dark futuristic theme - unchanged)
# =============================================================================
def inject_custom_css() -> None:
    """Inject the dark futuristic theme used across the whole app."""
    st.markdown(
        """
        <style>
        /* ---------- Global ---------- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        html, body, [class*="css"] {
            font-family: 'Segoe UI', 'Inter', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at top left, #0d1117 0%, #05070a 60%, #000000 100%);
            color: #e6edf3;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0e14 0%, #050709 100%);
            border-right: 1px solid rgba(0, 255, 200, 0.15);
        }

        section[data-testid="stSidebar"] * {
            color: #d7f5ec !important;
        }

        /* ---------- Header / Title glow ---------- */
        .jarvis-title {
            font-size: 2.1rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: 3px;
            background: linear-gradient(90deg, #00f5d4, #00bbf9, #00f5d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 25px rgba(0, 245, 212, 0.35);
            margin-bottom: 0.2rem;
        }

        .jarvis-subtitle {
            text-align: center;
            color: #7d8590;
            font-size: 0.85rem;
            letter-spacing: 2px;
            margin-bottom: 1.4rem;
        }

        /* ---------- Chat bubbles ---------- */
        div[data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(0, 245, 212, 0.08);
            border-radius: 14px;
            padding: 4px 6px;
            margin-bottom: 10px;
            box-shadow: 0 0 18px rgba(0, 0, 0, 0.25);
        }

        /* ---------- Buttons ---------- */
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            border: 1px solid rgba(0, 245, 212, 0.35);
            background: linear-gradient(135deg, rgba(0,245,212,0.08), rgba(0,187,249,0.08));
            color: #e6edf3;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            padding: 0.5rem 1rem;
        }

        .stButton > button:hover {
            border-color: #00f5d4;
            box-shadow: 0 0 16px rgba(0, 245, 212, 0.45);
            color: #00f5d4;
        }

        /* ---------- Chat input ---------- */
        .stChatInput textarea {
            background-color: #0d1117 !important;
            color: #e6edf3 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(0, 245, 212, 0.25) !important;
        }

        /* ---------- Thinking animation text ---------- */
        .jarvis-thinking {
            color: #00f5d4;
            font-style: italic;
            animation: pulseGlow 1.4s ease-in-out infinite;
        }

        @keyframes pulseGlow {
            0%   { opacity: 0.35; }
            50%  { opacity: 1.0;  }
            100% { opacity: 0.35; }
        }

        /* ---------- Scrollbar ---------- */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #05070a; }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 245, 212, 0.35);
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# AUTH UI (Login / Sign Up) - existing users.json based system
# =============================================================================
def render_auth_page() -> None:
    """Render the login/signup screen shown before authentication."""
    inject_custom_css()

    st.markdown(f'<div class="jarvis-title">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="jarvis-subtitle">YOUR PERSONAL AI ASSISTANT</div>',
        unsafe_allow_html=True,
    )

    col_left, col_center, col_right = st.columns([1, 1.4, 1])
    with col_center:
        login_tab, signup_tab = st.tabs(["🔐 Login", "🆕 Sign Up"])

        # ---------------- Login ----------------
        with login_tab:
            with st.form("login_form", clear_on_submit=False):
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input(
                    "Password", type="password", key="login_password"
                )
                login_submitted = st.form_submit_button("Enter JARVIS")

            if login_submitted:
                if authenticate_user(login_username, login_password):
                    st.session_state.authenticated = True
                    st.session_state.username = login_username.strip()
                    st.session_state.auth_error = ""
                    st.rerun()
                else:
                    st.session_state.auth_error = "Invalid username or password."

            if st.session_state.auth_error:
                st.error(st.session_state.auth_error)

        # ---------------- Sign Up ----------------
        with signup_tab:
            with st.form("signup_form", clear_on_submit=False):
                new_username = st.text_input("Choose a username", key="signup_username")
                new_password = st.text_input(
                    "Choose a password", type="password", key="signup_password"
                )
                confirm_password = st.text_input(
                    "Confirm password", type="password", key="signup_confirm"
                )
                signup_submitted = st.form_submit_button("Create Account")

            if signup_submitted:
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)


# =============================================================================
# MEMORY LAYER (runs on a background thread, never blocks the chat UI)
# Uses ONLY the existing methods: detector.extract() and memory.save_items()
# =============================================================================
def process_memory(user_input: str) -> None:
    """
    Detect and persist any memories from the latest user message.
    Executed on a background daemon thread so the UI never waits on it.
    """
    try:
        detector = MemoryDetector()
        items = detector.extract(user_input)

        if items:
            memory = MemoryManager()
            memory.save_items(items)
    except Exception as exc:  # noqa: BLE001 - never let memory errors break the app
        print(f"[JARVIS OS] Memory processing error: {exc}")


# =============================================================================
# CHAT UI
# =============================================================================
def render_message_history() -> None:
    """Render every past message stored in session_state."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def handle_new_user_message(prompt: str) -> None:
    """
    Handle a freshly submitted user prompt:
      1. Build the Brain's message payload from existing history.
      2. Store + render the user message.
      3. Stream the assistant's reply token-by-token (true streaming).
      4. Persist the assistant message.
      5. Kick off memory saving + voice synthesis on background threads.
    """
    # 1. Build history exactly as the existing Brain integration expects.
    history = []
    for msg in st.session_state.messages:
        history.append({"role": msg["role"], "content": msg["content"]})

    brain = JarvisBrain()
    messages = brain.create_messages(history=history, user_message=prompt)

    # 2. Store and render the user's message immediately.
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "time": datetime.now().isoformat()}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Stream the assistant's response token-by-token.
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown(
            '<span class="jarvis-thinking">🤖 Jarvis is thinking...</span>',
            unsafe_allow_html=True,
        )

        full_response = ""
        first_token_received = False

        try:
            llm = LLMService()

            for token in llm.stream_chat(messages):
                if not token:
                    continue

                if not first_token_received:
                    # The "thinking" placeholder is overwritten the moment the
                    # first real token arrives - no extra rerun needed.
                    first_token_received = True

                full_response += token
                response_placeholder.markdown(full_response + "▌")

            # Final render without the streaming cursor.
            response_placeholder.markdown(full_response if full_response else "…")

        except Exception as exc:  # noqa: BLE001 - surface the error, keep app alive
            full_response = f"⚠️ I ran into an error generating a response: {exc}"
            response_placeholder.markdown(full_response)

    # 4. Persist the assistant's message.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
            "time": datetime.now().isoformat(),
        }
    )

    # 5. Background work: memory extraction + voice, neither blocks the UI.
    threading.Thread(
        target=process_memory,
        args=(prompt,),
        daemon=True,
    ).start()

    if full_response and not full_response.startswith("⚠️"):
        tts = JarvisTTS()
        threading.Thread(
            target=tts.speak,
            args=(full_response,),
            daemon=True,
        ).start()


def render_sidebar() -> None:
    """Render the sidebar: user info, chat history, clear chat, logout."""
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, `{st.session_state.username}`")
        st.markdown("---")

        st.markdown("#### 💬 Chat History")
        if st.session_state.messages:
            user_turns = [m for m in st.session_state.messages if m["role"] == "user"]
            for i, turn in enumerate(user_turns[-15:], start=1):
                snippet = turn["content"][:40] + ("..." if len(turn["content"]) > 40 else "")
                st.caption(f"{i}. {snippet}")
        else:
            st.caption("No messages yet. Say hello!")

        st.markdown("---")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with col_b:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.messages = []
                st.rerun()

        st.markdown("---")
        st.caption("Powered by Ollama · Gemma3:4b · Piper TTS")


def render_chat_page() -> None:
    """Render the main authenticated chat experience."""
    inject_custom_css()
    render_sidebar()

    st.markdown(f'<div class="jarvis-title">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="jarvis-subtitle">ONLINE · READY TO ASSIST</div>',
        unsafe_allow_html=True,
    )

    # Render prior conversation first so new messages append below it,
    # avoiding flicker and duplicate re-draws.
    render_message_history()

    prompt = st.chat_input("Message JARVIS...")
    if prompt:
        handle_new_user_message(prompt)


# =============================================================================
# APP ENTRYPOINT
# =============================================================================
def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    if st.session_state.authenticated:
        render_chat_page()
    else:
        render_auth_page()


if __name__ == "__main__":
    main()