from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import applications

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    description="Backend API for managing job applications",
    version="1.0.0"
)

app.include_router(applications.router)