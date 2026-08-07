from pydantic import BaseModel, Field

class InterviewCreate(BaseModel):
    application_id: int
    round: str = Field(min_length=2)
    date: str
    time: str
    interviewer: str
    notes: str
    result: str


class InterviewRead(BaseModel):
    id: int
    application_id: int
    round: str
    date: str
    time: str
    interviewer: str
    notes: str
    result: str

    class Config:
        from_attributes = True


class InterviewUpdate(BaseModel):
    round: str
    date: str
    time: str
    interviewer: str
    notes: str
    result: str
