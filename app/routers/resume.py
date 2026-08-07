import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@router.post("/upload", summary="Upload resume", status_code=status.HTTP_201_CREATED)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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

@router.delete("", summary="Delete resume", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.resume_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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

@router.get("", summary="Get resume metadata")
def get_resume(
    current_user: User = Depends(get_current_user)
):
    if not current_user.resume_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume uploaded"
        )

    return {
        "resume_path": current_user.resume_path
    }


@router.get("/download", summary="Download resume file")
def download_resume(
    current_user: User = Depends(get_current_user)
):
    if not current_user.resume_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume uploaded"
        )
    
    if not os.path.exists(current_user.resume_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found on server"
        )
    
    filename = os.path.basename(current_user.resume_path)
    return FileResponse(
        path=current_user.resume_path,
        media_type="application/pdf",
        filename=filename
    )
