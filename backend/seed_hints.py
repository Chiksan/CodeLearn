"""
Добавляет подсказки к существующим урокам.
Запуск: docker exec codelearn-backend-1 python seed_hints.py
"""
import asyncio, json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update
from app.core.config import settings
from app.models.user import Lesson, Course

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

# title → hints  (ищем по названию урока)
HINTS = {
    # Python
    "Знакомство с Python": [
        "Используй функцию print() для вывода текста на экран.",
        "Текст нужно заключать в кавычки: print(\"Привет!\")",
    ],
    "Переменные и типы данных": [
        "Имя переменной пишется слева от знака =, например: name = \"Иван\"",
        "Строки нужно брать в кавычки, а числа — нет: age = 25",
    ],
    "Строки и операции с ними": [
        "f-строка начинается с буквы f перед кавычками: f\"{first_name} {last_name}\"",
        "Переменная вставляется внутри фигурных скобок {}: f\"Привет, {name}!\"",
    ],
    "Условия: if / elif / else": [
        "После if нужно ставить двоеточие: if x > 0:",
        "Блок кода внутри if должен иметь отступ в 4 пробела.",
        "else тоже с двоеточием: else:",
    ],
    "Цикл for": [
        "range(1, 6) генерирует числа 1, 2, 3, 4, 5 — правая граница не включается.",
        "Используй print(i) внутри цикла чтобы вывести каждое число.",
    ],
    "Функции": [
        "Функция создаётся с помощью ключевого слова def: def square(n):",
        "return возвращает результат: return n * n",
        "Вызов функции: print(square(5))",
    ],
    "Списки": [
        "Метод sort() сортирует список на месте: numbers.sort()",
        "После сортировки выведи список: print(numbers)",
    ],
    "Словари": [
        "Словарь создаётся фигурными скобками: student = {\"name\": \"Иван\"}",
        "Доступ к значению по ключу: student[\"name\"]",
    ],
    # JavaScript
    "Введение в JavaScript": [
        "Используй console.log() для вывода в консоль.",
        "Текст нужно заключать в кавычки: console.log(\"Привет!\")",
    ],
    "Переменные: let, const, var": [
        "Используй let для переменных которые можно менять: let city = \"Алматы\"",
        "Шаблонная строка начинается с обратного апострофа ` и позволяет вставлять переменные через ${}",
    ],
    "Условия в JavaScript": [
        "В JS условие пишется в круглых скобках: if (num % 2 === 0)",
        "Оператор % даёт остаток от деления: 8 % 2 равно 0, значит число чётное.",
    ],
    "Функции в JavaScript": [
        "Стрелочная функция без фигурных скобок сразу возвращает результат: (a, b) => a * b",
        "Вызов функции: console.log(multiply(3, 4))",
    ],
    "Массивы": [
        "map() создаёт новый массив, применяя функцию к каждому элементу.",
        "Умножь каждый элемент на 3: nums.map(n => n * 3)",
    ],
    # HTML/CSS
    "Структура HTML-страницы": [
        "Тег h1 создаёт заголовок первого уровня.",
        "Синтаксис тега: <h1>текст заголовка</h1>",
    ],
    "Основные теги HTML": [
        "Маркированный список создаётся тегом <ul>, а каждый пункт — тегом <li>.",
        "Пример: <ul><li>Яблоко</li><li>Банан</li></ul>",
        "Нужно 3 элемента <li> внутри <ul>.",
    ],
    "Введение в CSS": [
        "Селектор h1 выбирает все заголовки первого уровня.",
        "Свойство color задаёт цвет текста: color: red;",
        "CSS пишется внутри тега <style>: <style> h1 { color: red; } </style>",
    ],
}


async def seed_hints():
    async with Session() as db:
        result = await db.execute(select(Lesson))
        lessons = result.scalars().all()

        updated = 0
        for lesson in lessons:
            hints_list = HINTS.get(lesson.title)
            if hints_list:
                lesson.hints = json.dumps(hints_list, ensure_ascii=False)
                updated += 1
                print(f"  ✓ {lesson.title}")

        await db.commit()
        print(f"\n✅ Подсказки добавлены к {updated} урокам.")


if __name__ == "__main__":
    asyncio.run(seed_hints())
