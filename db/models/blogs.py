from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

now = lambda: datetime.now(UTC)

class Blog(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=128, index=True)
    content: str = Field()
    publish_date: datetime = Field(default_factory=now)
    last_update: datetime = Field(default_factory=now)