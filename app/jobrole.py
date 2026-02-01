import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

class JobRole(BaseModel):
    role: str = Field(description="The professional job role title")
    experience_level: str = Field(description="The typical experience level (e.g. Mid-Level, Senior)")
    skills: List[str] = Field(description="List of essential technical and soft skills")
    responsibilities: List[str] = Field(description="List of key responsibilities")
    qualifications: List[str] = Field(description="List of educational and professional qualifications")

# Initialize Parser
parser = PydanticOutputParser(pydantic_object=JobRole)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.9 # High temperature for variety/randomness
)

# Define Prompt
prompt = ChatPromptTemplate.from_template(
    """
    You are an expert HR strategist.
    
    Input Query: {query}
    
    Task:
    Analyze the query. 
    1. If the user provides a specific role, generate details for it.
    2. If the query asks for a random or generated role, create a UNIQUE, high-demand tech role.
       Avoid generic "Software Engineer" roles unless asked. Try roles like "AI Prompt Engineer", "Blockchain Developer", "SRE", "Data Scientist", etc.

    Return the result strictly in the following JSON format:
    {format_instructions}
    """
).partial(format_instructions=parser.get_format_instructions())

# Create Chain
chain = prompt | llm | parser

def generate_job_role(query: str = None) -> JobRole:
    """
    Generates a job role based on a query. 
    If query is None, generates a random trending tech role.
    """
    if not query:
        query = "Generate a random, strictly professional, high-demand technology job role. Do not use 'Software Engineer' every time. Surprise me with roles like 'DevSecOps', 'Data Engineer', 'AI Ethicist', 'Cloud Architect', etc."
    
    try:
        print(f"🤖 AI is thinking about: '{query}'...")
        result = chain.invoke({"query": query})
        return result
    except Exception as e:
        print(f"Error generating role: {e}")
        return None

if __name__ == "__main__":
    print("--- AI Job Role Generator ---")
    
    # Check if user passed arguments or needs random generation
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        role_data = generate_job_role(user_query)
    else:
        # AUTOMATIC MODE: No input prompt, just generate!
        print("(No specific role requested. Auto-generating a random tech role...)")
        role_data = generate_job_role(None)

    if role_data:
        print("\n" + "="*40)
        print(f"🎯 ROLE: {role_data.role.upper()}")
        print("="*40)
        print(f"📊 Level: {role_data.experience_level}")
        print("\n🛠️  [ Skills ]")
        for skill in role_data.skills:
            print(f" - {skill}")
        print("\n📋 [ Responsibilities ]")
        for resp in role_data.responsibilities:
            print(f" - {resp}")
        print("\n🎓 [ Qualifications ]")
        for qual in role_data.qualifications:
            print(f" - {qual}")
        print("="*40)
