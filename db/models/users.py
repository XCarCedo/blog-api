from sqlmodel import SQLModel, Field, Relationship
from datetime import UTC, datetime, timedelta
from uuid import uuid4

one_week = lambda: datetime.now(UTC) + timedelta(weeks=1)
string_uuid4 = lambda: str(uuid4())

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str = Field()
    superuser: bool = Field(False)
    tokens: list[RefreshToken] = Relationship(back_populates="user")

class RefreshToken(SQLModel, table=True):
    token: str = Field(default_factory=string_uuid4, index=True, primary_key=True)
    expiration: datetime = Field(default_factory=one_week)
    user: User = Relationship(back_populates="tokens")
    user_id: int = Field(foreign_key="user.id")
