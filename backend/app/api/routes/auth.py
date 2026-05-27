import secrets
import random
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User
from app.schemas.schemas import UserRegister, Token, UserOut
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.email import send_verification_email
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


class VerifyCodeRequest(BaseModel):
    email: str
    code: str


@router.post("/register", status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email уже используется")

    result2 = await db.execute(select(User).where(User.username == data.username))
    if result2.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

    code = str(random.randint(100000, 999999))

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
        is_verified=False,
        verify_token=code,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    send_verification_email(data.email, data.username, code)

    return {"message": "Код подтверждения отправлен на вашу почту"}


@router.post("/verify-code")
async def verify_code(data: VerifyCodeRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or user.verify_token != data.code:
        raise HTTPException(status_code=400, detail="Неверный код подтверждения")

    user.is_verified = True
    user.verify_token = None
    await db.commit()

    return {"message": "Email подтверждён! Теперь можешь войти."}


@router.get("/verify")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.verify_token == token))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Неверная или устаревшая ссылка")

    user.is_verified = True
    user.verify_token = None
    await db.commit()

    return {"message": "Email успешно подтверждён! Теперь можешь войти."}


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == form.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Сначала подтверди email. Проверь почту.")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
