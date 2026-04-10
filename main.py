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

@app.post("/token")
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = session.exec(select(User).where(User.username==form.username)).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No such user with username of '{form.username}'")
    if not verify(form.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Incorrect password")
    
    payload = {
        "id":user.id,
        "username":form.username
    }

    return Token(access_token=create_jwt_token(payload), token_type="bearer")

@app.post("/signup")
async def signup(user: UserSignup, session: SessionDep):
    username = user.username
    hashed_password = hash(user.password)

    new_user = User(username=username, password_hash=hashed_password)
    session.add(new_user)
    session.commit()

    return {"ok":True}

@app.get("/me")
async def get_me(user: UserDep):
    return user