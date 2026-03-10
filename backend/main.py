from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from engine import app as graph_app, extract_resume_text

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def agent():
    return {"message": "Hello I am Email-agent"}

@app.post("/Email-agent/")
async def apply_job(
    job_description: str = Form(...),
    hr_email: str = Form(...),
    user_email: str = Form(...),
    app_password: str = Form(...),
    file: UploadFile = File(...)
):

    temp_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_resume_text(temp_path)

    result = graph_app.invoke({
        "email": hr_email,
        "user_email": user_email,
        "app_password": app_password,
        "resume": resume_text,
        "job_description": job_description,
        "pdf_path": temp_path
    })

    return {
        "status": "success",
        "result": result
    }