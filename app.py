import streamlit as st
import requests
import base64
import os

st.set_page_config(page_title="💬 Ementora AI Assistant", layout="centered")

# === Helper to convert image to base64 ===
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# === Load avatar images ===
USER_AVATAR = image_to_base64("static/user.png")
BOT_AVATAR = image_to_base64("static/bot.png")

# === Session State ===
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# === CSS Styles ===
st.markdown("""
<style>
body {
    background-color: #f0f4fb;
}
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 20px;
}
.message {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 14px 18px;
    border-radius: 18px;
    max-width: 80%;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}
.bot {
    background-color: #e3f0ff;
    color: #003366;
    border: 1px solid #cce0ff;
}
.user {
    background-color: #d0e9ff;
    color: #002244;
    border: 1px solid #99ccff;
    align-self: flex-end;
    flex-direction: row-reverse;
}
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.input-box {
    padding: 10px;
    border-radius: 12px;
    background-color: #ffffff;
    border: 1px solid #d0d7de;
}
.send-button {
    background-color: #1e88e5;
    color: white;
    border-radius: 10px;
    padding: 8px 20px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# === Header & Sidebar ===
st.title("💬 Ementora AI Assistant")

with st.sidebar:
    st.image("static/bot.png", width=80)
    st.header("👤 User Info")
    user_id = st.text_input("Enter your User ID", value=st.session_state.get("user_id", ""))
    if user_id:
        st.session_state.user_id = user_id
    st.markdown("📝 The bot will ask for name, email, phone, and ID.")
    st.markdown("---")
    if st.button("🔄 Clear Chat"):
        st.session_state.chat = []

# === Chat Display ===
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.chat:
    role = msg["role"]
    content = msg["content"]
    avatar = USER_AVATAR if role == "user" else BOT_AVATAR
    role_class = "user" if role == "user" else "bot"

    st.markdown(f"""
    <div class="message {role_class}">
        <img src="data:image/png;base64,{avatar}" class="avatar" />
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# === Message Input Form ===
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", placeholder="Hi there!", key="input", help="Press Send to chat")
    submitted = st.form_submit_button("Send")

# === On Submit ===
if submitted and user_input and st.session_state.user_id:
    st.session_state.chat.append({"role": "user", "content": user_input})

    try:
        res = requests.post("https://ementora-bot-2.onrender.com/chat", json={
            "user_id": st.session_state.user_id,
            "message": user_input
        })
        reply = res.json().get("reply", "🤖 Sorry, I didn’t understand that.")
    except Exception as e:
        reply = f"❌ Error: {e}"

    st.session_state.chat.append({"role": "bot", "content": reply})
    st.rerun()
elif submitted and not st.session_state.user_id:
    st.warning("⚠️ Please enter a User ID in the sidebar to begin chatting.")
