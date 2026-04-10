from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.recipe import RecipeCreate
from app.services import recipe_service
from app.models.user import User
from app.utils.security import get_current_user
from app.models.recipe import Recipe
from app.models.like import Like
from app.models.save import Save

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/")
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return recipe_service.create_recipe(db, recipe, current_user.id)

@router.get("/feed")
def get_user_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return recipe_service.get_feed(db, current_user.id)

def get_feed(db, user_id: int):

    recipes = db.query(Recipe).all()

    result = []

    for recipe in recipes:

        likes_count = db.query(Like).filter(
            Like.recipe_id == recipe.id
        ).count()

        liked = db.query(Like).filter(
            Like.recipe_id == recipe.id,
            Like.user_id == user_id
        ).first() is not None

        saves_count = db.query(Save).filter(
            Save.recipe_id == recipe.id
        ).count()

        saved = db.query(Save).filter(
            Save.recipe_id == recipe.id,
            Save.user_id == user_id
        ).first() is not None

        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "image": recipe.image_url,
            "likes": likes_count,
            "liked_by_user": liked,
            "saves": saves_count,
            "saved_by_user": saved
        })

    return result

@router.post("/{recipe_id}/like")
def like(recipe_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return recipe_service.like_recipe(db, current_user.id, recipe_id)

@router.delete("/{recipe_id}/like")
def unlike(recipe_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return recipe_service.unlike_recipe(db, current_user.id, recipe_id)

@router.post("/{recipe_id}/save")
def save(recipe_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return recipe_service.save_recipe(db, current_user.id, recipe_id)

@router.delete("/{recipe_id}/save")
def unsave(recipe_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return recipe_service.unsave_recipe(db, current_user.id, recipe_id)

@router.get("/category/{category}")
def get_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    return recipe_service.get_recipes_by_category(db, category)

@router.get("/search")
def search_recipes(
    query: str,
    db: Session = Depends(get_db)
):
    return recipe_service.search_recipes(db, query)

@router.get("/search-smart")
def search_smart(query: str, db: Session = Depends(get_db)):
    return recipe_service.get_recipes_with_fallback(db, query)