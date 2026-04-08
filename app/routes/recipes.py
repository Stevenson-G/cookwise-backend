from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.recipe import RecipeCreate
from app.services import recipe_service
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/")
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return recipe_service.create_recipe(db, recipe, current_user.id)