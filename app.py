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
    # TAB 3: LIVE MOCK INTERVIEW (Idea B Flow!)
    # ----------------------------------------
    with tab3:
        st.header("1-on-1 Dynamic Interview Trainer")
        
        if 'current_question' not in st.session_state:
            st.session_state['current_question'] = None
            
        if st.button("Generate Dynamic Interview Question 🎲"):
            with st.spinner("Fetching question from server..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"Generate exactly one core technical interview question for a role as a '{selected_job}'. Do not provide any introduction, greetings, or multiple choices."
                    st.session_state['current_question'] = model.generate_content(prompt).text
                except Exception as e:
                    if "429" in str(e) or "Quota" in str(e):
                        st.warning("⏳ **Google Server Speed Bump!** Please wait 10-15 seconds for the free tier quota to reset, then click generate again!")
                    else:
                        st.error(f"An unexpected error occurred: {e}")
                
        if st.session_state['current_question']:
            st.info(f"🤖 **Interviewer:** {st.session_state['current_question']}")
            
            student_ans = st.text_area("✍️ Type your answer here:", height=100)
            
            if st.button("Submit Answer for Evaluation 📋"):
                if not student_ans.strip():
                    st.warning("Please type something before submitting!")
                else:
                    with st.spinner("AI is grading your technical accuracy..."):
                        try:
                            model = genai.GenerativeModel('gemini-2.5-flash')
                            eval_prompt = f"""
                            You are an expert interviewer. Grade this answer out of 10.
                            Question: {st.session_state['current_question']}
                            Candidate Answer: {student_ans}
                            Provide an objective score, technical correctness breakdown, and exactly two bullets points on how to phrase it better.
                            """
                            eval_res = model.generate_content(eval_prompt)
                            st.markdown(eval_res.text)
                        except Exception as e:
                            if "429" in str(e) or "Quota" in str(e):
                                st.warning("⏳ **Google Server Speed Bump!** The AI is processing data, but we hit the free-tier limit. Wait 15 seconds and hit submit again to get your scorecard!")
                            else:
                                st.error(f"An unexpected error occurred: {e}")

            