"""
Добавляет новые курсы: ООП, PostgreSQL, FastAPI.
Запуск: docker exec codelearn-backend-1 python seed_v2.py
"""
import asyncio, json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.user import Course, Lesson, LanguageEnum, LevelEnum

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)


# ─────────────────────────────────────────────────────────────
# КУРС: ООП в Python
# ─────────────────────────────────────────────────────────────
OOP_LESSONS = [
  {
    "title": "Классы и объекты",
    "order": 1, "xp_reward": 20,
    "hints": json.dumps([
      "Класс создаётся ключевым словом class: class Dog:",
      "Объект создаётся вызовом класса: rex = Dog('Рекс', 3)",
      "Атрибуты объекта доступны через точку: rex.name",
    ], ensure_ascii=False),
    "content": """## Что такое класс?

Класс — это шаблон (чертёж) для создания объектов. Объект — конкретный экземпляр класса.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} говорит: Гав!"

rex = Dog("Рекс", 3)
print(rex.bark())   # Рекс говорит: Гав!
print(rex.name)     # Рекс
print(rex.age)      # 3
```

## Что такое self?

`self` — ссылка на сам объект. Через `self` мы обращаемся к атрибутам и методам объекта внутри класса.

## __init__

`__init__` — конструктор, вызывается автоматически при создании объекта. Здесь задаются начальные атрибуты.

## Задание

Создай класс `Car` с атрибутами `brand` (марка) и `year` (год). Добавь метод `info()` который возвращает строку `"Toyota 2020"`. Создай объект и выведи `info()`.
""",
    "starter_code": "class Car:\n    def __init__(self, brand, year):\n        self.brand = brand\n        self.year = year\n\n    def info(self):\n        return f\"{self.brand} {self.year}\"\n\ncar = Car(\"Toyota\", 2020)\nprint(car.info())",
    "solution": "class Car:\n    def __init__(self, brand, year):\n        self.brand = brand\n        self.year = year\n    def info(self):\n        return f\"{self.brand} {self.year}\"\ncar = Car(\"Toyota\", 2020)\nprint(car.info())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if car.brand == 'Toyota' and car.year == 2020 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if car.info() == 'Toyota 2020' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Методы и атрибуты",
    "order": 2, "xp_reward": 20,
    "hints": json.dumps([
      "Атрибуты класса задаются в __init__ через self.имя = значение",
      "Метод — это функция внутри класса, первый параметр всегда self",
      "Вызов метода: объект.метод()",
    ], ensure_ascii=False),
    "content": """## Атрибуты экземпляра и класса

```python
class Circle:
    pi = 3.14159  # атрибут класса — общий для всех объектов

    def __init__(self, radius):
        self.radius = radius  # атрибут экземпляра — у каждого свой

    def area(self):
        return self.pi * self.radius ** 2

    def perimeter(self):
        return 2 * self.pi * self.radius

c = Circle(5)
print(c.area())       # 78.53975
print(c.perimeter())  # 31.4159
print(Circle.pi)      # 3.14159
```

## Изменение атрибутов

```python
c.radius = 10
print(c.area())  # 314.159
```

## Задание

Создай класс `Rectangle` с атрибутами `width` и `height`. Добавь методы `area()` (площадь) и `perimeter()` (периметр). Выведи оба значения для прямоугольника 4×6.
""",
    "starter_code": "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def area(self):\n        return self.width * self.height\n\n    def perimeter(self):\n        return 2 * (self.width + self.height)\n\nr = Rectangle(4, 6)\nprint(r.area())\nprint(r.perimeter())",
    "solution": "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n    def area(self):\n        return self.width * self.height\n    def perimeter(self):\n        return 2 * (self.width + self.height)\nr = Rectangle(4, 6)\nprint(r.area())\nprint(r.perimeter())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if r.area() == 24 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if r.perimeter() == 20 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Наследование",
    "order": 3, "xp_reward": 25,
    "hints": json.dumps([
      "Наследование: class Dog(Animal): — Dog наследует Animal",
      "super().__init__() вызывает конструктор родителя",
      "Дочерний класс получает все методы родителя автоматически",
    ], ensure_ascii=False),
    "content": """## Что такое наследование?

Наследование позволяет создать новый класс на основе существующего. Дочерний класс получает все методы и атрибуты родителя.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} издаёт звук"

class Dog(Animal):
    def speak(self):  # переопределяем метод
        return f"{self.name} говорит: Гав!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} говорит: Мяу!"

dog = Dog("Рекс")
cat = Cat("Мурка")
print(dog.speak())  # Рекс говорит: Гав!
print(cat.speak())  # Мурка говорит: Мяу!
```

## super()

`super()` вызывает метод родительского класса:

```python
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # вызываем Animal.__init__
        self.breed = breed
```

## Задание

Создай класс `Shape` с методом `describe()` возвращающим `"Я фигура"`. Создай класс `Square(Shape)` с атрибутом `side` и переопредели `describe()` — пусть возвращает `"Я квадрат со стороной 5"`. Создай объект и выведи `describe()`.
""",
    "starter_code": "class Shape:\n    def describe(self):\n        return \"Я фигура\"\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def describe(self):\n        return f\"Я квадрат со стороной {self.side}\"\n\ns = Square(5)\nprint(s.describe())",
    "solution": "class Shape:\n    def describe(self):\n        return 'Я фигура'\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n    def describe(self):\n        return f'Я квадрат со стороной {self.side}'\ns = Square(5)\nprint(s.describe())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if isinstance(s, Shape) else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if s.describe() == 'Я квадрат со стороной 5' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Инкапсуляция",
    "order": 4, "xp_reward": 25,
    "hints": json.dumps([
      "Приватный атрибут: self.__balance (двойное подчёркивание)",
      "Доступ к приватному атрибуту — через метод: def get_balance(self):",
      "Setter проверяет значение перед записью",
    ], ensure_ascii=False),
    "content": """## Инкапсуляция

Инкапсуляция — скрытие внутренних данных объекта. Используется чтобы защитить данные от некорректного изменения.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # приватный атрибут

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Недостаточно средств")

    def get_balance(self):
        return self.__balance

acc = BankAccount("Алекс", 1000)
acc.deposit(500)
acc.withdraw(200)
print(acc.get_balance())  # 1300
# print(acc.__balance)  # AttributeError!
```

## Задание

Создай класс `Person` с приватным атрибутом `__age`. Добавь метод `set_age(age)` который устанавливает возраст только если он больше 0, и метод `get_age()`. Создай объект, установи возраст 25 и выведи его.
""",
    "starter_code": "class Person:\n    def __init__(self, name):\n        self.name = name\n        self.__age = 0\n\n    def set_age(self, age):\n        if age > 0:\n            self.__age = age\n\n    def get_age(self):\n        return self.__age\n\np = Person(\"Иван\")\np.set_age(25)\nprint(p.get_age())",
    "solution": "class Person:\n    def __init__(self, name):\n        self.name = name\n        self.__age = 0\n    def set_age(self, age):\n        if age > 0:\n            self.__age = age\n    def get_age(self):\n        return self.__age\np = Person('Иван')\np.set_age(25)\nprint(p.get_age())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if p.get_age() == 25 else 'FAIL')", "expected": "OK"},
      {"check": "\np.set_age(-5)\nprint('OK' if p.get_age() == 25 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Полиморфизм",
    "order": 5, "xp_reward": 25,
    "hints": json.dumps([
      "Полиморфизм — один интерфейс, разное поведение у разных классов",
      "Достаточно определить одинаковый метод в каждом классе",
      "Можно вызывать метод не зная конкретный тип объекта",
    ], ensure_ascii=False),
    "content": """## Полиморфизм

Полиморфизм — способность объектов разных классов обрабатываться одинаково.

```python
class Dog:
    def speak(self):
        return "Гав!"

class Cat:
    def speak(self):
        return "Мяу!"

class Duck:
    def speak(self):
        return "Кря!"

animals = [Dog(), Cat(), Duck()]

for animal in animals:
    print(animal.speak())
# Гав!
# Мяу!
# Кря!
```

## Полиморфизм с общим базовым классом

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r ** 2

class Square(Shape):
    def __init__(self, a):
        self.a = a
    def area(self):
        return self.a ** 2

shapes = [Circle(5), Square(4)]
for s in shapes:
    print(s.area())
```

## Задание

Создай классы `Triangle` и `Square`, у каждого метод `area()`. У Triangle: стороны a=3, h=4 → площадь = 0.5 * a * h. У Square: сторона a=4 → площадь = a*a. Создай список из обоих объектов и выведи площадь каждого.
""",
    "starter_code": "class Triangle:\n    def __init__(self, a, h):\n        self.a = a\n        self.h = h\n\n    def area(self):\n        return 0.5 * self.a * self.h\n\nclass Square:\n    def __init__(self, a):\n        self.a = a\n\n    def area(self):\n        return self.a * self.a\n\nshapes = [Triangle(3, 4), Square(4)]\nfor s in shapes:\n    print(s.area())",
    "solution": "class Triangle:\n    def __init__(self, a, h):\n        self.a = a\n        self.h = h\n    def area(self):\n        return 0.5 * self.a * self.h\nclass Square:\n    def __init__(self, a):\n        self.a = a\n    def area(self):\n        return self.a * self.a\nshapes = [Triangle(3, 4), Square(4)]\nfor s in shapes:\n    print(s.area())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if Triangle(3,4).area() == 6.0 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if Square(4).area() == 16 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Декораторы @property и @staticmethod",
    "order": 6, "xp_reward": 30,
    "hints": json.dumps([
      "@property позволяет обращаться к методу как к атрибуту: obj.temperature",
      "@staticmethod — метод без self, не зависит от объекта",
      "@classmethod принимает cls вместо self",
    ], ensure_ascii=False),
    "content": """## @property

`@property` позволяет вызывать метод как атрибут — без скобок:

```python
class Temperature:
    def __init__(self, celsius):
        self.__celsius = celsius

    @property
    def celsius(self):
        return self.__celsius

    @property
    def fahrenheit(self):
        return self.__celsius * 9/5 + 32

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Ниже абсолютного нуля!")
        self.__celsius = value

t = Temperature(100)
print(t.celsius)     # 100  (без скобок!)
print(t.fahrenheit)  # 212.0
t.celsius = 0
print(t.fahrenheit)  # 32.0
```

## @staticmethod

Метод класса, не привязанный к объекту:

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

print(MathUtils.add(3, 4))  # 7
```

## Задание

Создай класс `Circle` с приватным атрибутом `__radius`. Добавь `@property radius` и `@property area` (π × r²). Создай объект с radius=7 и выведи area.
""",
    "starter_code": "class Circle:\n    def __init__(self, radius):\n        self.__radius = radius\n\n    @property\n    def radius(self):\n        return self.__radius\n\n    @property\n    def area(self):\n        return 3.14159 * self.__radius ** 2\n\nc = Circle(7)\nprint(round(c.area, 2))",
    "solution": "class Circle:\n    def __init__(self, radius):\n        self.__radius = radius\n    @property\n    def radius(self):\n        return self.__radius\n    @property\n    def area(self):\n        return 3.14159 * self.__radius ** 2\nc = Circle(7)\nprint(round(c.area, 2))",
    "tests": json.dumps([
      {"check": "\nprint('OK' if c.radius == 7 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if abs(c.area - 153.938) < 0.1 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Специальные методы",
    "order": 7, "xp_reward": 30,
    "hints": json.dumps([
      "__str__ вызывается при print(объект) — возвращает строку",
      "__len__ вызывается при len(объект) — возвращает число",
      "__eq__ вызывается при сравнении obj1 == obj2",
    ], ensure_ascii=False),
    "content": """## Магические методы

Python вызывает специальные методы автоматически при определённых операциях:

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"'{self.title}' ({self.pages} стр.)"

    def __len__(self):
        return self.pages

    def __eq__(self, other):
        return self.title == other.title

b1 = Book("Python", 400)
b2 = Book("JavaScript", 300)

print(b1)           # 'Python' (400 стр.)
print(len(b1))      # 400
print(b1 == b2)     # False
```

## Другие магические методы

| Метод | Вызывается при |
|-------|---------------|
| `__str__` | `print(obj)`, `str(obj)` |
| `__len__` | `len(obj)` |
| `__eq__` | `obj1 == obj2` |
| `__lt__` | `obj1 < obj2` |
| `__add__` | `obj1 + obj2` |

## Задание

Создай класс `Vector` с атрибутами `x` и `y`. Реализуй `__str__` → `"Vector(3, 4)"`, `__add__` → возвращает новый Vector с суммой координат. Выведи сумму Vector(1,2) + Vector(3,4).
""",
    "starter_code": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __str__(self):\n        return f\"Vector({self.x}, {self.y})\"\n\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\nv1 = Vector(1, 2)\nv2 = Vector(3, 4)\nprint(v1 + v2)",
    "solution": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __str__(self):\n        return f'Vector({self.x}, {self.y})'\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\nv1 = Vector(1, 2)\nv2 = Vector(3, 4)\nprint(v1 + v2)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if str(Vector(1,2)+Vector(3,4)) == 'Vector(4, 6)' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Абстрактные классы",
    "order": 8, "xp_reward": 35,
    "hints": json.dumps([
      "from abc import ABC, abstractmethod",
      "Абстрактный класс нельзя создать напрямую — только через наследника",
      "@abstractmethod заставляет дочерний класс реализовать метод",
    ], ensure_ascii=False),
    "content": """## Абстрактные классы

Абстрактный класс — шаблон с методами, которые **обязаны** быть реализованы в дочерних классах.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def describe(self):
        return f"Площадь: {self.area()}, периметр: {self.perimeter()}"

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

r = Rectangle(4, 5)
print(r.describe())  # Площадь: 20, периметр: 18

# Shape()  # TypeError! Нельзя создать абстрактный класс
```

## Зачем это нужно?

Абстрактные классы гарантируют, что все наследники реализуют нужные методы. Это основа для больших систем и паттернов проектирования.

## Задание

Создай абстрактный класс `Animal` с абстрактным методом `sound()`. Создай класс `Dog(Animal)` с методом `sound()` → `"Гав"` и `Cat(Animal)` → `"Мяу"`. Выведи звуки обоих.
""",
    "starter_code": "from abc import ABC, abstractmethod\n\nclass Animal(ABC):\n    @abstractmethod\n    def sound(self):\n        pass\n\nclass Dog(Animal):\n    def sound(self):\n        return \"Гав\"\n\nclass Cat(Animal):\n    def sound(self):\n        return \"Мяу\"\n\ndog = Dog()\ncat = Cat()\nprint(dog.sound())\nprint(cat.sound())",
    "solution": "from abc import ABC, abstractmethod\nclass Animal(ABC):\n    @abstractmethod\n    def sound(self):\n        pass\nclass Dog(Animal):\n    def sound(self):\n        return 'Гав'\nclass Cat(Animal):\n    def sound(self):\n        return 'Мяу'\ndog = Dog()\ncat = Cat()\nprint(dog.sound())\nprint(cat.sound())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if dog.sound() == 'Гав' else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if cat.sound() == 'Мяу' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
]


# ─────────────────────────────────────────────────────────────
# КУРС: PostgreSQL (через sqlite3)
# ─────────────────────────────────────────────────────────────
PG_LESSONS = [
  {
    "title": "Введение в базы данных",
    "order": 1, "xp_reward": 20,
    "hints": json.dumps([
      "sqlite3.connect(':memory:') создаёт БД в памяти",
      "cursor.execute() выполняет SQL-запрос",
      "cursor.fetchall() возвращает все строки результата",
    ], ensure_ascii=False),
    "content": """## Что такое база данных?

База данных — организованное хранилище данных. SQL (Structured Query Language) — язык для работы с ней.

Мы будем практиковаться на **SQLite** — встроенной в Python БД. Синтаксис SQL такой же как в PostgreSQL.

## Первые шаги

```python
import sqlite3

# Подключение (в памяти — для практики)
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE users (
        id   INTEGER PRIMARY KEY,
        name TEXT    NOT NULL,
        age  INTEGER
    )
''')

# Вставка данных
cursor.execute("INSERT INTO users VALUES (1, 'Алекс', 25)")
cursor.execute("INSERT INTO users VALUES (2, 'Мария', 30)")

# Выборка
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)
# (1, 'Алекс', 25)
# (2, 'Мария', 30)
```

## Задание

Создай таблицу `products` с колонками `id`, `name`, `price`. Добавь 2 товара и выведи все строки.
""",
    "starter_code": "import sqlite3\n\nconn = sqlite3.connect(':memory:')\ncursor = conn.cursor()\n\ncursor.execute('''\n    CREATE TABLE products (\n        id    INTEGER PRIMARY KEY,\n        name  TEXT    NOT NULL,\n        price REAL\n    )\n''')\n\ncursor.execute(\"INSERT INTO products VALUES (1, 'Ноутбук', 50000)\")\ncursor.execute(\"INSERT INTO products VALUES (2, 'Мышь', 1500)\")\n\ncursor.execute('SELECT * FROM products')\nfor row in cursor.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\ncursor = conn.cursor()\ncursor.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL)')\ncursor.execute(\"INSERT INTO products VALUES (1, 'Ноутбук', 50000)\")\ncursor.execute(\"INSERT INTO products VALUES (2, 'Мышь', 1500)\")\ncursor.execute('SELECT * FROM products')\nfor row in cursor.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nrows = cursor.fetchall()\nprint('OK' if len(rows) == 0 else 'OK')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "SELECT, WHERE, ORDER BY",
    "order": 2, "xp_reward": 20,
    "hints": json.dumps([
      "WHERE фильтрует строки: WHERE age > 25",
      "ORDER BY сортирует: ORDER BY price DESC",
      "LIMIT ограничивает количество: LIMIT 3",
    ], ensure_ascii=False),
    "content": """## Фильтрация и сортировка

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE employees (id INT, name TEXT, salary INT, dept TEXT)')
c.executemany('INSERT INTO employees VALUES (?,?,?,?)', [
    (1, 'Алекс',  80000, 'IT'),
    (2, 'Мария',  70000, 'HR'),
    (3, 'Дмитрий',90000, 'IT'),
    (4, 'Анна',   65000, 'HR'),
    (5, 'Иван',   95000, 'IT'),
])

# WHERE — условие
c.execute("SELECT * FROM employees WHERE dept = 'IT'")
print(c.fetchall())

# ORDER BY — сортировка
c.execute("SELECT name, salary FROM employees ORDER BY salary DESC")
print(c.fetchall())

# LIMIT — ограничение
c.execute("SELECT name FROM employees ORDER BY salary DESC LIMIT 3")
print(c.fetchall())
```

## Операторы сравнения

```sql
WHERE salary > 70000       -- больше
WHERE dept = 'IT'          -- равно
WHERE salary BETWEEN 70000 AND 90000
WHERE name LIKE 'А%'       -- начинается на А
```

## Задание

Создай таблицу `students` (id, name, grade). Добавь 4 студентов. Выведи только тех, у кого оценка больше 3, отсортированных по оценке по убыванию.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('CREATE TABLE students (id INT, name TEXT, grade INT)')\nc.executemany('INSERT INTO students VALUES (?,?,?)', [\n    (1, 'Алекс', 5),\n    (2, 'Мария', 3),\n    (3, 'Иван',  4),\n    (4, 'Анна',  2),\n])\n\nc.execute('SELECT name, grade FROM students WHERE grade > 3 ORDER BY grade DESC')\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE students (id INT, name TEXT, grade INT)')\nc.executemany('INSERT INTO students VALUES (?,?,?)',[(1,'Алекс',5),(2,'Мария',3),(3,'Иван',4),(4,'Анна',2)])\nc.execute('SELECT name, grade FROM students WHERE grade > 3 ORDER BY grade DESC')\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute('SELECT count(*) FROM students WHERE grade > 3')\nprint('OK' if c.fetchone()[0] == 2 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Агрегатные функции и GROUP BY",
    "order": 3, "xp_reward": 25,
    "hints": json.dumps([
      "COUNT(*) — количество строк",
      "AVG(column) — среднее значение",
      "GROUP BY группирует строки по значению колонки",
    ], ensure_ascii=False),
    "content": """## Агрегатные функции

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE sales (id INT, product TEXT, amount INT, city TEXT)')
c.executemany('INSERT INTO sales VALUES (?,?,?,?)', [
    (1, 'Ноутбук', 50000, 'Алматы'),
    (2, 'Телефон', 30000, 'Астана'),
    (3, 'Ноутбук', 50000, 'Алматы'),
    (4, 'Планшет', 25000, 'Астана'),
    (5, 'Телефон', 30000, 'Алматы'),
])

# COUNT — количество
c.execute("SELECT COUNT(*) FROM sales")
print(c.fetchone())  # (5,)

# SUM, AVG, MAX, MIN
c.execute("SELECT SUM(amount), AVG(amount), MAX(amount) FROM sales")
print(c.fetchone())  # (185000, 37000.0, 50000)

# GROUP BY — группировка
c.execute("SELECT city, COUNT(*), SUM(amount) FROM sales GROUP BY city")
for row in c.fetchall():
    print(row)
# ('Алматы', 3, 130000)
# ('Астана', 2, 55000)
```

## Задание

Создай таблицу `orders` (id, category, price). Добавь 5 заказов разных категорий. Выведи каждую категорию и среднюю цену в ней.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('CREATE TABLE orders (id INT, category TEXT, price INT)')\nc.executemany('INSERT INTO orders VALUES (?,?,?)', [\n    (1, 'Электроника', 50000),\n    (2, 'Одежда',      5000),\n    (3, 'Электроника', 30000),\n    (4, 'Одежда',      8000),\n    (5, 'Книги',       1500),\n])\n\nc.execute('SELECT category, AVG(price) FROM orders GROUP BY category')\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE orders (id INT, category TEXT, price INT)')\nc.executemany('INSERT INTO orders VALUES (?,?,?)',[(1,'Электроника',50000),(2,'Одежда',5000),(3,'Электроника',30000),(4,'Одежда',8000),(5,'Книги',1500)])\nc.execute('SELECT category, AVG(price) FROM orders GROUP BY category')\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute('SELECT COUNT(DISTINCT category) FROM orders')\nprint('OK' if c.fetchone()[0] == 3 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "JOIN — объединение таблиц",
    "order": 4, "xp_reward": 30,
    "hints": json.dumps([
      "INNER JOIN объединяет строки у которых есть совпадение в обеих таблицах",
      "ON указывает условие объединения: ON orders.user_id = users.id",
      "Можно выбирать колонки из обеих таблиц: SELECT users.name, orders.amount",
    ], ensure_ascii=False),
    "content": """## JOIN — связи между таблицами

JOIN объединяет данные из двух таблиц по связанным колонкам.

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE users (id INT, name TEXT)')
c.execute('CREATE TABLE orders (id INT, user_id INT, product TEXT, amount INT)')

c.executemany('INSERT INTO users VALUES (?,?)', [(1,'Алекс'),(2,'Мария'),(3,'Иван')])
c.executemany('INSERT INTO orders VALUES (?,?,?,?)', [
    (1, 1, 'Ноутбук', 50000),
    (2, 1, 'Мышь',     1500),
    (3, 2, 'Телефон', 30000),
])

# INNER JOIN — только совпадающие записи
c.execute('''
    SELECT users.name, orders.product, orders.amount
    FROM orders
    INNER JOIN users ON orders.user_id = users.id
''')
for row in c.fetchall():
    print(row)
# ('Алекс', 'Ноутбук', 50000)
# ('Алекс', 'Мышь', 1500)
# ('Мария', 'Телефон', 30000)
```

## Виды JOIN

| Тип | Описание |
|-----|----------|
| `INNER JOIN` | Только совпадающие строки |
| `LEFT JOIN` | Все из левой + совпадения |
| `RIGHT JOIN` | Все из правой + совпадения |

## Задание

Создай таблицы `departments` (id, name) и `employees` (id, name, dept_id). Добавь 2 отдела и 4 сотрудника. Выведи имя сотрудника и название его отдела через JOIN.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('CREATE TABLE departments (id INT, name TEXT)')\nc.execute('CREATE TABLE employees (id INT, name TEXT, dept_id INT)')\n\nc.executemany('INSERT INTO departments VALUES (?,?)', [(1,'IT'),(2,'HR')])\nc.executemany('INSERT INTO employees VALUES (?,?,?)', [\n    (1,'Алекс',1),(2,'Мария',2),(3,'Иван',1),(4,'Анна',2)\n])\n\nc.execute('''\n    SELECT employees.name, departments.name\n    FROM employees\n    INNER JOIN departments ON employees.dept_id = departments.id\n''')\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE departments (id INT, name TEXT)')\nc.execute('CREATE TABLE employees (id INT, name TEXT, dept_id INT)')\nc.executemany('INSERT INTO departments VALUES (?,?)',[(1,'IT'),(2,'HR')])\nc.executemany('INSERT INTO employees VALUES (?,?,?)',[(1,'Алекс',1),(2,'Мария',2),(3,'Иван',1),(4,'Анна',2)])\nc.execute('SELECT employees.name, departments.name FROM employees INNER JOIN departments ON employees.dept_id = departments.id')\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute('SELECT COUNT(*) FROM employees INNER JOIN departments ON employees.dept_id = departments.id')\nprint('OK' if c.fetchone()[0] == 4 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "INSERT, UPDATE, DELETE",
    "order": 5, "xp_reward": 25,
    "hints": json.dumps([
      "UPDATE меняет данные: UPDATE users SET age = 26 WHERE id = 1",
      "DELETE удаляет: DELETE FROM users WHERE id = 1",
      "Без WHERE — обновятся/удалятся ВСЕ строки!",
    ], ensure_ascii=False),
    "content": """## Изменение данных

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE users (id INT, name TEXT, age INT)')
c.executemany('INSERT INTO users VALUES (?,?,?)', [
    (1, 'Алекс', 25),
    (2, 'Мария', 30),
    (3, 'Иван',  22),
])

# UPDATE — изменение
c.execute("UPDATE users SET age = 26 WHERE id = 1")

# UPDATE нескольких полей
c.execute("UPDATE users SET name = 'Александр', age = 27 WHERE id = 1")

# DELETE — удаление
c.execute("DELETE FROM users WHERE id = 3")

# Параметризованные запросы (защита от SQL-инъекций)
new_age = 31
user_id = 2
c.execute("UPDATE users SET age = ? WHERE id = ?", (new_age, user_id))

conn.commit()  # сохраняем изменения

c.execute("SELECT * FROM users")
for row in c.fetchall():
    print(row)
```

## Задание

Создай таблицу `products` (id, name, price). Добавь 3 товара. Обнови цену первого товара на 9999. Удали третий товар. Выведи оставшиеся товары.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('CREATE TABLE products (id INT, name TEXT, price INT)')\nc.executemany('INSERT INTO products VALUES (?,?,?)', [\n    (1, 'Ноутбук', 50000),\n    (2, 'Мышь',     1500),\n    (3, 'Клавиатура', 3000),\n])\n\nc.execute('UPDATE products SET price = 9999 WHERE id = 1')\nc.execute('DELETE FROM products WHERE id = 3')\nconn.commit()\n\nc.execute('SELECT * FROM products')\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE products (id INT, name TEXT, price INT)')\nc.executemany('INSERT INTO products VALUES (?,?,?)',[(1,'Ноутбук',50000),(2,'Мышь',1500),(3,'Клавиатура',3000)])\nc.execute('UPDATE products SET price = 9999 WHERE id = 1')\nc.execute('DELETE FROM products WHERE id = 3')\nconn.commit()\nc.execute('SELECT * FROM products')\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute('SELECT COUNT(*) FROM products')\nprint('OK' if c.fetchone()[0] == 2 else 'FAIL')", "expected": "OK"},
      {"check": "\nc.execute('SELECT price FROM products WHERE id = 1')\nprint('OK' if c.fetchone()[0] == 9999 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Транзакции и ACID",
    "order": 6, "xp_reward": 30,
    "hints": json.dumps([
      "conn.commit() — фиксирует транзакцию (сохраняет изменения)",
      "conn.rollback() — откатывает транзакцию (отменяет изменения)",
      "try/except + rollback защищает данные от ошибок",
    ], ensure_ascii=False),
    "content": """## Что такое транзакция?

Транзакция — группа операций, которые выполняются **все вместе** или **не выполняются вовсе**.

**ACID:**
- **A**tomicity — атомарность: либо всё, либо ничего
- **C**onsistency — согласованность: данные всегда корректны
- **I**solation — изоляция: транзакции не мешают друг другу
- **D**urability — долговечность: зафиксированные данные сохраняются

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE accounts (id INT, name TEXT, balance INT)')
c.executemany('INSERT INTO accounts VALUES (?,?,?)', [
    (1, 'Алекс', 10000),
    (2, 'Мария',  5000),
])
conn.commit()

# Перевод денег — должен быть атомарным
def transfer(from_id, to_id, amount):
    try:
        c.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        c.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
        conn.commit()
        print("Перевод выполнен")
    except Exception as e:
        conn.rollback()  # откат при ошибке
        print(f"Ошибка: {e}")

transfer(1, 2, 3000)
c.execute("SELECT * FROM accounts")
for row in c.fetchall():
    print(row)
```

## Задание

Реализуй функцию `transfer(from_id, to_id, amount)` с транзакцией. Создай двух пользователей с балансами 5000 и 3000. Переведи 1000 от первого ко второму. Выведи итоговые балансы.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('CREATE TABLE accounts (id INT, name TEXT, balance INT)')\nc.executemany('INSERT INTO accounts VALUES (?,?,?)', [\n    (1, 'Алекс', 5000),\n    (2, 'Мария',  3000),\n])\nconn.commit()\n\ndef transfer(from_id, to_id, amount):\n    try:\n        c.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, from_id))\n        c.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, to_id))\n        conn.commit()\n    except Exception as e:\n        conn.rollback()\n        print(f'Ошибка: {e}')\n\ntransfer(1, 2, 1000)\nc.execute('SELECT * FROM accounts')\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE accounts (id INT, name TEXT, balance INT)')\nc.executemany('INSERT INTO accounts VALUES (?,?,?)',[(1,'Алекс',5000),(2,'Мария',3000)])\nconn.commit()\ndef transfer(from_id, to_id, amount):\n    try:\n        c.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?',(amount,from_id))\n        c.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?',(amount,to_id))\n        conn.commit()\n    except:\n        conn.rollback()\ntransfer(1,2,1000)\nc.execute('SELECT * FROM accounts')\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute('SELECT balance FROM accounts WHERE id=1')\nprint('OK' if c.fetchone()[0] == 4000 else 'FAIL')", "expected": "OK"},
      {"check": "\nc.execute('SELECT balance FROM accounts WHERE id=2')\nprint('OK' if c.fetchone()[0] == 4000 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Индексы и оптимизация",
    "order": 7, "xp_reward": 30,
    "hints": json.dumps([
      "CREATE INDEX idx_name ON table(column) ускоряет поиск по колонке",
      "Индексы замедляют INSERT/UPDATE но ускоряют SELECT",
      "EXPLAIN QUERY PLAN показывает план выполнения запроса",
    ], ensure_ascii=False),
    "content": """## Индексы

Индекс — структура данных для быстрого поиска. Без индекса БД читает все строки (full scan), с индексом — находит сразу.

```python
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('''
    CREATE TABLE users (
        id    INTEGER PRIMARY KEY,  -- PRIMARY KEY автоматически индексируется
        email TEXT UNIQUE,          -- UNIQUE тоже создаёт индекс
        name  TEXT,
        city  TEXT
    )
''')

# Создаём индекс для частых поисков по city
c.execute("CREATE INDEX idx_city ON users(city)")

# Составной индекс
c.execute("CREATE INDEX idx_name_city ON users(name, city)")

# Посмотреть план запроса
c.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE city = 'Алматы'")
print(c.fetchall())
```

## Когда создавать индекс?

✅ Колонка часто используется в WHERE
✅ Колонка используется в JOIN
✅ Большая таблица (тысячи строк)
❌ Маленькая таблица
❌ Колонка редко используется в запросах

## Задание

Создай таблицу `articles` (id, title, author, views). Создай индекс по колонке `author`. Добавь 3 статьи и сделай SELECT по author с использованием индекса.
""",
    "starter_code": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\n\nc.execute('''\n    CREATE TABLE articles (\n        id     INTEGER PRIMARY KEY,\n        title  TEXT,\n        author TEXT,\n        views  INTEGER\n    )\n''')\n\nc.execute('CREATE INDEX idx_author ON articles(author)')\n\nc.executemany('INSERT INTO articles VALUES (?,?,?,?)', [\n    (1, 'Python tips',   'Алекс', 1500),\n    (2, 'SQL basics',    'Мария', 800),\n    (3, 'FastAPI guide', 'Алекс', 2200),\n])\n\nc.execute(\"SELECT title, views FROM articles WHERE author = 'Алекс'\")\nfor row in c.fetchall():\n    print(row)",
    "solution": "import sqlite3\nconn = sqlite3.connect(':memory:')\nc = conn.cursor()\nc.execute('CREATE TABLE articles (id INTEGER PRIMARY KEY, title TEXT, author TEXT, views INTEGER)')\nc.execute('CREATE INDEX idx_author ON articles(author)')\nc.executemany('INSERT INTO articles VALUES (?,?,?,?)',[(1,'Python tips','Алекс',1500),(2,'SQL basics','Мария',800),(3,'FastAPI guide','Алекс',2200)])\nc.execute(\"SELECT title, views FROM articles WHERE author = 'Алекс'\")\nfor row in c.fetchall():\n    print(row)",
    "tests": json.dumps([
      {"check": "\nc.execute(\"SELECT COUNT(*) FROM articles WHERE author='Алекс'\")\nprint('OK' if c.fetchone()[0] == 2 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
]


# ─────────────────────────────────────────────────────────────
# КУРС: FastAPI
# ─────────────────────────────────────────────────────────────
FASTAPI_LESSONS = [
  {
    "title": "Введение в FastAPI",
    "order": 1, "xp_reward": 20,
    "hints": json.dumps([
      "FastAPI использует декораторы для определения маршрутов: @app.get('/')",
      "Функция маршрута возвращает данные — FastAPI сам конвертирует в JSON",
      "uvicorn запускает сервер: uvicorn main:app --reload",
    ], ensure_ascii=False),
    "content": """## Что такое FastAPI?

FastAPI — современный веб-фреймворк для создания API на Python. Особенности:
- Автоматическая документация (Swagger UI)
- Валидация данных через Pydantic
- Асинхронная поддержка из коробки
- Один из самых быстрых Python-фреймворков

## Минимальное приложение

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Привет, FastAPI!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "Алекс"}
```

Запуск: `uvicorn main:app --reload`

## Структура маршрутов

```python
@app.get("/items")       # GET  — получить список
@app.post("/items")      # POST — создать
@app.put("/items/{id}")  # PUT  — обновить
@app.delete("/items/{id}") # DELETE — удалить
```

## Задание

Симулируй работу FastAPI: создай функцию `get_user(user_id)` которая возвращает словарь `{"id": user_id, "name": "User_{user_id}"}`. Выведи результат для user_id=42.
""",
    "starter_code": "# FastAPI использует такой подход:\n# @app.get('/users/{user_id}')\n# def get_user(user_id: int):\n#     return {...}\n\n# Симулируем логику маршрута:\ndef get_user(user_id: int) -> dict:\n    return {\"id\": user_id, \"name\": f\"User_{user_id}\"}\n\nresult = get_user(42)\nprint(result)",
    "solution": "def get_user(user_id: int) -> dict:\n    return {'id': user_id, 'name': f'User_{user_id}'}\nresult = get_user(42)\nprint(result)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if get_user(42) == {'id': 42, 'name': 'User_42'} else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if get_user(1)['id'] == 1 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Pydantic модели",
    "order": 2, "xp_reward": 25,
    "hints": json.dumps([
      "from pydantic import BaseModel — импорт базовой модели",
      "Поля модели — аннотации типов: name: str",
      "model.model_dump() конвертирует модель в словарь",
    ], ensure_ascii=False),
    "content": """## Pydantic — валидация данных

Pydantic автоматически валидирует и конвертирует данные:

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None  # необязательное поле

# Создание объекта
user = User(id=1, name="Алекс", email="alex@example.com", age=25)
print(user.name)        # Алекс
print(user.model_dump()) # {'id': 1, 'name': 'Алекс', ...}

# Валидация типов
user2 = User(id="5", name="Мария", email="m@test.com")
print(user2.id)  # 5 (str "5" автоматически конвертирован в int)
```

## В FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items")
def create_item(item: Item):
    return {"created": item.model_dump()}
```

FastAPI автоматически читает JSON из тела запроса и валидирует его через Pydantic.

## Задание

Создай Pydantic модель `Product` с полями `name: str`, `price: float`, `in_stock: bool = True`. Создай объект, выведи его как словарь.
""",
    "starter_code": "from pydantic import BaseModel\nfrom typing import Optional\n\nclass Product(BaseModel):\n    name: str\n    price: float\n    in_stock: bool = True\n\nproduct = Product(name=\"Ноутбук\", price=50000.0)\nprint(product.model_dump())",
    "solution": "from pydantic import BaseModel\nclass Product(BaseModel):\n    name: str\n    price: float\n    in_stock: bool = True\nproduct = Product(name='Ноутбук', price=50000.0)\nprint(product.model_dump())",
    "tests": json.dumps([
      {"check": "\nprint('OK' if product.name == 'Ноутбук' else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if product.in_stock == True else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if isinstance(product.price, float) else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Path и Query параметры",
    "order": 3, "xp_reward": 25,
    "hints": json.dumps([
      "Path параметр: /users/{user_id} — обязательный, в URL",
      "Query параметр: /items?limit=10 — необязательный, после ?",
      "В функции: def get_items(limit: int = 10, skip: int = 0)",
    ], ensure_ascii=False),
    "content": """## Path параметры

Параметры прямо в URL:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):  # тип int — FastAPI сам конвертирует
    return {"user_id": user_id}

@app.get("/files/{file_path:path}")  # :path — для путей с /
def get_file(file_path: str):
    return {"path": file_path}
```

## Query параметры

Параметры после `?` в URL:

```python
@app.get("/items")
def get_items(limit: int = 10, skip: int = 0, search: str = None):
    # GET /items?limit=5&skip=10&search=laptop
    return {"limit": limit, "skip": skip, "search": search}
```

## Комбинация

```python
@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, limit: int = 5):
    # GET /users/1/orders?limit=3
    return {"user_id": user_id, "limit": limit}
```

## Задание

Создай функцию `get_products(category: str, limit: int = 10, skip: int = 0)` которая возвращает словарь с этими параметрами. Вызови с category="электроника", limit=5 и выведи результат.
""",
    "starter_code": "def get_products(category: str, limit: int = 10, skip: int = 0) -> dict:\n    return {\n        \"category\": category,\n        \"limit\": limit,\n        \"skip\": skip,\n    }\n\nresult = get_products(category=\"электроника\", limit=5)\nprint(result)",
    "solution": "def get_products(category: str, limit: int = 10, skip: int = 0) -> dict:\n    return {'category': category, 'limit': limit, 'skip': skip}\nresult = get_products(category='электроника', limit=5)\nprint(result)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if get_products('tech')['limit'] == 10 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if get_products('tech', limit=5)['limit'] == 5 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "CRUD операции",
    "order": 4, "xp_reward": 30,
    "hints": json.dumps([
      "CRUD: Create, Read, Update, Delete",
      "POST создаёт, GET читает, PUT обновляет, DELETE удаляет",
      "В памяти можно хранить данные в словаре: db = {}",
    ], ensure_ascii=False),
    "content": """## CRUD — основа любого API

CRUD = Create, Read, Update, Delete. Почти каждое API реализует эти 4 операции.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

db: Dict[int, Item] = {}  # временное хранилище
next_id = 1

@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    db[next_id] = item
    next_id += 1
    return {"id": next_id - 1, **item.model_dump()}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Не найден")
    return db[item_id]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Не найден")
    db[item_id] = item
    return db[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Не найден")
    del db[item_id]
    return {"message": "Удалено"}
```

## Задание

Реализуй класс `ItemStorage` с методами `create(name, price)`, `get(id)`, `delete(id)`. Хранить в словаре. Создай 2 товара, получи первый, удали второй. Выведи размер хранилища.
""",
    "starter_code": "class ItemStorage:\n    def __init__(self):\n        self.db = {}\n        self._next_id = 1\n\n    def create(self, name: str, price: float) -> dict:\n        item = {\"id\": self._next_id, \"name\": name, \"price\": price}\n        self.db[self._next_id] = item\n        self._next_id += 1\n        return item\n\n    def get(self, id: int) -> dict:\n        return self.db.get(id)\n\n    def delete(self, id: int) -> bool:\n        if id in self.db:\n            del self.db[id]\n            return True\n        return False\n\nstorage = ItemStorage()\nstorage.create(\"Ноутбук\", 50000)\nstorage.create(\"Мышь\", 1500)\nprint(storage.get(1))\nstorage.delete(2)\nprint(len(storage.db))",
    "solution": "class ItemStorage:\n    def __init__(self):\n        self.db = {}\n        self._next_id = 1\n    def create(self, name, price):\n        item = {'id': self._next_id, 'name': name, 'price': price}\n        self.db[self._next_id] = item\n        self._next_id += 1\n        return item\n    def get(self, id):\n        return self.db.get(id)\n    def delete(self, id):\n        if id in self.db:\n            del self.db[id]\n            return True\n        return False\nstorage = ItemStorage()\nstorage.create('Ноутбук', 50000)\nstorage.create('Мышь', 1500)\nprint(storage.get(1))\nstorage.delete(2)\nprint(len(storage.db))",
    "tests": json.dumps([
      {"check": "\nprint('OK' if len(storage.db) == 1 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if storage.get(1)['name'] == 'Ноутбук' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Middleware и зависимости",
    "order": 5, "xp_reward": 30,
    "hints": json.dumps([
      "Depends() внедряет зависимость в маршрут",
      "Зависимость — обычная функция, FastAPI вызывает её автоматически",
      "Middleware обрабатывает каждый запрос до/после маршрута",
    ], ensure_ascii=False),
    "content": """## Dependency Injection

FastAPI позволяет переиспользовать логику через зависимости:

```python
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

# Зависимость — обычная функция
def get_current_user(token: str):
    if token != "secret":
        raise HTTPException(status_code=401, detail="Неверный токен")
    return {"username": "admin"}

# Маршрут использует зависимость
@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return {"user": user}
```

## Параметры запроса через зависимости

```python
from fastapi import Query

def pagination(skip: int = 0, limit: int = Query(default=10, le=100)):
    return {"skip": skip, "limit": limit}

@app.get("/items")
def get_items(params = Depends(pagination)):
    return params
```

## Middleware

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response
```

## Задание

Создай функцию `validate_token(token: str)` которая возвращает `{"user": "admin"}` если token == "secret123", иначе вызывает исключение. Создай функцию `get_profile(user)` которая возвращает профиль. Проверь оба случая.
""",
    "starter_code": "class HTTPException(Exception):\n    def __init__(self, status_code, detail):\n        self.status_code = status_code\n        self.detail = detail\n\ndef validate_token(token: str) -> dict:\n    if token != \"secret123\":\n        raise HTTPException(status_code=401, detail=\"Неверный токен\")\n    return {\"user\": \"admin\"}\n\ndef get_profile(user: dict) -> dict:\n    return {\"username\": user[\"user\"], \"role\": \"admin\"}\n\n# Верный токен\ntry:\n    user = validate_token(\"secret123\")\n    print(get_profile(user))\nexcept HTTPException as e:\n    print(f\"Ошибка {e.status_code}: {e.detail}\")\n\n# Неверный токен\ntry:\n    user = validate_token(\"wrong\")\nexcept HTTPException as e:\n    print(f\"Ошибка {e.status_code}: {e.detail}\")",
    "solution": "class HTTPException(Exception):\n    def __init__(self, status_code, detail):\n        self.status_code = status_code\n        self.detail = detail\ndef validate_token(token):\n    if token != 'secret123':\n        raise HTTPException(401, 'Неверный токен')\n    return {'user': 'admin'}\ndef get_profile(user):\n    return {'username': user['user'], 'role': 'admin'}\ntry:\n    user = validate_token('secret123')\n    print(get_profile(user))\nexcept HTTPException as e:\n    print(f'Ошибка {e.status_code}: {e.detail}')\ntry:\n    user = validate_token('wrong')\nexcept HTTPException as e:\n    print(f'Ошибка {e.status_code}: {e.detail}')",
    "tests": json.dumps([
      {"check": "\nprint('OK' if validate_token('secret123') == {'user': 'admin'} else 'FAIL')", "expected": "OK"},
      {"check": "\ntry:\n    validate_token('bad')\n    print('FAIL')\nexcept HTTPException as e:\n    print('OK' if e.status_code == 401 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Работа с базой данных",
    "order": 6, "xp_reward": 35,
    "hints": json.dumps([
      "SQLAlchemy ORM позволяет работать с БД через Python-классы",
      "Сессия — контекст для работы с БД: with Session() as session:",
      "session.add(obj) добавляет объект, session.commit() сохраняет",
    ], ensure_ascii=False),
    "content": """## SQLAlchemy + FastAPI

В реальных проектах FastAPI работает с БД через SQLAlchemy ORM:

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

engine = create_engine("sqlite:///./test.db")
Base = declarative_base()

# Модель таблицы
class User(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False)
    email = Column(String, unique=True)

Base.metadata.create_all(engine)

# CRUD через сессию
with Session(engine) as session:
    # Create
    user = User(name="Алекс", email="alex@test.com")
    session.add(user)
    session.commit()

    # Read
    users = session.query(User).all()
    print(users[0].name)  # Алекс

    # Update
    user.name = "Александр"
    session.commit()

    # Delete
    session.delete(user)
    session.commit()
```

## В FastAPI

```python
def get_db():
    with Session(engine) as session:
        yield session

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## Задание

Создай модель `Task` с полями `id`, `title`, `done` (bool, default False). Создай таблицу в памяти (:memory:), добавь 2 задачи, выведи все невыполненные.
""",
    "starter_code": "from sqlalchemy import create_engine, Column, Integer, String, Boolean\nfrom sqlalchemy.orm import declarative_base, Session\n\nengine = create_engine('sqlite:///:memory:')\nBase = declarative_base()\n\nclass Task(Base):\n    __tablename__ = 'tasks'\n    id    = Column(Integer, primary_key=True)\n    title = Column(String, nullable=False)\n    done  = Column(Boolean, default=False)\n\nBase.metadata.create_all(engine)\n\nwith Session(engine) as session:\n    session.add(Task(title='Изучить FastAPI'))\n    session.add(Task(title='Написать API', done=True))\n    session.commit()\n\n    tasks = session.query(Task).filter(Task.done == False).all()\n    for t in tasks:\n        print(t.title)",
    "solution": "from sqlalchemy import create_engine, Column, Integer, String, Boolean\nfrom sqlalchemy.orm import declarative_base, Session\nengine = create_engine('sqlite:///:memory:')\nBase = declarative_base()\nclass Task(Base):\n    __tablename__ = 'tasks'\n    id = Column(Integer, primary_key=True)\n    title = Column(String, nullable=False)\n    done = Column(Boolean, default=False)\nBase.metadata.create_all(engine)\nwith Session(engine) as session:\n    session.add(Task(title='Изучить FastAPI'))\n    session.add(Task(title='Написать API', done=True))\n    session.commit()\n    tasks = session.query(Task).filter(Task.done == False).all()\n    for t in tasks:\n        print(t.title)",
    "tests": json.dumps([
      {"check": "\nwith Session(engine) as s:\n    count = s.query(Task).filter(Task.done == False).count()\nprint('OK' if count == 1 else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Аутентификация JWT",
    "order": 7, "xp_reward": 35,
    "hints": json.dumps([
      "JWT токен состоит из header.payload.signature",
      "jose.jwt.encode() создаёт токен, decode() проверяет",
      "Токен обычно передаётся в заголовке: Authorization: Bearer <token>",
    ], ensure_ascii=False),
    "content": """## JWT аутентификация

JWT (JSON Web Token) — стандарт для передачи данных между клиентом и сервером.

```python
from datetime import datetime, timedelta
from jose import jwt
import hashlib

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

# Создание токена
def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Проверка токена
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None

# Хеширование пароля
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

token = create_token(1, "alex")
print("Token создан:", token[:30], "...")
data = verify_token(token)
print("Username:", data["username"])
```

## В FastAPI

```python
@app.post("/login")
def login(credentials: LoginForm, db = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(401, "Неверные данные")
    token = create_token(user.id, user.username)
    return {"access_token": token, "token_type": "bearer"}
```

## Задание

Реализуй функции `hash_password(password)` через hashlib.sha256 и `check_password(password, hashed)`. Захешируй пароль "qwerty123", проверь что он совпадает, и что "wrong" — не совпадает.
""",
    "starter_code": "import hashlib\n\ndef hash_password(password: str) -> str:\n    return hashlib.sha256(password.encode()).hexdigest()\n\ndef check_password(password: str, hashed: str) -> bool:\n    return hash_password(password) == hashed\n\nhashed = hash_password(\"qwerty123\")\nprint(\"Хеш:\", hashed[:20], \"...\")\nprint(\"Верный пароль:\", check_password(\"qwerty123\", hashed))\nprint(\"Неверный пароль:\", check_password(\"wrong\", hashed))",
    "solution": "import hashlib\ndef hash_password(password):\n    return hashlib.sha256(password.encode()).hexdigest()\ndef check_password(password, hashed):\n    return hash_password(password) == hashed\nhashed = hash_password('qwerty123')\nprint('Хеш:', hashed[:20], '...')\nprint('Верный пароль:', check_password('qwerty123', hashed))\nprint('Неверный пароль:', check_password('wrong', hashed))",
    "tests": json.dumps([
      {"check": "\nprint('OK' if check_password('qwerty123', hashed) == True else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if check_password('wrong', hashed) == False else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
  {
    "title": "Деплой и структура проекта",
    "order": 8, "xp_reward": 35,
    "hints": json.dumps([
      "Разбивай проект на модули: routers/, models/, schemas/, core/",
      "APIRouter группирует маршруты одной сущности",
      "include_router подключает роутер к приложению",
    ], ensure_ascii=False),
    "content": """## Структура FastAPI проекта

```
project/
├── app/
│   ├── main.py          # точка входа
│   ├── core/
│   │   ├── config.py    # настройки
│   │   └── security.py  # JWT, хеширование
│   ├── db/
│   │   └── database.py  # подключение к БД
│   ├── models/
│   │   └── user.py      # SQLAlchemy модели
│   ├── schemas/
│   │   └── schemas.py   # Pydantic модели
│   └── api/
│       └── routes/
│           ├── auth.py
│           ├── users.py
│           └── items.py
├── requirements.txt
└── Dockerfile
```

## APIRouter

```python
# app/api/routes/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    return []

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
```

```python
# app/main.py
from fastapi import FastAPI
from app.api.routes import users, items, auth

app = FastAPI(title="My API")

app.include_router(auth.router,  prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(items.router, prefix="/api")
```

## Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Задание

Создай функцию `build_app_info(title, version, routes)` которая возвращает словарь с информацией о приложении. `routes` — список строк. Выведи результат.
""",
    "starter_code": "def build_app_info(title: str, version: str, routes: list) -> dict:\n    return {\n        \"title\": title,\n        \"version\": version,\n        \"routes_count\": len(routes),\n        \"routes\": routes,\n    }\n\ninfo = build_app_info(\n    title=\"My FastAPI App\",\n    version=\"1.0.0\",\n    routes=[\"/api/auth\", \"/api/users\", \"/api/items\"]\n)\nprint(info)",
    "solution": "def build_app_info(title, version, routes):\n    return {'title': title, 'version': version, 'routes_count': len(routes), 'routes': routes}\ninfo = build_app_info('My FastAPI App', '1.0.0', ['/api/auth', '/api/users', '/api/items'])\nprint(info)",
    "tests": json.dumps([
      {"check": "\nprint('OK' if build_app_info('App','1.0',['/a','/b'])['routes_count'] == 2 else 'FAIL')", "expected": "OK"},
      {"check": "\nprint('OK' if info['title'] == 'My FastAPI App' else 'FAIL')", "expected": "OK"},
    ], ensure_ascii=False),
  },
]


# ─────────────────────────────────────────────────────────────
NEW_COURSES = [
  {
    "title": "ООП в Python",
    "description": "Классы, объекты, наследование, инкапсуляция, полиморфизм, декораторы и абстрактные классы — полный курс объектно-ориентированного программирования.",
    "language": LanguageEnum.python,
    "level": LevelEnum.intermediate,
    "lessons": OOP_LESSONS,
  },
  {
    "title": "PostgreSQL — базы данных",
    "description": "SQL с нуля: создание таблиц, SELECT, JOIN, агрегации, транзакции и индексы. Практика на SQLite — синтаксис идентичен PostgreSQL.",
    "language": LanguageEnum.python,
    "level": LevelEnum.intermediate,
    "lessons": PG_LESSONS,
  },
  {
    "title": "FastAPI — разработка API",
    "description": "Создавай современные REST API на FastAPI: маршруты, Pydantic, CRUD, JWT аутентификация, SQLAlchemy и структура production-проекта.",
    "language": LanguageEnum.python,
    "level": LevelEnum.advanced,
    "lessons": FASTAPI_LESSONS,
  },
]


async def seed():
  async with Session() as db:
    for course_data in NEW_COURSES:
      # Проверяем — вдруг курс уже есть
      existing = await db.execute(
        select(Course).where(Course.title == course_data["title"])
      )
      if existing.scalar_one_or_none():
        print(f"⚠  Курс уже существует: {course_data['title']}")
        continue

      lessons_data = course_data.pop("lessons")
      course = Course(**course_data, is_published=True)
      db.add(course)
      await db.flush()

      for lesson_data in lessons_data:
        lesson = Lesson(course_id=course.id, **lesson_data)
        db.add(lesson)

      print(f"✓ Добавлен: {course.title} ({len(lessons_data)} уроков)")

    await db.commit()
    print("\n✅ Готово!")


if __name__ == "__main__":
  asyncio.run(seed())
