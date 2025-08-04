# layout.py

import streamlit as st

def render_navbar():
    st.markdown("""
        <style>
        .main {
            padding: 0rem 2rem;
        }
        .navbar-sticky {
            position: sticky;
            top: 0;
            z-index: 9999;
            background-color: #1E1E1E;
        }
        .nav-container {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 30px;
        }
        .stRadio > div {
            flex-direction: row;
            justify-content: center;
            background-color: #1E1E1E;
            padding: 10px;
            border-radius: 10px;
        }
        .stRadio > div > label {
            background-color: #2E2E2E;
            color: white;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .stRadio > div > label:hover {
            background-color: #555;
            transform: scale(1.05);
        }
        .stRadio > div > label[data-selected="true"] {
            background-color: #00BFFF;
            color: black;
            font-weight: bold;
        }

        /* Fade-in animation */
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
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='navbar-sticky nav-container'>", unsafe_allow_html=True)
        selected = st.radio(
            "Choose Analysis Section:",
            ["🧠 Mood Analysis", "☁️ Word Cloud", "📊 Content Stats", "😀 Emoji Analysis", "🤖 AI Mood Advice"],
            horizontal=True,
            label_visibility="collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    return selected