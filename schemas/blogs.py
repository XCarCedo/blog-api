from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class BlogBase(SQLModel):
    title: str = Field(max_length=128)
    content: str

class BlogCreate(BlogBase):
    pass

class BlogPublic(BlogBase):
    id: int

class BlogUpdate(BlogBase):
    title: str | None = Field(None, max_length=128)
    content: str | None = Field(None)