from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import create_database_and_tables
from routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)