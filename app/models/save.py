from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database.base import Base

class Save(Base):
    __tablename__ = "saves"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id', name='unique_save'),
    )