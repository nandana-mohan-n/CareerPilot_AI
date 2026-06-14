# 🚀 CareerPilot AI

[![Python Version](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Model Engine](https://img.shields.io/badge/AI-Gemini_2.5_Flash-007ACC?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

> **An Agentic Career Counseling & Adaptive Mock Interview Ecosystem**

CareerPilot AI is an intelligent full-stack career engineering web application designed to help engineering students bridge the gap between academic skills and industry expectations. It analyzes student profiles against real-world job market data matrices and leverages Generative AI to map personalized learning paths and host dynamic, stateful mock interview simulation chambers.

---

## ✨ Core Features

* **📊 Profile Matrix Analyzer:** Leverages an engineered dataset of IT job roles to calculate a student's technical alignment percentage and maps explicit core competency gaps via a sleek multi-select UI.
* **🗺️ Smart Curated Roadmap:** Uses Google Gemini to dynamically orchestrate custom, week-by-week chronological learning paths and practical project conceptual blueprints based on identified skill gaps.
* **🤖 1-on-1 Interview Simulator:** Features an interactive evaluation chamber that serves technical questions one-at-a-time, grades responses out of 10, and provides real-time, constructive phrasing enhancements.

---

## 🛠️ Tech Stack & Architecture

* **Frontend UI Engine:** Streamlit Framework wrapped in premium custom glassmorphism CSS overrides.
* **Data Science Layer:** Pandas Dataframe processing engine.
* **AI Orchestration:** Google GenAI SDK (`gemini-2.5-flash`) utilizing stateful conversational structures and custom system instructions.
* **Environment Configuration:** Python-Dotenv secret manager.

---

## 📊 Dataset Schema Overview

The background algorithm matches user inputs against a standardized `IT_Job_Roles_Skills.csv` workbook file structured as follows:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Job Title` | String (Key) | The targeted professional industry track (e.g., Data Engineer) |
| `Skills` | String (CSV) | Comma-separated list of core baseline technologies expected by the industry |
| `Certifications` | String | Highly rated industry credentials recommended to clear screening filters |

---

## 🚀 Local Installation & Setup

Follow these structured steps to deploy the workspace ecosystem on your local workstation:

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/CareerPilot_AI.git](https://github.com/YOUR_USERNAME/CareerPilot_AI.git)
cd CareerPilot_AI

2. Configure Dependencies
Ensure you have Python 3.12+ configured. Install the required ecosystem library dependencies:

Bash
python -m pip install streamlit pandas google-generativeai python-dotenv
3. Establish Secret Environmental Tokens
Create a hidden file named .env in the root directory structure and insert your generative AI credentials:

Plaintext
GEMINI_API_KEY=your_free_gemini_api_key_here
4. Run the Application
Execute the host interface compiler layer via your command terminal:

Bash
python -m streamlit run app.py
Developed as a Capstone Engineering Milestone Project.