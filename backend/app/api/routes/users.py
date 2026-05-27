from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.user import User

router = APIRouter()


@router.get("/leaderboard")
async def leaderboard(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User.id, User.username, User.xp, User.created_at)
        .where(User.is_active == True)
        .order_by(User.xp.desc())
        .limit(20)
    )
    users = result.all()
    return [
        {
            "rank": i + 1,
            "id": u.id,
            "username": u.username,
            "xp": u.xp,
            "joined": u.created_at.strftime("%b %Y") if u.created_at else None,
        }
        for i, u in enumerate(users)
    ]
