from app.models.follow import Follow
from fastapi import HTTPException

def follow_user(db, current_user_id: int, target_user_id: int):

    if current_user_id == target_user_id:
        raise HTTPException(status_code=400, detail="No puedes seguirte a ti mismo")

    existing = db.query(Follow).filter(
        Follow.follower_id == current_user_id,
        Follow.following_id == target_user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya sigues a este usuario")

    follow = Follow(
        follower_id=current_user_id,
        following_id=target_user_id
    )

    db.add(follow)
    db.commit()

    return {"message": "Usuario seguido"}

def unfollow_user(db, current_user_id: int, target_user_id: int):

    follow = db.query(Follow).filter(
        Follow.follower_id == current_user_id,
        Follow.following_id == target_user_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="No sigues a este usuario")

    db.delete(follow)
    db.commit()

    return {"message": "Usuario dejado de seguir"}

def get_follow_stats(db, user_id: int):
    followers_count = db.query(Follow).filter(
        Follow.following_id == user_id
    ).count()

    following_count = db.query(Follow).filter(
        Follow.follower_id == user_id
    ).count()

    return {
        "followers": followers_count,
        "following": following_count
    }