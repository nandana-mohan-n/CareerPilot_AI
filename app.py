import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load secret API key from the hidden .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini library
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🔑 API Key missing! Make sure you added GEMINI_API_KEY inside your .env file.")

# Set up web page configurations
st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="wide")

# ==========================================
# 🎨 BRUTE-FORCE CRIMSON & OBSIDIAN OVERRIDE (CSS)
# ==========================================
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@400;600&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

    <style>
        /* 1. FORCE GLOBAL FONTS & BACKGROUNDS */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
            background-color: #040406 !important;
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* 2. PREMIUM CRIMSON HERO HEADER */
        .hero-banner {
            background: linear-gradient(135px, #08080C 0%, #220505 60%, #990000 100%) !important;
            padding: 18px 30px !important;
            border-radius: 12px !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
            margin-bottom: 25px !important;
            border: 1px solid #990000 !important;
        }
        
        .hero-banner h2 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
            margin: 0 !important;
            font-size: 1.8rem !important;
        }
        
        .hero-banner p {
            color: #FCA5A5 !important;
            margin: 0 !important;
            font-size: 0.9rem !important;
            font-family: 'JetBrains Mono', monospace !important;
        }
        
        /* 3. OBSIDIAN DASHBOARD CARDS */
        .dashboard-card {
            background-color: #09090D !important;
            padding: 25px !important;
            border-radius: 12px !important;
            border: 1px solid #1A1A24 !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6) !important;
            margin-bottom: 18px !important;
        }
        
        .section-title {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1.5rem !important;
            margin-bottom: 15px !important;
            margin-top: 0px !important;
        }
        
        /* 4. FORCE FONT SCALING ON ALL LABELS & TEXT */
        p, li, label, .stMarkdown, div {
            font-size: 1.02rem !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* 5. CRIMSON SCORE WIDGET */
        .score-widget {
            background-color: #060608 !important;
            padding: 22px !important;
            border-radius: 12px !important;
            text-align: center !important;
            border: 2px solid #EF4444 !important;
            box-shadow: 0 0 25px rgba(239, 68, 68, 0.2) !important;
            margin: 15px 0 !important;
        }
        
        /* 6. METTE JETBRAINS MONO TAGS */
        .skill-tag-have {
            display: inline-block !important;
            background-color: #1F2937 !important;
            color: #F9FAFB !important;
            padding: 8px 15px !important;
            border-radius: 6px !important;
            margin: 5px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            border: 1px solid #4B5563 !important;
            font-family: 'JetBrains Mono', monospace !important;
        }
        .skill-tag-need {
            display: inline-block !important;
            background-color: rgba(220, 38, 38, 0.15) !important;
            color: #FCA5A5 !important;
            padding: 8px 15px !important;
            border-radius: 6px !important;
            margin: 5px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            border: 1px solid rgba(220, 38, 38, 0.4) !important;
            font-family: 'JetBrains Mono', monospace !important;
        }
        
        .cert-tag {
            display: inline-block !important;
            background-color: rgba(245, 158, 11, 0.1) !important;
            color: #F59E0B !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            margin: 5px !important;
            font-weight: 700 !important;
            border: 1px solid rgba(245, 158, 11, 0.35) !important;
            font-family: 'Inter', sans-serif !important;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.05) !important;
        }

        /* 7. FORCE NAVIGATION TABS OVERRIDE */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px !important;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #09090D !important;
            border-radius: 6px 6px 0px 0px !important;
            padding: 12px 24px !important;
            color: #9CA3AF !important;
            font-weight: 700 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 1rem !important;
            border: 1px solid #1A1A24 !important;
            border-bottom: none !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #991B1B !important;
            color: #FFFFFF !important;
            border: 1px solid #EF4444 !important;
            border-bottom: none !important;
        }

        /* 8. HIGH-TECH GLOW ACTION BUTTONS & MULTISELECT ADJUSTMENTS */
        div.stButton > button {
            background: linear-gradient(90deg, #111116 0%, #220505 100%) !important;
            color: #F3F4F6 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
            text-transform: uppercase !important;
            border-radius: 8px !important;
            border: 1px solid #EF4444 !important;
            padding: 14px 28px !important;
            transition: all 0.3s ease-in-out !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
            width: 100% !important;
        }
        
        div.stButton > button:hover {
            background: linear-gradient(90deg, #991B1B 0%, #EF4444 100%) !important;
            color: #FFFFFF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 0 30px rgba(239, 68, 68, 0.6) !important;
        }

        /* Target the multiselect search wrapper background */
        div[data-baseweb="multiselect"] {
            background-color: #09111f !important;
            border: 1px solid rgba(0, 212, 255, .15) !important;
            border-radius: 12px !important;
        }
            
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING LAYER (Pandas)
# ==========================================
@st.cache_data
def load_dataset():
    try:
        df = pd.read_csv("IT_Job_Roles_Skills.csv", encoding='latin1')
        return df
    except Exception as e:
        st.error(f"❌ Could not find 'IT_Job_Roles_Skills.csv'! Error: {e}")
        return None

df = load_dataset()

# ==========================================
# DATA PARSING LAYER (Extracting Unique Skills)
# ==========================================
def get_all_unique_skills(dataframe):
    if dataframe is None:
        return []
    all_skills = set()
    # Read each row from the 'Skills' column, split by comma, clean and gather them
    for skills_raw in dataframe['Skills'].dropna():
        for skill in skills_raw.split(','):
            cleaned_skill = skill.strip()
            if cleaned_skill:
                all_skills.add(cleaned_skill)
    return sorted(list(all_skills))

unique_skills_list = get_all_unique_skills(df)

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
# EXECUTIVE LAYOUT STREAM
# ==========================================

# Minimalist Title Banner Element
st.markdown("""
    <div class="hero-banner">
        <h2>CAREERPILOT AI</h2>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    tab1, tab2, tab3 = st.tabs(["📊 PROFILE MATRIX ANALYZER", "🗺️ SMART CURATED ROADMAP", "🤖 LIVE INTERVIEW SIMULATOR"])
    
    # ----------------------------------------
    # TAB 1: PROFILE ANALYZER
    # ----------------------------------------
    with tab1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("<h3 class='section-title'>🎯 Profile Alignment Matrix</h3>", unsafe_allow_html=True)
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            # Dropdown with neutral default index entry
            available_roles = ["-- Select Target Profession --"] + sorted(list(df['Job Title'].unique()))
            selected_job = st.selectbox("Target Industry Profession:", available_roles, index=0)
        with col_in2:
            # MULTISELECT DROPDOWN INSTALLED: Starts clean and empty
            user_skills_input = st.multiselect(
                "Select Your Current Core Skillsets:",
                options=unique_skills_list,
                default=[],
                placeholder="Choose or search your skills..."
            )
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("RUN CORE MATRIX SELECTION ⚡", key="analyze_btn"):
            # Checking boundaries before triggering analytics stack
            if selected_job == "-- Select Target Profession --":
                st.warning("⚠️ Action Needed: Please choose your desired target role from the dropdown menu first.")
            elif not user_skills_input:
                st.warning("⚠️ Action Needed: Please select at least one core skill from the dropdown options.")
            else:
                # user_skills_input is already a clean list from st.multiselect
                with st.spinner("Processing local tracking metrics..."):
                    results = analyze_profile(user_skills_input, selected_job)
                    
                    if results:
                        st.session_state['analysis'] = results
                        
                        st.markdown(f"""
                            <div class="score-widget">
                                <div style="color: #9CA3AF; font-size: 0.9rem; font-weight: 700; letter-spacing: 2px; margin-bottom: 5px; font-family:'JetBrains Mono', monospace;">JOB COMPLIANCE RATING</div>
                                <div style="color: #EF4444; font-size: 3.2rem; font-weight: 800; line-height: 1; font-family:'Plus Jakarta Sans', sans-serif;">{results['Match Percentage']}%</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('<div class="dashboard-card" style="border-top: 3px solid #4B5563;">', unsafe_allow_html=True)
                            st.markdown("<h5 style='color: #FFFFFF; margin-top: 0; font-weight:700; font-family:\"Plus Jakarta Sans\"'>🟢 VALIDATED SKILLS</h5>", unsafe_allow_html=True)
                            if results['Skills You Have']:
                                for s in results['Skills You Have']:
                                    st.markdown(f'<span class="skill-tag-have">{s.upper()}</span>', unsafe_allow_html=True)
                            else:
                                st.write("No matching components identified.")
                            st.markdown('</div>', unsafe_allow_html=True)
                                
                        with col2:
                            st.markdown('<div class="dashboard-card" style="border-top: 3px solid #991B1B;">', unsafe_allow_html=True)
                            st.markdown("<h5 style='color: #F87171; margin-top: 0; font-weight:700; font-family:\"Plus Jakarta Sans\"'>🔴 DETECTED SKILL GAPS</h5>", unsafe_allow_html=True)
                            if results_need := results['Skills You Need']:
                                for s in results_need:
                                    st.markdown(f'<span class="skill-tag-need">{s.upper()}</span>', unsafe_allow_html=True)
                            else:
                                st.success("100% database parameters matched perfectly.")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Premium Fragmented Certification Dashboard Layout
                        st.markdown(f"""
                            <div class="dashboard-card" style="border-left: 4px solid #F59E0B; background: rgba(9, 15, 30, .75);">
                                <h5 style="color: #FFFFFF; margin-top: 0; font-weight: 700; font-family:'Orbitron'; letter-spacing:0.5px;">🎓 TARGET PROFESSIONAL CERTIFICATIONS</h5>
                                <div style="margin-top: 12px;">
                        """, unsafe_allow_html=True)
                        
                        if results['Certifications'] and pd.notna(results['Certifications']):
                            cert_list = [c.strip() for c in results['Certifications'].split(",") if c.strip()]
                            for cert in cert_list:
                                st.markdown(f'<span class="cert-tag">{cert.upper()}</span>', unsafe_allow_html=True)
                        else:
                            st.write("No foundational industry credentials tracked for this specific path framework.")
                            
                        st.markdown("""
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

    # ----------------------------------------
    # TAB 2: SMART ROADMAP
    # ----------------------------------------
    with tab2:
        if 'analysis' not in st.session_state:
            st.info("⚠️ Please process your profile alignment matrix in Tab 1 first.")
        else:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown("<h3 class='section-title'>🗺️ Chronological Learning Blueprint</h3>", unsafe_allow_html=True)
            analysis = st.session_state['analysis']
            
            if st.button("RUN AGENTIC ROADMAP ENGINE 🗺️", use_container_width=True):
                with st.spinner("AI Agent orchestrating weekly tracking roadmap..."):
                    try:
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        prompt = f"""
                        Act as an elite tech mentor. Generate a detailed, week-by-week chronological learning roadmap for a student aiming for a '{selected_job}' role. 
                        They need to learn these specific missing skills: {analysis['Skills You Need']}.
                        Structure it using clear headers for each week and add 2 project concepts they can build to practice. Use markdown formatting.
                        """
                        response = model.generate_content(prompt)
                        st.markdown(f"<div style='background-color: #050508; padding: 25px; border-radius: 10px; border: 1px solid #1A1A24; margin-top: 15px; line-height:1.6;'>{response.text}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error calling model: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------
    # TAB 3: LIVE MOCK INTERVIEW
    # ----------------------------------------
    with tab2 if 'analysis' not in st.session_state else tab3:
        if 'analysis' in st.session_state:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown("<h3 class='section-title'>🤖 Adaptive Evaluation Chamber</h3>", unsafe_allow_html=True)
            
            analysis = st.session_state['analysis']
            missing_skills_str = ", ".join(analysis['Skills You Need']) if analysis['Skills You Need'] else "Core criteria met"
            
            if 'interview_messages' not in st.session_state:
                st.session_state['interview_messages'] = []
                
            if 'gemini_chat' not in st.session_state:
                try:
                    # 1. Define the rigorous interview persona guidelines
                    system_prompt = f"""
                    You are an expert, elite technical interviewer assessing a final-year BTech engineering student.
                    The student has specified that they are targeting the exact role of a '{selected_job}'.
                    
                    CRITICAL OBJECTIVE:
                    You must immediately test them on their specific missing technical skill gaps: [{missing_skills_str}]. 
                    Keep the question difficulty strictly at an 'Easy to Medium' level appropriate for a graduating college student.
                    
                    STRICT LAWS OF ENGAGEMENT:
                    1. Introduce yourself briefly in ONE sentence with an interview emoji, acknowledge their target role, and ask exactly ONE relevant technical question to start.
                    2. When the candidate types a response, evaluate their technical correctness by giving an objective score out of 10.
                    3. Provide exactly two short, scannable bullet points detailing how they can phrase their answer better.
                    4. Immediately follow your feedback by asking the NEXT single technical question. Never break character.
                    """
                    
                    model = genai.GenerativeModel(
                        model_name='gemini-2.5-flash',
                        system_instruction=system_prompt
                    )
                    
                    # Open the continuous conversational stream channel
                    st.session_state['gemini_chat'] = model.start_chat(history=[])
                    
                    with st.spinner("Initializing system assessment logs..."):
                        initial_trigger = "Initiate the interview protocol now by greeting the user and presenting your first single technical question."
                        response = st.session_state['gemini_chat'].send_message(initial_trigger)
                        st.session_state['interview_messages'].append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Failed to initialize evaluation stack: {e}")

            # Draw Chat history
            for msg in st.session_state['interview_messages']:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            if user_reply := st.chat_input("Input technical response parameter context..."):
                with st.chat_message("user"):
                    st.markdown(user_reply)
                st.session_state['interview_messages'].append({"role": "user", "content": user_reply})
                
                with st.chat_message("assistant"):
                    with st.spinner("Evaluating response sequence parameters..."):
                        try:
                            ai_response = st.session_state['gemini_chat'].send_message(user_reply)
                            st.markdown(ai_response.text)
                            st.session_state['interview_messages'].append({"role": "assistant", "content": ai_response.text})
                        except Exception as e:
                            st.error(f"Communication sequence dropped: {e}")
            st.markdown('</div>', unsafe_allow_html=True)