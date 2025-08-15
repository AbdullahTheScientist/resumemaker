



# from fastapi import FastAPI, HTTPException
# from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request, BackgroundTasks, Depends
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List, Optional, Dict
# import os
# import uvicorn
# from generate_resume import generate_resume, generate_coverletter
# import logging
# from typing import Dict, Any, Callable
# import tempfile
# import time
# from collections import defaultdict
# import uuid

# # Import the enhanced models
# from pydantic import BaseModel, Field

# class PersonalInfo_2(BaseModel):
#     template_name : Optional[str] = Field(None, description="name of cover letter template")
#     page_size : Optional[str] = Field(None, description="page size for cover letter" )
#     name: str = Field(..., description="Full name")
#     title: Optional[str] = Field(None, description="Job title or profession")
#     phone: Optional[str] = Field(None, description="Phone number")
#     email: Optional[str] = Field(None, description="Email address")
#     location: Optional[str] = Field(None, description="Location/Address")
#     company_name: Optional[str] = Field(None, description="company name")
#     hiring_manager_name: Optional[str] = Field(None, description="Manager name")
#     paragraph : Optional[list[str]] = Field(None, description="Why are you best fit for this job")

# # Personal Information Model
# class PersonalInfo(BaseModel):
#     name: str = Field(..., description="Full name")
#     title: Optional[str] = Field(None, description="Job title or profession")
#     phone: Optional[str] = Field(None, description="Phone number")
#     email: Optional[str] = Field(None, description="Email address")
#     github: Optional[str] = Field(None, description="GitHub profile URL")
#     location: Optional[str] = Field(None, description="Location/Address")
#     linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
#     website: Optional[str] = Field(None, description="Personal website URL")

# class Custom_link(BaseModel):
#     name: Optional[str] = Field(None, description="Link name")
#     url: Optional[str] = Field(None, description='url')

# # Work Experience Model
# class WorkExperience(BaseModel):
#     company: str = Field(..., description="Company name")
#     position: str = Field(..., description="Job position/title")
#     start_date: str = Field(..., description="Start date")
#     end_date: Optional[str] = Field(None, description="End date (None if current)")
#     description: Optional[str] = Field(None, description="Job description bullet points")

# # Education Model
# class Education(BaseModel):
#     institution: str = Field(..., description="Educational institution")
#     degree: str = Field(..., description="Degree obtained")
#     start_date: Optional[str] = Field(None, description="Start date")
#     end_date: Optional[str] = Field(None, description="End date")

# # Academic Projects Model
# class AcademicProject(BaseModel):
#     title: str = Field(..., description="Project title")
#     date: str = Field(..., description="Project date")
#     technologies: Optional[str] = Field(None, description="Technologies used")
#     # description: Optional[List[str]] = Field(None, description="Project description")
#     description: Optional[str] = Field(None, description="Job description bullet points")
#     links: Optional[Dict[str, str]] = Field(None, description="Project links")

# # Certifications Model
# class Certification(BaseModel):
#     name: str = Field(..., description="Certification name")
#     issuer: str = Field(..., description="Issuing organization")
#     date: str = Field(..., description="Date obtained")
#     credential_id: Optional[str] = Field(None, description="Credential ID")
#     url: Optional[str] = Field(None, description="Certificate URL")
#     description: Optional[str] = Field(None, description="Job description bullet points")
#     # description: Optional[List[str]] = Field(None, description="Certification description")

# # Publications Model
# class Publication(BaseModel):
#     title: str = Field(..., description="Publication title")
#     authors: str = Field(..., description="Authors")
#     journal: str = Field(..., description="Journal or publication venue")
#     date: str = Field(..., description="Publication date")
#     url: Optional[str] = Field(None, description="Publication URL")
#     # description: Optional[List[str]] = Field(None, description="Publication description")
#     description: Optional[str] = Field(None, description="Job description bullet points")

# # Referees Model
# class Referee(BaseModel):
#     name: str = Field(..., description="Reference name")
#     position: str = Field(..., description="Reference position")
#     organization: Optional[str] = Field(None, description="Organization")
#     email: Optional[str] = Field(None, description="Email address")
#     phone: Optional[str] = Field(None, description="Phone number")
#     relationship: Optional[str] = Field(None, description="Relationship to applicant")

# # Custom Text
# # class CustomText(BaseModel):
# #     title: str = Field(..., description="Title of custom section")
# #     description: Optional[str] = Field(None, description="Description of Custom section")

# class Link(BaseModel):
#     name: Optional[str] = Field(..., description="Display name of the link (e.g., Facebook, LinkedIn)")
#     url: Optional[str] = Field(None, description="URL of the link")

# class CustomText(BaseModel):
#     title: str = Field(..., description="Title of custom section")
#     description: Optional[str] = Field(None, description="Description of the custom section")
#     link: Optional[Link] = Field(None, description="Optional link with name and URL")

# # Main Resume Request Model
# class ResumeRequest(BaseModel):
#     template_name: Optional[str] = Field("modern7", description="Template name")
#     personal_info: PersonalInfo = Field(..., description="Personal information")
#     photo: Optional[str] = Field(None, description="Base64-encoded image string")  # ✅ Add this line

#     custom_links: Optional[list[Custom_link]] = Field(None, description="custom_links")
#     professional_summary: Optional[str] = Field(None, description="Professional summary")
#     page_size: Optional[str] = Field("A4", description="Page size")
#     work_experience: Optional[List[WorkExperience]] = Field(None, description="Work experience")
#     education: Optional[List[Education]] = Field(None, description="Education")
#     skills: Optional[List[str]] = Field(None, description="Skills list")
#     academic_projects: Optional[List[AcademicProject]] = Field(None, description="Academic projects")
#     certifications: Optional[List[Certification]] = Field(None, description="Certifications")
#     publications: Optional[List[Publication]] = Field(None, description="Publications")
#     hobbies: Optional[List[str]] = Field(None, description="Hobbies and interests")
#     languages: Optional[List[str]] = Field(None, description="Languages")
#     referees: Optional[List[Referee]] = Field(None, description="References")
#     custom_text: Optional[list[CustomText]] = Field(None, description= "custom text")

# class CoverLetterRequest(BaseModel):
#     cover_letter_info : PersonalInfo_2 = Field(..., description="Information for cover letter")

# from dotenv import load_dotenv
# from starlette.middleware.base import BaseHTTPMiddleware
# from fastapi import FastAPI, Response, Request
# from fastapi.middleware.gzip import GZipMiddleware

# app = FastAPI(
#     title="Enhanced Resume Generator API", 
#     version="2.0.0",
#     description="A comprehensive resume generator supporting multiple sections and formats"
# )

# # ---- POST Endpoint to generate resume ----
# @app.post("/generate-resume/")
# def create_resume(data: ResumeRequest):
#     try:
#         # Convert Pydantic model to dict
#         resume_data = data.model_dump()
        
#         # Clean the data (remove None values and empty lists)
#         clean_data = {}
#         for key, value in resume_data.items():
#             if value is not None:
#                 if isinstance(value, list) and len(value) == 0:
#                     continue
#                 clean_data[key] = value
        
#         # Generate resume PDF
#         pdf_path = generate_resume(clean_data)
        
#         # Create a clean filename
#         name = clean_data.get('personal_info', {}).get('name', 'Resume')
#         clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
#         filename = f"{clean_name.replace(' ', '_')}_resume.pdf"
        
#         return FileResponse(
#             pdf_path,
#             media_type="application/pdf",
#             filename=filename,
#             headers={"Content-Disposition": f"attachment; filename={filename}"}
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

# # For local development
# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port, reload=DEBUG)





from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
import os
import uvicorn
from generate_resume import generate_resume, generate_coverletter
import logging
from typing import Dict, Any, Callable
import tempfile
import time
from collections import defaultdict
import uuid

# Import the enhanced models
from pydantic import BaseModel, Field

class PersonalInfo_2(BaseModel):
    template_name : Optional[str] = Field(None, description="name of cover letter template")
    page_size : Optional[str] = Field(None, description="page size for cover letter" )
    name: str = Field(..., description="Full name")
    title: Optional[str] = Field(None, description="Job title or profession")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    location: Optional[str] = Field(None, description="Location/Address")
    company_name: Optional[str] = Field(None, description="company name")
    hiring_manager_name: Optional[str] = Field(None, description="Manager name")
    paragraph : Optional[list[str]] = Field(None, description="Why are you best fit for this job")

# Personal Information Model
class PersonalInfo(BaseModel):
    name: str = Field(..., description="Full name")
    title: Optional[str] = Field(None, description="Job title or profession")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    location: Optional[str] = Field(None, description="Location/Address")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    website: Optional[str] = Field(None, description="Personal website URL")

class Custom_link(BaseModel):
    name: Optional[str] = Field(None, description="Link name")
    url: Optional[str] = Field(None, description='url')

# Work Experience Model
class WorkExperience(BaseModel):
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job position/title")
    start_date: str = Field(..., description="Start date")
    end_date: Optional[str] = Field(None, description="End date (None if current)")
    description: Optional[str] = Field(None, description="Job description bullet points")

# Education Model
class Education(BaseModel):
    institution: str = Field(..., description="Educational institution")
    degree: str = Field(..., description="Degree obtained")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date")

# Academic Projects Model
class AcademicProject(BaseModel):
    title: str = Field(..., description="Project title")
    date: str = Field(..., description="Project date")
    technologies: Optional[str] = Field(None, description="Technologies used")
    # description: Optional[List[str]] = Field(None, description="Project description")
    description: Optional[str] = Field(None, description="Job description bullet points")
    links: Optional[Dict[str, str]] = Field(None, description="Project links")

# Certifications Model
class Certification(BaseModel):
    name: str = Field(..., description="Certification name")
    issuer: str = Field(..., description="Issuing organization")
    date: str = Field(..., description="Date obtained")
    credential_id: Optional[str] = Field(None, description="Credential ID")
    url: Optional[str] = Field(None, description="Certificate URL")
    description: Optional[str] = Field(None, description="Job description bullet points")
    # description: Optional[List[str]] = Field(None, description="Certification description")

# Publications Model
class Publication(BaseModel):
    title: str = Field(..., description="Publication title")
    authors: str = Field(..., description="Authors")
    journal: str = Field(..., description="Journal or publication venue")
    date: str = Field(..., description="Publication date")
    url: Optional[str] = Field(None, description="Publication URL")
    # description: Optional[List[str]] = Field(None, description="Publication description")
    description: Optional[str] = Field(None, description="Job description bullet points")

# Referees Model
class Referee(BaseModel):
    name: str = Field(..., description="Reference name")
    position: str = Field(..., description="Reference position")
    organization: Optional[str] = Field(None, description="Organization")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    relationship: Optional[str] = Field(None, description="Relationship to applicant")

# Custom Text
# class CustomText(BaseModel):
#     title: str = Field(..., description="Title of custom section")
#     description: Optional[str] = Field(None, description="Description of Custom section")

class Link(BaseModel):
    name: Optional[str] = Field(..., description="Display name of the link (e.g., Facebook, LinkedIn)")
    url: Optional[str] = Field(None, description="URL of the link")

class CustomText(BaseModel):
    title: str = Field(..., description="Title of custom section")
    description: Optional[str] = Field(None, description="Description of the custom section")
    link: Optional[Link] = Field(None, description="Optional link with name and URL")

# Main Resume Request Model
class ResumeRequest(BaseModel):
    template_name: Optional[str] = Field("modern7", description="Template name")
    personal_info: PersonalInfo = Field(..., description="Personal information")
    photo: Optional[str] = Field(None, description="Base64-encoded image string")  # ✅ Add this line

    custom_links: Optional[list[Custom_link]] = Field(None, description="custom_links")
    professional_summary: Optional[str] = Field(None, description="Professional summary")
    page_size: Optional[str] = Field("A4", description="Page size")
    work_experience: Optional[List[WorkExperience]] = Field(None, description="Work experience")
    education: Optional[List[Education]] = Field(None, description="Education")
    skills: Optional[List[str]] = Field(None, description="Skills list")
    academic_projects: Optional[List[AcademicProject]] = Field(None, description="Academic projects")
    certifications: Optional[List[Certification]] = Field(None, description="Certifications")
    publications: Optional[List[Publication]] = Field(None, description="Publications")
    hobbies: Optional[List[str]] = Field(None, description="Hobbies and interests")
    languages: Optional[List[str]] = Field(None, description="Languages")
    referees: Optional[List[Referee]] = Field(None, description="References")
    custom_text: Optional[list[CustomText]] = Field(None, description= "custom text")

class CoverLetterRequest(BaseModel):
    cover_letter_info : PersonalInfo_2 = Field(..., description="Information for cover letter")

from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Response, Request
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(
    title="Enhanced Resume Generator API", 
    version="2.0.0",
    description="A comprehensive resume generator supporting multiple sections and formats"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add health check endpoint
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Resume Generator API is running"}

# ---- POST Endpoint to generate resume ----
@app.post("/generate-resume/")
def create_resume(data: ResumeRequest):
    try:
        # Convert Pydantic model to dict
        resume_data = data.model_dump()
        
        # Clean the data (remove None values and empty lists)
        clean_data = {}
        for key, value in resume_data.items():
            if value is not None:
                if isinstance(value, list) and len(value) == 0:
                    continue
                clean_data[key] = value
        
        # Generate resume PDF
        pdf_path = generate_resume(clean_data)
        
        # Create a clean filename
        name = clean_data.get('personal_info', {}).get('name', 'Resume')
        clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{clean_name.replace(' ', '_')}_resume.pdf"
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

# ---- POST Endpoint to generate cover letter ----
@app.post("/generate-coverletter/")
def create_cover_letter(data: CoverLetterRequest):
    try:
        # Convert Pydantic model to dict
        cover_letter_data = data.model_dump()
        
        # Generate cover letter PDF
        pdf_path = generate_coverletter(cover_letter_data)
        
        # Create a clean filename
        name = cover_letter_data.get('cover_letter_info', {}).get('name', 'CoverLetter')
        clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{clean_name.replace(' ', '_')}_cover_letter.pdf"
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")

# For local development
if __name__ == "__main__":
    import os
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=DEBUG)