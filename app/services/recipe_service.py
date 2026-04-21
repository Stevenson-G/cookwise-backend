from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate
from app.models.follow import Follow
from app.models.like import Like
from app.models.save import Save
from fastapi import HTTPException

import json
import requests

from app.config import settings

from app.utils.supabase_client import upload_image


def _normalize_ingredients(raw_ingredients):
    """Normalize ingredient payloads coming from different clients."""
    normalized = []

    for ingredient in raw_ingredients or []:
        if not isinstance(ingredient, dict):
            continue

        name = ingredient.get("name") or ingredient.get("ingredient") or ""
        amount = (
            ingredient.get("amount")
            or ingredient.get("quantity")
            or ingredient.get("cantidad")
            or ""
        )
        unit = ingredient.get("unit") or ingredient.get("unidad") or ""

        normalized.append(
            {
                "name": str(name).strip(),
                "amount": str(amount).strip(),
                "unit": str(unit).strip(),
            }
        )

    return normalized

def create_recipe(db, recipe_data, user_id):

    image_url = None

    if recipe_data.get("image"):
        try:
            print("📤 Intentando subir imagen...")
            image_url = upload_image(recipe_data["image"])
            print("Imagen subida:", image_url)
        except Exception as e:
            print("ERROR subiendo imagen:", e)
            image_url = None

    new_recipe = Recipe(
        title=recipe_data["title"],
        portion=recipe_data["portion"],
        food_type=recipe_data["foodType"],
        ingredients=_normalize_ingredients(recipe_data.get("ingredients")),
        steps=recipe_data["steps"],
        image_url=image_url,
        user_id=user_id
)
    

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe

def get_feed(db, user_id: int):

    recipes = db.query(Recipe).all()

    result = []

    for recipe in recipes:

        is_following = db.query(Follow).filter(
            Follow.follower_id == user_id,
            Follow.following_id == recipe.user_id
        ).first() is not None

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
            "image": recipe.image_url or "",
            "ingredients": recipe.ingredients or [],
            "steps": recipe.steps or [],
            "portion": recipe.portion or "",
            "likes": likes_count,
            "saves": saves_count,
            "liked": liked,
            "saved": saved,
            "user": {
                "id": recipe.user_id,
                "name": recipe.user.username if recipe.user else "Anónimo",
                "is_following": is_following,
            }
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

def search_recipes(db, query: str, limit: int = 20):
    recipes = db.query(Recipe).filter(
        Recipe.title.ilike(f"%{query}%")
    ).limit(limit).all()

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

SPOONACULAR_API_KEY = settings.SPOONACULAR_API_KEY

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    
    params = {
        "includeNutrition": False,
        "apiKey": SPOONACULAR_API_KEY
    }

    response = requests.get(url, params=params)
    return response.json()

def get_recipes_with_fallback(db, query: str):

    local_recipes = db.query(Recipe).filter(
        Recipe.title.ilike(f"%{query}%")
    ).all()

    if local_recipes:
        return local_recipes

    search_url = "https://api.spoonacular.com/recipes/complexSearch"

    params = {
        "query": query,
        "number": 5,
        "apiKey": SPOONACULAR_API_KEY
    }

    try:
        response = requests.get(search_url, params=params)
        data = response.json()
    except Exception as e:
        print("ERROR SPOONACULAR:", e)
        return []

    results = data.get("results", [])
    saved_recipes = []

    for r in results:
        details = get_recipe_details(r["id"])

        if not details:
            continue

        ingredients = [
            {
                "name": ing.get("name", ""),
                "amount": str(ing.get("amount", "")),
                "unit": ing.get("unit", "")
            }
            for ing in details.get("extendedIngredients", [])
        ]

        steps = []
        instructions = details.get("analyzedInstructions", [])

        if instructions and len(instructions) > 0:
            for step in instructions[0].get("steps", []):
                steps.append(step.get("step", ""))

        new_recipe = Recipe(
            title=details.get("title") or "",
            image_url=details.get("image") or "",
            food_type="external",
            ingredients=ingredients,
            steps=steps,
            portion=str(details.get("servings", "N/A")),
            user_id=None
        )

        db.add(new_recipe)
        db.flush()

        saved_recipes.append(new_recipe)

    db.commit()

    result = []

    for recipe in saved_recipes:
        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "image": recipe.image_url,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "portion": recipe.portion,
            "likes": 0,
            "saves": 0,
            "liked": False,
            "saved": False,
            "user": {
                "id": None,
                "name": "Spoonacular"
            }
        })

    return result