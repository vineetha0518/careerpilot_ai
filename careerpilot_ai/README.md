# 🚀 CareerPilot AI

An AI-powered career readiness platform built for national-level hackathons.
CareerPilot AI bridges the gap between academic learning and industry
expectations with personalized career recommendations, skill gap analysis,
learning roadmaps, resume analysis, AI mock interviews, internship
simulations, and a career readiness dashboard — all powered by Google
Gemini.

## ✨ Features

| # | Feature | Description |
|---|---------|--------------|
| 1 | 👤 Student Profile | Capture name, degree, skills, interests, and career goal |
| 2 | 🎯 Career Recommendation | AI-matched top 3 careers with match %, salary range, and outlook |
| 3 | 📊 Skill Gap Analysis | Current skills vs. target career, with priority & difficulty |
| 4 | 🗺 Learning Roadmap | Personalized 8-week plan with projects and resources |
| 5 | 📄 Resume Analyzer | Upload a PDF resume, get an ATS score + gauge chart + suggestions |
| 6 | 🎤 AI Mock Interview | Role-specific Q&A with AI scoring and feedback |
| 7 | 💼 Internship Simulation | Realistic take-home task with hiring-manager-style review |
| 8 | 🏠 Dashboard | Career Readiness Score composed from all of the above |
| 9 | ⚙ Settings | API key / database status and app info |

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **AI:** Google Gemini API (`gemini-2.5-flash`)
- **Database:** SQLite
- **Key libraries:** `streamlit`, `google-genai`, `python-dotenv`, `pandas`,
  `plotly`, `pdfplumber`, `pydantic`

## 📁 Project Structure

```
careerpilot_ai/
├── app.py                     # Entry point — sidebar nav + routing
├── ui_helpers.py              # Shared CSS + reusable UI components
├── pages/
│   ├── dashboard.py           # Feature 8: Career Readiness Dashboard
│   ├── career.py              # Feature 2: Career Recommendation
│   ├── skill_gap.py           # Feature 3: Skill Gap Analysis
│   ├── roadmap.py             # Feature 4: Learning Roadmap
│   ├── resume.py              # Feature 5: Resume Analyzer
│   ├── interview.py           # Feature 6: AI Mock Interview
│   ├── simulation.py          # Feature 7: Internship Simulation
│   ├── profile.py             # Feature 1: Student Profile
│   └── settings.py            # Feature 9: Settings
├── ai/
│   ├── gemini.py              # Gemini client wrapper (generate_json / generate_text)
│   └── prompts/
│       ├── career_prompt.py
│       ├── skill_gap_prompt.py
│       ├── roadmap_prompt.py
│       ├── resume_prompt.py
│       ├── interview_prompt.py
│       └── simulation_prompt.py
├── database/
│   └── database.py            # SQLite schema + all CRUD helpers
├── assets/
│   └── logo.png
├── .streamlit/
│   └── config.toml            # Blue/white theme + custom nav settings
├── .env.example
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone / unzip the project

```bash
cd careerpilot_ai
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Copy `.env.example` to `.env` and add your key:

```bash
cp .env.example .env
```

Get a free key at **https://aistudio.google.com/apikey**, then edit `.env`:

```
GEMINI_API_KEY=your_actual_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## 🧭 Usage Flow

1. Fill in your **Student Profile** first — every other feature personalizes
   itself using this data.
2. Generate **Career Recommendations** to see your top 3 AI-matched careers.
3. Run **Skill Gap Analysis** against your chosen target career.
4. Generate your **8-Week Learning Roadmap**.
5. Upload your resume in the **Resume Analyzer** for an ATS score.
6. Practice with the **AI Mock Interview**.
7. Try a realistic **Internship Simulation** task.
8. Check your overall **Career Readiness Score** on the Dashboard.

## 🗄 Database

CareerPilot AI uses a single SQLite file, `careerpilot.db`, created
automatically on first run in the project root. It stores the student
profile plus the history of every AI-generated artifact (career
recommendations, skill gap results, roadmaps, resume analyses, interview
sessions, and simulations), which is also what powers the Career Readiness
Score calculation.

## 🔒 Security Notes

- The Gemini API key is read only from environment variables via `.env`
  (never hardcoded).
- `.env` is excluded from version control — only commit `.env.example`.

## 🧩 Notes for Judges / Reviewers

- All AI prompts request structured JSON output (`response_mime_type:
  application/json`) for reliable, deterministic parsing — see `ai/prompts/`.
- The `pages/` directory is used as plain importable modules (each exposing
  a `render()` function) rather than Streamlit's native multipage
  auto-navigation, so the app can offer a fully custom, branded sidebar.
  `client.showSidebarNavigation = false` in `.streamlit/config.toml`
  disables the default navigation widget to prevent a duplicate menu.
