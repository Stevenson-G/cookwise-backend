from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

following = relationship(
    "Follow",
    foreign_keys="[Follow.follower_id]",
    backref="follower"
)

followers = relationship(
    "Follow",
    foreign_keys="[Follow.following_id]",
    backref="following_user"
)