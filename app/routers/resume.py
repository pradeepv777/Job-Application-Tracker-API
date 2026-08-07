import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Ensure uploads/resumes directory exists
    os.makedirs(os.path.join("uploads", "resumes"), exist_ok=True)

    # Clean up old resume if it exists
    if current_user.resume_path and os.path.exists(current_user.resume_path):
        try:
            os.remove(current_user.resume_path)
        except Exception:
            pass

    # Generate unique filename using UUID
    filename = f"{current_user.id}_{uuid.uuid4().hex}.pdf"
    file_path = os.path.join("uploads", "resumes", filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    current_user.resume_path = file_path

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Resume uploaded successfully",
        "resume_path": file_path
    }

@router.delete("")
def delete_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.resume_path:
        raise HTTPException(
            status_code=404,
            detail="No resume uploaded"
        )

    if os.path.exists(current_user.resume_path):
        try:
            os.remove(current_user.resume_path)
        except Exception:
            pass

    current_user.resume_path = None
    db.commit()

    return {
        "message": "Resume deleted successfully"
    }

@router.get("")
def get_resume(
    current_user: User = Depends(get_current_user)
):
    if not current_user.resume_path:
        raise HTTPException(
            status_code=404,
            detail="No resume uploaded"
        )

    return {
        "resume_path": current_user.resume_path
    }