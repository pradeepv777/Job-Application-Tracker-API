from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from sqlalchemy import func
from app import models


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    total = (
        db.query(func.count(models.Application.id))
        .filter(models.Application.user_id == current_user.id)
        .scalar()
    )

    applied = (
        db.query(func.count(models.Application.id))
        .filter(
            models.Application.user_id == current_user.id,
            models.Application.status == "Applied"
        )
        .scalar()
    )

    interview = (
        db.query(func.count(models.Application.id))
        .filter(
            models.Application.user_id == current_user.id,
            models.Application.status == "Interview"
        )
        .scalar()
    )

    offer = (
        db.query(func.count(models.Application.id))
        .filter(
            models.Application.user_id == current_user.id,
            models.Application.status == "Offer"
        )
        .scalar()
    )

    rejected = (
        db.query(func.count(models.Application.id))
        .filter(
            models.Application.user_id == current_user.id,
            models.Application.status == "Rejected"
        )
        .scalar()
    )

    return {
        "total_applications": total,
        "applied": applied,
        "interview": interview,
        "offer": offer,
        "rejected": rejected
    }
