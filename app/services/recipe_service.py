from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate


def create_recipe(db: Session, recipe_data: RecipeCreate, user_id: int):
    new_recipe = Recipe(
        title=recipe_data.title,
        portion=recipe_data.portion,
        food_type=recipe_data.food_type,
        ingredients=recipe_data.ingredients,
        steps=recipe_data.steps,
        image_url=recipe_data.image_url,
        user_id=user_id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe