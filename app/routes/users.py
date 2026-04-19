from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.database.session import get_db
from app.services import user_service
from app.utils.security import get_current_user
from app.models.user import User

from app.services.user_service import follow_user, unfollow_user
from app.utils.supabase_client import upload_image

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/upload-profile-image")
def upload_profile_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("📤 Subiendo imagen de perfil...")

    image_url = upload_image(image)

    print("Imagen subida:", image_url)

    if not image_url:
        return {"error": "No se pudo subir la imagen"}

    current_user.profile_image = image_url
    db.commit()

    return {"image_url": image_url}

@router.post("/{user_id}/follow")
def follow(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return follow_user(db, current_user.id, user_id)


@router.delete("/{user_id}/follow")
def unfollow(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return unfollow_user(db, current_user.id, user_id)

@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "profile_image": current_user.profile_image
    }

@router.get("/me/username")
def get_username(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}

@router.get("/me/stats")
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.get_follow_stats(db, current_user.id)

@router.get("/me/recipes")
def get_my_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.get_user_recipes(db, current_user.id)


@router.get("/me/liked")
def get_liked_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.get_liked_recipes(db, current_user.id)


@router.get("/me/saved")
def get_saved_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.get_saved_recipes(db, current_user.id)

@router.get("/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_follow_stats(db, user_id)