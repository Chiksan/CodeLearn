from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.models.user import User, UserProgress
from app.schemas.schemas import ProgressOut
from app.core.security import get_current_user

router = APIRouter()


@router.get("/me", response_model=List[ProgressOut])
async def my_progress(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/me/course/{course_id}", response_model=List[ProgressOut])
async def my_course_progress(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == current_user.id,
            UserProgress.course_id == course_id,
        )
    )
    return result.scalars().all()
