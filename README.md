# 🚀 CareerPilot AI

[![Python Version](https://img.shields.io/badge/Python-3.12-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Model Engine](https://img.shields.io/badge/AI-Gemini_2.5_Flash-007ACC?logo=google\&logoColor=white)](https://deepmind.google/technologies/gemini/)

> **An Agentic Career Counseling & Adaptive Mock Interview Ecosystem**

CareerPilot AI is an intelligent full-stack career engineering web application designed to help engineering students bridge the gap between academic skills and industry expectations. It analyzes student profiles against real-world job market data and leverages Generative AI to create personalized learning paths and conduct adaptive mock interviews.

---

## ✨ Core Features

### 📊 Profile Matrix Analyzer

* Calculates skill alignment percentage for selected IT roles.
* Identifies competency gaps using a structured skill matrix.
* Interactive multi-select skill assessment interface.

### 🗺️ Smart Curated Roadmap

* Generates personalized week-by-week learning plans.
* Suggests certificates based on identified skill gaps.
* Powered by Gemini 2.5 Flash.

### 🤖 1-on-1 Interview Simulator

* Conducts dynamic technical interviews.
* Evaluates responses.
* Provides real-time feedback and improvement suggestions.

---

## 🛠️ Tech Stack & Architecture

* **Frontend:** Streamlit
* **Data Processing:** Pandas
* **AI Engine:** Gemini 2.5 Flash
* **Environment Management:** Python-Dotenv

---

## 📊 Dataset Schema Overview

The application uses an `IT_Job_Roles_Skills.csv` dataset.

| Column Name    | Data Type    | Description                                 |
| -------------- | ------------ | ------------------------------------------- |
| Job Title      | String       | Target IT role (e.g., Data Engineer)        |
| Skills         | String (CSV) | Core technical skills required for the role |
| Certifications | String       | Recommended industry certifications         |

---

## 🚀 Local Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CareerPilot_AI.git
cd CareerPilot_AI
```

### 2. Install Dependencies

```bash
python -m pip install streamlit pandas google-generativeai python-dotenv
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_free_gemini_api_key_here
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

---
