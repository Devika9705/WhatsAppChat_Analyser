# app.py

import streamlit as st
import preprocess
import helper
import selection
from layout import render_navbar

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Hide menu/footer and style app
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .fade-in {
        animation: fadeIn 0.6s ease-in-out;
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    html {
        scroll-behavior: smooth;
    }
    .navbar-container {
        position: fixed;
        top: 10px;
        left: 0;
        right: 0;
        width: 100%;
        z-index: 9999;
        background-color: #111;
        padding: 10px 20px;
        border-radius: 10px;
    }
    .stApp {
        padding-top: 100px !important;
    }
    .placeholder-section {
        background-color: #222;
        padding: 30px;
        border-radius: 10px;
        color: #ccc;
        text-align: center;
        margin-top: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Upload & Theme Toggle
st.sidebar.title("📂 Upload Chat File")
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat (.txt)", type=["txt"])

# Theme toggle
is_dark = st.sidebar.checkbox("🌙 Dark Mode", value=True)

if is_dark:
    st.markdown("""
        <style>
        body, .stApp { background-color: #111; color: white; }
        .stMarkdown, .stDataFrame, .stText, .stTable { color: white; }
        </style>
    """, unsafe_allow_html=True)

# Session states for button handling
if 'analysis_requested' not in st.session_state:
    st.session_state.analysis_requested = False

if 'analysis_ready' not in st.session_state:
    st.session_state.analysis_ready = False

# Handle uploaded file
if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analyze chat for:", user_list)

    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        if st.button("🔍 Show Analysis"):
            st.session_state.analysis_requested = True
            st.session_state.analysis_ready = True
    with col2:
        if st.button("❌ Clear Selection"):
            st.session_state.analysis_requested = False
            st.session_state.analysis_ready = False
            st.rerun()

# Analysis section after upload and button press
if uploaded_file and st.session_state.analysis_requested:
    # Show sticky navbar
    st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
    selected_section = render_navbar()
    st.markdown('</div>', unsafe_allow_html=True)

    # Debugging output
    st.write(f"🛠️ DEBUG: Selected section: {selected_section}")

    if not selected_section:
        st.markdown("""
            <div class="placeholder-section">
                <h3>👋 Welcome!</h3>
                <p>Please select an analysis section from the top navigation bar to begin exploring the chat.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        if st.session_state.analysis_ready:
            st.markdown('<div class="fade-in" id="analysis-section">', unsafe_allow_html=True)

            if selected_section == "🧠 Mood Analysis":
                selection.show_mood_analysis(df, selected_user)

            elif selected_section == "☁️ Word Cloud":
                selection.show_wordcloud(df, selected_user)

            elif selected_section == "📊 Content Stats":
                selection.show_stats(df, selected_user)

            elif selected_section == "😀 Emoji Analysis":
                selection.show_emoji_analysis(df, selected_user)

            elif selected_section == "🤖 AI Mood Advice":
                selection.show_ai_advice(df, selected_user)

            else:
                st.warning("❗ Unknown section selected.")

            st.markdown('</div>', unsafe_allow_html=True)

# Landing screen if no file is uploaded
elif not uploaded_file:
    st.markdown("""
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <div class="fade-in" style="text-align:center; padding: 100px 30px;">
            <h1 style="font-size: 50px; color: #ffc107;">📱 WhatsApp Chat Analyzer</h1>
            <p style="font-size: 20px; color: #aaa;">Upload your exported WhatsApp chat and explore stats, mood trends, emoji usage & AI-powered suggestions.</p>
            <p style="color: #999;">Use the left sidebar to upload your <code>.txt</code> file and choose what to analyze.</p>
            <lottie-player src="https://lottie.host/df9cbeed-7907-4a75-a92e-bb7b40cd0e84/c7cF5XNXYn.json"
                background="transparent" speed="1" style="max-width: 300px; margin-top: 20px;" loop autoplay>
            </lottie-player>
        </div>
    """, unsafe_allow_html=True)

# File uploaded but analysis not yet shown
elif uploaded_file and not st.session_state.analysis_ready:
    st.markdown("""
        <div class="placeholder-section">
            <h3>📊 Ready to Analyze</h3>
            <p>Please select a section and click <strong>Show Analysis</strong> to proceed.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="position: fixed; bottom: 0; width: 100%; text-align: center; color: gray;">
        <hr>
        <p>Developed by Devika Shukla</p>
    </div>
""", unsafe_allow_html=True)
