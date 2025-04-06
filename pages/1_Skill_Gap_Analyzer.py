import fitz  # PyMuPDF
import streamlit as st
import google.generativeai as genai
from urllib.parse import quote
from utils.skills_data import skill_map, domains
from streamlit_extras.switch_page_button import switch_page



# 🌐 Gemini API Config
import streamlit as st
import google.generativeai as genai

# 🔐 Check if API key exists
# Use API key from session
if "api_key" in st.session_state:
    genai.configure(api_key=st.session_state.api_key)
else:
    st.error("⚠️ API Key not found. Please return to the home page and enter it.")
    if st.button("🔙 Go to Home Page"):
        switch_page("index.py") 
    st.stop()

model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 🧠 Chatbot Logic
# 🔄 Initialize session
for key in ["stage", "selected_domain", "known_skills"]:
    if key not in st.session_state:
        st.session_state[key] = None
if st.session_state.stage is None:
    st.session_state.stage = "chat"

# 💄 Style
st.set_page_config(page_title="AI Skill Gap Analyszer", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background-color: #EDF9FF;
            color: #1F2937;
        }
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        .message {
            padding: 10px 15px;
            border-radius: 14px;
            margin: 5px 0;
            width: fit-content;
            font-size: 16px;
        }
        .user { background-color: #D1F5D3; align-self: flex-end; margin-left: auto; }
        .bot { background-color: #E0E7FF; align-self: flex-start; }
            
        .stButton>button {
            background-color: #6366F1;
            color: white;
            border-radius: 10px;
        }

        .stButton>button:hover {
            background-color: #4F46E5;
        }
            
        .stAlert {
            color: black !important; /* Change this to your desired font color */
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Skill Gap Analyzer Chatbot")
st.markdown("""
    <div style="text-align:center; padding: 20px; background-color:#F9FAFC;">
        <h2 style="color:#4F46E5;">🚀 Unlock Your Future with the AI Skill Gap Analyzer</h2>
        <h3 style="color:#1F2937;">Discover Where You Stand. Design Where You're Going.</h3>
        <p style="font-size:20px; color:#1F2937;">
            Step into the future of work — AI, Web3, Data Science, Machine Learning, Robotics, Cyber Security, and more.<br>
            Our intelligent assistant pinpoints exactly <strong>what skills you have</strong> and <strong>what’s missing</strong> for the careers of 2027.
        </p>
        <p style="font-size:17px; color:#4B5563;">
            📄 Upload your resume or ✍️ chat with our AI to:
        </p>
        <ul style="text-align:left; display:inline-block; font-size:16px; color:#374151;">
            <li>🔍 Analyze your current strengths</li>
            <li>📌 Reveal booming domains tailored to you</li>
            <li>🚧 Uncover critical skill gaps</li>
            <li>🗺️ Get a personalized roadmap with resources & projects</li>
        </ul>
        <p style="font-size:18px; color:#1F2937; margin-top: 10px;"><strong>💡 Don’t just learn. Learn what matters.</strong><br>Your future-proof journey begins now.</p>
    </div>
""", unsafe_allow_html=True)


with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # 🧠 Show Gemini chat history
    for msg in st.session_state.chat.history:
        role = "user" if msg.role == "user" else "bot"
        st.markdown(f'<div class="message {role}">{msg.parts[0].text}</div>', unsafe_allow_html=True)

    # 🧩 Custom Skill Gap Logic
    if st.session_state.stage == "chat":
        prompt = st.chat_input("Type a message...")
        if prompt:
            st.session_state.chat.send_message(prompt)
            st.rerun()

        # Button below chat
        # st.write("👇 Want to analyze your **Skill Gap**?")
        # if st.button("Start Skill Gap Analysis"):
        #     st.session_state.stage = "ask_domain"
        #     st.rerun()

        # Entry options below chat
        st.write("👇 Choose how you'd like to start your Skill Gap analysis:")

        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Start Skill Gap Analysis"):
                st.session_state.stage = "ask_domain"
                st.rerun()

        with col2:
            uploaded_file = None 
            if st.button("Upload Resume"):
                st.session_state.show_uploader = True  # 👈 control visibility
            
            if st.session_state.get("show_uploader", False):
                uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"], label_visibility="collapsed",key="resume_upload")
                
            
                if uploaded_file is not None:
                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    text = ""
                    for page in doc:
                        text += page.get_text()
                
                    st.session_state.resume_text = text
                    st.session_state.stage = "resume_analysis"
                    st.success("✅ Resume uploaded successfully!")
                    st.session_state.show_uploader = False
                    st.rerun()

    elif st.session_state.stage == "ask_domain":
        st.markdown("🎯 <strong>What domain are you into?</strong>", unsafe_allow_html=True)

        st.markdown("""
        <style>
            button[data-testid="baseButton-secondary"] {
            background-color: #6366F1;
            color: white;
            font-weight: 500;
            border-radius: 12px;
            padding: 0.5rem 1rem;
        }
            button[data-testid="baseButton-secondary"]:hover {
                background-color: #4F46E5;
            }
        </style>
            """, unsafe_allow_html=True)

    # Display buttons in rows of 3 or 4
        num_cols = 4
        for i in range(0, len(domains), num_cols):
            row_domains = domains[i:i + num_cols]
            cols = st.columns(len(row_domains))  # Only create the number of needed columns
            for col, domain in zip(cols, row_domains):
                if col.button(domain):
                    st.session_state.selected_domain = domain
                    st.session_state.stage = "skill_check"
                    st.rerun()


    elif st.session_state.stage == "skill_check":
        domain = st.session_state.selected_domain
        skills = skill_map[domain]

        st.write(f"🧪 Selected Domain: **{domain}**")
        st.markdown(f"🧠 <strong>Select the skills you already know in <u>{domain}</u> 👇</strong>", unsafe_allow_html=True)

        known_skills = st.multiselect(
        "Select your known skills",
        options=skills
        )

        if st.button("Analyze Gap"):
        # Save selected skills into session state
            st.session_state.known_skills = known_skills
            st.session_state.stage = "show_gap"
            st.rerun()


    elif st.session_state.stage == "show_gap":
        doamin = st.session_state.selected_domain
        known = set(st.session_state.known_skills)
        all_skills = set(skill_map[doamin])
        gap = list(all_skills - known)

        st.markdown("""
            <div style="background-color:#D1F5D3; padding:10px 15px; border-radius:10px; color:#065F46; font-weight:600;">
            ✅ Skills you know:
            </div>
            """, unsafe_allow_html=True)

        st.write(", ".join(known) if known else "None")

        
        st.markdown("""
            <div style="background-color:#E0E7FF; padding:10px 15px; border-radius:10px; color:#065F46; font-weight:600;">
            🚧 Skills you need to learn:
            </div>
            """, unsafe_allow_html=True)
        st.write(", ".join(gap) if gap else "You're all set!")

        if gap:
            with st.spinner("📚 Generating your personalized roadmap..."):
                query = f"Create a skill gap roadmap for {domains}. The user already knows {', '.join(known)} but lacks {', '.join(gap)}. Include timelines, learning paths, and project suggestions."
                gemini_response = model.generate_content(query)
                st.markdown("### 🗺️ Roadmap Recommendation:")
                st.markdown(gemini_response.text)

        if st.button("🔄 Restart"):
            for key in ["stage", "selected_domain", "known_skills", "chat"]:
                st.session_state[key] = None
            st.session_state.chat = model.start_chat(history=[])
            st.rerun()

    elif st.session_state.stage == "resume_analysis":
        st.subheader("📄 Resume Analysis by Gemini")
        
        resume_text = st.session_state.get("resume_text", "")
        if resume_text:
            st.text_area("📝 Extracted Text", resume_text, height=300)
        # You can now pass resume_text to Gemini/LLM here
        else:
            st.warning("No text found in the resume.")

        with st.spinner("🔍 Analyzing your resume..."):
            prompt = f"""
            You are a career coach. Analyze this resume content and give insights on:
            1. Top domains the person fits into
            2. Their strong skills
            3. Skills they should learn to stay competitive
            4. A short roadmap with resources and projects

            Resume:
            {st.session_state.resume_text}
            """
            resume_response = model.generate_content(prompt)

        st.markdown("### 📌 Gemini Recommendations:")
        st.markdown(resume_response.text)

        if st.button("🔄 Restart"):
            for key in ["stage", "selected_domain", "known_skills", "chat", "resume_text"]:
                st.session_state.pop(key, None)
            st.session_state.chat = model.start_chat(history=[])
            st.rerun()


    st.markdown("</div>", unsafe_allow_html=True)
