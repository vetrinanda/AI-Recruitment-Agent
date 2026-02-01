import shutil
import tempfile
import os
from fastapi import FastAPI, UploadFile, File, Form
from app.agent import process_application

app = FastAPI()

@app.post("/process-application")
async def process_application_endpoint(
    file: UploadFile = File(...),
    job_role: str = Form(...)
):
    # 1. Create a safe temporary directory
    temp_dir = tempfile.mkdtemp()
    # 2. Construct a file path (keeping extension is often helpful for loaders)
    file_name = file.filename or "resume.pdf"
    temp_path = os.path.join(temp_dir, file_name)
    
    try:
        # 3. Write uploaded bytes to disk
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"Processing file: {temp_path}")
        
        # 4. Pass the FILE PATH to the agent (let the agent handle loading)
        result = process_application(
            application_text="", 
            file_path=temp_path, 
            job_role=job_role
        )
        return result
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        # 5. Cleanup temp files
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