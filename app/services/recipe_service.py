from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate
from app.models.follow import Follow
from app.models.like import Like
from app.models.save import Save
from fastapi import HTTPException

def create_recipe(db, recipe_data, user_id):

    new_recipe = Recipe(
        title=recipe_data.title,
        portion=recipe_data.portion,
        food_type=recipe_data.category,
        ingredients=[ing.dict() for ing in recipe_data.ingredients],
        steps=recipe_data.steps,
        image_url=recipe_data.image,
        user_id=user_id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe

def get_feed(db, user_id: int):

    recipes = (
        db.query(Recipe)
        .join(Follow, Recipe.user_id == Follow.following_id)
        .filter(Follow.follower_id == user_id)
        .all()
    )

    result = []

    for recipe in recipes:

        likes_count = db.query(Like).filter(
            Like.recipe_id == recipe.id
        ).count()

        saves_count = db.query(Save).filter(
            Save.recipe_id == recipe.id
        ).count()

        liked = db.query(Like).filter(
            Like.user_id == user_id,
            Like.recipe_id == recipe.id
        ).first() is not None

        saved = db.query(Save).filter(
            Save.user_id == user_id,
            Save.recipe_id == recipe.id
        ).first() is not None

        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "image": recipe.image_url,
            "likes": likes_count,
            "saves": saves_count,
            "liked": liked,
            "saved": saved,
            "user_id": recipe.user_id
        })

    return result

def like_recipe(db, user_id: int, recipe_id: int):

    existing = db.query(Like).filter(
        Like.user_id == user_id,
        Like.recipe_id == recipe_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya has dado like")

    like = Like(user_id=user_id, recipe_id=recipe_id)

    db.add(like)
    db.commit()

    return {"message": "Like añadido"}

def unlike_recipe(db, user_id: int, recipe_id: int):

    like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.recipe_id == recipe_id
    ).first()

    if not like:
        raise HTTPException(status_code=404, detail="No has dado like")

    db.delete(like)
    db.commit()

    return {"message": "Like eliminado"}

def get_likes_count(db, recipe_id: int):
    return db.query(Like).filter(Like.recipe_id == recipe_id).count()

def save_recipe(db, user_id: int, recipe_id: int):

    existing = db.query(Save).filter(
        Save.user_id == user_id,
        Save.recipe_id == recipe_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya está guardada")

    save = Save(user_id=user_id, recipe_id=recipe_id)

    db.add(save)
    db.commit()

    return {"message": "Receta guardada"}

def unsave_recipe(db, user_id: int, recipe_id: int):

    save = db.query(Save).filter(
        Save.user_id == user_id,
        Save.recipe_id == recipe_id
    ).first()

    if not save:
        raise HTTPException(status_code=404, detail="No estaba guardada")

    db.delete(save)
    db.commit()

    return {"message": "Receta eliminada de guardados"}

def get_saves_count(db, recipe_id: int):
    return db.query(Save).filter(Save.recipe_id == recipe_id).count()

def is_saved(db, user_id: int, recipe_id: int):
    return db.query(Save).filter(
        Save.user_id == user_id,
        Save.recipe_id == recipe_id
    ).first() is not None

def get_recipes_by_category(db, category: str):

    recipes = db.query(Recipe).filter(
        Recipe.food_type.ilike(f"%{category}%")
    ).all()

    result = []

    for recipe in recipes:
        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "image": recipe.image_url,
            "category": recipe.food_type,
            "user_id": recipe.user_id
        })

    return result

def search_recipes(db, query: str):

    recipes = db.query(Recipe).filter(
        Recipe.title.ilike(f"%{query}%")
    ).all()

    result = []

    for recipe in recipes:
        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "image": recipe.image_url,
            "category": recipe.food_type,
            "user_id": recipe.user_id
        })

    return result