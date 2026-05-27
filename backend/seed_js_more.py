"""
Добавляет уроки 6-13 в курс "JavaScript основы".
Запуск: docker exec codelearn-backend-1 python seed_js_more.py
"""
import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.user import Course, Lesson

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

NEW_LESSONS = [
    {
        "title": "Циклы: for, while, for...of",
        "order": 6, "xp_reward": 20,
        "content": """## Цикл for

```javascript
for (let i = 0; i < 5; i++) {
  console.log(i); // 0 1 2 3 4
}
```

## Цикл while

Выполняется пока условие `true`:

```javascript
let count = 0;
while (count < 3) {
  console.log(count);
  count++;
}
```

## Цикл for...of

Удобен для перебора массивов:

```javascript
const fruits = ["яблоко", "банан", "вишня"];
for (const fruit of fruits) {
  console.log(fruit);
}
```

## break и continue

```javascript
for (let i = 0; i < 10; i++) {
  if (i === 3) continue; // пропустить 3
  if (i === 6) break;    // остановиться на 6
  console.log(i);
}
// 0 1 2 4 5
```

## Задание

Выведи все чётные числа от 1 до 10 с помощью цикла `for`.
""",
        "starter_code": "for (let i = 1; i <= 10; i++) {\n  if (i % 2 === 0) {\n    console.log(i);\n  }\n}",
        "solution": "for (let i = 2; i <= 10; i += 2) {\n  console.log(i);\n}",
        "tests": "[]",
        "hints": json.dumps([
            "Чётное число делится на 2 без остатка: i % 2 === 0",
            "Можно начать i с 2 и прибавлять 2: i += 2",
            "Или проверять условие внутри цикла через if"
        ]),
    },
    {
        "title": "Объекты",
        "order": 7, "xp_reward": 20,
        "content": """## Что такое объект?

Объект хранит данные в виде пар **ключ: значение**:

```javascript
const person = {
  name: "Алекс",
  age: 25,
  city: "Алматы"
};
```

## Доступ к свойствам

```javascript
console.log(person.name);       // Алекс
console.log(person["age"]);     // 25
```

## Изменение и добавление

```javascript
person.age = 26;              // изменить
person.email = "a@b.com";    // добавить
delete person.city;           // удалить
```

## Методы объекта

```javascript
const user = {
  name: "Мария",
  greet() {
    return `Привет, я ${this.name}!`;
  }
};

console.log(user.greet()); // Привет, я Мария!
```

## Object.keys / values / entries

```javascript
const car = { brand: "Toyota", year: 2020 };

console.log(Object.keys(car));    // ["brand", "year"]
console.log(Object.values(car));  // ["Toyota", 2020]
console.log(Object.entries(car)); // [["brand","Toyota"],["year",2020]]
```

## Задание

Создай объект `book` с полями `title`, `author`, `year`. Выведи все значения через `Object.values()`.
""",
        "starter_code": 'const book = {\n  title: "Мастер и Маргарита",\n  author: "Булгаков",\n  year: 1967\n};\n\nconsole.log(Object.values(book));',
        "solution": 'const book = { title: "Мастер и Маргарита", author: "Булгаков", year: 1967 };\nconsole.log(Object.values(book));',
        "tests": "[]",
        "hints": json.dumps([
            "Объект создаётся через фигурные скобки {}",
            "Object.values(obj) возвращает массив всех значений",
            "Доступ к свойству: book.title или book['title']"
        ]),
    },
    {
        "title": "Деструктуризация",
        "order": 8, "xp_reward": 25,
        "content": """## Деструктуризация объектов

Позволяет «распаковать» свойства объекта в переменные:

```javascript
const person = { name: "Алекс", age: 25, city: "Алматы" };

// Без деструктуризации:
const name = person.name;
const age  = person.age;

// С деструктуризацией:
const { name, age } = person;
console.log(name, age); // Алекс 25
```

## Переименование

```javascript
const { name: userName, age: userAge } = person;
console.log(userName); // Алекс
```

## Значения по умолчанию

```javascript
const { name, country = "Казахстан" } = person;
console.log(country); // Казахстан
```

## Деструктуризация массивов

```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
console.log(first);  // 1
console.log(second); // 2
console.log(rest);   // [3, 4, 5]
```

## В параметрах функции

```javascript
function greet({ name, age }) {
  console.log(`${name}, ${age} лет`);
}

greet({ name: "Мария", age: 22 }); // Мария, 22 лет
```

## Задание

Деструктурируй объект `{ brand: "Nike", size: 42, color: "black" }` и выведи каждое поле отдельно.
""",
        "starter_code": 'const shoe = { brand: "Nike", size: 42, color: "black" };\n\nconst { brand, size, color } = shoe;\nconsole.log(brand);\nconsole.log(size);\nconsole.log(color);',
        "solution": 'const shoe = { brand: "Nike", size: 42, color: "black" };\nconst { brand, size, color } = shoe;\nconsole.log(brand);\nconsole.log(size);\nconsole.log(color);',
        "tests": "[]",
        "hints": json.dumps([
            "Деструктуризация: const { field1, field2 } = object",
            "Имена переменных должны совпадать с ключами объекта",
            "Можно переименовать: const { brand: name } = shoe"
        ]),
    },
    {
        "title": "Spread и Rest операторы",
        "order": 9, "xp_reward": 25,
        "content": """## Spread оператор `...`

Разворачивает массив или объект:

```javascript
// Копирование массива
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5]; // [1, 2, 3, 4, 5]

// Объединение массивов
const merged = [...arr1, ...arr2];

// Копирование объекта
const original = { a: 1, b: 2 };
const copy = { ...original, c: 3 }; // { a:1, b:2, c:3 }
```

## Rest параметры

Собирает оставшиеся аргументы в массив:

```javascript
function sum(...numbers) {
  return numbers.reduce((acc, n) => acc + n, 0);
}

console.log(sum(1, 2, 3, 4)); // 10
console.log(sum(10, 20));     // 30
```

## Практический пример

```javascript
// Добавить элемент в массив (без мутации)
const todos = ["купить хлеб", "позвонить маме"];
const newTodos = [...todos, "сходить в зал"];

// Обновить объект (без мутации)
const user = { name: "Алекс", age: 25 };
const updated = { ...user, age: 26 };
```

## Задание

Напиши функцию `multiply(factor, ...nums)` которая умножает каждый из чисел на `factor` и выводит результат.
""",
        "starter_code": "function multiply(factor, ...nums) {\n  const result = nums.map(n => n * factor);\n  console.log(result);\n}\n\nmultiply(2, 1, 2, 3, 4); // [2, 4, 6, 8]",
        "solution": "function multiply(factor, ...nums) {\n  console.log(nums.map(n => n * factor));\n}\nmultiply(2, 1, 2, 3, 4);",
        "tests": "[]",
        "hints": json.dumps([
            "Rest параметр ...nums собирает все аргументы после factor в массив",
            "Используй .map() чтобы умножить каждый элемент",
            "Spread (...) и Rest (...) выглядят одинаково но используются по-разному"
        ]),
    },
    {
        "title": "Замыкания",
        "order": 10, "xp_reward": 30,
        "content": """## Что такое замыкание?

Замыкание — это функция, которая «запоминает» переменные из внешней области видимости даже после того, как внешняя функция завершила работу.

```javascript
function makeCounter() {
  let count = 0;           // переменная внешней функции

  return function() {      // внутренняя функция
    count++;
    return count;
  };
}

const counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
```

Переменная `count` «замкнута» внутри и недоступна снаружи.

## Практический пример — фабрика функций

```javascript
function multiply(factor) {
  return (number) => number * factor;
}

const double = multiply(2);
const triple = multiply(3);

console.log(double(5));  // 10
console.log(triple(5));  // 15
```

## Приватные данные

```javascript
function createAccount(initialBalance) {
  let balance = initialBalance;  // приватное!

  return {
    deposit: (amount) => { balance += amount; },
    withdraw: (amount) => { balance -= amount; },
    getBalance: () => balance,
  };
}

const acc = createAccount(100);
acc.deposit(50);
console.log(acc.getBalance()); // 150
```

## Задание

Напиши функцию `makeAdder(x)` которая возвращает функцию, прибавляющую `x` к аргументу. Выведи `makeAdder(5)(3)`.
""",
        "starter_code": "function makeAdder(x) {\n  return function(y) {\n    return x + y;\n  };\n}\n\nconst add5 = makeAdder(5);\nconsole.log(add5(3));  // 8\nconsole.log(makeAdder(10)(7)); // 17",
        "solution": "function makeAdder(x) {\n  return (y) => x + y;\n}\nconsole.log(makeAdder(5)(3));",
        "tests": "[]",
        "hints": json.dumps([
            "makeAdder возвращает функцию (не значение)",
            "Внутренняя функция имеет доступ к x из внешней — это и есть замыкание",
            "makeAdder(5)(3) — сначала вызываем makeAdder(5), получаем функцию, потом вызываем её с (3)"
        ]),
    },
    {
        "title": "Промисы (Promise)",
        "order": 11, "xp_reward": 30,
        "content": """## Зачем нужны промисы?

JavaScript — однопоточный язык. Промисы позволяют работать с асинхронными операциями (запросы к серверу, чтение файлов) не блокируя выполнение кода.

## Создание промиса

```javascript
const promise = new Promise((resolve, reject) => {
  // асинхронная операция
  const success = true;

  if (success) {
    resolve("Данные получены!");
  } else {
    reject("Что-то пошло не так");
  }
});
```

## Использование .then() и .catch()

```javascript
promise
  .then(result => console.log(result))  // успех
  .catch(error => console.log(error))   // ошибка
  .finally(() => console.log("Готово")); // всегда
```

## Цепочка промисов

```javascript
fetch("https://api.example.com/users")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(err => console.log("Ошибка:", err));
```

## Promise.all — ждём несколько промисов

```javascript
const p1 = Promise.resolve(1);
const p2 = Promise.resolve(2);
const p3 = Promise.resolve(3);

Promise.all([p1, p2, p3]).then(values => {
  console.log(values); // [1, 2, 3]
});
```

## Задание

Создай промис который через «задержку» (setTimeout 1000мс) выдаёт строку `"Готово!"`. Выведи результат через `.then()`.
""",
        "starter_code": "const myPromise = new Promise((resolve) => {\n  setTimeout(() => {\n    resolve(\"Готово!\");\n  }, 1000);\n});\n\nmyPromise.then(result => {\n  console.log(result); // Готово!\n});",
        "solution": "const p = new Promise(resolve => setTimeout(() => resolve('Готово!'), 1000));\np.then(r => console.log(r));",
        "tests": "[]",
        "hints": json.dumps([
            "new Promise принимает функцию с двумя параметрами: resolve и reject",
            "setTimeout(fn, 1000) вызывает fn через 1 секунду",
            "resolve('значение') — передаёт значение в .then()"
        ]),
    },
    {
        "title": "async / await",
        "order": 12, "xp_reward": 30,
        "content": """## Что такое async/await?

`async/await` — более читаемый способ работы с промисами. Вместо цепочки `.then()` код выглядит как синхронный.

## async функция

```javascript
async function getData() {
  return "Данные";  // автоматически оборачивается в Promise
}

getData().then(data => console.log(data)); // Данные
```

## await

`await` останавливает выполнение функции до завершения промиса:

```javascript
async function fetchUser() {
  const response = await fetch("https://api.example.com/user/1");
  const user = await response.json();
  console.log(user.name);
}
```

## Обработка ошибок

```javascript
async function loadData() {
  try {
    const data = await somePromise();
    console.log(data);
  } catch (error) {
    console.log("Ошибка:", error);
  }
}
```

## Сравнение: промисы vs async/await

```javascript
// Промисы
getUser()
  .then(user => getPosts(user.id))
  .then(posts => console.log(posts))
  .catch(err => console.log(err));

// async/await — то же самое, но читабельнее
async function load() {
  try {
    const user  = await getUser();
    const posts = await getPosts(user.id);
    console.log(posts);
  } catch (err) {
    console.log(err);
  }
}
```

## Задание

Напиши `async` функцию `delay(ms)` которая ждёт `ms` миллисекунд (через Promise + setTimeout) и возвращает `"Прошло " + ms + " мс"`. Вызови её с `await`.
""",
        "starter_code": "function wait(ms) {\n  return new Promise(resolve => setTimeout(resolve, ms));\n}\n\nasync function delay(ms) {\n  await wait(ms);\n  return `Прошло ${ms} мс`;\n}\n\nasync function main() {\n  const result = await delay(500);\n  console.log(result);\n}\n\nmain();",
        "solution": "function wait(ms) { return new Promise(r => setTimeout(r, ms)); }\nasync function delay(ms) { await wait(ms); return `Прошло ${ms} мс`; }\nasync function main() { console.log(await delay(500)); }\nmain();",
        "tests": "[]",
        "hints": json.dumps([
            "async функция всегда возвращает Promise",
            "await можно использовать только внутри async функции",
            "Оберни вызов в async main() { ... } и вызови main()"
        ]),
    },
    {
        "title": "Классы (ES6)",
        "order": 13, "xp_reward": 35,
        "content": """## Классы в JavaScript

Классы — синтаксический сахар над прототипным наследованием ES5:

```javascript
class Animal {
  constructor(name, sound) {
    this.name  = name;
    this.sound = sound;
  }

  speak() {
    console.log(`${this.name} говорит: ${this.sound}!`);
  }
}

const dog = new Animal("Собака", "Гав");
dog.speak(); // Собака говорит: Гав!
```

## Наследование

```javascript
class Dog extends Animal {
  constructor(name) {
    super(name, "Гав");  // вызов конструктора родителя
  }

  fetch() {
    console.log(`${this.name} приносит мяч!`);
  }
}

const rex = new Dog("Рекс");
rex.speak();  // Рекс говорит: Гав!
rex.fetch();  // Рекс приносит мяч!
```

## Геттеры и сеттеры

```javascript
class Circle {
  constructor(radius) {
    this._radius = radius;
  }

  get area() {
    return Math.PI * this._radius ** 2;
  }

  set radius(value) {
    if (value < 0) throw new Error("Радиус не может быть отрицательным");
    this._radius = value;
  }
}

const c = new Circle(5);
console.log(c.area.toFixed(2)); // 78.54
```

## Статические методы

```javascript
class MathHelper {
  static add(a, b) { return a + b; }
}

console.log(MathHelper.add(3, 4)); // 7
```

## Задание

Создай класс `Rectangle` с полями `width` и `height`. Добавь метод `area()` который возвращает площадь, и метод `perimeter()` который возвращает периметр.
""",
        "starter_code": "class Rectangle {\n  constructor(width, height) {\n    this.width = width;\n    this.height = height;\n  }\n\n  area() {\n    return this.width * this.height;\n  }\n\n  perimeter() {\n    return 2 * (this.width + this.height);\n  }\n}\n\nconst rect = new Rectangle(5, 3);\nconsole.log('Площадь:', rect.area());       // 15\nconsole.log('Периметр:', rect.perimeter()); // 16",
        "solution": "class Rectangle {\n  constructor(w, h) { this.width = w; this.height = h; }\n  area() { return this.width * this.height; }\n  perimeter() { return 2 * (this.width + this.height); }\n}\nconst r = new Rectangle(5, 3);\nconsole.log(r.area(), r.perimeter());",
        "tests": "[]",
        "hints": json.dumps([
            "constructor() вызывается при создании объекта через new",
            "Площадь прямоугольника: width * height",
            "Периметр: 2 * (width + height)"
        ]),
    },
]


async def seed():
    async with Session() as db:
        result = await db.execute(
            select(Course).where(Course.title == "JavaScript основы")
        )
        course = result.scalar_one_or_none()
        if not course:
            print("❌ Курс 'JavaScript основы' не найден")
            return

        existing = await db.execute(
            select(Lesson).where(Lesson.course_id == course.id)
        )
        existing_orders = {l.order for l in existing.scalars().all()}

        added = 0
        for data in NEW_LESSONS:
            if data["order"] in existing_orders:
                print(f"  — Урок {data['order']} уже есть, пропускаем")
                continue
            lesson = Lesson(course_id=course.id, **data)
            db.add(lesson)
            added += 1

        await db.commit()
        print(f"✅ Добавлено {added} уроков в '{course.title}'")


if __name__ == "__main__":
    asyncio.run(seed())
