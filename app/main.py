from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import application, auth
from app.routers import dashboard   
from app.routers import resume
from app.routers import interview
from app.routers import analytics

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Job Application Tracker API",
    description="Backend API for managing job applications",
    version="1.0.0"
)

app.include_router(application.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(resume.router)
app.include_router(interview.router)
app.include_router(analytics.router)

