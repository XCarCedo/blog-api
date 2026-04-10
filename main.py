from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import select
from contextlib import asynccontextmanager

from hash import hash, verify
from db.models.users import User
from db.database import create_database_and_tables
from schemas.users import Token, UserSignup
from dependencies.auth import UserDep, create_jwt_token
from dependencies.database import SessionDep

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_and_tables()
    yield

app = FastAPI(lifespan=lifespan)



@app.get("/me")
async def get_me(user: UserDep):
    return user