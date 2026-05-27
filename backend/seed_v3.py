"""
Добавляет новые уроки в существующие курсы.
Запуск: docker exec codelearn-backend-1 python seed_v3.py
"""
import asyncio, json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.user import Course, Lesson

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)


# ─────────────────────────────────────────────────────────────
# Новые уроки для "Python с нуля" (добавляем к order 8)
# ─────────────────────────────────────────────────────────────
PYTHON_NEW = [
  {
    "title": "Работа с файлами",
    "order": 9, "xp_reward": 20,
    "hints": json.dumps([
      "open('file.txt', 'r') — открыть для чтения, 'w' — для записи",
      "with open(...) as f — файл закроется автоматически",
      "f.read() читает весь файл, f.readlines() — список строк",
    ], ensure_ascii=False),
    "content": """## Чтение и запись файлов

Python умеет работать с файлами через функцию `open()`.

```python
# Запись в файл
with open('notes.txt', 'w', encoding='utf-8') as f:
    f.write('Первая строка\\n')
    f.write('Вторая строка\\n')

# Чтение файла
with open('notes.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# Чтение построчно
with open('notes.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())
```

## Режимы открытия

| Режим | Описание |
|-------|----------|
| `'r'` | Чтение (по умолчанию) |
| `'w'` | Запись (перезаписывает) |
| `'a'` | Добавление в конец |
| `'rb'` | Чтение бинарного файла |

## Задание

Запиши в файл `data.txt` три строки: `"Python"`, `"is"`, `"awesome"` (каждую на новой строке). Затем прочитай файл и выведи количество строк.
""",
    "starter_code": "# Запись\nwith open('data.txt', 'w', encoding='utf-8') as f:\n    f.write('Python\\n')\n    f.write('is\\n')\n    f.write('awesome\\n')\n\n# Чтение\nwith open('data.txt', 'r', encoding='utf-8') as f:\n    lines = f.readlines()\n\nprint(len(lines))",
    "solution": "with open('data.txt', 'w', encoding='utf-8') as f:\n    f.write('Python\\n')\n    f.write('is\\n')\n    f.write('awesome\\n')\nwith open('data.txt', 'r', encoding='utf-8') as f:\n    lines = f.readlines()\nprint(len(lines))",
    "tests": json.dumps([
      {"check": "\nwith open('data.txt','r',encoding='utf-8') as f:\n    lines=f.readlines()\nprint('OK' if len(lines)==3 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Исключения: try / except",
    "order": 10, "xp_reward": 20,
    "hints": json.dumps([
      "try: — блок который может вызвать ошибку",
      "except ValueError: — перехватываем конкретный тип ошибки",
      "finally: — выполняется всегда, даже если была ошибка",
    ], ensure_ascii=False),
    "content": """## Обработка ошибок

Когда в программе возникает ошибка — Python бросает **исключение**. Его можно поймать и обработать.

```python
try:
    x = int(input("Введи число: "))
    result = 10 / x
    print(f"10 / {x} = {result}")
except ValueError:
    print("Ошибка: введи число, а не текст!")
except ZeroDivisionError:
    print("Ошибка: на ноль делить нельзя!")
finally:
    print("Программа завершена")
```

## Несколько исключений

```python
try:
    data = [1, 2, 3]
    print(data[10])      # IndexError
except (IndexError, KeyError) as e:
    print(f"Ошибка доступа: {e}")
except Exception as e:   # ловит всё остальное
    print(f"Неизвестная ошибка: {e}")
```

## Собственные исключения

```python
class AgeError(Exception):
    pass

def set_age(age):
    if age < 0:
        raise AgeError("Возраст не может быть отрицательным")
    return age

try:
    set_age(-5)
except AgeError as e:
    print(e)
```

## Задание

Напиши функцию `safe_divide(a, b)` которая делит a на b. Если b == 0 — возвращает `"Деление на ноль"`. Если переданы не числа — возвращает `"Неверный тип"`. Проверь оба случая.
""",
    "starter_code": "def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return \"Деление на ноль\"\n    except TypeError:\n        return \"Неверный тип\"\n\nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))\nprint(safe_divide(10, \"x\"))",
    "solution": "def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return 'Деление на ноль'\n    except TypeError:\n        return 'Неверный тип'\nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))\nprint(safe_divide(10, 'x'))",
    "tests": json.dumps([
      {"check": "\nprint('OK' if safe_divide(10, 2) == 5.0 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if safe_divide(10, 0) == 'Деление на ноль' else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if safe_divide(10, 'x') == 'Неверный тип' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Модули и пакеты",
    "order": 11, "xp_reward": 20,
    "hints": json.dumps([
      "import math — подключить стандартный модуль",
      "from math import sqrt — импортировать конкретную функцию",
      "import random — модуль для случайных чисел",
    ], ensure_ascii=False),
    "content": """## Модули

Модуль — файл с Python-кодом, который можно подключить через `import`.

```python
import math

print(math.pi)          # 3.14159...
print(math.sqrt(16))    # 4.0
print(math.ceil(4.2))   # 5
print(math.floor(4.8))  # 4
```

## Выборочный импорт

```python
from math import sqrt, pi
from random import randint, choice

print(sqrt(25))           # 5.0
print(randint(1, 10))     # случайное от 1 до 10
print(choice(['a','b','c']))  # случайный элемент
```

## Полезные стандартные модули

```python
import os
print(os.getcwd())        # текущая папка
print(os.listdir('.'))    # список файлов

import datetime
now = datetime.datetime.now()
print(now.year, now.month, now.day)

import json
data = {"name": "Алекс", "age": 25}
s = json.dumps(data)      # dict → строка JSON
d = json.loads(s)         # строка JSON → dict
```

## Задание

Используй модуль `random` и `math`. Сгенерируй список из 5 случайных чисел от 1 до 100. Найди среднее (сумма / количество) и округли до 2 знаков через `round()`. Выведи список и среднее.
""",
    "starter_code": "import random\nimport math\n\nnumbers = [random.randint(1, 100) for _ in range(5)]\naverage = round(sum(numbers) / len(numbers), 2)\n\nprint(numbers)\nprint(average)",
    "solution": "import random\nnumbers = [random.randint(1, 100) for _ in range(5)]\naverage = round(sum(numbers) / len(numbers), 2)\nprint(numbers)\nprint(average)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if len(numbers) == 5 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if all(1 <= n <= 100 for n in numbers) else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Lambda и функции высшего порядка",
    "order": 12, "xp_reward": 25,
    "hints": json.dumps([
      "lambda x: x * 2 — анонимная функция, умножающая на 2",
      "map(func, list) — применяет функцию к каждому элементу",
      "filter(func, list) — оставляет элементы где func возвращает True",
    ], ensure_ascii=False),
    "content": """## Lambda-функции

Lambda — короткая анонимная функция в одну строку:

```python
# Обычная функция
def square(x):
    return x ** 2

# Та же функция через lambda
square = lambda x: x ** 2
print(square(5))  # 25

# Lambda с двумя параметрами
add = lambda a, b: a + b
print(add(3, 4))  # 7
```

## map() и filter()

```python
numbers = [1, 2, 3, 4, 5, 6]

# map — трансформация
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8, 10, 12]

# filter — фильтрация
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6]
```

## sorted() с ключом

```python
people = [
    {"name": "Иван",  "age": 30},
    {"name": "Мария", "age": 25},
    {"name": "Алекс", "age": 35},
]

# Сортировка по возрасту
sorted_people = sorted(people, key=lambda p: p["age"])
for p in sorted_people:
    print(p["name"], p["age"])
```

## Задание

Дан список слов `words = ["banana", "apple", "cherry", "date", "elderberry"]`. Используй `filter` чтобы оставить слова длиннее 5 букв. Отсортируй результат по длине. Выведи.
""",
    "starter_code": "words = [\"banana\", \"apple\", \"cherry\", \"date\", \"elderberry\"]\n\nlong_words = list(filter(lambda w: len(w) > 5, words))\nlong_words.sort(key=lambda w: len(w))\n\nprint(long_words)",
    "solution": "words = ['banana', 'apple', 'cherry', 'date', 'elderberry']\nlong_words = list(filter(lambda w: len(w) > 5, words))\nlong_words.sort(key=lambda w: len(w))\nprint(long_words)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if 'date' not in long_words else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if 'apple' not in long_words else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if long_words == sorted(long_words, key=len) else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Генераторы и list comprehension",
    "order": 13, "xp_reward": 25,
    "hints": json.dumps([
      "List comprehension: [выражение for элемент in список]",
      "С условием: [x for x in list if x > 0]",
      "Dict comprehension: {k: v for k, v in items}",
    ], ensure_ascii=False),
    "content": """## List Comprehension

Компактный способ создать список:

```python
# Обычный способ
squares = []
for i in range(1, 6):
    squares.append(i ** 2)

# List comprehension — то же самое в одну строку
squares = [i ** 2 for i in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# С условием
evens = [x for x in range(20) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Вложенный
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(matrix)  # [[1,2,3],[2,4,6],[3,6,9]]
```

## Dict и Set Comprehension

```python
words = ["hello", "world", "python"]

# Dict comprehension
word_lengths = {w: len(w) for w in words}
print(word_lengths)  # {'hello': 5, 'world': 5, 'python': 6}

# Set comprehension (уникальные значения)
lengths = {len(w) for w in words}
print(lengths)  # {5, 6}
```

## Генераторы

```python
# Генератор не хранит все данные в памяти
gen = (x ** 2 for x in range(1000000))  # не занимает много памяти
print(next(gen))  # 0
print(next(gen))  # 1

# Функция-генератор
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(8)])  # [0,1,1,2,3,5,8,13]
```

## Задание

Дан список чисел от 1 до 20. Используй list comprehension чтобы создать список квадратов только нечётных чисел. Выведи результат.
""",
    "starter_code": "numbers = range(1, 21)\n\nodd_squares = [x ** 2 for x in numbers if x % 2 != 0]\n\nprint(odd_squares)",
    "solution": "numbers = range(1, 21)\nodd_squares = [x ** 2 for x in numbers if x % 2 != 0]\nprint(odd_squares)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if len(odd_squares) == 10 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if odd_squares[0] == 1 and odd_squares[-1] == 361 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
]


# ─────────────────────────────────────────────────────────────
# Новые уроки для "ООП в Python" (добавляем к order 8)
# ─────────────────────────────────────────────────────────────
OOP_NEW = [
  {
    "title": "Датаклассы",
    "order": 9, "xp_reward": 30,
    "hints": json.dumps([
      "from dataclasses import dataclass",
      "@dataclass автоматически генерирует __init__, __str__, __eq__",
      "field(default_factory=list) для изменяемых значений по умолчанию",
    ], ensure_ascii=False),
    "content": """## Датаклассы

`@dataclass` — декоратор который автоматически генерирует стандартные методы (`__init__`, `__repr__`, `__eq__`):

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    name: str
    age: int
    grades: List[int] = field(default_factory=list)

    def average(self) -> float:
        return sum(self.grades) / len(self.grades) if self.grades else 0

s = Student("Алекс", 20, [85, 90, 78])
print(s)           # Student(name='Алекс', age=20, grades=[85, 90, 78])
print(s.average()) # 84.33...
print(s.name)      # Алекс

# __eq__ работает автоматически
s2 = Student("Алекс", 20, [85, 90, 78])
print(s == s2)     # True
```

## Замороженные датаклассы

```python
@dataclass(frozen=True)  # неизменяемый
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 5  # FrozenInstanceError!
```

## Задание

Создай датакласс `Product` с полями `name: str`, `price: float`, `quantity: int = 0`. Добавь метод `total()` → price * quantity. Создай объект и выведи total().
""",
    "starter_code": "from dataclasses import dataclass\n\n@dataclass\nclass Product:\n    name: str\n    price: float\n    quantity: int = 0\n\n    def total(self) -> float:\n        return self.price * self.quantity\n\np = Product(name=\"Ноутбук\", price=50000.0, quantity=3)\nprint(p)\nprint(p.total())",
    "solution": "from dataclasses import dataclass\n@dataclass\nclass Product:\n    name: str\n    price: float\n    quantity: int = 0\n    def total(self):\n        return self.price * self.quantity\np = Product(name='Ноутбук', price=50000.0, quantity=3)\nprint(p)\nprint(p.total())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if p.total() == 150000.0 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if Product('x', 100, 0).total() == 0 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Паттерн Singleton",
    "order": 10, "xp_reward": 35,
    "hints": json.dumps([
      "Singleton гарантирует что класс создаётся только один раз",
      "Храни экземпляр в атрибуте класса: cls._instance",
      "__new__ вызывается до __init__ при создании объекта",
    ], ensure_ascii=False),
    "content": """## Паттерны проектирования

Паттерн — проверенное решение типичной задачи. Один из самых известных — **Singleton**.

## Singleton

Гарантирует что у класса есть только **один экземпляр**:

```python
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
        return cls._instance

    def connect(self, url):
        self.url = url
        self.connected = True
        print(f"Подключено к {url}")

db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 is db2)  # True — один и тот же объект!

db1.connect("postgresql://localhost/mydb")
print(db2.connected)  # True — потому что db1 == db2
```

## Паттерн Factory

Создаёт объекты нужного типа:

```python
class Animal:
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Гав!"

class Cat(Animal):
    def speak(self): return "Мяу!"

class AnimalFactory:
    @staticmethod
    def create(animal_type: str) -> Animal:
        animals = {"dog": Dog, "cat": Cat}
        cls = animals.get(animal_type)
        if not cls:
            raise ValueError(f"Неизвестный тип: {animal_type}")
        return cls()

dog = AnimalFactory.create("dog")
print(dog.speak())  # Гав!
```

## Задание

Реализуй Singleton класс `Config` с атрибутом `debug = False`. Создай два объекта Config, установи `debug = True` через первый. Проверь что второй тоже видит `debug = True`.
""",
    "starter_code": "class Config:\n    _instance = None\n\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n            cls._instance.debug = False\n        return cls._instance\n\nc1 = Config()\nc2 = Config()\n\nc1.debug = True\n\nprint(c1 is c2)    # True\nprint(c2.debug)    # True",
    "solution": "class Config:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n            cls._instance.debug = False\n        return cls._instance\nc1 = Config()\nc2 = Config()\nc1.debug = True\nprint(c1 is c2)\nprint(c2.debug)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if c1 is c2 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if c2.debug == True else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
]


# ─────────────────────────────────────────────────────────────
# Новые уроки для "PostgreSQL — базы данных" (добавляем к order 7)
# ─────────────────────────────────────────────────────────────
PG_NEW = [
  {
    "title": "Подзапросы",
    "order": 8, "xp_reward": 30,
    "hints": json.dumps([
      "Подзапрос — SELECT внутри другого SELECT",
      "WHERE id IN (SELECT ...) — подзапрос возвращает список",
      "SELECT (SELECT MAX(salary) FROM ...) — скалярный подзапрос",
    ], ensure_ascii=False),
    "content": """## Подзапросы (Subqueries)

Подзапрос — это SELECT внутри другого запроса:

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE employees (id INT, name TEXT, salary INT, dept TEXT)')
c.executemany('INSERT INTO employees VALUES (?,?,?,?)', [
    (1, 'Алекс',   80000, 'IT'),
    (2, 'Мария',   70000, 'HR'),
    (3, 'Дмитрий', 95000, 'IT'),
    (4, 'Анна',    65000, 'HR'),
    (5, 'Иван',    90000, 'IT'),
])

# Сотрудники с зарплатой выше средней
c.execute('''
    SELECT name, salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees)
    ORDER BY salary DESC
''')
print("Выше средней:")
for row in c.fetchall():
    print(row)

# IN с подзапросом
c.execute('''
    SELECT name FROM employees
    WHERE dept IN (
        SELECT dept FROM employees
        GROUP BY dept
        HAVING AVG(salary) > 75000
    )
''')
print("Из высокооплачиваемых отделов:")
for row in c.fetchall():
    print(row)
```

## Задание

Создай таблицу `products` (id, name, price, category). Добавь 5 товаров. Выведи товары дороже средней цены по их категории.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('CREATE TABLE products (id INT, name TEXT, price INT, category TEXT)')\nc.executemany('INSERT INTO products VALUES (?,?,?,?)', [\n    (1, 'MacBook',    150000, 'Ноутбуки'),\n    (2, 'Lenovo',      60000, 'Ноутбуки'),\n    (3, 'iPhone',      80000, 'Телефоны'),\n    (4, 'Samsung',     40000, 'Телефоны'),\n    (5, 'Dell',        90000, 'Ноутбуки'),\n])\n\nc.execute('''\n    SELECT name, price, category\n    FROM products p\n    WHERE price > (\n        SELECT AVG(price)\n        FROM products\n        WHERE category = p.category\n    )\n    ORDER BY category\n''')\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE products (id INT, name TEXT, price INT, category TEXT)')\nc.executemany('INSERT INTO products VALUES (?,?,?,?)',[(1,'MacBook',150000,'Ноутбуки'),(2,'Lenovo',60000,'Ноутбуки'),(3,'iPhone',80000,'Телефоны'),(4,'Samsung',40000,'Телефоны'),(5,'Dell',90000,'Ноутбуки')])\nc.execute('SELECT name, price, category FROM products p WHERE price > (SELECT AVG(price) FROM products WHERE category = p.category) ORDER BY category')\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute('SELECT COUNT(*) FROM products')\nprint('OK' if c.fetchone()[0] == 5 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "VIEW — представления",
    "order": 9, "xp_reward": 30,
    "hints": json.dumps([
      "CREATE VIEW name AS SELECT ... — создаёт представление",
      "VIEW — это сохранённый запрос, работает как таблица",
      "SELECT * FROM view_name — обращение к представлению",
    ], ensure_ascii=False),
    "content": """## Что такое VIEW?

VIEW (представление) — это сохранённый SELECT-запрос, к которому можно обращаться как к таблице.

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE orders (id INT, customer TEXT, product TEXT, amount INT, status TEXT)')
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?)', [
    (1, 'Алекс', 'Ноутбук', 50000, 'paid'),
    (2, 'Мария', 'Телефон', 30000, 'pending'),
    (3, 'Алекс', 'Мышь',     1500, 'paid'),
    (4, 'Иван',  'Клавиатура',3000,'cancelled'),
    (5, 'Мария', 'Планшет',  25000, 'paid'),
])

# Создаём VIEW — оплаченные заказы
c.execute('''
    CREATE VIEW paid_orders AS
    SELECT customer, product, amount
    FROM orders
    WHERE status = 'paid'
''')

# Используем VIEW как обычную таблицу
c.execute("SELECT * FROM paid_orders")
print("Оплаченные заказы:")
for row in c.fetchall():
    print(row)

# Агрегация через VIEW
c.execute("SELECT customer, SUM(amount) FROM paid_orders GROUP BY customer")
print("Итого по клиентам:")
for row in c.fetchall():
    print(row)
```

## Зачем нужны VIEW?

- Упрощают сложные запросы — пишешь один раз
- Контроль доступа — показываешь только нужные данные
- Переиспользование логики без дублирования

## Задание

Создай таблицу `employees` (id, name, salary, active). Добавь 4 сотрудника (2 активных, 2 нет). Создай VIEW `active_employees` для активных. Выведи через VIEW.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('CREATE TABLE employees (id INT, name TEXT, salary INT, active INT)')\nc.executemany('INSERT INTO employees VALUES (?,?,?,?)', [\n    (1, 'Алекс',   80000, 1),\n    (2, 'Мария',   70000, 1),\n    (3, 'Иван',    60000, 0),\n    (4, 'Анна',    75000, 0),\n])\n\nc.execute('''\n    CREATE VIEW active_employees AS\n    SELECT name, salary FROM employees WHERE active = 1\n''')\n\nc.execute('SELECT * FROM active_employees')\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE employees (id INT, name TEXT, salary INT, active INT)')\nc.executemany('INSERT INTO employees VALUES (?,?,?,?)',[(1,'Алекс',80000,1),(2,'Мария',70000,1),(3,'Иван',60000,0),(4,'Анна',75000,0)])\nc.execute('CREATE VIEW active_employees AS SELECT name, salary FROM employees WHERE active = 1')\nc.execute('SELECT * FROM active_employees')\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute('SELECT COUNT(*) FROM active_employees')\nprint('OK' if c.fetchone()[0] == 2 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
]


# ─────────────────────────────────────────────────────────────
# Новые уроки для "FastAPI — разработка API" (добавляем к order 8)
# ─────────────────────────────────────────────────────────────
FASTAPI_NEW = [
  {
    "title": "Валидация данных",
    "order": 9, "xp_reward": 30,
    "hints": json.dumps([
      "Field(gt=0) — значение должно быть больше 0",
      "Field(min_length=3) — минимальная длина строки",
      "@field_validator — кастомная валидация поля",
    ], ensure_ascii=False),
    "content": """## Валидация через Pydantic

Pydantic позволяет задать ограничения прямо в модели:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0, description="Цена должна быть > 0")
    quantity: int = Field(ge=0, default=0)  # >= 0
    discount: float = Field(ge=0, le=100, default=0)  # 0-100%

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Имя не может быть пустым')
        return v.strip().title()

# Корректные данные
p = Product(name="ноутбук dell", price=50000, quantity=5)
print(p.name)   # Ноутбук Dell (title case)
print(p.price)  # 50000

# Ошибка валидации
try:
    bad = Product(name="x", price=-100)
except Exception as e:
    print(e)
```

## Типы ограничений Field

| Параметр | Значение |
|----------|----------|
| `gt=0` | больше 0 |
| `ge=0` | больше или равно 0 |
| `lt=100` | меньше 100 |
| `le=100` | меньше или равно 100 |
| `min_length=3` | мин. длина строки |
| `max_length=50` | макс. длина строки |

## Задание

Создай модель `UserRegister` с полями: `username` (мин. 3 символа), `email: str`, `age: int` (от 18 до 120). Создай корректный объект и выведи его. Попробуй создать с age=10 и поймай ошибку.
""",
    "starter_code": "from pydantic import BaseModel, Field, ValidationError\n\nclass UserRegister(BaseModel):\n    username: str = Field(min_length=3)\n    email: str\n    age: int = Field(ge=18, le=120)\n\n# Корректный пользователь\nuser = UserRegister(username=\"alex\", email=\"alex@test.com\", age=25)\nprint(user)\n\n# Некорректный возраст\ntry:\n    bad = UserRegister(username=\"bob\", email=\"b@b.com\", age=10)\nexcept ValidationError as e:\n    print(\"Ошибка:\", e.error_count(), \"нарушение(й)\")",
    "solution": "from pydantic import BaseModel, Field, ValidationError\nclass UserRegister(BaseModel):\n    username: str = Field(min_length=3)\n    email: str\n    age: int = Field(ge=18, le=120)\nuser = UserRegister(username='alex', email='alex@test.com', age=25)\nprint(user)\ntry:\n    bad = UserRegister(username='bob', email='b@b.com', age=10)\nexcept ValidationError as e:\n    print('Ошибка:', e.error_count(), 'нарушение(й)')",
    "tests": json.dumps([
      {"check": "\nprint('OK' if user.username == 'alex' and user.age == 25 else 'FAIL')", "expected": "OK"},
      {"check": "\ntry:\n    UserRegister(username='bob', email='b@b.com', age=10)\n    print('FAIL')\nexcept ValidationError:\n    print('OK')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Обработка ошибок в API",
    "order": 10, "xp_reward": 30,
    "hints": json.dumps([
      "HTTPException(status_code=404, detail='Не найден') — стандартная ошибка",
      "status_code=422 — ошибка валидации (FastAPI делает автоматически)",
      "@app.exception_handler(404) — глобальный обработчик ошибок",
    ], ensure_ascii=False),
    "content": """## HTTP коды ответов

| Код | Значение |
|-----|----------|
| 200 | OK — успех |
| 201 | Created — создано |
| 400 | Bad Request — неверный запрос |
| 401 | Unauthorized — нет авторизации |
| 403 | Forbidden — нет доступа |
| 404 | Not Found — не найдено |
| 422 | Unprocessable Entity — ошибка валидации |
| 500 | Internal Server Error — ошибка сервера |

## HTTPException в FastAPI

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

db = {1: {"name": "Алекс"}, 2: {"name": "Мария"}}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь {user_id} не найден"
        )
    return db[user_id]
```

## Кастомные обработчики

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Не найдено", "path": str(request.url)}
    )
```

## Задание

Реализуй функцию `find_user(users_db, user_id)`. Если user_id есть в словаре — вернуть пользователя. Если нет — вернуть `{"error": "Not found", "id": user_id}`. Проверь оба случая.
""",
    "starter_code": "def find_user(users_db: dict, user_id: int) -> dict:\n    if user_id in users_db:\n        return users_db[user_id]\n    return {\"error\": \"Not found\", \"id\": user_id}\n\nusers = {\n    1: {\"id\": 1, \"name\": \"Алекс\"},\n    2: {\"id\": 2, \"name\": \"Мария\"},\n}\n\nprint(find_user(users, 1))\nprint(find_user(users, 99))",
    "solution": "def find_user(users_db, user_id):\n    if user_id in users_db:\n        return users_db[user_id]\n    return {'error': 'Not found', 'id': user_id}\nusers = {1: {'id':1,'name':'Алекс'}, 2: {'id':2,'name':'Мария'}}\nprint(find_user(users, 1))\nprint(find_user(users, 99))",
    "tests": json.dumps([
      {"check": "\nprint('OK' if find_user(users, 1)['name'] == 'Алекс' else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if find_user(users, 99)['error'] == 'Not found' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
]


# ─────────────────────────────────────────────────────────────
ADDITIONS = [
  ("Python с нуля",              PYTHON_NEW),
  ("ООП в Python",               OOP_NEW),
  ("PostgreSQL — базы данных",   PG_NEW),
  ("FastAPI — разработка API",   FASTAPI_NEW),
]


async def seed():
  async with Session() as db:
    for course_title, new_lessons in ADDITIONS:
      result = await db.execute(select(Course).where(Course.title == course_title))
      course = result.scalar_one_or_none()
      if not course:
        print(f"⚠  Курс не найден: {course_title}")
        continue

      # Проверяем какие order уже есть
      existing = await db.execute(
        select(Lesson.order).where(Lesson.course_id == course.id)
      )
      existing_orders = {row[0] for row in existing.fetchall()}

      added = 0
      for lesson_data in new_lessons:
        if lesson_data["order"] in existing_orders:
          print(f"   пропуск (уже есть): {lesson_data['title']}")
          continue
        lesson = Lesson(course_id=course.id, **lesson_data)
        db.add(lesson)
        added += 1

      print(f"✓ {course_title}: +{added} уроков")

    await db.commit()
    print("\n✅ Готово!")


if __name__ == "__main__":
  asyncio.run(seed())
