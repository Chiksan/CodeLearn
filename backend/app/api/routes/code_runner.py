from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import subprocess, sys, json, tempfile, os

from app.db.database import get_db
from app.models.user import User, Lesson, UserProgress
from app.schemas.schemas import CodeSubmit, CodeResult
from app.core.security import get_current_user
from datetime import datetime

router = APIRouter()

TIMEOUT_SECONDS = 5
ALLOWED_LANGUAGES = {"python", "javascript"}


def run_python(code: str) -> tuple[str, str]:
    """Запускаем Python-код в отдельном процессе с таймаутом."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        fname = f.name
    try:
        result = subprocess.run(
            [sys.executable, fname],
            capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS,
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "Превышено время выполнения (5 сек)"
    finally:
        os.unlink(fname)


def run_javascript(code: str) -> tuple[str, str]:
    """Запускаем JS через Node.js."""
    with tempfile.NamedTemporaryFile(suffix=".js", mode="w", delete=False) as f:
        f.write(code)
        fname = f.name
    try:
        result = subprocess.run(
            ["node", fname],
            capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS,
        )
        return result.stdout, result.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "", "Node.js не найден или превышен таймаут"
    finally:
        os.unlink(fname)


def check_tests(code: str, tests_json: str, language: str) -> tuple[int, int, str]:
    """Запускаем тесты из JSON и считаем пройденные."""
    if not tests_json:
        return 0, 0, ""

    try:
        tests = json.loads(tests_json)
    except json.JSONDecodeError:
        return 0, 0, "Ошибка в конфигурации тестов"

    passed = 0
    output_lines = []

    for i, test in enumerate(tests):
        test_code = code + "\n" + test.get("check", "")
        if language == "python":
            out, err = run_python(test_code)
        else:
            out, err = run_javascript(test_code)

        expected = test.get("expected", "").strip()
        lines = [l for l in out.strip().splitlines() if l.strip()]
        actual = lines[-1] if lines else ""

        if not err and actual == expected:
            passed += 1
            output_lines.append(f"✓ Тест {i+1}: пройден")
        else:
            output_lines.append(f"✗ Тест {i+1}: ожидалось «{expected}», получено «{actual or err}»")

    return passed, len(tests), "\n".join(output_lines)


@router.post("/run", response_model=CodeResult)
async def run_code(
    data: CodeSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Получаем урок
    result = await db.execute(select(Lesson).where(Lesson.id == data.lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")

    # Запускаем код
    if data.language == "python":
        output, error = run_python(data.code)
    elif data.language == "javascript":
        output, error = run_javascript(data.code)
    elif data.language == "html":
        output, error = "", ""  # HTML не выполняется, тесты не нужны
    else:
        raise HTTPException(status_code=400, detail="Язык не поддерживается")

    if error:
        return CodeResult(success=False, output="", error=error)

    # Прогоняем тесты
    passed, total, test_output = check_tests(data.code, lesson.tests, data.language.value)
    success = (total == 0) or (passed == total)

    # Обновляем прогресс пользователя
    prog_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == current_user.id,
            UserProgress.lesson_id == lesson.id,
        )
    )
    progress = prog_result.scalar_one_or_none()

    xp_earned = 0
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            course_id=lesson.course_id,
            lesson_id=lesson.id,
        )
        db.add(progress)

    progress.last_code = data.code
    progress.attempts = (progress.attempts or 0) + 1

    if success and not progress.completed:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        xp_earned = lesson.xp_reward
        current_user.xp += xp_earned

    combined_output = output
    if test_output:
        combined_output = (output + "\n\n" + test_output).strip()

    return CodeResult(
        success=success,
        output=combined_output,
        error=None,
        passed_tests=passed,
        total_tests=total,
        xp_earned=xp_earned,
    )
