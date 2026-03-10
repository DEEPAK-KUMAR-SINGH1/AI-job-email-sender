from langgraph.graph import StateGraph,START,END
from typing import TypedDict

from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pydantic import BaseModel

from database import save_application

# load API KEY
#load_dotenv()

# pdf Text Extractor
def extract_resume_text(pdf_path):
    loader = PyPDFLoader(pdf_path)
    text=loader.load()
    text_t="\n".join([text.page_content for text in text])
    return text_t

# Models
class details(BaseModel):
    name:str
    phone:str
    email:str
    github:str
    linkedin:str

class Resume(TypedDict):
    name:str
    phone:str
    email:str
    user_email:str
    app_password:str
    resume:str
    job_description:str
    email_body:str
    message:str
    github_link : str 
    linkedin_link : str
    pdf_path:str

# LLM's
llm = ChatMistralAI(api_key=os.getenv('MISTRAL_API_KEY'))
llm_with_s = llm.with_structured_output(details)

def extreact_details(state:Resume)->Resume:
    llm_with_s = llm.with_structured_output(details)
    response = llm_with_s.invoke(state["resume"])
    return{
        "name": response.name,
        "phone": response.phone,
        "github_link": response.github,
        "linkedin_link": response.linkedin
    }

def generate_email_body(state:Resume) -> str:
    
    prompt =f"""
You are a senior Technical Recruiter and expert business email writer.

Your task is to write a highly professional, structured, and personalized job application email body.

JOB DESCRIPTION:
{state['job_description']}

CANDIDATE RESUME:
{state['resume']}

Instructions:

1. Carefully analyze the job description and extract:
   - Core technical skills
   - Key responsibilities
   - Tools/technologies mentioned
   - Type of environment (startup, enterprise, production, etc.)

2. Match the candidate’s most relevant experience and skills directly to those requirements.
   - Do NOT repeat the entire resume.
   - Focus only on the strongest alignment.

3. Email Structure (STRICTLY FOLLOW):

   Paragraph 1:
   - Express interest in the role
   - Mention the company/domain
   - Brief 1-line positioning statement

   Paragraph 2:
   - Highlight 3–5 highly relevant skills/achievements
   - Show impact (performance, scalability, production systems, etc.)
   - Align directly with job requirements

   Paragraph 3:
   - Express enthusiasm for contributing
   - Mention collaboration, ownership, or production mindset
   - Invite further discussion

Rules:
- Start with: 👩‍💼Dear Hiring Manager,
- Do NOT include subject line
- Do NOT include sender/receiver emails
- Keep length between 170–220 words
- Professional, confident, not desperate
- No bullet points
- No placeholders
- End exactly with: Best Regards,

Return ONLY the email body.
"""

    response = llm.invoke(prompt)

    return {'email_body': response.content.strip()}

def send_email_node(state:Resume):
    
    sender_email = state.get('user_email')
    app_password = state.get('app_password')

    # Create message container
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = state["email"]
    msg["Subject"] = "Job Application"

        # Email Body
    body = f"""
{state["email_body"]}

🔗 Project Links:
Name : {state.get('name')}
Email : {state.get('user_email')}
Phone No: {state.get('phone')}
GitHub : {state.get('github_link')}
Linkedin : {state.get('linkedin_link')}

Thank you for your time and consideration.
"""
    msg.attach(MIMEText(body, "plain"))

    pdf_path = state['pdf_path']

    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(pdf_path)}",
        )

    msg.attach(part)

        # Send Email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()

    # DATABASE PART
    save_application({
        "user_email": state.get("user_email"),
        "email": state.get("email"),
        "name": state.get("name"),
        "phone": state.get("phone"),
        "github_link": state.get("github_link"),
        "linkedin_link": state.get("linkedin_link"),
        "job_description": state.get("job_description"),
        "email_body": state.get("email_body"),
        "status": "sent"
    })

    return {"message":"sent email"}

graph = StateGraph(Resume)

# Nodes
graph.add_node('Extreact_Details',extreact_details)
graph.add_node('Email_maker',generate_email_body)
graph.add_node('Send_mail',send_email_node)

# Egde
graph.add_edge(START,'Extreact_Details')
graph.add_edge('Extreact_Details','Email_maker')
graph.add_edge('Email_maker','Send_mail')
graph.add_edge('Send_mail',END)

app = graph.compile()