from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.database import Base


class LanguageEnum(str, enum.Enum):
    python = "python"
    javascript = "javascript"
    html = "html"


class LevelEnum(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    username   = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active       = Column(Boolean, default=True)
    is_admin        = Column(Boolean, default=False)
    is_verified     = Column(Boolean, default=False)
    verify_token    = Column(String, nullable=True)
    xp              = Column(Integer, default=0)
    created_at      = Column(DateTime, default=datetime.utcnow)

    progress = relationship("UserProgress", back_populates="user")


class Course(Base):
    __tablename__ = "courses"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    description = Column(Text)
    language    = Column(Enum(LanguageEnum), nullable=False)
    level       = Column(Enum(LevelEnum), nullable=False)
    order       = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    lessons  = relationship("Lesson", back_populates="course", order_by="Lesson.order")
    progress = relationship("UserProgress", back_populates="course")


class Lesson(Base):
    __tablename__ = "lessons"

    id           = Column(Integer, primary_key=True, index=True)
    course_id    = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title        = Column(String, nullable=False)
    content      = Column(Text)           # Теория в Markdown
    starter_code = Column(Text)           # Стартовый код для редактора
    solution     = Column(Text)           # Эталонное решение
    tests        = Column(Text)           # JSON с тестами
    hints        = Column(Text)           # JSON-массив подсказок
    xp_reward    = Column(Integer, default=10)
    order        = Column(Integer, default=0)

    course   = relationship("Course", back_populates="lessons")
    progress = relationship("UserProgress", back_populates="lesson")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id   = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lesson_id   = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed   = Column(Boolean, default=False)
    last_code   = Column(Text)            # Последний код пользователя
    attempts    = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)

    user   = relationship("User", back_populates="progress")
    course = relationship("Course", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
