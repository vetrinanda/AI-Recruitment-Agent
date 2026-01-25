from email.mime import application
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict
import os
load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(api_key=api_key, model="gemini-2.5-flash")

class State(TypedDict):
    application: str
    experience_level: str
    skill_match:str
    response: str

graph = StateGraph(State)

def categorize_application(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        template="""
        You are an expert HR specialist. 
        Categorize the following job application into one of three experience levels: Entry-level, Mid-level, Senior-level.
        Job Application:
        {application}
        """,
    )

    chain = prompt | llm

    response = chain.invoke({"application": state["application"]})
    print("LLM Response:", response)
    return {'experience_level': response}

    # # Parse the response to extract experience level and skill match
    # lines = response.splitlines()
    # experience_level = lines[0].split(":")[1].strip()
    # skill_match = lines[1].split(":")[1].strip()

    # state["experience_level"] = experience_level
    # state["skill_match"] = skill_match
    # state["response"] = response
    # return state
    
    
def skill_match_application(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        template="""
        You are an expert HR specialist. 
        Analyze the following job application for a python developer, access the candidate's skillset
        Responed with either "Match" or "Mismatch".
        Job Application:
        {application}
        """,
    )

    chain = prompt | llm

    response = chain.invoke({"application": state["application"]})
    print("skill_match:", response)
    return {'skill_match': response}



def generate_response(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        template="""
        You are an expert HR specialist. 
        Based on the candidate's experience level: {experience_level} and skill match: {skill_match},
        generate a response to the candidate regarding their application status.
        """,
    )

    chain = prompt | llm

    response = chain.invoke({
        "experience_level": state["experience_level"],
        "skill_match": state["skill_match"]
    })
    print("Final Response:", response)
    return {'response': response}

def scheldue_interview(state: State) -> State:
    print("Scheduling interview for candidate")
    return {"response": "Interview Scheduled"}


def reject_application(state: State) -> State:
    print("Rejecting application")
    return {"response": "Application Rejected"}

def Escalate_to_recruiter(state: State) -> State:
    print("Escalating to recruiter")
    return {"response": "Application Escalated to Recruiter as Candidate is Senior-level but Skill Mismatch"}

def route_app(state: State) -> str:
    if "Match" in state["skill_match"]:
        return "scheldue_interview"
    elif "Senior-level" in state["experience_level"]:
        return "Escalate_to_recruiter"
    else:
        return "reject_application"




graph.add_node("categorize_application", categorize_application)
graph.add_node("skill_match_application", skill_match_application)
graph.add_node("scheldue_interview", scheldue_interview)
graph.add_node("reject_application", reject_application)
graph.add_node("Escalate_to_recruiter", Escalate_to_recruiter)

graph.add_edge(START, "categorize_application")
graph.add_edge("categorize_application", "skill_match_application")
graph.add_conditional_edges(
    "skill_match_application",
    route_app,
    {
        "scheldue_interview": "scheldue_interview",
        "reject_application": "reject_application",
        "Escalate_to_recruiter": "Escalate_to_recruiter",
    }
)
graph.add_edge("scheldue_interview", END)
graph.add_edge("reject_application", END)
graph.add_edge("Escalate_to_recruiter", END)


app= graph.compile()

def process_application(application_text: str) -> str:
    results=app.invoke({
        "application": application_text
    })
    return {
        "expereince_level": results["experience_level"],
        "skill_match": results["skill_match"],
        "response": results["response"]
    }

# application_text = "I have 10 years of experience in software development with expertise in JAVA."

# result = process_application(application_text)
# print("Final Result:", result)
# def main():
#     initial_state: State = {
#         "application": """Dear Hiring Manager 

# from IPython.display import Image, display

# with open("app_flowchart.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

# print("Graph saved as 'app_flowchart.png'")

# from IPython.display import Image, display

# display(Image(
#     app.get_graph().draw_mermaid_png()
# ))