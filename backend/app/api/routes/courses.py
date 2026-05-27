from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.database import get_db
from app.models.user import Course, Lesson, User
from app.schemas.schemas import CourseCreate, CourseOut
from app.core.security import get_current_user

router = APIRouter()


def course_with_count(course: Course, count: int) -> dict:
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "language": course.language,
        "level": course.level,
        "is_published": course.is_published,
        "lesson_count": count,
    }


@router.get("/", response_model=List[CourseOut])
async def get_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course, func.count(Lesson.id).label("cnt"))
        .outerjoin(Lesson, Lesson.course_id == Course.id)
        .where(Course.is_published == True)
        .group_by(Course.id)
    )
    rows = result.all()
    return [course_with_count(course, cnt) for course, cnt in rows]


@router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course, func.count(Lesson.id).label("cnt"))
        .outerjoin(Lesson, Lesson.course_id == Course.id)
        .where(Course.id == course_id)
        .group_by(Course.id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Курс не найден")
    course, cnt = row
    return course_with_count(course, cnt)


@router.post("/", response_model=CourseOut, status_code=201)
async def create_course(
    data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только для администраторов")
    course = Course(**data.model_dump())
    db.add(course)
    await db.flush()
    await db.refresh(course)
    return course
