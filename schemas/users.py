from sqlmodel import SQLModel

class UserPayload(SQLModel):
    username: str

class UserCreate(SQLModel):
    username: str
    password_hash: str

class UserPublic(SQLModel):
    username: str

class UserUpdate(SQLModel):
    username: str

class Token(SQLModel):
    access_token: str
    token_type: str