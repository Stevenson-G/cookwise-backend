from fastapi import FastAPI
from app.routes import auth
from app.database.base import Base
from app.database.session import engine
from app.models import user, recipe, follow, like, save
from app.routes import auth, recipes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(recipes.router)

