import shutil
import tempfile
import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.agent import process_application
from app.jobrole import generate_job_role

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Recruitment Agent is running!"}


@app.post("/generate-job-role")
def generate_job_role_endpoint():
    result = generate_job_role()
    if result:
        return result.model_dump()
    return {"error": "Failed to generate job role"}

@app.post("/process-application")
async def process_application_endpoint(
    file: UploadFile = File(...),
    job_role: Optional[str] = Form(None)
):
    # If no specific job role is provided, let's generate a random trending one to recruit for!
    if not job_role:
        print("No job role provided. Generating a random trending role...")
        generated_role = generate_job_role()
        if generated_role:
            job_role = generated_role.role
            print(f"Recruiting for Generated Role: {job_role}")
        else:
            job_role = "Software Engineer" # Fallback

    # 1. Create a safe temporary directory
    temp_dir = tempfile.mkdtemp()
    # 2. Construct a file path
    file_name = file.filename or "resume.pdf"
    temp_path = os.path.join(temp_dir, file_name)
    
    try:
        # 3. Write uploaded bytes to disk
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"Processing application for role: '{job_role}'")
        
        # 4. Pass path to agent
        result = process_application(
            application_text="", 
            file_path=temp_path, 
            job_role=job_role
        )
        # Add the job role to the output so the frontend knows what we screened for
        result["screened_for_role"] = job_role
        return result
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        # 5. Cleanup
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except:
                pass