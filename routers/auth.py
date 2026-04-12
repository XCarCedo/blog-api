from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload
from datetime import datetime, UTC

from hash import hash, verify
from db.models.users import User, RefreshToken
from schemas.users import Token, UserSignup, UserPayload, RefreshTokenScheme, AccessToken
from dependencies.auth import UserDep, create_jwt_token
from dependencies.database import SessionDep

router = APIRouter()

@router.post("/token")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = session.exec(select(User).where(User.username==form.username).options(selectinload(User.tokens))).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No such user with username of '{form.username}'")
    if not verify(form.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Incorrect password")
    
    # Invalidate all previous refresh tokens for this user
    if len(user.tokens) > 0:
        for token in user.tokens:
            session.delete(token)
        session.commit()
        session.refresh(user)

    print(f"{user.model_dump()=}")
    payload = UserPayload(**user.model_dump())

    refresh_token = RefreshToken(user_id=user.id)
    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)

    return Token(access_token=create_jwt_token(payload.model_dump()), token_type="bearer", refresh_token=refresh_token.token)

@router.post("/signup")
async def signup(user: UserSignup, session: SessionDep):
    username = user.username
    hashed_password = hash(user.password)

    new_user = User(username=username, password_hash=hashed_password)
    session.add(new_user)
    session.commit()

    return {"ok":True}

@router.post("/refresh")
async def refresh_token(refresh_token: RefreshTokenScheme, session: SessionDep):
    token = session.exec(select(RefreshToken).options(joinedload(RefreshToken.user))).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    exp = token.expiration.replace(tzinfo=UTC)
    
    if datetime.now(UTC) > exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is expired")
    
    payload = UserPayload(**token.user.model_dump())
    return AccessToken(access_token=create_jwt_token(payload.model_dump()), token_type="bearer")

@router.get("/me")
async def get_me(user: UserDep):
    return user