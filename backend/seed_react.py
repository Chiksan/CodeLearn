"""
Курс React основы — 8 уроков с живым превью в браузере.
Запуск: docker exec codelearn-backend-1 python seed_react.py
"""
import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.user import Course, Lesson, LanguageEnum, LevelEnum

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

REACT_CDN = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; margin: 0; }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">"""

REACT_CDN_END = """
  </script>
</body>
</html>"""


def make_starter(jsx_code: str) -> str:
    return REACT_CDN + "\n" + jsx_code + "\n" + REACT_CDN_END


REACT_LESSONS = [
    {
        "title": "Знакомство с React",
        "order": 1,
        "xp_reward": 10,
        "content": """## Что такое React?

React — это библиотека JavaScript для создания пользовательских интерфейсов. Её разработала компания Meta (Facebook).

## Почему React?

- **Компонентный подход** — интерфейс разбивается на маленькие переиспользуемые части
- **Быстрое обновление** — React сам решает что перерисовать
- **Огромная экосистема** — миллионы библиотек и компонентов

## Первый компонент

Компонент — это просто функция, которая возвращает JSX (похожий на HTML):

```jsx
function App() {
  return <h1>Привет, React!</h1>;
}
```

## Рендеринг

Чтобы показать компонент на странице:

```jsx
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
```

## Задание

Измени текст внутри `<h1>` на `"Привет, [твоё имя]!"` и посмотри результат в превью.
""",
        "starter_code": make_starter("""    function App() {
      return <h1>Привет, React!</h1>;
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": make_starter("""    function App() {
      return <h1>Привет, Алекс!</h1>;
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Компонент — это просто функция которая возвращает JSX",
            "Измени текст внутри тегов <h1>...</h1>",
            "Не забудь что JSX похож на HTML — используй обычные теги"
        ]),
    },
    {
        "title": "JSX — HTML внутри JavaScript",
        "order": 2,
        "xp_reward": 15,
        "content": """## Что такое JSX?

JSX — это специальный синтаксис, который позволяет писать HTML прямо внутри JavaScript:

```jsx
const element = <h1>Привет!</h1>;
```

## Правила JSX

**1. Один корневой элемент:**
```jsx
// ❌ Ошибка — два корневых элемента
return <h1>Заголовок</h1><p>Текст</p>

// ✅ Правильно — оборачиваем в div или <>
return (
  <div>
    <h1>Заголовок</h1>
    <p>Текст</p>
  </div>
)
```

**2. Выражения в фигурных скобках:**
```jsx
const name = "Алекс";
return <h1>Привет, {name}!</h1>;
```

**3. `className` вместо `class`:**
```jsx
<div className="container">...</div>
```

## Задание

Создай компонент с заголовком `<h1>` и абзацем `<p>` внутри одного `<div>`.
""",
        "starter_code": make_starter("""    function App() {
      const name = "React";

      return (
        <div>
          <h1>Добро пожаловать в {name}!</h1>
          <p>Это мой первый компонент с несколькими элементами.</p>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": make_starter("""    function App() {
      const name = "React";
      return (
        <div>
          <h1>Добро пожаловать в {name}!</h1>
          <p>Изучаем JSX синтаксис.</p>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "В JSX нужен один корневой элемент — оберни всё в <div>",
            "Переменные вставляются через фигурные скобки: {name}",
            "JSX нужно обернуть в скобки () если он занимает несколько строк"
        ]),
    },
    {
        "title": "Props — передача данных",
        "order": 3,
        "xp_reward": 20,
        "content": """## Что такое Props?

Props (properties) — это способ передать данные в компонент. Как атрибуты в HTML, только для React-компонентов.

## Передача props

```jsx
function Greeting({ name }) {
  return <h2>Привет, {name}!</h2>;
}

// Использование:
<Greeting name="Алекс" />
<Greeting name="Мария" />
```

## Несколько props

```jsx
function UserCard({ name, age, city }) {
  return (
    <div>
      <h3>{name}</h3>
      <p>Возраст: {age}</p>
      <p>Город: {city}</p>
    </div>
  );
}

<UserCard name="Алекс" age={25} city="Алматы" />
```

## Props по умолчанию

```jsx
function Button({ text = "Нажми меня" }) {
  return <button>{text}</button>;
}
```

## Задание

Создай компонент `Card` с props `title` и `description`. Покажи две карточки с разными данными.
""",
        "starter_code": make_starter("""    function Card({ title, description }) {
      return (
        <div style={{ border: '1px solid #ddd', padding: '16px', borderRadius: '8px', marginBottom: '12px' }}>
          <h3 style={{ margin: '0 0 8px' }}>{title}</h3>
          <p style={{ margin: 0, color: '#666' }}>{description}</p>
        </div>
      );
    }

    function App() {
      return (
        <div>
          <Card title="React" description="Библиотека для создания интерфейсов" />
          <Card title="JavaScript" description="Язык программирования для веба" />
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": make_starter("""    function Card({ title, description }) {
      return (
        <div style={{ border: '1px solid #ddd', padding: '16px', borderRadius: '8px', marginBottom: '12px' }}>
          <h3>{title}</h3>
          <p style={{ color: '#666' }}>{description}</p>
        </div>
      );
    }

    function App() {
      return (
        <div>
          <Card title="Python" description="Язык для науки о данных" />
          <Card title="React" description="Библиотека для интерфейсов" />
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Props передаются как атрибуты: <Card title='...' />",
            "Принимают props через деструктуризацию: function Card({ title, description })",
            "Внутри JSX props используются в фигурных скобках: {title}"
        ]),
    },
    {
        "title": "useState — состояние компонента",
        "order": 4,
        "xp_reward": 25,
        "content": """## Что такое состояние?

Состояние (state) — это данные компонента, которые могут меняться. При изменении state React автоматически перерисовывает компонент.

## useState

```jsx
import { useState } — не нужен в CDN-версии, useState доступен как React.useState

const [count, setCount] = React.useState(0);
```

- `count` — текущее значение
- `setCount` — функция для изменения
- `0` — начальное значение

## Пример — счётчик

```jsx
function Counter() {
  const [count, setCount] = React.useState(0);

  return (
    <div>
      <p>Счёт: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(count - 1)}>-1</button>
    </div>
  );
}
```

## Задание

Создай счётчик с кнопками `+` и `-`. Добавь кнопку `Сброс` которая возвращает счёт к 0.
""",
        "starter_code": make_starter("""    function Counter() {
      const [count, setCount] = React.useState(0);

      return (
        <div style={{ textAlign: 'center', marginTop: '40px' }}>
          <h2 style={{ fontSize: '48px', margin: '0 0 20px' }}>{count}</h2>
          <button onClick={() => setCount(count - 1)}
            style={{ padding: '10px 24px', fontSize: '20px', marginRight: '8px', cursor: 'pointer' }}>
            −
          </button>
          <button onClick={() => setCount(0)}
            style={{ padding: '10px 24px', fontSize: '16px', marginRight: '8px', cursor: 'pointer' }}>
            Сброс
          </button>
          <button onClick={() => setCount(count + 1)}
            style={{ padding: '10px 24px', fontSize: '20px', cursor: 'pointer' }}>
            +
          </button>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Counter />);"""),
        "solution": make_starter("""    function Counter() {
      const [count, setCount] = React.useState(0);
      return (
        <div style={{ textAlign: 'center', marginTop: '40px' }}>
          <h2 style={{ fontSize: '48px' }}>{count}</h2>
          <button onClick={() => setCount(count - 1)}>−</button>
          <button onClick={() => setCount(0)}>Сброс</button>
          <button onClick={() => setCount(count + 1)}>+</button>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Counter />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "useState возвращает массив: [значение, функция_изменения]",
            "Чтобы изменить state вызови setCount(новое_значение)",
            "Для сброса: setCount(0) вернёт счёт к начальному значению"
        ]),
    },
    {
        "title": "Обработка событий",
        "order": 5,
        "xp_reward": 25,
        "content": """## События в React

React использует те же события что и HTML, но в camelCase:

| HTML | React |
|------|-------|
| `onclick` | `onClick` |
| `onchange` | `onChange` |
| `onsubmit` | `onSubmit` |
| `onmouseover` | `onMouseOver` |

## Обработчик события

```jsx
function Button() {
  const handleClick = () => {
    alert("Кнопка нажата!");
  };

  return <button onClick={handleClick}>Нажми меня</button>;
}
```

## Работа с input

```jsx
function Form() {
  const [text, setText] = React.useState("");

  return (
    <div>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Введи текст..."
      />
      <p>Ты написал: {text}</p>
    </div>
  );
}
```

## Задание

Создай поле ввода имени. При вводе — показывай приветствие `"Привет, [имя]!"`.
""",
        "starter_code": make_starter("""    function Greeter() {
      const [name, setName] = React.useState("");

      return (
        <div style={{ padding: '20px' }}>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Введи своё имя..."
            style={{ padding: '10px', fontSize: '16px', width: '220px', borderRadius: '6px', border: '1px solid #ccc' }}
          />
          {name && (
            <h2 style={{ marginTop: '20px', color: '#534AB7' }}>
              Привет, {name}!
            </h2>
          )}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Greeter />);"""),
        "solution": make_starter("""    function Greeter() {
      const [name, setName] = React.useState("");
      return (
        <div style={{ padding: '20px' }}>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Введи своё имя..."
            style={{ padding: '10px', fontSize: '16px' }}
          />
          {name && <h2>Привет, {name}!</h2>}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Greeter />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "onChange получает событие e, текст находится в e.target.value",
            "Храни введённый текст в state через useState",
            "Условный рендеринг: {name && <h2>...</h2>} покажет элемент только если name не пустой"
        ]),
    },
    {
        "title": "Списки и ключи",
        "order": 6,
        "xp_reward": 25,
        "content": """## Рендеринг списков

Используй метод `.map()` чтобы отрисовать массив данных:

```jsx
const fruits = ["Яблоко", "Банан", "Вишня"];

function FruitList() {
  return (
    <ul>
      {fruits.map((fruit, index) => (
        <li key={index}>{fruit}</li>
      ))}
    </ul>
  );
}
```

## Зачем нужен key?

React использует `key` чтобы отслеживать какие элементы изменились. Без `key` будет предупреждение.

Лучше использовать уникальный ID вместо индекса:

```jsx
const users = [
  { id: 1, name: "Алекс" },
  { id: 2, name: "Мария" },
];

{users.map(user => (
  <div key={user.id}>{user.name}</div>
))}
```

## Задание

Создай список задач из массива. Отобрази каждую задачу как `<li>` с порядковым номером.
""",
        "starter_code": make_starter("""    const tasks = [
      { id: 1, text: "Изучить React" },
      { id: 2, text: "Сделать проект" },
      { id: 3, text: "Написать резюме" },
      { id: 4, text: "Получить оффер" },
    ];

    function TaskList() {
      return (
        <div style={{ padding: '20px' }}>
          <h2>📋 Мои задачи</h2>
          <ol>
            {tasks.map(task => (
              <li key={task.id} style={{ marginBottom: '8px', fontSize: '16px' }}>
                {task.text}
              </li>
            ))}
          </ol>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<TaskList />);"""),
        "solution": make_starter("""    const tasks = [
      { id: 1, text: "Изучить React" },
      { id: 2, text: "Сделать проект" },
    ];

    function TaskList() {
      return (
        <ul>
          {tasks.map(task => (
            <li key={task.id}>{task.text}</li>
          ))}
        </ul>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<TaskList />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Используй .map() для перебора массива и создания JSX-элементов",
            "Каждый элемент списка должен иметь уникальный атрибут key",
            "key лучше брать из id объекта: key={task.id}"
        ]),
    },
    {
        "title": "Условный рендеринг",
        "order": 7,
        "xp_reward": 30,
        "content": """## Условный рендеринг

React позволяет показывать разный контент в зависимости от условий.

## Способ 1 — оператор &&

```jsx
{isLoggedIn && <p>Добро пожаловать!</p>}
```
Элемент отображается только если условие `true`.

## Способ 2 — тернарный оператор

```jsx
{isLoggedIn
  ? <p>Ты вошёл в систему</p>
  : <p>Войди в аккаунт</p>
}
```

## Способ 3 — if внутри функции

```jsx
function Status({ online }) {
  if (online) {
    return <span style={{ color: 'green' }}>● Онлайн</span>;
  }
  return <span style={{ color: 'red' }}>● Оффлайн</span>;
}
```

## Задание

Создай компонент с кнопкой "Войти/Выйти". При нажатии меняй состояние и показывай разный текст.
""",
        "starter_code": make_starter("""    function LoginToggle() {
      const [isLoggedIn, setIsLoggedIn] = React.useState(false);

      return (
        <div style={{ padding: '24px', textAlign: 'center' }}>
          {isLoggedIn
            ? <h2 style={{ color: 'green' }}>✅ Добро пожаловать!</h2>
            : <h2 style={{ color: '#888' }}>🔒 Вы не вошли в систему</h2>
          }

          <button
            onClick={() => setIsLoggedIn(!isLoggedIn)}
            style={{
              marginTop: '16px',
              padding: '10px 28px',
              background: isLoggedIn ? '#e53e3e' : '#534AB7',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              fontSize: '15px',
              cursor: 'pointer'
            }}
          >
            {isLoggedIn ? 'Выйти' : 'Войти'}
          </button>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<LoginToggle />);"""),
        "solution": make_starter("""    function LoginToggle() {
      const [isLoggedIn, setIsLoggedIn] = React.useState(false);
      return (
        <div style={{ padding: '24px', textAlign: 'center' }}>
          {isLoggedIn ? <h2>Добро пожаловать!</h2> : <h2>Вы не вошли</h2>}
          <button onClick={() => setIsLoggedIn(!isLoggedIn)}>
            {isLoggedIn ? 'Выйти' : 'Войти'}
          </button>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<LoginToggle />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Используй useState для хранения состояния входа: true/false",
            "Тернарный оператор: {условие ? 'если да' : 'если нет'}",
            "!isLoggedIn инвертирует значение (true → false, false → true)"
        ]),
    },
    {
        "title": "Мини-проект: список задач",
        "order": 8,
        "xp_reward": 40,
        "content": """## Финальный проект — Todo List

Собери всё что изучил в один проект: список задач с добавлением и удалением.

Используем:
- `useState` — для списка задач и текста ввода
- `map()` — для рендеринга списка
- `onClick` / `onChange` — для событий
- Условный рендеринг — если список пустой

## Что должно работать:
1. Вводишь задачу в поле ввода
2. Нажимаешь кнопку "Добавить" — задача появляется в списке
3. Нажимаешь ✕ рядом с задачей — задача удаляется
4. Если список пустой — показывается сообщение

## Задание

Реализуй полноценный Todo List. Код уже частично готов — доделай функцию `removeTask`.
""",
        "starter_code": make_starter("""    function TodoApp() {
      const [tasks, setTasks] = React.useState(["Изучить React"]);
      const [input, setInput] = React.useState("");

      const addTask = () => {
        if (!input.trim()) return;
        setTasks([...tasks, input.trim()]);
        setInput("");
      };

      const removeTask = (index) => {
        // Удали задачу по индексу
        setTasks(tasks.filter((_, i) => i !== index));
      };

      return (
        <div style={{ maxWidth: '400px', margin: '20px auto', fontFamily: 'Arial' }}>
          <h2>📋 Todo List</h2>

          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && addTask()}
              placeholder="Новая задача..."
              style={{ flex: 1, padding: '8px 12px', borderRadius: '6px', border: '1px solid #ddd', fontSize: '14px' }}
            />
            <button
              onClick={addTask}
              style={{ padding: '8px 16px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
            >
              Добавить
            </button>
          </div>

          {tasks.length === 0
            ? <p style={{ color: '#aaa', textAlign: 'center' }}>Задач нет. Добавь первую!</p>
            : <ul style={{ listStyle: 'none', padding: 0 }}>
                {tasks.map((task, i) => (
                  <li key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: '#f8f8fc', borderRadius: '8px', marginBottom: '8px' }}>
                    <span>{task}</span>
                    <button
                      onClick={() => removeTask(i)}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#e53e3e', fontSize: '18px' }}
                    >
                      ✕
                    </button>
                  </li>
                ))}
              </ul>
          }
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<TodoApp />);"""),
        "solution": make_starter("""    function TodoApp() {
      const [tasks, setTasks] = React.useState([]);
      const [input, setInput] = React.useState("");

      const addTask = () => {
        if (!input.trim()) return;
        setTasks([...tasks, input.trim()]);
        setInput("");
      };

      const removeTask = (index) => {
        setTasks(tasks.filter((_, i) => i !== index));
      };

      return (
        <div style={{ maxWidth: '400px', margin: '20px auto' }}>
          <h2>Todo List</h2>
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Задача..." />
          <button onClick={addTask}>Добавить</button>
          <ul>
            {tasks.map((task, i) => (
              <li key={i}>{task} <button onClick={() => removeTask(i)}>✕</button></li>
            ))}
          </ul>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<TodoApp />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "addTask использует spread: [...tasks, новая_задача] — создаёт новый массив",
            "removeTask: tasks.filter((_, i) => i !== index) — оставляет все кроме удаляемого",
            "Для ввода по Enter: onKeyDown={(e) => e.key === 'Enter' && addTask()}"
        ]),
    },
]


async def seed():
    async with Session() as db:
        result = await db.execute(
            select(Course).where(Course.title == "React основы")
        )
        if result.scalar_one_or_none():
            print("⚠️  Курс 'React основы' уже существует, пропускаем.")
            return

        course = Course(
            title="React основы",
            description="Изучи React с нуля: компоненты, props, useState, события и списки. Каждый урок с живым превью в браузере.",
            language=LanguageEnum.javascript,
            level=LevelEnum.intermediate,
            order=2,
            is_published=True,
        )
        db.add(course)
        await db.flush()

        for lesson_data in REACT_LESSONS:
            lesson = Lesson(course_id=course.id, **lesson_data)
            db.add(lesson)

        await db.commit()
        print(f"✅ Курс 'React основы' добавлен — {len(REACT_LESSONS)} уроков")


if __name__ == "__main__":
    asyncio.run(seed())
