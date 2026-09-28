import json
import os
import uuid
from datetime import datetime

import streamlit as st

# Use logo.png next to app.py if it exists, otherwise fall back to an emoji
LOGO = "logo.png" if os.path.exists("logo.png") else "🛡️"

st.set_page_config(page_title="Incident Response Assistant", page_icon=LOGO, layout="wide")

HISTORY_FILE = "chat_history.json"
rerun = st.rerun if hasattr(st, "rerun") else st.experimental_rerun

# ---------- Styling ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer {visibility: hidden;}
[data-testid="stAppDeployButton"] {display: none;}
.stDeployButton {display: none;}

.stApp {background-color: #0A0F1C; color: #E5E9F0;}
.block-container {padding-top: 2rem; padding-bottom: 6rem; max-width: 820px;}

/* Header */
.header {
    padding: 4px 0 18px 0;
    border-bottom: 1px solid #1D2939;
    margin-bottom: 24px;
}
.header h1 {
    margin: 0; font-size: 1.55rem; font-weight: 700;
    color: #F8FAFC; letter-spacing: -0.01em;
}
.header p {margin: 6px 0 0; color: #98A2B3; font-size: 0.92rem;}

/* Welcome panel */
.welcome {
    background: #101828;
    border: 1px solid #1D2939;
    border-left: 3px solid #38BDF8;
    border-radius: 12px;
    padding: 22px 24px;
}
.welcome h3 {margin: 0 0 8px; font-size: 1.05rem; color: #F8FAFC; font-weight: 600;}
.welcome p {margin: 0 0 10px; color: #98A2B3; font-size: 0.92rem; line-height: 1.55;}
.welcome ul {margin: 0; padding-left: 18px; color: #C7D0DC; font-size: 0.9rem; line-height: 1.8;}

/* Sidebar */
[data-testid="stSidebar"] {background-color: #0D1424; border-right: 1px solid #1D2939;}
.brand {display: flex; align-items: center; gap: 10px; margin-bottom: 4px;}
.brand-title {font-size: 1.05rem; font-weight: 700; color: #F8FAFC;}
.brand-sub {font-size: 0.75rem; color: #667085; margin-bottom: 14px;}
.group-label {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: #667085; margin: 16px 0 6px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #101828;
    border: 1px solid #1D2939;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 12px;
}
[data-testid="stChatMessage"] p {line-height: 1.6;}

/* Buttons */
.stButton > button {
    width: 100%; text-align: left; border-radius: 8px;
    border: 1px solid #1D2939; color: #C7D0DC; background: #101828;
    font-size: 0.86rem; font-weight: 500; transition: all .15s ease;
}
.stButton > button:hover {border-color: #38BDF8; color: #38BDF8; background: #0F1B2E;}
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: #38BDF8; color: #04101F; border: 1px solid #38BDF8;
    font-weight: 600; text-align: center;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: #7DD3FC; border-color: #7DD3FC; color: #04101F;
}
.stDownloadButton > button {
    width: 100%; border-radius: 8px; border: 1px solid #1D2939;
    color: #C7D0DC; background: #101828; font-size: 0.86rem; font-weight: 500;
}
.stDownloadButton > button:hover {border-color: #38BDF8; color: #38BDF8;}

/* Footer note */
.footnote {text-align: center; color: #667085; font-size: 0.75rem; margin-top: 8px;}
</style>
    """,
    unsafe_allow_html=True,
)

# ---------- Load saved chats ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                st.session_state.chats = json.load(f)
        except Exception:
            st.session_state.chats = {}
    st.session_state.current = None

chats = st.session_state.chats

# ---------- Sidebar ----------
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=44)
    st.sidebar.markdown(
        '<div class="brand-title">IR Assistant</div>'
        '<div class="brand-sub">Incident response support</div>',
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        """
<div class="brand">
<svg width="34" height="34" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="lg" x1="6" y1="4" x2="42" y2="44" gradientUnits="userSpaceOnUse"><stop stop-color="#38BDF8"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs>
<path d="M24 4L7 10v13c0 10.5 7.2 18.2 17 21 9.8-2.8 17-10.5 17-21V10L24 4z" fill="url(#lg)"/>
<path d="M13 25h6l3-7 5 14 3-7h5" stroke="#0A0F1C" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
<span class="brand-title">IR Assistant</span>
</div>
<div class="brand-sub">Incident response support</div>
        """,
        unsafe_allow_html=True,
    )

if st.sidebar.button("+  New incident", type="primary"):
    st.session_state.current = None
    rerun()

search = st.sidebar.text_input("Search", placeholder="Search incidents...", label_visibility="collapsed")

sorted_ids = sorted(chats, key=lambda k: chats[k]["created"], reverse=True)
today = datetime.now().date()
last_group = None
shown = 0

for cid in sorted_ids:
    chat = chats[cid]
    if search:
        text = chat["title"] + " " + " ".join(m["content"] for m in chat["messages"])
        if search.lower() not in text.lower():
            continue

    days_old = (today - datetime.fromisoformat(chat["created"]).date()).days
    if days_old == 0:
        group = "Today"
    elif days_old == 1:
        group = "Yesterday"
    else:
        group = "Earlier"

    if group != last_group:
        st.sidebar.markdown('<div class="group-label">' + group + "</div>", unsafe_allow_html=True)
        last_group = group

    col1, col2 = st.sidebar.columns([6, 1])
    label = ("● " if cid == st.session_state.current else "") + chat["title"]
    if col1.button(label, key="open_" + cid):
        st.session_state.current = cid
        rerun()
    if col2.button("✕", key="del_" + cid):
        del chats[cid]
        with open(HISTORY_FILE, "w") as f:
            json.dump(chats, f, indent=2)
        if st.session_state.current == cid:
            st.session_state.current = None
        rerun()
    shown += 1

if shown == 0:
    st.sidebar.caption("No incidents found.")

st.sidebar.markdown('<div class="group-label">Actions</div>', unsafe_allow_html=True)

if st.session_state.current in chats:
    current_chat = chats[st.session_state.current]
    transcript = "\n\n".join(
        "[" + m.get("time", "") + "] " + m["role"].upper() + ": " + m["content"]
        for m in current_chat["messages"]
    )
    st.sidebar.download_button(
        "Export this incident",
        data=transcript,
        file_name="incident_" + datetime.now().strftime("%Y%m%d_%H%M") + ".txt",
        mime="text/plain",
    )

if st.sidebar.button("Clear all history"):
    st.session_state.chats = {}
    st.session_state.current = None
    with open(HISTORY_FILE, "w") as f:
        json.dump({}, f)
    rerun()

st.sidebar.caption("Saved incidents: " + str(len(chats)))

# ---------- Header ----------
st.markdown(
    """
<div class="header">
    <h1>Incident Response Assistant</h1>
    <p>Describe a security incident to receive structured triage and response guidance.</p>
</div>
    """,
    unsafe_allow_html=True,
)

# ---------- Show current chat ----------
if st.session_state.current in chats:
    messages = chats[st.session_state.current]["messages"]
else:
    messages = []

if len(messages) == 0:
    st.markdown(
        """
<div class="welcome">
    <h3>Describe the incident</h3>
    <p>Include what you observed, which systems are affected, and when it started. For example:</p>
    <ul>
        <li>Suspicious login from an unknown IP on the finance server</li>
        <li>Ransomware note found on a shared drive</li>
        <li>Unusual outbound traffic from a production database</li>
    </ul>
</div>
        """,
        unsafe_allow_html=True,
    )

for message in messages:
    avatar = "👤" if message["role"] == "user" else LOGO
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("time"):
            st.caption(message["time"])

# ---------- Input ----------
prompt = st.chat_input("Describe the incident...")

if prompt:
    is_new = False
    if st.session_state.current not in chats:
        new_id = str(uuid.uuid4())
        title = prompt[:34] + ("..." if len(prompt) > 34 else "")
        chats[new_id] = {"title": title, "created": datetime.now().isoformat(), "messages": []}
        st.session_state.current = new_id
        is_new = True

    messages = chats[st.session_state.current]["messages"]
    stamp = datetime.now().strftime("%d %b %Y, %H:%M")

    messages.append({"role": "user", "content": prompt, "time": stamp})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        st.caption(stamp)

    # >>> Replace this line with your chatbot's response <
    # `messages` holds the full conversation so far if your bot needs it
    response = "You said: " + prompt

    reply_stamp = datetime.now().strftime("%d %b %Y, %H:%M")
    messages.append({"role": "assistant", "content": response, "time": reply_stamp})
    with st.chat_message("assistant", avatar=LOGO):
        st.markdown(response)
        st.caption(reply_stamp)

    with open(HISTORY_FILE, "w") as f:
        json.dump(chats, f, indent=2)

    if is_new:
        rerun()  # refresh the sidebar so the new chat shows up

st.markdown(
    '<div class="footnote">Verify all recommendations before acting on production systems.</div>',
    unsafe_allow_html=True,
)