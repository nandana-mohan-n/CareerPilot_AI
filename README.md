# 🚀 CareerPilot AI: Agentic Career Counseling & Mock Interview Companion

CareerPilot AI is an intelligent full-stack web application designed to help engineering students bridge the gap between academic skills and industry expectations. It analyzes student profiles using real job market data and leverages Generative AI to map personalized learning paths and host dynamic, interactive mock interviews.

## ✨ Core Features
- **📊 Profile Analyzer:** Leverages a Kaggle dataset of IT job roles to calculate a student's skills-alignment percentage and map exact technical gaps.
- **🗺️ Smart Roadmap:** Uses Google Gemini to dynamically generate custom, week-by-week chronological learning paths and practical project ideas based on identified skill gaps.
- **🤖 1-on-1 Interview Trainer:** Features an interactive interview simulator that serves technical questions one-at-a-time and provides real-time, analytical corporate scorecards with feedback.

## 🛠️ Tech Stack
- **Frontend/UI:** Streamlit
- **Data Engine:** Pandas
- **AI Orchestration:** Google GenAI SDK (Gemini 2.5 Flash)
- **Environment:** Python 3.12

## 🚀 Local Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/CareerPilot_AI.git
cd CareerPilot_AI
```

2. Install the required dependencies:
```bash
python -m pip install -r requirements.txt
```
3. Configure your environment variables:
Create a `.env` file in the root directory and add your Gemini API Key:
```text
GEMINI_API_KEY=your_free_gemini_api_key_here
```

4. Run the application:
```bash
python -m streamlit run app.py
```
