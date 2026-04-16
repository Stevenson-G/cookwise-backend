from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.database.session import get_db
from app.services import user_service
from app.utils.security import get_current_user
from app.models.user import User

from app.services.user_service import follow_user, unfollow_user

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

@router.post("/{user_id}/follow")
def follow(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return follow_user(db, current_user.id, user_id)


@router.delete("/{user_id}/follow")
def unfollow(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return unfollow_user(db, current_user.id, user_id)

@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/username")
def get_username(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}

@router.get("/me/stats")
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.get_follow_stats(db, current_user.id)

@router.get("/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_follow_stats(db, user_id)