from pydantic import BaseModel

class Application(BaseModel):
    company: str
    role: str
    salary: int
    status: str


class ApplicationResponse(BaseModel):
    message: str
    company: str
    salary: int