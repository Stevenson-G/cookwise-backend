from app.models.follow import Follow
from fastapi import HTTPException
from app.models.recipe import Recipe
from app.models.like import Like
from app.models.save import Save


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

    posts_count = db.query(Recipe).filter(
        Recipe.user_id == user_id
    ).count()

    return {
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": posts_count
    }


def get_user_recipes(db, user_id: int):
    return db.query(Recipe).filter(Recipe.user_id == user_id).all()


def get_liked_recipes(db, user_id: int):
    likes = db.query(Like).filter(Like.user_id == user_id).all()
    recipe_ids = [l.recipe_id for l in likes]

    return db.query(Recipe).filter(Recipe.id.in_(recipe_ids)).all()


def get_saved_recipes(db, user_id: int):
    saves = db.query(Save).filter(Save.user_id == user_id).all()
    recipe_ids = [s.recipe_id for s in saves]

    return db.query(Recipe).filter(Recipe.id.in_(recipe_ids)).all()