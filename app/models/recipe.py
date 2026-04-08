from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    portion = Column(String)
    food_type = Column(String)
    ingredients = Column(JSON)
    steps = Column(JSON)
    image_url = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")