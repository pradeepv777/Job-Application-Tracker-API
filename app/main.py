import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models
from app.routers import application, auth
from app.routers import dashboard   
from app.routers import resume
from app.routers import interview
from app.routers import analytics

Base.metadata.create_all(bind=engine)

# Create upload directories automatically
os.makedirs("uploads/resumes", exist_ok=True)

app = FastAPI(
    title="Job Application Tracker API",
    description="Backend API for managing job applications",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(application.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(resume.router)
app.include_router(interview.router)
app.include_router(analytics.router)
