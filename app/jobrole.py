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
    temperature=0.7 # Slight creativity for "generating own role"
)

# Define Prompt
prompt = ChatPromptTemplate.from_template(
    """
    You are an expert HR strategist.
    
    Input Query: {query}
    
    Task:
    Analyze the query. 
    1. If the user provides a specific role, generate details for it.
    2. If the user provides a vague description, infer the best professional title.
    3. If the query is empty or asks for a suggestion, GENERATE a high-demand, modern tech role of your choice (e.g. AI Ethicist, MLOps Engineer, Cloud Architect).

    Return the result strictly in the following JSON format:
    {format_instructions}
    """
).partial(format_instructions=parser.get_format_instructions())

# Create Chain
chain = prompt | llm | parser

if __name__ == "__main__":
    print("--- AI Job Role Generator ---")
    
    # 1. Check Command Line Arguments
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        # 2. Interactive Input
        try:
            print("Enter a Job Title, Description, or press Enter for a random AI-generated role:")
            user_query = input("> ").strip()
        except EOFError:
            user_query = ""

    # 3. Default for automation/lazy usage
    if not user_query:
        print("\n(No input detected. Asking AI to generate a trending role...)")
        user_query = "Generate a trending, high-salary technology job role"

    try:
        print(f"\nProcessing: '{user_query}'...")
        result = chain.invoke({"query": user_query})
        
        print("\n" + "="*40)
        print(f"ROLE: {result.role.upper()}")
        print("="*40)
        print(f"Level: {result.experience_level}")
        print("\n[ Skills ]")
        for skill in result.skills:
            print(f" - {skill}")
        print("\n[ Responsibilities ]")
        for resp in result.responsibilities:
            print(f" - {resp}")
        print("\n" + "="*40)
        
    except Exception as e:
        print(f"Error: {e}")
