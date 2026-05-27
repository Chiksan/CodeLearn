"""
Курс "React: хуки и состояние" — intermediate, 10 уроков.
Запуск: docker exec codelearn-backend-1 python seed_react_intermediate.py
"""
import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.user import Course, Lesson, LanguageEnum, LevelEnum

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

CDN_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>body{font-family:Arial,sans-serif;padding:20px;margin:0}</style>
</head>
<body><div id="root"></div>
<script type="text/babel">"""

CDN_FOOT = "\n</script></body></html>"


def wrap(code): return CDN_HEAD + "\n" + code + CDN_FOOT


LESSONS = [
    {
        "title": "useEffect — побочные эффекты",
        "order": 1, "xp_reward": 25,
        "content": """## Что такое useEffect?

`useEffect` выполняет код **после рендера** компонента. Используется для:
- Запросов к API
- Подписок на события
- Работы с таймерами

## Синтаксис

```jsx
React.useEffect(() => {
  // код который выполнится после рендера
}, [зависимости]);
```

## Примеры зависимостей

```jsx
useEffect(() => { ... });          // каждый рендер
useEffect(() => { ... }, []);      // только при монтировании
useEffect(() => { ... }, [count]); // когда count меняется
```

## Пример — изменение заголовка

```jsx
function Counter() {
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    document.title = `Счёт: ${count}`;
  }, [count]);

  return <button onClick={() => setCount(c => c + 1)}>+1 (счёт: {count})</button>;
}
```

## Задание

Создай компонент с полем ввода. При каждом изменении текста выводи его длину через `useEffect`.
""",
        "starter_code": wrap("""    function TextAnalyzer() {
      const [text, setText] = React.useState("");
      const [len, setLen] = React.useState(0);

      React.useEffect(() => {
        setLen(text.length);
      }, [text]);

      return (
        <div>
          <h2>Анализатор текста</h2>
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="Введи текст..."
            style={{ width: '100%', height: '80px', padding: '8px', fontSize: '14px' }}
          />
          <p>Символов: <strong>{len}</strong></p>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<TextAnalyzer />);"""),
        "solution": wrap("""    function TextAnalyzer() {
      const [text, setText] = React.useState("");
      const [len, setLen] = React.useState(0);
      React.useEffect(() => { setLen(text.length); }, [text]);
      return (
        <div>
          <textarea value={text} onChange={e => setText(e.target.value)} />
          <p>Символов: {len}</p>
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<TextAnalyzer />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "useEffect принимает функцию и массив зависимостей",
            "[text] как зависимость — эффект сработает при каждом изменении text",
            "text.length возвращает количество символов"
        ]),
    },
    {
        "title": "useEffect — таймер и очистка",
        "order": 2, "xp_reward": 25,
        "content": """## Очистка эффектов

Некоторые эффекты нужно «убирать» при размонтировании компонента (утечки памяти):

```jsx
React.useEffect(() => {
  const timer = setInterval(() => {
    console.log("тик");
  }, 1000);

  return () => clearInterval(timer); // функция очистки
}, []);
```

Функция которую возвращает `useEffect` — это **cleanup** (очистка). Она вызывается перед следующим эффектом или при размонтировании.

## Пример — секундомер

```jsx
function Stopwatch() {
  const [seconds, setSeconds] = React.useState(0);
  const [running, setRunning] = React.useState(false);

  React.useEffect(() => {
    if (!running) return;

    const id = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);

    return () => clearInterval(id); // очищаем при остановке
  }, [running]);

  return (
    <div>
      <h2>{seconds} сек</h2>
      <button onClick={() => setRunning(r => !r)}>
        {running ? "Стоп" : "Старт"}
      </button>
    </div>
  );
}
```

## Задание

Реализуй секундомер с кнопками Старт/Стоп и Сброс. Код уже готов — изучи как работает cleanup.
""",
        "starter_code": wrap("""    function Stopwatch() {
      const [seconds, setSeconds] = React.useState(0);
      const [running, setRunning] = React.useState(false);

      React.useEffect(() => {
        if (!running) return;
        const id = setInterval(() => setSeconds(s => s + 1), 1000);
        return () => clearInterval(id);
      }, [running]);

      const reset = () => {
        setRunning(false);
        setSeconds(0);
      };

      return (
        <div style={{ textAlign: 'center', marginTop: '40px' }}>
          <div style={{ fontSize: '64px', fontWeight: 'bold', color: '#534AB7' }}>
            {String(Math.floor(seconds / 60)).padStart(2,'0')}:{String(seconds % 60).padStart(2,'0')}
          </div>
          <div style={{ marginTop: '20px', display: 'flex', gap: '12px', justifyContent: 'center' }}>
            <button
              onClick={() => setRunning(r => !r)}
              style={{ padding: '10px 28px', fontSize: '16px', background: running ? '#e53e3e' : '#27ae60', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
            >
              {running ? 'Стоп' : 'Старт'}
            </button>
            <button
              onClick={reset}
              style={{ padding: '10px 28px', fontSize: '16px', background: '#888', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
            >
              Сброс
            </button>
          </div>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Stopwatch />);"""),
        "solution": wrap("""    function Stopwatch() {
      const [seconds, setSeconds] = React.useState(0);
      const [running, setRunning] = React.useState(false);
      React.useEffect(() => {
        if (!running) return;
        const id = setInterval(() => setSeconds(s => s + 1), 1000);
        return () => clearInterval(id);
      }, [running]);
      return (
        <div>
          <h2>{seconds} сек</h2>
          <button onClick={() => setRunning(r => !r)}>{running ? 'Стоп' : 'Старт'}</button>
          <button onClick={() => { setRunning(false); setSeconds(0); }}>Сброс</button>
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<Stopwatch />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "return () => clearInterval(id) — это функция очистки, вызывается при остановке",
            "setSeconds(s => s + 1) — функциональное обновление, не требует зависимости",
            "Когда running меняется, эффект перезапускается с новым значением"
        ]),
    },
    {
        "title": "useRef — работа с DOM",
        "order": 3, "xp_reward": 25,
        "content": """## useRef

`useRef` создаёт «ссылку» на DOM-элемент или хранит значение которое не вызывает рендер при изменении.

## Доступ к DOM-элементу

```jsx
function AutoFocus() {
  const inputRef = React.useRef(null);

  React.useEffect(() => {
    inputRef.current.focus(); // ставим фокус при монтировании
  }, []);

  return <input ref={inputRef} placeholder="Фокус автоматически" />;
}
```

## Хранение значения без рендера

```jsx
function Timer() {
  const [count, setCount] = React.useState(0);
  const intervalRef = React.useRef(null);

  const start = () => {
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
  };

  const stop = () => clearInterval(intervalRef.current);

  return (
    <div>
      <p>{count}</p>
      <button onClick={start}>Старт</button>
      <button onClick={stop}>Стоп</button>
    </div>
  );
}
```

## Отличие от useState

| | useState | useRef |
|--|--|--|
| Вызывает рендер | ✅ | ❌ |
| Хранит значение | ✅ | ✅ |
| Доступ к DOM | ❌ | ✅ |

## Задание

Создай компонент с кнопкой «Сфокусировать». При нажатии — устанавливай фокус на поле ввода через `useRef`.
""",
        "starter_code": wrap("""    function FocusInput() {
      const inputRef = React.useRef(null);

      const handleFocus = () => {
        inputRef.current.focus();
      };

      return (
        <div style={{ padding: '20px' }}>
          <input
            ref={inputRef}
            placeholder="Нажми кнопку чтобы сфокусироваться..."
            style={{ padding: '10px', width: '280px', fontSize: '14px', borderRadius: '6px', border: '1px solid #ccc' }}
          />
          <br /><br />
          <button
            onClick={handleFocus}
            style={{ padding: '10px 24px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' }}
          >
            Сфокусировать
          </button>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<FocusInput />);"""),
        "solution": wrap("""    function FocusInput() {
      const inputRef = React.useRef(null);
      return (
        <div>
          <input ref={inputRef} placeholder="Фокус..." />
          <button onClick={() => inputRef.current.focus()}>Сфокусировать</button>
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<FocusInput />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "const ref = React.useRef(null) — создаём ссылку",
            "Добавь ref={inputRef} к элементу <input>",
            "inputRef.current — это сам DOM-элемент, у него есть метод .focus()"
        ]),
    },
    {
        "title": "useContext — глобальные данные",
        "order": 4, "xp_reward": 30,
        "content": """## Проблема: prop drilling

Когда нужно передать данные через много уровней компонентов — это неудобно:

```
App → Header → UserMenu → Avatar (нужен user)
```

Каждый компонент вынужден передавать `user` дальше даже если не использует.

## Решение: Context

```jsx
// 1. Создаём контекст
const ThemeContext = React.createContext("light");

// 2. Оборачиваем дерево в Provider
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Page />
    </ThemeContext.Provider>
  );
}

// 3. Читаем в любом дочернем компоненте
function Button() {
  const theme = React.useContext(ThemeContext);
  return <button className={theme}>Кнопка</button>;
}
```

## Задание

Реализуй переключатель темы (светлая/тёмная) через Context. При переключении меняй фон и цвет текста всей страницы.
""",
        "starter_code": wrap("""    const ThemeContext = React.createContext("light");

    function ThemedPage() {
      const theme = React.useContext(ThemeContext);
      const isDark = theme === "dark";

      return (
        <div style={{
          minHeight: '100vh',
          background: isDark ? '#1a1a2e' : '#fff',
          color: isDark ? '#eee' : '#111',
          padding: '32px',
          transition: 'all 0.3s',
          margin: '-20px'
        }}>
          <h1>Привет!</h1>
          <p>Текущая тема: <strong>{theme}</strong></p>
        </div>
      );
    }

    function App() {
      const [theme, setTheme] = React.useState("light");

      return (
        <ThemeContext.Provider value={theme}>
          <button
            onClick={() => setTheme(t => t === "light" ? "dark" : "light")}
            style={{ position: 'fixed', top: '16px', right: '16px', padding: '8px 16px', cursor: 'pointer', borderRadius: '8px', border: 'none', background: '#534AB7', color: '#fff' }}
          >
            Сменить тему
          </button>
          <ThemedPage />
        </ThemeContext.Provider>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    const ThemeContext = React.createContext("light");
    function Page() {
      const theme = React.useContext(ThemeContext);
      return <div style={{ background: theme === 'dark' ? '#222' : '#fff', color: theme === 'dark' ? '#fff' : '#000', padding: '20px' }}>Тема: {theme}</div>;
    }
    function App() {
      const [theme, setTheme] = React.useState("light");
      return (
        <ThemeContext.Provider value={theme}>
          <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>Переключить</button>
          <Page />
        </ThemeContext.Provider>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "React.createContext() создаёт объект контекста",
            "Provider передаёт значение: <Context.Provider value={...}>",
            "React.useContext(ThemeContext) читает текущее значение контекста"
        ]),
    },
    {
        "title": "useReducer — сложное состояние",
        "order": 5, "xp_reward": 30,
        "content": """## Когда useState не хватает?

Когда состояние сложное и обновляется по-разному — используй `useReducer`.

## Синтаксис

```jsx
const [state, dispatch] = React.useReducer(reducer, initialState);
```

- `reducer(state, action)` — чистая функция, возвращает новое состояние
- `dispatch({ type: "...", payload: ... })` — отправляет действие

## Пример — корзина

```jsx
const initialState = { items: [], total: 0 };

function cartReducer(state, action) {
  switch (action.type) {
    case "ADD":
      return {
        items: [...state.items, action.item],
        total: state.total + action.item.price,
      };
    case "CLEAR":
      return initialState;
    default:
      return state;
  }
}

function Cart() {
  const [cart, dispatch] = React.useReducer(cartReducer, initialState);

  return (
    <div>
      <button onClick={() => dispatch({ type: "ADD", item: { name: "Книга", price: 500 } })}>
        Добавить книгу
      </button>
      <p>Итого: {cart.total} тг</p>
    </div>
  );
}
```

## Задание

Реализуй счётчик через useReducer с действиями: increment, decrement, reset. Код уже настроен — изучи как работает reducer.
""",
        "starter_code": wrap("""    function reducer(state, action) {
      switch (action.type) {
        case 'increment': return { count: state.count + 1 };
        case 'decrement': return { count: state.count - 1 };
        case 'reset':     return { count: 0 };
        default: return state;
      }
    }

    function Counter() {
      const [state, dispatch] = React.useReducer(reducer, { count: 0 });

      return (
        <div style={{ textAlign: 'center', marginTop: '40px' }}>
          <h1 style={{ fontSize: '64px', color: '#534AB7' }}>{state.count}</h1>
          <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
            <button onClick={() => dispatch({ type: 'decrement' })}
              style={{ padding: '10px 24px', fontSize: '20px', cursor: 'pointer', borderRadius: '8px', border: '1px solid #ddd' }}>−</button>
            <button onClick={() => dispatch({ type: 'reset' })}
              style={{ padding: '10px 24px', fontSize: '14px', cursor: 'pointer', borderRadius: '8px', border: '1px solid #ddd' }}>Сброс</button>
            <button onClick={() => dispatch({ type: 'increment' })}
              style={{ padding: '10px 24px', fontSize: '20px', cursor: 'pointer', borderRadius: '8px', border: '1px solid #ddd' }}>+</button>
          </div>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Counter />);"""),
        "solution": wrap("""    function reducer(state, action) {
      switch (action.type) {
        case 'increment': return { count: state.count + 1 };
        case 'decrement': return { count: state.count - 1 };
        case 'reset': return { count: 0 };
        default: return state;
      }
    }
    function Counter() {
      const [state, dispatch] = React.useReducer(reducer, { count: 0 });
      return (
        <div>
          <h1>{state.count}</h1>
          <button onClick={() => dispatch({ type: 'decrement' })}>−</button>
          <button onClick={() => dispatch({ type: 'reset' })}>Сброс</button>
          <button onClick={() => dispatch({ type: 'increment' })}>+</button>
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<Counter />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "reducer(state, action) — принимает текущее состояние и действие, возвращает новое",
            "dispatch({ type: 'increment' }) — отправляет действие в reducer",
            "switch/case по action.type определяет как меняется состояние"
        ]),
    },
    {
        "title": "Кастомный хук useLocalStorage",
        "order": 6, "xp_reward": 35,
        "content": """## Зачем создавать свои хуки?

Кастомные хуки позволяют вынести логику из компонента и переиспользовать её.

Правило: название начинается с `use`.

## useLocalStorage

```jsx
function useLocalStorage(key, initialValue) {
  const [value, setValue] = React.useState(() => {
    try {
      const stored = localStorage.getItem(key);
      return stored ? JSON.parse(stored) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStored = (newValue) => {
    setValue(newValue);
    localStorage.setItem(key, JSON.stringify(newValue));
  };

  return [value, setStored];
}
```

## Использование

```jsx
function App() {
  const [name, setName] = useLocalStorage("username", "");

  return (
    <input
      value={name}
      onChange={e => setName(e.target.value)}
      placeholder="Введи имя (сохранится после перезагрузки)"
    />
  );
}
```

## Задание

Используй `useLocalStorage` чтобы сохранять заметку. После обновления страницы текст должен остаться.
""",
        "starter_code": wrap("""    function useLocalStorage(key, initialValue) {
      const [value, setValue] = React.useState(() => {
        try {
          const stored = localStorage.getItem(key);
          return stored ? JSON.parse(stored) : initialValue;
        } catch {
          return initialValue;
        }
      });

      const setStored = (newValue) => {
        setValue(newValue);
        localStorage.setItem(key, JSON.stringify(newValue));
      };

      return [value, setStored];
    }

    function NoteApp() {
      const [note, setNote] = useLocalStorage("my-note", "");

      return (
        <div style={{ padding: '20px' }}>
          <h2>📝 Моя заметка</h2>
          <p style={{ color: '#888', fontSize: '13px' }}>Текст сохраняется автоматически</p>
          <textarea
            value={note}
            onChange={e => setNote(e.target.value)}
            placeholder="Напиши что-нибудь..."
            style={{ width: '100%', height: '150px', padding: '12px', fontSize: '15px', borderRadius: '8px', border: '1px solid #ddd', resize: 'vertical', boxSizing: 'border-box' }}
          />
          <p style={{ fontSize: '13px', color: '#aaa' }}>Символов: {note.length}</p>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<NoteApp />);"""),
        "solution": wrap("""    function useLocalStorage(key, init) {
      const [val, setVal] = React.useState(() => {
        const s = localStorage.getItem(key);
        return s ? JSON.parse(s) : init;
      });
      const set = v => { setVal(v); localStorage.setItem(key, JSON.stringify(v)); };
      return [val, set];
    }
    function App() {
      const [note, setNote] = useLocalStorage("note", "");
      return <textarea value={note} onChange={e => setNote(e.target.value)} />;
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Кастомный хук — обычная функция, название начинается с use",
            "localStorage.getItem(key) — читает, localStorage.setItem(key, val) — сохраняет",
            "JSON.parse/JSON.stringify нужны для хранения объектов в localStorage"
        ]),
    },
    {
        "title": "Запросы к API",
        "order": 7, "xp_reward": 35,
        "content": """## Загрузка данных в React

Стандартный паттерн: `useEffect` + `fetch` + `useState` для данных и загрузки.

```jsx
function UserList() {
  const [users, setUsers] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []); // [] — только при монтировании

  if (loading) return <p>Загрузка...</p>;
  if (error)   return <p>Ошибка: {error}</p>;

  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}
```

## async/await вариант

```jsx
React.useEffect(() => {
  async function load() {
    const res  = await fetch("https://...");
    const data = await res.json();
    setUsers(data);
  }
  load();
}, []);
```

## Задание

Загрузи список постов с `https://jsonplaceholder.typicode.com/posts?_limit=5` и отобрази их заголовки. Добавь состояние загрузки.
""",
        "starter_code": wrap("""    function PostList() {
      const [posts, setPosts] = React.useState([]);
      const [loading, setLoading] = React.useState(true);
      const [error, setError] = React.useState(null);

      React.useEffect(() => {
        fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
          .then(res => res.json())
          .then(data => { setPosts(data); setLoading(false); })
          .catch(err => { setError(err.message); setLoading(false); });
      }, []);

      if (loading) return (
        <div style={{ padding: '20px', color: '#888' }}>⏳ Загрузка постов...</div>
      );

      if (error) return (
        <div style={{ padding: '20px', color: 'red' }}>❌ Ошибка: {error}</div>
      );

      return (
        <div style={{ padding: '20px' }}>
          <h2>📰 Последние посты</h2>
          {posts.map(post => (
            <div key={post.id} style={{ background: '#f8f8fc', padding: '14px', borderRadius: '8px', marginBottom: '10px' }}>
              <strong>#{post.id}</strong> {post.title}
            </div>
          ))}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<PostList />);"""),
        "solution": wrap("""    function PostList() {
      const [posts, setPosts] = React.useState([]);
      const [loading, setLoading] = React.useState(true);
      React.useEffect(() => {
        fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
          .then(r => r.json()).then(d => { setPosts(d); setLoading(false); });
      }, []);
      if (loading) return <p>Загрузка...</p>;
      return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<PostList />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "fetch возвращает Promise, используй .then(res => res.json()) для получения данных",
            "[] как зависимость useEffect — запрос выполнится только один раз при монтировании",
            "Показывай loading пока данные не пришли: if (loading) return <p>Загрузка...</p>"
        ]),
    },
    {
        "title": "Формы и валидация",
        "order": 8, "xp_reward": 30,
        "content": """## Контролируемые компоненты

В React форма управляется через state:

```jsx
function LoginForm() {
  const [form, setForm] = React.useState({ email: "", password: "" });
  const [errors, setErrors] = React.useState({});

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const validate = () => {
    const errs = {};
    if (!form.email.includes("@")) errs.email = "Некорректный email";
    if (form.password.length < 6)  errs.password = "Минимум 6 символов";
    return errs;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    alert("Форма отправлена!");
  };
}
```

## Задание

Создай форму регистрации с полями имя (мин. 2 символа), email и пароль (мин. 6 символов). При ошибках — показывай сообщения под полями.
""",
        "starter_code": wrap("""    function RegisterForm() {
      const [form, setForm] = React.useState({ name: '', email: '', password: '' });
      const [errors, setErrors] = React.useState({});
      const [submitted, setSubmitted] = React.useState(false);

      const handle = e => setForm({ ...form, [e.target.name]: e.target.value });

      const validate = () => {
        const errs = {};
        if (form.name.length < 2)        errs.name = 'Минимум 2 символа';
        if (!form.email.includes('@'))    errs.email = 'Некорректный email';
        if (form.password.length < 6)    errs.password = 'Минимум 6 символов';
        return errs;
      };

      const handleSubmit = e => {
        e.preventDefault();
        const errs = validate();
        setErrors(errs);
        if (Object.keys(errs).length === 0) setSubmitted(true);
      };

      if (submitted) return <div style={{ padding: '20px', color: 'green' }}>✅ Регистрация успешна!</div>;

      const inputStyle = { width: '100%', padding: '10px', marginTop: '4px', borderRadius: '6px', border: '1px solid #ddd', fontSize: '14px', boxSizing: 'border-box' };
      const errStyle = { color: '#e53e3e', fontSize: '12px', marginTop: '4px' };

      return (
        <form onSubmit={handleSubmit} style={{ maxWidth: '360px', padding: '24px' }}>
          <h2>Регистрация</h2>
          <div style={{ marginBottom: '16px' }}>
            <label>Имя</label>
            <input name="name" value={form.name} onChange={handle} style={inputStyle} />
            {errors.name && <p style={errStyle}>{errors.name}</p>}
          </div>
          <div style={{ marginBottom: '16px' }}>
            <label>Email</label>
            <input name="email" value={form.email} onChange={handle} style={inputStyle} />
            {errors.email && <p style={errStyle}>{errors.email}</p>}
          </div>
          <div style={{ marginBottom: '20px' }}>
            <label>Пароль</label>
            <input name="password" type="password" value={form.password} onChange={handle} style={inputStyle} />
            {errors.password && <p style={errStyle}>{errors.password}</p>}
          </div>
          <button type="submit" style={{ width: '100%', padding: '12px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '15px', cursor: 'pointer' }}>
            Зарегистрироваться
          </button>
        </form>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<RegisterForm />);"""),
        "solution": wrap("""    function Form() {
      const [form, setForm] = React.useState({ name: '', email: '', password: '' });
      const [errors, setErrors] = React.useState({});
      const handle = e => setForm({ ...form, [e.target.name]: e.target.value });
      const submit = e => {
        e.preventDefault();
        const errs = {};
        if (form.name.length < 2) errs.name = 'Мин. 2 символа';
        if (!form.email.includes('@')) errs.email = 'Некорректный email';
        if (form.password.length < 6) errs.password = 'Мин. 6 символов';
        setErrors(errs);
        if (!Object.keys(errs).length) alert('OK!');
      };
      return (
        <form onSubmit={submit}>
          <input name="name" value={form.name} onChange={handle} placeholder="Имя" />{errors.name && <span>{errors.name}</span>}
          <input name="email" value={form.email} onChange={handle} placeholder="Email" />{errors.email && <span>{errors.email}</span>}
          <input name="password" type="password" value={form.password} onChange={handle} placeholder="Пароль" />{errors.password && <span>{errors.password}</span>}
          <button>Отправить</button>
        </form>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<Form />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "[e.target.name]: e.target.value — обновляет конкретное поле по имени",
            "e.preventDefault() — отменяет стандартную отправку формы",
            "Object.keys(errs).length === 0 — проверяет что ошибок нет"
        ]),
    },
    {
        "title": "memo — оптимизация рендеров",
        "order": 9, "xp_reward": 35,
        "content": """## Проблема лишних рендеров

React перерисовывает компонент при каждом изменении родителя, даже если props не изменились.

```jsx
function Child({ name }) {
  console.log("Child отрендерился");
  return <p>{name}</p>;
}

function Parent() {
  const [count, setCount] = React.useState(0);
  // Child рендерится при каждом клике, хотя name не меняется!
  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      <Child name="Алекс" />
    </div>
  );
}
```

## React.memo

Мемоизирует компонент — перерисовывает только если props изменились:

```jsx
const Child = React.memo(function Child({ name }) {
  console.log("Child отрендерился");
  return <p>{name}</p>;
});
```

## useMemo — мемоизация значений

```jsx
const expensiveValue = React.useMemo(() => {
  return heavyCalculation(data);
}, [data]); // пересчитывается только когда data меняется
```

## useCallback — мемоизация функций

```jsx
const handleClick = React.useCallback(() => {
  doSomething(id);
}, [id]); // новая функция только когда id меняется
```

## Задание

Открой консоль (F12) и понаблюдай — Child перестаёт рендериться при изменении счётчика после добавления React.memo.
""",
        "starter_code": wrap("""    // Попробуй убрать React.memo и посмотреть в консоль
    const ExpensiveChild = React.memo(function ExpensiveChild({ color }) {
      console.log("ExpensiveChild отрендерился с цветом:", color);
      return (
        <div style={{ padding: '16px', background: color, borderRadius: '8px', marginTop: '12px', color: '#fff', fontWeight: 'bold' }}>
          Мой цвет: {color}
        </div>
      );
    });

    function App() {
      const [count, setCount] = React.useState(0);
      const [color, setColor] = React.useState('#534AB7');

      return (
        <div style={{ padding: '20px' }}>
          <h2>Демо React.memo</h2>
          <p>Счётчик: <strong>{count}</strong></p>
          <button onClick={() => setCount(c => c + 1)}
            style={{ padding: '8px 20px', marginRight: '8px', cursor: 'pointer', borderRadius: '6px', border: '1px solid #ddd' }}>
            +1 (не меняет color)
          </button>
          <button onClick={() => setColor(c => c === '#534AB7' ? '#e53e3e' : '#534AB7')}
            style={{ padding: '8px 20px', cursor: 'pointer', borderRadius: '6px', border: '1px solid #ddd' }}>
            Сменить цвет
          </button>

          <ExpensiveChild color={color} />
          <p style={{ color: '#888', fontSize: '13px', marginTop: '12px' }}>
            Открой консоль (F12) — Child рендерится только при смене цвета
          </p>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    const Child = React.memo(({ color }) => <div style={{ background: color, padding: '16px' }}>Цвет: {color}</div>);
    function App() {
      const [count, setCount] = React.useState(0);
      const [color, setColor] = React.useState('blue');
      return (
        <div>
          <button onClick={() => setCount(c => c + 1)}>{count}</button>
          <button onClick={() => setColor(c => c === 'blue' ? 'red' : 'blue')}>Цвет</button>
          <Child color={color} />
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "React.memo(Component) — оборачивает компонент для мемоизации",
            "Без memo — Child рендерится при каждом изменении родителя",
            "С memo — Child рендерится только когда его props меняются"
        ]),
    },
    {
        "title": "Мини-проект: заметки с localStorage",
        "order": 10, "xp_reward": 50,
        "content": """## Финальный проект курса

Собери все знания вместе: приложение для заметок с сохранением в `localStorage`.

## Что должно работать:
1. Добавлять новые заметки
2. Удалять заметки
3. Все заметки сохраняются в `localStorage` — не пропадают после перезагрузки
4. Показывать количество заметок
5. Пустой список — показывать соответствующее сообщение

## Используемые хуки:
- `useState` — для текста ввода
- `useLocalStorage` (кастомный) — для хранения заметок
- `useEffect` — опционально

## Задание

Изучи готовый код и добавь функцию **редактирования** заметки по двойному клику (`onDoubleClick`).
""",
        "starter_code": wrap("""    function useLocalStorage(key, init) {
      const [val, setVal] = React.useState(() => {
        try { const s = localStorage.getItem(key); return s ? JSON.parse(s) : init; }
        catch { return init; }
      });
      const set = v => { setVal(v); localStorage.setItem(key, JSON.stringify(v)); };
      return [val, set];
    }

    function NotesApp() {
      const [notes, setNotes] = useLocalStorage('react-notes', []);
      const [input, setInput] = React.useState('');

      const addNote = () => {
        if (!input.trim()) return;
        setNotes([{ id: Date.now(), text: input.trim() }, ...notes]);
        setInput('');
      };

      const deleteNote = id => setNotes(notes.filter(n => n.id !== id));

      return (
        <div style={{ maxWidth: '480px', margin: '0 auto', padding: '24px' }}>
          <h2>📝 Мои заметки <span style={{ fontSize: '14px', color: '#888', fontWeight: 'normal' }}>({notes.length})</span></h2>

          <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && addNote()}
              placeholder="Новая заметка..."
              style={{ flex: 1, padding: '10px 14px', borderRadius: '8px', border: '1px solid #ddd', fontSize: '14px' }}
            />
            <button onClick={addNote}
              style={{ padding: '10px 20px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer' }}>
              Добавить
            </button>
          </div>

          {notes.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#aaa' }}>
              <div style={{ fontSize: '40px' }}>📭</div>
              <p>Заметок пока нет</p>
            </div>
          ) : (
            notes.map(note => (
              <div key={note.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 16px', background: '#f8f8fc', borderRadius: '8px', marginBottom: '8px' }}>
                <span style={{ fontSize: '14px' }}>{note.text}</span>
                <button onClick={() => deleteNote(note.id)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#e53e3e', fontSize: '18px' }}>✕</button>
              </div>
            ))
          )}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<NotesApp />);"""),
        "solution": wrap("""    function useLS(key, init) {
      const [v, setV] = React.useState(() => { try { const s = localStorage.getItem(key); return s ? JSON.parse(s) : init; } catch { return init; } });
      const set = x => { setV(x); localStorage.setItem(key, JSON.stringify(x)); };
      return [v, set];
    }
    function App() {
      const [notes, setNotes] = useLS('notes', []);
      const [input, setInput] = React.useState('');
      const add = () => { if (!input.trim()) return; setNotes([{ id: Date.now(), text: input }, ...notes]); setInput(''); };
      return (
        <div>
          <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key==='Enter'&&add()} />
          <button onClick={add}>+</button>
          {notes.map(n => <div key={n.id}>{n.text} <button onClick={() => setNotes(notes.filter(x=>x.id!==n.id))}>✕</button></div>)}
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Date.now() генерирует уникальный id на основе текущего времени",
            "[новая, ...старые] — добавляет заметку в начало массива",
            "filter(n => n.id !== id) — создаёт новый массив без удалённой заметки"
        ]),
    },
]


async def seed():
    async with Session() as db:
        result = await db.execute(
            select(Course).where(Course.title == "React: хуки и состояние")
        )
        if result.scalar_one_or_none():
            print("⚠️  Курс уже существует")
            return

        course = Course(
            title="React: хуки и состояние",
            description="Глубокое погружение в хуки React: useEffect, useRef, useContext, useReducer и кастомные хуки. Работа с API, формами и оптимизацией.",
            language=LanguageEnum.javascript,
            level=LevelEnum.intermediate,
            order=3,
            is_published=True,
        )
        db.add(course)
        await db.flush()

        for data in LESSONS:
            db.add(Lesson(course_id=course.id, **data))

        await db.commit()
        print(f"✅ Курс '{course.title}' добавлен — {len(LESSONS)} уроков")


if __name__ == "__main__":
    asyncio.run(seed())
