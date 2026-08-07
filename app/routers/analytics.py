from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app import models

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("")
def analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Salary statistics
    salary_stats = (
        db.query(
            func.avg(models.Application.salary).label("average_salary"),
            func.max(models.Application.salary).label("highest_salary"),
            func.min(models.Application.salary).label("lowest_salary"),
        )
        .filter(models.Application.user_id == current_user.id)
        .first()
    )

    # Application status counts
    status_counts = (
        db.query(
            models.Application.status,
            func.count(models.Application.id)
        )
        .filter(models.Application.user_id == current_user.id)
        .group_by(models.Application.status)
        .all()
    )

    status_dict = {
        status: count
        for status, count in status_counts
    }

    # Interview statistics
    interview_stats = (
        db.query(
            func.count(models.Interview.id).label("total"),
            func.sum(
                case(
                    (models.Interview.result == "Scheduled", 1),
                    else_=0
                )
            ).label("scheduled"),
            func.sum(
                case(
                    (models.Interview.result == "Completed", 1),
                    else_=0
                )
            ).label("completed"),
        )
        .join(
            models.Application,
            models.Interview.application_id == models.Application.id
        )
        .filter(
            models.Application.user_id == current_user.id
        )
        .first()
    )

    total_applications = sum(status_dict.values())
    offers = status_dict.get("Offer", 0)

    success_rate = (
        round((offers / total_applications) * 100, 2)
        if total_applications > 0
        else 0
    )

    return {
        "salary": {
            "average": salary_stats.average_salary or 0,
            "highest": salary_stats.highest_salary or 0,
            "lowest": salary_stats.lowest_salary or 0,
        },
        "applications": {
            "applied": status_dict.get("Applied", 0),
            "interview": status_dict.get("Interview", 0),
            "offer": status_dict.get("Offer", 0),
            "rejected": status_dict.get("Rejected", 0),
            "total": total_applications
        },
        "interviews": {
            "total": interview_stats.total or 0,
            "scheduled": interview_stats.scheduled or 0,
            "completed": interview_stats.completed or 0,
        },
        "success_rate": success_rate
    }