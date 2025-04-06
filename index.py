import streamlit as st

# Page config
st.set_page_config(page_title="Skill Gap Analyzer", page_icon="🧠", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
    # .stApp {
    #         background-color: #0D0D0D;
    #         color: #D9E1E8;
    #     }
    
    .big-title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
    }
    .subtitle {
        font-size: 1.2em;
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }
    .note {
        font-size: 0.9em;
        color: #666;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Landing Content ---
st.markdown('<div class="big-title">🚀 Welcome to Skill Gap Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Reimagine your career. Bridge the gap. Upskill for the future.</div>', unsafe_allow_html=True)

# API Key Input
api_key = st.text_input("🔑 Enter your Gemini AI API Key", type="password")
st.session_state["api_key"] = api_key

# Navigate Button
if st.button("✨ Launch Skill Analyzer"):
    if not api_key:
        st.warning("Please enter your Gemini AI API key to proceed.")
    else:
        st.success("API Key saved. Loading the Chat Bot...")
        st.session_state["api_key"] = api_key
        st.switch_page("pages/1_Skill_Gap_Analyzer.py") 

# Footer
st.markdown('<div class="note">Future domains. Real-time insights. AI-powered learning.</div>', unsafe_allow_html=True)
st.markdown('<div class="note">© 2023 Skill Gap Analyzer. All rights reserved.</div>', unsafe_allow_html=True)
st.markdown('<div class="note">Developed by Vini</div>', unsafe_allow_html=True)
st.markdown('<div class="note">Powered by Gemini AI</div>', unsafe_allow_html=True)
