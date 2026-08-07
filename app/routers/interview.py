from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app import models
from app.schemas import (
    InterviewCreate,
    InterviewRead,
    InterviewUpdate,
)

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)
@router.post(
    "",
    response_model=InterviewRead
)
def create_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    application = (
        db.query(models.Application)
        .filter(
            models.Application.id == interview.application_id
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db_interview = models.Interview(
        application_id=interview.application_id,
        round=interview.round,
        date=interview.date,
        time=interview.time,
        interviewer=interview.interviewer,
        notes=interview.notes,
        result=interview.result
    )

    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    return db_interview

@router.get(
    "/application/{application_id}",
    response_model=list[InterviewRead]
)
def get_application_interviews(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    application = (
        db.query(models.Application)
        .filter(
            models.Application.id == application_id
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return application.interviews

@router.put(
    "/{interview_id}",
    response_model=InterviewRead
)
def update_interview(
    interview_id: int,
    updated_interview: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interview = (
        db.query(models.Interview)
        .filter(
            models.Interview.id == interview_id
        )
        .first()
    )

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    if interview.application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    interview.round = updated_interview.round
    interview.date = updated_interview.date
    interview.time = updated_interview.time
    interview.interviewer = updated_interview.interviewer
    interview.notes = updated_interview.notes
    interview.result = updated_interview.result

    db.commit()
    db.refresh(interview)

    return interview

@router.delete(
    "/{interview_id}",
    status_code=204
)
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interview = (
        db.query(models.Interview)
        .filter(
            models.Interview.id == interview_id
        )
        .first()
    )

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    if interview.application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(interview)
    db.commit()

    return
summary="Create interview"
summary="Get interviews for application"
summary="Update interview"
summary="Delete interview"