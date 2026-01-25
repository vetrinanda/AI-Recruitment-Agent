# AI Recruitment Application

## Overview

AI Recruitment is an intelligent automated recruitment system that leverages Large Language Models (LLMs) to streamline the candidate evaluation process. The application analyzes job applications, assesses candidate qualifications, matches skills requirements, and routes applicants through a decision workflow to determine appropriate next steps in the hiring process.

## Features

- **Automated Application Analysis**: Uses AI to categorize candidates by experience level (Entry-level, Mid-level, Senior-level)
- **Skill Matching**: Evaluates candidate skillsets against job requirements to identify technical alignment
- **Intelligent Routing**: Implements conditional routing logic to appropriately handle different candidate profiles
- **Decision Workflow**: Automatically schedules interviews for qualified candidates, escalates edge cases to recruiters, and rejects unsuitable applications
- **LangGraph Integration**: Utilizes LangGraph for building and visualizing complex workflow graphs
- **Google Generative AI**: Powered by Google's Gemini 2.5 Flash model for natural language understanding

## Architecture

The application employs a state machine workflow with the following nodes:

1. **categorize_application**: Extracts and categorizes candidate experience level
2. **skill_match_application**: Evaluates technical skill alignment for Python developer roles
3. **Routing Decision**: Conditional branching based on experience level and skill match results
4. **Output Nodes**:
   - `schedule_interview`: Schedules interviews for skilled candidates
   - `reject_application`: Rejects unqualified applications
   - `escalate_to_recruiter`: Escalates senior-level candidates with skill mismatches for manual review

## Prerequisites

- Python 3.9+
- Google API Key for Gemini model access
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI-recruitment
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root and add:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

Run the recruitment workflow:

```bash
python main.py
```

The application processes an application text and returns:
- `experience_level`: Categorized experience level
- `skill_match`: Whether candidate skills match job requirements
- `response`: Final decision (Interview Scheduled, Application Rejected, or Escalated to Recruiter)

### Example

```python
from app.main import process_application

application_text = "I have 10 years of experience in software development with expertise in Python."
result = process_application(application_text)
print(result)
```

## Project Structure

```
AI-recruitment/
├── main.py                 # Entry point
├── app/
│   └── main.py            # Core workflow and AI logic
├── requirements.txt       # Project dependencies
├── .env                   # Environment configuration (not in repo)
└── README.md             # This file
```

## Technologies Used

- **LangGraph**: Workflow orchestration and state management
- **LangChain**: LLM prompt templates and chain construction
- **Google Generative AI**: Gemini 2.5 Flash language model
- **Python**: Core application language

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please submit pull requests with clear descriptions of changes and improvements.
