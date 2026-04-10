from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from db.database import create_database_and_tables
from schemas.users import Token
from dependencies.auth import UserDep, create_jwt_token

async def lifespan(app: FastAPI):
    create_database_and_tables()

app = FastAPI(lifespan=lifespan)

@app.post("/token")
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    pass

@app.get("/me")
async def get_me(user: UserDep):
    return user