"""
Скрипт заполнения БД курсами и уроками.
Запуск: docker exec codelearn-backend-1 python seed.py
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.db.database import Base
from app.models.user import Course, Lesson, LanguageEnum, LevelEnum

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

# ─────────────────────────────────────────────────────────────
# КУРС 1 — Python с нуля
# ─────────────────────────────────────────────────────────────
PYTHON_LESSONS = [
  {
    "title": "Знакомство с Python",
    "order": 1, "xp_reward": 10,
    "content": """## Что такое Python?

Python — один из самых популярных языков программирования в мире. Он используется в:
- **Анализе данных** и машинном обучении
- **Веб-разработке** (Django, FastAPI)
- **Автоматизации** рутинных задач
- **Науке** и исследованиях

## Твоя первая программа

Самая простая команда — `print()`. Она выводит текст на экран:

```python
print("Привет, мир!")
```

Запусти этот код — и увидишь результат справа.

## Комментарии

Комментарии — строки, которые Python игнорирует. Они помогают объяснить код:

```python
# Это комментарий
print("Код без комментария")
```
""",
    "starter_code": '# Выведи приветствие\nprint("Привет, мир!")',
    "solution": 'print("Привет, мир!")',
    "tests": '[{"check": "\\nprint(\'OK\' if True else \'FAIL\')", "expected": "OK"}]',
  },
  {
    "title": "Переменные и типы данных",
    "order": 2, "xp_reward": 15,
    "content": """## Переменные

Переменная — это контейнер для хранения данных. Создать переменную просто:

```python
name = "Алекс"
age = 25
height = 1.78
```

## Основные типы данных

| Тип | Пример | Описание |
|-----|--------|----------|
| `str` | `"Привет"` | Строка (текст) |
| `int` | `42` | Целое число |
| `float` | `3.14` | Дробное число |
| `bool` | `True` | Логическое значение |

## Узнать тип переменной

```python
x = 42
print(type(x))  # <class 'int'>
```

## Задание

Создай переменную `name` со своим именем и выведи её.
""",
    "starter_code": "# Создай переменную name и выведи её\nname = \"Твоё имя\"\nprint(name)",
    "solution": 'name = "Алекс"\nprint(name)',
    "tests": '[{"check": "\\nprint(\'OK\' if isinstance(name, str) else \'FAIL\')", "expected": "OK"}]',
  },
  {
    "title": "Строки и операции с ними",
    "order": 3, "xp_reward": 15,
    "content": """## Строки в Python

Строка — последовательность символов в кавычках:

```python
greeting = "Привет"
name = 'Алекс'
```

## Конкатенация (склейка)

```python
full = "Привет, " + "мир!"
print(full)  # Привет, мир!
```

## f-строки (форматирование)

Самый удобный способ вставить переменную в строку:

```python
name = "Алекс"
age = 25
print(f"Меня зовут {name}, мне {age} лет")
```

## Полезные методы строк

```python
s = "  hello world  "
print(s.upper())    # HELLO WORLD
print(s.strip())    # hello world
print(s.replace("hello", "bye"))  # bye world
print(len("Python"))  # 6
```

## Задание

Создай переменные `first_name` и `last_name`, выведи полное имя через f-строку.
""",
    "starter_code": 'first_name = "Иван"\nlast_name = "Иванов"\n# Выведи полное имя через f-строку\nprint(f"{first_name} {last_name}")',
    "solution": 'first_name = "Иван"\nlast_name = "Иванов"\nprint(f"{first_name} {last_name}")',
    "tests": '[{"check": "\\nprint(\'OK\' if first_name and last_name else \'FAIL\')", "expected": "OK"}]',
  },
  {
    "title": "Условия: if / elif / else",
    "order": 4, "xp_reward": 20,
    "content": """## Условия

Условие позволяет выполнять разный код в зависимости от ситуации:

```python
age = 18

if age >= 18:
    print("Совершеннолетний")
else:
    print("Несовершеннолетний")
```

## Несколько условий: elif

```python
score = 75

if score >= 90:
    print("Отлично")
elif score >= 70:
    print("Хорошо")
elif score >= 50:
    print("Удовлетворительно")
else:
    print("Неудовлетворительно")
```

## Операторы сравнения

| Оператор | Значение |
|----------|----------|
| `==` | равно |
| `!=` | не равно |
| `>` | больше |
| `<` | меньше |
| `>=` | больше или равно |
| `<=` | меньше или равно |

## Задание

Напиши программу: если число `x` больше 0 — выведи `"положительное"`, иначе — `"отрицательное или ноль"`.
""",
    "starter_code": "x = 5\n# Напиши условие\nif x > 0:\n    print(\"положительное\")\nelse:\n    print(\"отрицательное или ноль\")",
    "solution": "x = 5\nif x > 0:\n    print(\"положительное\")\nelse:\n    print(\"отрицательное или ноль\")",
    "tests": '[{"check": "\\nx = 5\\nresult = \'положительное\' if x > 0 else \'отрицательное или ноль\'\\nprint(\'OK\' if result == \'положительное\' else \'FAIL\')", "expected": "OK"}]',
  },
  {
    "title": "Цикл for",
    "order": 5, "xp_reward": 20,
    "content": """## Цикл for

Цикл `for` позволяет повторять действие несколько раз:

```python
for i in range(5):
    print(i)
# 0 1 2 3 4
```

## range()

`range(n)` генерирует числа от 0 до n-1:

```python
range(5)      # 0, 1, 2, 3, 4
range(2, 6)   # 2, 3, 4, 5
range(0, 10, 2)  # 0, 2, 4, 6, 8
```

## Перебор списка

```python
fruits = ["яблоко", "банан", "вишня"]
for fruit in fruits:
    print(fruit)
```

## Задание

Выведи числа от 1 до 5 с помощью цикла `for`.
""",
    "starter_code": "# Выведи числа от 1 до 5\nfor i in range(1, 6):\n    print(i)",
    "solution": "for i in range(1, 6):\n    print(i)",
    "tests": '[{"check": "\\noutput = []\\nfor i in range(1, 6): output.append(str(i))\\nprint(\'OK\')", "expected": "OK"}]',
  },
  {
    "title": "Функции",
    "order": 6, "xp_reward": 25,
    "content": """## Что такое функция?

Функция — это блок кода, который можно вызывать многократно:

```python
def greet(name):
    print(f"Привет, {name}!")

greet("Алекс")   # Привет, Алекс!
greet("Мария")   # Привет, Мария!
```

## Функция с возвращаемым значением

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)  # 7
```

## Параметры по умолчанию

```python
def greet(name, greeting="Привет"):
    print(f"{greeting}, {name}!")

greet("Алекс")             # Привет, Алекс!
greet("Мария", "Здравствуй")  # Здравствуй, Мария!
```

## Задание

Напиши функцию `square(n)`, которая возвращает квадрат числа, и выведи `square(5)`.
""",
    "starter_code": "def square(n):\n    return n * n\n\nprint(square(5))",
    "solution": "def square(n):\n    return n * n\nprint(square(5))",
    "tests": '[{"check": "\\nprint(\'OK\' if square(5) == 25 else \'FAIL\')", "expected": "OK"}]',
  },
  {
    "title": "Списки",
    "order": 7, "xp_reward": 25,
    "content": """## Списки в Python

Список хранит несколько значений в одной переменной:

```python
numbers = [1, 2, 3, 4, 5]
fruits = ["яблоко", "банан", "вишня"]
mixed = [1, "строка", True, 3.14]
```

## Доступ по индексу

Индексы начинаются с 0:

```python
fruits = ["яблоко", "банан", "вишня"]
print(fruits[0])   # яблоко
print(fruits[-1])  # вишня (последний)
```

## Методы списков

```python
lst = [3, 1, 4, 1, 5]
lst.append(9)     # добавить в конец
lst.remove(1)     # удалить первое вхождение
lst.sort()        # сортировка
print(len(lst))   # длина списка
```

## Задание

Создай список `numbers = [3, 1, 4, 1, 5, 9]`, отсортируй его и выведи.
""",
    "starter_code": "numbers = [3, 1, 4, 1, 5, 9]\nnumbers.sort()\nprint(numbers)",
    "solution": "numbers = [3, 1, 4, 1, 5, 9]\nnumbers.sort()\nprint(numbers)",
    "tests": '[{"check": "\\nprint(\'OK\' if numbers == sorted(numbers) else \'FAIL\')", "expected": "OK"}]',
  },
  {
    "title": "Словари",
    "order": 8, "xp_reward": 30,
    "content": """## Словари

Словарь хранит пары **ключ: значение**:

```python
person = {
    "name": "Алекс",
    "age": 25,
    "city": "Москва"
}
```

## Доступ к значениям

```python
print(person["name"])       # Алекс
print(person.get("age"))    # 25
print(person.get("email", "нет"))  # нет (значение по умолчанию)
```

## Изменение и добавление

```python
person["age"] = 26          # изменить
person["email"] = "a@b.com" # добавить новый ключ
```

## Перебор словаря

```python
for key, value in person.items():
    print(f"{key}: {value}")
```

## Задание

Создай словарь `student` с ключами `name` и `grade`. Выведи значение по ключу `name`.
""",
    "starter_code": 'student = {"name": "Иван", "grade": 5}\nprint(student["name"])',
    "solution": 'student = {"name": "Иван", "grade": 5}\nprint(student["name"])',
    "tests": '[{"check": "\\nprint(\'OK\' if isinstance(student, dict) and \'name\' in student else \'FAIL\')", "expected": "OK"}]',
  },
]

# ─────────────────────────────────────────────────────────────
# КУРС 2 — JavaScript основы
# ─────────────────────────────────────────────────────────────
JS_LESSONS = [
  {
    "title": "Введение в JavaScript",
    "order": 1, "xp_reward": 10,
    "content": """## Что такое JavaScript?

JavaScript — язык программирования для веба. Он работает прямо в браузере и позволяет делать страницы интерактивными.

Сегодня JavaScript используется везде:
- **Фронтенд** — интерфейсы сайтов
- **Бэкенд** — Node.js серверы
- **Мобильные** приложения

## Вывод в консоль

```javascript
console.log("Привет, мир!");
console.log(42);
console.log(true);
```

## Комментарии

```javascript
// Однострочный комментарий

/* Многострочный
   комментарий */
```

## Задание

Выведи `"Привет, JavaScript!"` в консоль.
""",
    "starter_code": '// Выведи приветствие\nconsole.log("Привет, JavaScript!");',
    "solution": 'console.log("Привет, JavaScript!");',
    "tests": "[]",
  },
  {
    "title": "Переменные: let, const, var",
    "order": 2, "xp_reward": 15,
    "content": """## Объявление переменных

В современном JS используют `let` и `const`:

```javascript
let name = "Алекс";     // можно изменить
const age = 25;          // нельзя изменить
```

**`var`** — старый способ, лучше не использовать.

## Типы данных

```javascript
let str    = "Строка";
let num    = 42;
let float  = 3.14;
let bool   = true;
let empty  = null;
let undef  = undefined;
```

## Шаблонные строки

```javascript
let name = "Алекс";
let age = 25;
console.log(`Меня зовут ${name}, мне ${age} лет`);
```

## Задание

Создай переменную `city` со своим городом и выведи её через шаблонную строку.
""",
    "starter_code": 'let city = "Алматы";\nconsole.log(`Я живу в городе ${city}`);',
    "solution": 'let city = "Алматы";\nconsole.log(`Я живу в городе ${city}`);',
    "tests": "[]",
  },
  {
    "title": "Условия в JavaScript",
    "order": 3, "xp_reward": 20,
    "content": """## if / else

```javascript
let age = 18;

if (age >= 18) {
  console.log("Совершеннолетний");
} else {
  console.log("Несовершеннолетний");
}
```

## else if

```javascript
let score = 75;

if (score >= 90) {
  console.log("Отлично");
} else if (score >= 70) {
  console.log("Хорошо");
} else {
  console.log("Нужно подтянуть");
}
```

## Тернарный оператор

Краткая запись if/else:

```javascript
let age = 20;
let status = age >= 18 ? "взрослый" : "ребёнок";
console.log(status);  // взрослый
```

## Задание

Выведи `"чётное"` если число 8 чётное, иначе `"нечётное"`.
""",
    "starter_code": "let num = 8;\nif (num % 2 === 0) {\n  console.log(\"чётное\");\n} else {\n  console.log(\"нечётное\");\n}",
    "solution": "let num = 8;\nif (num % 2 === 0) {\n  console.log(\"чётное\");\n} else {\n  console.log(\"нечётное\");\n}",
    "tests": "[]",
  },
  {
    "title": "Функции в JavaScript",
    "order": 4, "xp_reward": 25,
    "content": """## Объявление функции

```javascript
function greet(name) {
  return `Привет, ${name}!`;
}

console.log(greet("Алекс"));  // Привет, Алекс!
```

## Стрелочные функции

Более короткий синтаксис:

```javascript
const add = (a, b) => a + b;
console.log(add(3, 4));  // 7

const square = n => n * n;
console.log(square(5));  // 25
```

## Функции с несколькими строками

```javascript
const greet = (name) => {
  const message = `Привет, ${name}!`;
  return message;
};
```

## Задание

Напиши стрелочную функцию `multiply(a, b)` которая возвращает произведение двух чисел. Выведи `multiply(3, 4)`.
""",
    "starter_code": "const multiply = (a, b) => a * b;\nconsole.log(multiply(3, 4));",
    "solution": "const multiply = (a, b) => a * b;\nconsole.log(multiply(3, 4));",
    "tests": "[]",
  },
  {
    "title": "Массивы",
    "order": 5, "xp_reward": 25,
    "content": """## Массивы в JavaScript

```javascript
let fruits = ["яблоко", "банан", "вишня"];
let numbers = [1, 2, 3, 4, 5];
```

## Доступ и изменение

```javascript
console.log(fruits[0]);     // яблоко
fruits[1] = "манго";        // изменить
console.log(fruits.length); // 3
```

## Методы массивов

```javascript
fruits.push("груша");       // добавить в конец
fruits.pop();               // удалить последний
fruits.unshift("арбуз");    // добавить в начало

// Перебор
fruits.forEach(f => console.log(f));

// Трансформация
let doubled = numbers.map(n => n * 2);
// [2, 4, 6, 8, 10]

// Фильтрация
let evens = numbers.filter(n => n % 2 === 0);
// [2, 4]
```

## Задание

Создай массив `nums = [1, 2, 3, 4, 5]`, выведи массив где каждый элемент умножен на 3.
""",
    "starter_code": "const nums = [1, 2, 3, 4, 5];\nconst tripled = nums.map(n => n * 3);\nconsole.log(tripled);",
    "solution": "const nums = [1, 2, 3, 4, 5];\nconst tripled = nums.map(n => n * 3);\nconsole.log(tripled);",
    "tests": "[]",
  },
]

# ─────────────────────────────────────────────────────────────
# КУРС 3 — HTML/CSS основы
# ─────────────────────────────────────────────────────────────
HTML_LESSONS = [
  {
    "title": "Структура HTML-страницы",
    "order": 1, "xp_reward": 10,
    "content": """## Что такое HTML?

HTML (HyperText Markup Language) — язык разметки для создания веб-страниц. Каждый сайт в интернете написан с использованием HTML.

## Базовая структура

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Моя страница</title>
  </head>
  <body>
    <h1>Привет, мир!</h1>
    <p>Это мой первый сайт.</p>
  </body>
</html>
```

- `<!DOCTYPE html>` — говорит браузеру что это HTML5
- `<head>` — невидимая часть (мета-информация)
- `<body>` — всё что видит пользователь
- `<title>` — название вкладки

## Задание

Напиши заголовок `<h1>` с текстом `"Мой первый сайт"`.
""",
    "starter_code": "<!-- Напиши заголовок h1 -->\n<h1>Мой первый сайт</h1>",
    "solution": "<h1>Мой первый сайт</h1>",
    "tests": "[]",
  },
  {
    "title": "Основные теги HTML",
    "order": 2, "xp_reward": 15,
    "content": """## Заголовки

```html
<h1>Самый большой</h1>
<h2>Поменьше</h2>
<h3>Ещё меньше</h3>
```

## Текст

```html
<p>Обычный абзац текста.</p>
<strong>Жирный текст</strong>
<em>Курсив</em>
<br>  <!-- перенос строки -->
```

## Ссылки и изображения

```html
<a href="https://google.com">Перейти на Google</a>
<img src="photo.jpg" alt="Описание фото">
```

## Списки

```html
<!-- Маркированный -->
<ul>
  <li>Яблоко</li>
  <li>Банан</li>
</ul>

<!-- Нумерованный -->
<ol>
  <li>Первый</li>
  <li>Второй</li>
</ol>
```

## Задание

Создай маркированный список из 3 любимых фруктов.
""",
    "starter_code": "<!-- Создай список из 3 фруктов -->\n<ul>\n  <li>Яблоко</li>\n  <li>Банан</li>\n  <li>Вишня</li>\n</ul>",
    "solution": "<ul>\n  <li>Яблоко</li>\n  <li>Банан</li>\n  <li>Вишня</li>\n</ul>",
    "tests": "[]",
  },
  {
    "title": "Введение в CSS",
    "order": 3, "xp_reward": 20,
    "content": """## Что такое CSS?

CSS (Cascading Style Sheets) — язык стилей. Он говорит браузеру как отображать HTML-элементы.

## Синтаксис

```css
selector {
  property: value;
}
```

## Подключение к HTML

```html
<style>
  h1 {
    color: blue;
    font-size: 24px;
  }
</style>
```

## Основные свойства

```css
/* Цвет и фон */
color: red;
background-color: #f0f0f0;

/* Шрифт */
font-size: 16px;
font-weight: bold;
font-family: Arial, sans-serif;

/* Отступы */
margin: 10px;      /* снаружи */
padding: 10px;     /* внутри */

/* Размеры */
width: 200px;
height: 100px;
```

## Задание

Напиши CSS чтобы заголовок `h1` был красного цвета.
""",
    "starter_code": "<!-- HTML -->\n<h1>Красный заголовок</h1>\n\n<!-- CSS (внутри <style>) -->\n<style>\n  h1 {\n    color: red;\n  }\n</style>",
    "solution": "<h1>Заголовок</h1>\n<style>\n  h1 { color: red; }\n</style>",
    "tests": "[]",
  },
]

COURSES_DATA = [
  {
    "title": "Python с нуля",
    "description": "Изучи Python с нуля до уверенного уровня. Переменные, условия, циклы, функции, списки и словари — всё на практике.",
    "language": LanguageEnum.python,
    "level": LevelEnum.beginner,
    "lessons": PYTHON_LESSONS,
  },
  {
    "title": "JavaScript основы",
    "description": "Освой базовый JavaScript: переменные, функции, массивы и DOM. Старт для веб-разработки.",
    "language": LanguageEnum.javascript,
    "level": LevelEnum.beginner,
    "lessons": JS_LESSONS,
  },
  {
    "title": "HTML/CSS для начинающих",
    "description": "Создай свою первую веб-страницу. Научись писать разметку HTML и оформлять её стилями CSS.",
    "language": LanguageEnum.html,
    "level": LevelEnum.beginner,
    "lessons": HTML_LESSONS,
  },
]


async def seed():
  async with Session() as db:
    for course_data in COURSES_DATA:
      lessons_data = course_data.pop("lessons")

      course = Course(
        **course_data,
        is_published=True,
      )
      db.add(course)
      await db.flush()

      for lesson_data in lessons_data:
        lesson = Lesson(course_id=course.id, **lesson_data)
        db.add(lesson)

      print(f"✓ Курс добавлен: {course.title} ({len(lessons_data)} уроков)")

    await db.commit()
    print("\n✅ База данных успешно заполнена!")


if __name__ == "__main__":
  asyncio.run(seed())
