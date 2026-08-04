from pydantic import BaseModel, Field

class Application(BaseModel):
    company: str = Field(min_length=2, max_length=100)
    role: str = Field(min_length=3, max_length=100)
    salary: int = Field(gt=10000)
    status: str = Field(default="Applied")


class ApplicationResponse(BaseModel):
    message: str
    company: str
    salary: int
class ApplicationRead(BaseModel):
    id: int
    company: str
    role: str
    salary: int
    status: str

    class Config:
        from_attributes = True #Important for sqlalchemy to map to ORM
        
class ApplicationUpdate(BaseModel):
    company: str = Field(min_length=2, max_length=100)
    role: str = Field(min_length=3, max_length=100)
    salary: int = Field(gt=10000)
    status: str