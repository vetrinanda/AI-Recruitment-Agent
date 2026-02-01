import os
from dotenv import load_dotenv
from typing import TypedDict, Optional, List
from enum import Enum
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables
load_dotenv()

# --- Configurations ---
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.5-flash"  # Updated to stable version

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    google_api_key=API_KEY, 
    model=MODEL_NAME, 
    temperature=0.0
)

# --- Data Structures & State ---

class ExperienceLevel(str, Enum):
    ENTRY = "Entry-level"
    MID = "Mid-level"
    SENIOR = "Senior-level"

class SkillMatchStatus(str, Enum):
    MATCH = "Match"
    MISMATCH = "Mismatch"

# Pydantic models for structured output
class ExperienceAssessment(BaseModel):
    level: ExperienceLevel = Field(..., description="The assessed experience level of the candidate")
    reasoning: str = Field(..., description="Brief reasoning for the classification")

class SkillAssessment(BaseModel):
    status: SkillMatchStatus = Field(..., description="Whether the candidate matches the required skills")
    missing_skills: List[str] = Field(default_factory=list, description="List of missing critical skills, if any")

class State(TypedDict):
    application_text: str
    file_path: Optional[str]
    job_role: str
    experience_level: str
    skill_match: str
    final_decision: str

# --- Nodes ---

def load_application(state: State) -> State:
    """Loads application content from file if path provided, else uses raw text."""
    file_path = state.get("file_path")
    content = state.get("application_text", "")

    if file_path and os.path.exists(file_path):
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            # Combine all page content
            content = "\n".join([doc.page_content for doc in docs])
            print(f"Loaded {len(docs)} pages from {file_path}")
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            # Fallback to empty or existing content
    
    return {"application_text": content}

def categorize_application(state: State) -> State:
    structured_llm = llm.with_structured_output(ExperienceAssessment)
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert HR specialist.
        Categorize the following job application for the role of '{job_role}' into one of three experience levels: Entry-level, Mid-level, Senior-level.
        
        Job Application Content:
        {application}
        """
    )
    
    chain = prompt | structured_llm
    result: ExperienceAssessment = chain.invoke({
        "job_role": state["job_role"],
        "application": state["application_text"]
    })
    
    print(f"Experience Level: {result.level} ({result.reasoning})")
    return {"experience_level": result.level.value}

def skill_match_application(state: State) -> State:
    structured_llm = llm.with_structured_output(SkillAssessment)
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert HR specialist.
        Analyze the following application for the role of '{job_role}'.
        Determine if the candidate's skills match the requirements. 
        Look strictly for skills relevant to '{job_role}'.
        
        Job Application Content:
        {application}
        """
    )
    
    chain = prompt | structured_llm
    result: SkillAssessment = chain.invoke({
        "job_role": state["job_role"],
        "application": state["application_text"]
    })
    
    print(f"Skill Match: {result.status} (Missing: {result.missing_skills})")
    return {"skill_match": result.status.value}

def schedule_interview(state: State) -> State:
    print("Decision: Scheduling interview")
    return {"final_decision": "Interview Scheduled"}

def reject_application(state: State) -> State:
    print("Decision: Rejecting application")
    return {"final_decision": "Application Rejected"}

def escalate_to_recruiter(state: State) -> State:
    print("Decision: Escalating to recruiter (Senior but Mismatch/Complex)")
    return {"final_decision": "Escalated to Recruiter"}

# --- Routing ---

def route_app(state: State) -> str:
    skill = state["skill_match"]
    experience = state["experience_level"]
    
    if skill == SkillMatchStatus.MATCH.value:
        return "schedule_interview"
    elif experience == ExperienceLevel.SENIOR.value:
        return "escalate_to_recruiter"
    else:
        return "reject_application"

# --- Graph Construction ---

graph = StateGraph(State)

graph.add_node("load_application", load_application)
graph.add_node("categorize_application", categorize_application)
graph.add_node("skill_match_application", skill_match_application)
graph.add_node("schedule_interview", schedule_interview)
graph.add_node("reject_application", reject_application)
graph.add_node("escalate_to_recruiter", escalate_to_recruiter)

# Flow
graph.add_edge(START, "load_application")
graph.add_edge("load_application", "categorize_application")
graph.add_edge("categorize_application", "skill_match_application")

graph.add_conditional_edges(
    "skill_match_application",
    route_app,
    {
        "schedule_interview": "schedule_interview",
        "reject_application": "reject_application",
        "escalate_to_recruiter": "escalate_to_recruiter",
    }
)

graph.add_edge("schedule_interview", END)
graph.add_edge("reject_application", END)
graph.add_edge("escalate_to_recruiter", END)

app = graph.compile()

# --- Public Interface ---

def process_application(application_text: str = "", file_path: str = None, job_role: str = "Python Developer") -> dict:
    """
    Process an application (text or file) for a specific job role.
    """
    inputs = {
        "application_text": application_text,  # Fixed key here
        "file_path": file_path,
        "job_role": job_role
    }
    
    results = app.invoke(inputs)
    
    return {
        "experience_level": results.get("experience_level"),
        "skill_match": results.get("skill_match"),
        "final_decision": results.get("final_decision")
    }