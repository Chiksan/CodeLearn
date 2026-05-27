from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.db.database import get_db
from app.models.user import Lesson, Course, User
from app.schemas.schemas import LessonCreate, LessonOut
from app.core.security import get_current_user

router = APIRouter()


def lesson_with_language(lesson: Lesson) -> dict:
    return {
        "id": lesson.id,
        "course_id": lesson.course_id,
        "title": lesson.title,
        "content": lesson.content,
        "starter_code": lesson.starter_code,
        "hints": lesson.hints,
        "xp_reward": lesson.xp_reward,
        "order": lesson.order,
        "language": lesson.course.language if lesson.course else None,
    }


@router.get("/course/{course_id}", response_model=List[LessonOut])
async def get_lessons(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson)
        .options(selectinload(Lesson.course))
        .where(Lesson.course_id == course_id)
        .order_by(Lesson.order)
    )
    lessons = result.scalars().all()
    return [lesson_with_language(l) for l in lessons]


@router.get("/{lesson_id}", response_model=LessonOut)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson)
        .options(selectinload(Lesson.course))
        .where(Lesson.id == lesson_id)
    )
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    return lesson_with_language(lesson)


@router.post("/course/{course_id}", response_model=LessonOut, status_code=201)
async def create_lesson(
    course_id: int,
    data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только для администраторов")
    lesson = Lesson(course_id=course_id, **data.model_dump())
    db.add(lesson)
    await db.flush()
    await db.refresh(lesson)
    return lesson_with_language(lesson)
