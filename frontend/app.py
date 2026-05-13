import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(
    page_title="TailorTalk AI",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,60,200,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(30,180,140,0.12) 0%, transparent 55%),
        #0a0a0f !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0e0d17 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem !important;
}

/* ── Main content padding ── */
.block-container {
    padding: 2.5rem 2.5rem 2rem !important;
    max-width: 860px !important;
}

/* ── Header ── */
.tt-header {
    display: flex;
    align-items: flex-end;
    gap: 1rem;
    margin-bottom: 0.25rem;
}

.tt-logo-box {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #7c4dff 0%, #00c9a7 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(124,77,255,0.35);
}

.tt-title {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.75rem !important;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #d4c8ff 0%, #7c4dff 40%, #00c9a7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
}

.tt-caption {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2rem;
    padding-left: 56px;
}

/* ── Divider ── */
.tt-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,77,255,0.4), rgba(0,201,167,0.3), transparent);
    margin-bottom: 1.75rem;
}

/* ── Chat container ── */
.tt-chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
}

/* ── Message bubbles ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stChatMessage"][data-testid*="user"],
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
}

/* User messages */
[data-testid="chatAvatarIcon-user"] + div,
.stChatMessageContent:has(+ [data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #3d2a80 0%, #5a3ab8 100%) !important;
    border: 1px solid rgba(124,77,255,0.3) !important;
    border-radius: 16px 16px 4px 16px !important;
}

/* ── Message content styling ── */
.stChatMessage .stMarkdown p {
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Avatar circles */
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"] {
    border-radius: 8px !important;
    width: 32px !important;
    height: 32px !important;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #7c4dff, #00c9a7) !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: rgba(124,77,255,0.25) !important;
    border: 1px solid rgba(124,77,255,0.5) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border-radius: 14px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(124,77,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,77,255,0.12) !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] > div > div > textarea,
.stChatInput textarea {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.875rem !important;
    color: black !important;
    -webkit-text-fill-color: black !important;
    opacity: 1 !important;
    background: transparent !important;
    caret-color: #7c4dff !important;
}

[data-testid="stChatInput"] textarea::placeholder,
.stChatInput textarea::placeholder {
    color: rgba(255,255,255,0.35) !important;
    -webkit-text-fill-color: rgba(255,255,255,0.35) !important;
    opacity: 1 !important;
}

/* ── Empty state ── */
.tt-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
}

.tt-empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 20px rgba(124,77,255,0.5));
}

.tt-empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.tt-empty-sub {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.75);
    max-width: 320px;
    line-height: 1.7;
}

/* ── Quick prompt chips ── */
.tt-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin-top: 1.5rem;
}

.tt-chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 100px;
    padding: 0.35rem 0.9rem;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.45);
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: 'DM Mono', monospace;
    white-space: nowrap;
}

.tt-chip:hover {
    border-color: rgba(124,77,255,0.5);
    color: rgba(200,180,255,0.9);
    background: rgba(124,77,255,0.08);
}

/* ── Sidebar sections ── */
.sb-section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
}

.sb-section-label:first-child { margin-top: 0; }

.sb-about {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.78);
    line-height: 1.8;
}

.sb-query-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 0.6rem;
    border-radius: 8px;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.88);
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    margin-bottom: 0.2rem;
}

.sb-query-item:hover {
    background: rgba(124,77,255,0.1);
    color: rgba(200,180,255,0.85);
}

.sb-query-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c4dff, #00c9a7);
    flex-shrink: 0;
}

/* ── Status badge ── */
.sb-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: rgba(0,201,167,0.08);
    border: 1px solid rgba(0,201,167,0.2);
    border-radius: 8px;
    font-size: 0.72rem;
    color: rgba(0,201,167,0.8);
    margin-top: 1.25rem;
}

.sb-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #00c9a7;
    box-shadow: 0 0 6px rgba(0,201,167,0.7);
    flex-shrink: 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.sb-stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.35rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.sb-stat-label {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.3);
}

.sb-stat-value {
    font-size: 0.78rem;
    font-weight: 500;
    color: rgba(255,255,255,0.65);
    font-family: 'Syne', sans-serif;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] {
    color: #7c4dff !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,77,255,0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,77,255,0.5); }

/* ── Animations ── */

/* Page load fade-in */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* Shimmer sweep for divider */
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}

/* Floating bob for empty-state icon */
@keyframes float {
    0%, 100% { transform: translateY(0px);   }
    50%       { transform: translateY(-8px);  }
}

/* Orbit ring around logo */
@keyframes spin-slow {
    from { transform: rotate(0deg);   }
    to   { transform: rotate(360deg); }
}

/* Typing dots */
@keyframes blink {
    0%, 80%, 100% { opacity: 0.15; transform: scale(0.8); }
    40%            { opacity: 1;    transform: scale(1);   }
}

/* Slide-in from right for user messages, left for assistant */
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(24px); }
    to   { opacity: 1; transform: translateX(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-24px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* Chip entrance stagger */
@keyframes chipPop {
    from { opacity: 0; transform: scale(0.85) translateY(6px); }
    to   { opacity: 1; transform: scale(1)    translateY(0);   }
}

/* Glow pulse for logo box */
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(124,77,255,0.35); }
    50%       { box-shadow: 0 0 36px rgba(124,77,255,0.65), 0 0 60px rgba(0,201,167,0.2); }
}

/* Header entrance */
.tt-header { animation: fadeInUp 0.55s cubic-bezier(.22,1,.36,1) both; }
.tt-caption { animation: fadeInUp 0.55s 0.1s cubic-bezier(.22,1,.36,1) both; }

/* Animated shimmer divider */
.tt-divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(124,77,255,0.6) 30%,
        rgba(0,201,167,0.5) 55%,
        rgba(124,77,255,0.4) 70%,
        transparent 100%
    );
    background-size: 200% auto;
    animation: shimmer 3s linear infinite, fadeIn 0.6s 0.2s both;
    margin-bottom: 1.75rem;
}

/* Logo box glow pulse */
.tt-logo-box {
    animation: glowPulse 3s ease-in-out infinite;
}

/* Empty state icon float */
.tt-empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: inline-block;
    animation: float 3.5s ease-in-out infinite,
               fadeIn 0.5s both;
    filter: drop-shadow(0 0 20px rgba(124,77,255,0.5));
}

.tt-empty-title {
    animation: fadeInUp 0.5s 0.1s both;
}

.tt-empty-sub {
    animation: fadeInUp 0.5s 0.2s both;
}

/* Chip staggered pop-in */
.tt-chips { animation: fadeIn 0.4s 0.3s both; }
.tt-chip:nth-child(1) { animation: chipPop 0.4s 0.3s both; }
.tt-chip:nth-child(2) { animation: chipPop 0.4s 0.38s both; }
.tt-chip:nth-child(3) { animation: chipPop 0.4s 0.46s both; }
.tt-chip:nth-child(4) { animation: chipPop 0.4s 0.54s both; }
.tt-chip:nth-child(5) { animation: chipPop 0.4s 0.62s both; }

.tt-chip {
    transition: all 0.2s cubic-bezier(.34,1.56,.64,1) !important;
}

.tt-chip:hover {
    transform: translateY(-2px) scale(1.04);
    border-color: rgba(124,77,255,0.5);
    color: rgba(200,180,255,0.9);
    background: rgba(124,77,255,0.08);
    box-shadow: 0 4px 16px rgba(124,77,255,0.15);
}

/* Chat messages slide in */
[data-testid="stChatMessage"] {
    animation: slideInLeft 0.35s cubic-bezier(.22,1,.36,1) both;
}

/* Sidebar entrance */
[data-testid="stSidebar"] {
    animation: fadeIn 0.6s both;
}

.sb-status {
    animation: fadeInUp 0.5s 0.25s both;
    transition: box-shadow 0.3s ease;
}

.sb-status:hover {
    box-shadow: 0 0 12px rgba(0,201,167,0.15);
}

.sb-query-item {
    animation: fadeInUp 0.4s both;
    transition: background 0.2s, color 0.2s, transform 0.2s cubic-bezier(.34,1.56,.64,1) !important;
}

.sb-query-item:hover {
    background: rgba(124,77,255,0.1);
    color: white !important;
    -webkit-text-fill-color: white !important;
}

/* Stat rows fade in */
.sb-stat-row {
    animation: fadeInUp 0.4s both;
    transition: background 0.15s;
}

.sb-stat-row:hover {
    background: rgba(255,255,255,0.025);
    border-radius: 4px;
    padding-left: 4px;
}

/* Clear button hover lift */
button[kind="secondary"] {
    transition: transform 0.2s cubic-bezier(.34,1.56,.64,1), box-shadow 0.2s !important;
}

button[kind="secondary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.3) !important;
}

/* Spinner dots animation */
[data-testid="stSpinner"] > div {
    animation: fadeIn 0.3s both;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now().strftime("%H:%M")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.25rem;">
        <div style="width:32px;height:32px;background:linear-gradient(135deg,#7c4dff,#00c9a7);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;box-shadow:0 0 14px rgba(124,77,255,0.4);">🗂</div>
        <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;background:linear-gradient(90deg,#d4c8ff,#7c4dff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">TailorTalk</span>
    </div>
    <div style="font-size:0.65rem;color:rgba(255,255,255,0.25);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1.5rem;padding-left:42px;">AI · v2.0</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-status"><div class="sb-status-dot"></div>Google Drive connected</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label" style="margin-top:1.75rem;">Session</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sb-stat-row">
        <span class="sb-stat-label">Queries sent</span>
        <span class="sb-stat-value">{st.session_state.query_count}</span>
    </div>
    <div class="sb-stat-row">
        <span class="sb-stat-label">Session start</span>
        <span class="sb-stat-value">{st.session_state.session_start}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">About</div>', unsafe_allow_html=True)
    st.markdown('<p class="sb-about">Discover files in your Google Drive using plain language. No filters, no folders — just ask.</p>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">Example Queries</div>', unsafe_allow_html=True)
    queries = [
        ("📄", "Find PDF reports from last week"),
        ("🖼️", "Show me all images"),
        ("🧾", "Find invoices from vendors"),
        ("📊", "Any spreadsheets with budgets?"),
        ("🔗", "Find shared documents"),
        ("🗃️", "Locate QR code files"),
    ]
    for icon, label in queries:
        st.markdown(f"""
        <div class="sb-query-item">
            <span style="font-size:0.85rem;">{icon}</span>
            <span>{label}</span>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.messages:
        st.markdown('<div class="sb-section-label" style="margin-top:1.5rem;">Actions</div>', unsafe_allow_html=True)
        if st.button("Clear conversation", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.query_count = 0
            st.rerun()

# ── Main Area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tt-header">
    <div class="tt-logo-box">🗂️</div>
    <div class="tt-title">TailorTalk AI</div>
</div>
<div class="tt-caption">Conversational Google Drive File Discovery</div>
<div class="tt-divider"></div>
""", unsafe_allow_html=True)

# ── Chat History ──────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="tt-empty">
        <div class="tt-empty-icon">🗂️</div>
        <div class="tt-empty-title">What are you looking for?</div>
        <div class="tt-empty-sub">
            Ask anything about your Google Drive files using natural language.
            No technical syntax needed.
        </div>
        <div class="tt-chips">
            <span class="tt-chip">📄 PDF reports</span>
            <span class="tt-chip">🖼️ Images</span>
            <span class="tt-chip">🧾 Invoices</span>
            <span class="tt-chip">📊 Spreadsheets</span>
            <span class="tt-chip">🔗 Shared files</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
prompt = st.chat_input("Search your Drive — e.g. 'Find budget spreadsheets from March'")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.query_count += 1

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching Google Drive…"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": prompt},
                    timeout=30
                )
                data = response.json()
                result = data.get("result", "No results returned.")
            except requests.exceptions.ConnectionError:
                result = "⚠️ Could not reach the backend at `localhost:8000`. Make sure your FastAPI server is running."
            except Exception as e:
                result = f"⚠️ Unexpected error: {str(e)}"

        st.markdown(result)

    st.session_state.messages.append({"role": "assistant", "content": result})
    st.rerun()