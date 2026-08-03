from fastapi import FastAPI, status
from app.schemas import Application,ApplicationResponse

app = FastAPI()


@app.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(application: Application):
    return {
        "message": f"Application submitted to {application.company}",
        "salary": application.salary
    }
