import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated, Any
from datetime import datetime, timedelta, timezone

from dependencies.settings import SettingsDep, get_settings
from schemas.users import UserPayload

oauth2_scheme = OAuth2PasswordBearer("token")

SchemeDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token: SchemeDep, settings: SettingsDep) -> UserPayload:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret, [settings.alg])
        return UserPayload(**payload)
    except jwt.InvalidTokenError:
        raise credentials_exception

def create_jwt_token(payload: dict[str, Any], exp_delta: timedelta | None = None) -> str:
    settings = get_settings()
    if exp_delta is None:
        # exp_delta = datetime.now() + timedelta(minutes=settings.access_exp_min)
        exp_delta = datetime.now(timezone.utc) + timedelta(seconds=30)

    to_encode = payload.copy()
    to_encode.update({"exp":exp_delta})
    return jwt.encode(to_encode, settings.secret, settings.alg)

UserDep = Annotated[UserPayload, Depends(get_current_user)]
