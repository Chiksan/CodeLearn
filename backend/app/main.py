from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.database import engine, Base
from app.api.routes import auth, courses, lessons, code_runner, progress, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте (в продакшене используй Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="CodeLearn API",
    description="Платформа для интерактивного обучения программированию",
    version="1.0.0",
    lifespan=lifespan,
)

import os
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,        prefix="/api/auth",     tags=["auth"])
app.include_router(courses.router,     prefix="/api/courses",  tags=["courses"])
app.include_router(lessons.router,     prefix="/api/lessons",  tags=["lessons"])
app.include_router(code_runner.router, prefix="/api/code",     tags=["code"])
app.include_router(progress.router,    prefix="/api/progress", tags=["progress"])
app.include_router(users.router,       prefix="/api/users",    tags=["users"])


@app.get("/")
async def root():
    return {"message": "CodeLearn API работает", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}
