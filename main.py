from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import create_database_and_tables
from routers import auth, blogs


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(blogs.router)
