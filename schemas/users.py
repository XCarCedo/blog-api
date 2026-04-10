from sqlmodel import SQLModel

class UserPayload(SQLModel):
    id: int
    username: str

class UserPublic(SQLModel):
    username: str

class UserUpdate(SQLModel):
    username: str

class UserSignup(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str