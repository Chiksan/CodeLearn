from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from app.models.user import LanguageEnum, LevelEnum


# ── Auth ──────────────────────────────────────────────────
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    xp: int
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Courses ───────────────────────────────────────────────
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    language: LanguageEnum
    level: LevelEnum

class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    language: LanguageEnum
    level: LevelEnum
    is_published: bool
    lesson_count: Optional[int] = 0

    class Config:
        from_attributes = True


# ── Lessons ───────────────────────────────────────────────
class LessonCreate(BaseModel):
    title: str
    content: Optional[str] = None
    starter_code: Optional[str] = None
    solution: Optional[str] = None
    tests: Optional[str] = None
    xp_reward: int = 10
    order: int = 0

class LessonOut(BaseModel):
    id: int
    course_id: int
    title: str
    content: Optional[str]
    starter_code: Optional[str]
    hints: Optional[str] = None
    xp_reward: int
    order: int
    language: Optional[LanguageEnum] = None

    class Config:
        from_attributes = True


# ── Code runner ───────────────────────────────────────────
class CodeSubmit(BaseModel):
    lesson_id: int
    language: LanguageEnum
    code: str

class CodeResult(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None
    passed_tests: int = 0
    total_tests: int = 0
    xp_earned: int = 0


# ── Progress ──────────────────────────────────────────────
class ProgressOut(BaseModel):
    lesson_id: int
    completed: bool
    attempts: int
    last_code: Optional[str]

    class Config:
        from_attributes = True
