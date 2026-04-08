from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.database.session import get_db
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/upload-profile-image")
def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file_location = f"uploads/{current_user.id}_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_user.profile_image = file_location
    db.commit()

    return {"image_url": file_location}