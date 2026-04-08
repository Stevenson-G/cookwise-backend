from pydantic import BaseModel
from typing import List, Dict, Optional

class RecipeCreate(BaseModel):
    title: str
    portion: str
    food_type: str
    ingredients: List[Dict]
    steps: List[str]
    image_url: Optional[str] = None