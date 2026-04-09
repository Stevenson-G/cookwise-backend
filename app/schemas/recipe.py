from pydantic import BaseModel
from typing import List, Dict, Optional

class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str

class RecipeCreate(BaseModel):
    title: str
    portion: str
    category: str
    ingredients: List[Ingredient]
    steps: List[str]
    image: Optional[str] = None