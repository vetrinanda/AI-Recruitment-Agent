# 🤖 AI Recruitment Agent V2.0

![AI Recruitment Agent](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Backend-FastAPI-blue) ![React](https://img.shields.io/badge/Frontend-React%20%7C%20Shadcn-violet) ![AI](https://img.shields.io/badge/AI-Google%20Gemini%202.5-orange)

An intelligent, full-stack automated recruitment screening system. The **AI Recruitment Agent** helps HR teams dynamically generate job profiles and instantly screen candidate resumes against them using advanced LLM reasoning.

## ✨ Key Features

*   **🧠 Dynamic Job Role Generation**: 
    *   Uses **Google Gemini 2.5 Flash** to instantly create detailed job descriptions (Roles, Skills, Responsibilities, Qualifications) based on trending tech demands or specific user queries.
    *   Supports "Surprise Me" mode for random high-demand role generation.
*   **📄 Intelligent Resume Screening**:
    *   Accepts PDF resume uploads.
    *   Performs deep semantic analysis to compare candidate profiles against the generated job requirements.
*   **🎯 Smart Verdict System**:
    *   **Experience Matching**: Classifies candidates as Entry, Mid, or Senior level.
    *   **Skill Alignment**: detailed breakdown of matched vs. missing skills.
    *   **Final Decision**: binary "Interview Scheduled" or "Escalate/Reject" recommendation with reasoning.
*   **🎨 Premium UI/UX**:
    *   Professional **Dark Mode** interface.
    *   Built with **React**, **Vite**, **Tailwind CSS**, and **Shadcn UI**.
    *   Features glassmorphism, smooth animations, and skeleton loading states.

---

## 🛠️ Tech Stack

### Backend 🐍
*   **Framework**: FastAPI
*   **AI/LLM**: LangChain + Google Gemini (gemini-2.5-flash)
*   **Data Validation**: Pydantic
*   **Orchestration**: LangGraph (Stateful Agent Workflow)

### Frontend ⚛️
*   **Framework**: React 19 (Vite)
*   **Styling**: Tailwind CSS v4
*   **Components**: Shadcn UI (Radix Primitives)
*   **Icons**: Lucide React
*   **Font**: Public Sans

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AI-recruitment-agent.git
cd AI-recruitment
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file in the root directory and add:
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Frontend Setup
```bash
cd web-app

# Install dependencies
npm install

# Start Development Server
npm run dev
```

### 4. Running the Application
1.  **Start Backend**: 
    ```bash
    # From root directory
    uvicorn app.main:app --reload --port 8000
    ```
2.  **Start Frontend**:
    ```bash
    # From web-app directory
    npm run dev
    ```
3.  Open `http://localhost:5173` in your browser.

---

## 📖 Usage Workflow

1.  **Generate Role**: Click "Generate New Role" on the dashboard. The AI will create a comprehensive job profile (e.g., "Senior DevOps Engineer") with specific requirements.
2.  **Upload Resume**: Drag & Drop a candidate's PDF resume into the "Candidate Portal".
3.  **Analyze**: Click "Start Alignment Analysis".
4.  **View Results**: The AI will process the resume for ~60 seconds (simulated deep thinking) and present a structured verdict:
    *   **Verdict**: Recommended / Not Selected
    *   **Experience Level**: Assessed level of candidate.
    *   **Skill Match**: Alignment score.
    *   **Reasoning**: Detailed AI explanation for the decision.

---

## 📂 Project Structure

```
AI-Recruitment/
├── app/
│   ├── agent.py         # Core LangGraph agent logic (Screening/Matching)
│   ├── jobrole.py       # Job Role Generator (LLM Chain)
│   ├── main.py          # FastAPI Endpoints
│   └── rag.py           # RAG utilities (PDF loading, Vector Store)
├── web-app/             # React Frontend
│   ├── src/
│   │   ├── components/  # Shadcn UI Components
│   │   └── App.tsx      # Main UI Logic
│   └── package.json
├── requirements.txt     # Python Dependencies
└── README.md            # Documentation
```

## 🔮 Future Roadmap
*   **Chat with Candidate**: Add RAG-based chat to ask specific questions about the resume.
*   **Bulk Upload**: Screen multiple resumes simultaneously.
*   **Email Integration**: Auto-send rejection or interview invite emails.

---
