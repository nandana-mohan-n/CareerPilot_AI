import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load our secret API key from the hidden .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini library
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🔑 API Key missing! Make sure you added GEMINI_API_KEY inside your .env file.")

# Set up beautiful web page configurations
st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="wide")

# ==========================================
# DATA LOADING LAYER (Pandas)
# ==========================================
@st.cache_data # Why? This keeps the app fast by caching the dataset in memory
def load_dataset():
    try:
        df = pd.read_csv("IT_Job_Roles_Skills.csv", encoding='latin1')
        return df
    except Exception as e:
        st.error(f"❌ Could not find 'IT_Job_Roles_Skills.csv' in this folder! Error: {e}")
        return None

df = load_dataset()

# ==========================================
# CORE ALGORITHM LAYER (Skill Matching)
# ==========================================
def analyze_profile(user_skills, target_job):
    job_row = df[df['Job Title'].str.lower() == target_job.lower()]
    if job_row.empty:
        return None
    
    required_skills_raw = job_row['Skills'].values[0]
    required_skills = [skill.strip().lower() for skill in required_skills_raw.split(',')]
    cleaned_user_skills = [skill.strip().lower() for skill in user_skills]
    
    matched_skills = list(set(required_skills) & set(cleaned_user_skills))
    missing_skills = list(set(required_skills) - set(cleaned_user_skills))
    match_percentage = (len(matched_skills) / len(required_skills)) * 100
    suggested_certs = job_row['Certifications'].values[0]
    
    return {
        "Match Percentage": round(match_percentage, 2),
        "Skills You Have": matched_skills,
        "Skills You Need": missing_skills,
        "Certifications": suggested_certs
    }

# ==========================================
# THE WAITRE/FRONTEND WEB DASHBOARD (Streamlit)
# ==========================================
st.title("🚀 CareerPilot AI")
st.subheader("An Agentic Career Counseling & Mock Interview Companion")
st.markdown("---")

if df is not None:
    # 🌟 Create 3 tabs for clean organization (Recruiters will love this scannability!)
    tab1, tab2, tab3 = st.tabs(["📊 Profile Analyzer", "🗺️ Smart Roadmap", "🤖 Live Mock Interview"])
    
    # ----------------------------------------
    # TAB 1: PROFILE ANALYZER
    # ----------------------------------------
    with tab1:
        st.header("Check Your Industry Alignment")
        
        # User input fields
        available_roles = sorted(df['Job Title'].unique())
        selected_job = st.selectbox("🎯 Select Your Dream Target Role:", available_roles)
        
        user_skills_input = st.text_input("✍️ Enter Your Current Skills (comma separated):", "Python, SQL, Git")
        
        if st.button("Calculate Skill Gap 📊", key="analyze_btn"):
            skills_list = [s.strip() for s in user_skills_input.split(",") if s.strip()]
            
            with st.spinner("Analyzing dataset..."):
                results = analyze_profile(skills_list, selected_job)
                
                if results:
                    # Show Match percentage in a beautiful metric card
                    st.metric(label="Overall Job Market Match Rating", value=f"{results['Match Percentage']}%")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"🟢 Skills You Have ({len(results['Skills You Have'])}):")
                        st.write(", ".join([s.title() for s in results['Skills You Have']]) if results['Skills You Have'] else "None yet")
                    with col2:
                        st.error(f"🔴 Missing Skills You Need ({len(results['Skills You Need'])}):")
                        st.write(", ".join([s.title() for s in results['Skills You Need']]) if results['Skills You Need'] else "Wow! 100% Match!")
                        
                    st.warning(f"🎓 Recommended Industry Certifications:\n\n{results['Certifications']}")
                    
                    # Store results in Streamlit session memory for Tab 2 and Tab 3 to read later!
                    st.session_state['analysis'] = results

    # ----------------------------------------
    # TAB 2: SMART ROADMAP (AI Generation Layer)
    # ----------------------------------------
    with tab2:
        st.header("Customized Structural Learning Path")
        if 'analysis' not in st.session_state:
            st.info("⚠️ Please analyze your profile in Tab 1 first to generate a customized roadmap.")
        else:
            analysis = st.session_state['analysis']
            if st.button("Generate Week-by-Week Roadmap 🗺️"):
                with st.spinner("Our AI Career Coach is designing your learning path..."):
                    try:
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        prompt = f"""
                        Act as an elite tech mentor. Generate a detailed, week-by-week chronological learning roadmap for a student aiming for a '{selected_job}' role. 
                        They need to learn these specific missing skills: {analysis['Skills You Need']}.
                        Structure it using clear headers for each week and add 2 project concepts they can build to practice. Use markdown formatting.
                        """
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                    except Exception as e:
                        if "429" in str(e) or "Quota" in str(e):
                            st.warning("⏳ **Google Server Speed Bump!** We are on the free tier (5 requests/min). Please wait 10-15 seconds and try clicking the button again!")
                        else:
                            st.error(f"An unexpected error occurred: {e}")

    # ----------------------------------------
    # TAB 3: LIVE MOCK INTERVIEW (Agentic Chat UI Upgrade)
    # ----------------------------------------
    with tab3:
        st.header("🤖 1-on-1 Dynamic Interview Trainer")
        
        # Guard rail: Make sure they analyzed their profile in Tab 1 first!
        if 'analysis' not in st.session_state:
            st.info("⚠️ Please analyze your profile in Tab 1 first so the interviewer knows your target role and skill gaps!")
        else:
            analysis = st.session_state['analysis']
            missing_skills_str = ", ".join(analysis['Skills You Need']) if analysis['Skills You Need'] else "None (Core requirements met)"
            
            # 1. Initialize the Chat Message History Storage
            if 'interview_messages' not in st.session_state:
                st.session_state['interview_messages'] = []
                
            # 2. Initialize the Persistent Gemini Chat Session
            if 'gemini_chat' not in st.session_state:
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # System Instructions establish the AI's identity, constraints, and target difficulty level
                    system_prompt = f"""
                    You are an elite, empathetic technical interviewer assessing a final-year BTech engineering student.
                    The student is targeting the role of a '{selected_job}'.
                    
                    CRITICAL INSTRUCTION:
                    Your goal is to test them on their missing skills: [{missing_skills_str}]. 
                    Keep the question difficulty strictly at an 'Easy to Medium' level appropriate for a graduating college student.
                    
                    RULES:
                    1. Ask exactly ONE technical question at a time.
                    2. When the student provides an answer, briefly grade it (give technical correctness feedback out of 10), provide 1-2 quick bullet points on how to phrase it better, and then seamlessly ask the next question.
                    3. Do not write lengthy paragraphs. Keep your responses short, scannable, and engaging.
                    """
                    
                    # We start a conversational thread session with our system persona rules
                    st.session_state['gemini_chat'] = model.start_chat(history=[])
                    
                    # Trigger the first greeting question from the interviewer agent
                    with st.spinner("Initializing interviewer agent..."):
                        initial_trigger = f"Introduce yourself briefly with a welcoming emoji and ask the very first easy technical question regarding the missing skills: {missing_skills_str}."
                        response = st.session_state['gemini_chat'].send_message(initial_trigger)
                        
                        # Save this first question to our visual UI log
                        st.session_state['interview_messages'].append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Failed to start the AI session: {e}")

            # 3. Redraw the entire WhatsApp-style chat history layout on every single rerun
            for msg in st.session_state['interview_messages']:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # 4. Handle New User Input Replies
            if user_reply := st.chat_input("Type your technical answer here..."):
                
                # Immediately show and save what you typed
                with st.chat_message("user"):
                    st.markdown(user_reply)
                st.session_state['interview_messages'].append({"role": "user", "content": user_reply})
                
                # Send your answer to the running Gemini session and await the evaluation + next question
                with st.chat_message("assistant"):
                    with st.spinner("Interviewer is evaluating..."):
                        try:
                            ai_response = st.session_state['gemini_chat'].send_message(user_reply)
                            st.markdown(ai_response.text)
                            
                            # Save the interviewer's critique and next question to memory logs
                            st.session_state['interview_messages'].append({"role": "assistant", "content": ai_response.text})
                        except Exception as e:
                            if "429" in str(e) or "Quota" in str(e):
                                st.warning("⏳ **Google Rate Limit Hit!** Please wait 10 seconds and try sending your message again.")
                            else:
                                st.error(f"Error communicating with AI: {e}")

            