"""
Добавляет уроки 4-13 в курс "HTML/CSS для начинающих".
Запуск: docker exec codelearn-backend-1 python seed_html_more.py
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
        "title": "Формы и поля ввода",
        "order": 4, "xp_reward": 20,
        "content": """## HTML Формы

Форма позволяет пользователю вводить данные:

```html
<form action="/submit" method="POST">
  <!-- поля формы -->
</form>
```

## Типы полей ввода

```html
<!-- Текст -->
<input type="text" placeholder="Введи имя">

<!-- Email -->
<input type="email" placeholder="you@example.com">

<!-- Пароль -->
<input type="password" placeholder="Пароль">

<!-- Число -->
<input type="number" min="0" max="100">

<!-- Чекбокс -->
<input type="checkbox"> Согласен с условиями

<!-- Радио кнопки -->
<input type="radio" name="gender" value="m"> Мужской
<input type="radio" name="gender" value="f"> Женский

<!-- Выпадающий список -->
<select>
  <option>Python</option>
  <option>JavaScript</option>
</select>

<!-- Многострочный текст -->
<textarea rows="4" placeholder="Твой комментарий..."></textarea>

<!-- Кнопка отправки -->
<button type="submit">Отправить</button>
```

## label — подпись к полю

```html
<label for="email">Email:</label>
<input id="email" type="email">
```

## Задание

Создай форму регистрации с полями: имя, email, пароль и кнопкой «Зарегистрироваться».
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; padding: 24px; max-width: 400px; }
    label { display: block; margin-bottom: 4px; font-weight: bold; font-size: 14px; }
    input { width: 100%; padding: 10px; margin-bottom: 16px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
    button { width: 100%; padding: 12px; background: #534AB7; color: white; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; }
    button:hover { background: #4339a0; }
    h2 { margin-bottom: 20px; }
  </style>
</head>
<body>
  <h2>Регистрация</h2>
  <form>
    <label for="name">Имя</label>
    <input id="name" type="text" placeholder="Введи имя">

    <label for="email">Email</label>
    <input id="email" type="email" placeholder="you@example.com">

    <label for="pass">Пароль</label>
    <input id="pass" type="password" placeholder="Минимум 6 символов">

    <button type="submit">Зарегистрироваться</button>
  </form>
</body>
</html>""",
        "solution": "<form><input type='text' placeholder='Имя'><input type='email' placeholder='Email'><input type='password' placeholder='Пароль'><button>Зарегистрироваться</button></form>",
        "tests": "[]",
        "hints": json.dumps([
            "Форма создаётся тегом <form>",
            "type='email' автоматически проверяет формат email",
            "label for='id' + input id='id' — связывает подпись с полем"
        ]),
    },
    {
        "title": "Семантический HTML",
        "order": 5, "xp_reward": 20,
        "content": """## Что такое семантика?

Семантические теги описывают **смысл** содержимого, а не просто внешний вид. Это важно для:
- Поисковых систем (SEO)
- Доступности (screen readers)
- Читаемости кода

## Основные семантические теги

```html
<!DOCTYPE html>
<html>
<head>...</head>
<body>

  <header>
    <!-- Шапка сайта: логотип, навигация -->
    <nav>
      <a href="/">Главная</a>
      <a href="/about">О нас</a>
    </nav>
  </header>

  <main>
    <!-- Основной контент страницы -->
    <article>
      <h1>Заголовок статьи</h1>
      <p>Текст статьи...</p>
    </article>

    <aside>
      <!-- Боковая панель: реклама, похожие статьи -->
    </aside>
  </main>

  <footer>
    <!-- Подвал: копирайт, контакты -->
    <p>&copy; 2024 Мой сайт</p>
  </footer>

</body>
</html>
```

## Vs несемантический код

```html
<!-- ❌ Плохо -->
<div class="header">
  <div class="nav">...</div>
</div>

<!-- ✅ Хорошо -->
<header>
  <nav>...</nav>
</header>
```

## Задание

Создай структуру страницы с `<header>` (с навигацией), `<main>` (с заголовком и текстом) и `<footer>`.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; }
    header { background: #534AB7; color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
    header h1 { font-size: 18px; }
    nav a { color: white; text-decoration: none; margin-left: 16px; font-size: 14px; }
    nav a:hover { text-decoration: underline; }
    main { flex: 1; padding: 32px 24px; max-width: 800px; margin: 0 auto; width: 100%; }
    main h2 { margin-bottom: 12px; color: #1a1a1a; }
    main p { color: #555; line-height: 1.7; }
    footer { background: #1a1a1a; color: #aaa; text-align: center; padding: 16px; font-size: 14px; }
  </style>
</head>
<body>
  <header>
    <h1>🚀 Мой сайт</h1>
    <nav>
      <a href="#">Главная</a>
      <a href="#">О нас</a>
      <a href="#">Контакты</a>
    </nav>
  </header>

  <main>
    <h2>Добро пожаловать!</h2>
    <p>Это пример семантической разметки HTML5. Каждый тег несёт смысл — поисковики и браузеры лучше понимают структуру страницы.</p>
  </main>

  <footer>
    <p>&copy; 2024 Мой сайт. Все права защищены.</p>
  </footer>
</body>
</html>""",
        "solution": "<header><nav><a href='/'>Главная</a></nav></header><main><h1>Заголовок</h1><p>Текст</p></main><footer><p>© 2024</p></footer>",
        "tests": "[]",
        "hints": json.dumps([
            "<header> — шапка сайта с логотипом и навигацией",
            "<main> — основной контент, должен быть один на странице",
            "<footer> — подвал с контактами и копирайтом"
        ]),
    },
    {
        "title": "CSS селекторы",
        "order": 6, "xp_reward": 25,
        "content": """## Виды селекторов

### По тегу
```css
p { color: blue; }         /* все абзацы */
h1 { font-size: 32px; }   /* все заголовки h1 */
```

### По классу
```css
.highlight { background: yellow; }
.btn { padding: 10px 20px; }
```

```html
<p class="highlight">Выделенный текст</p>
<button class="btn">Кнопка</button>
```

### По ID
```css
#header { background: #333; }
```
```html
<div id="header">Шапка</div>
```

### Комбинированные
```css
/* Потомок */
div p { color: red; }      /* p внутри div */

/* Прямой потомок */
ul > li { list-style: none; }

/* Несколько классов */
.btn.primary { background: blue; }

/* При наведении */
a:hover { color: purple; }

/* Первый дочерний */
li:first-child { font-weight: bold; }
```

### Специфичность

Чем конкретнее селектор — тем выше его приоритет:
```
!important > inline style > #id > .class > tag
```

## Задание

Задай разные стили для заголовка, абзаца и кнопки через классы. Добавь эффект при наведении на кнопку.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; padding: 32px; }

    /* По тегу */
    h2 { color: #534AB7; }

    /* По классу */
    .card {
      background: #f8f8fc;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 16px;
      border: 1px solid #eee;
    }

    .text { color: #555; line-height: 1.7; }

    /* Кнопка с hover-эффектом */
    .btn {
      display: inline-block;
      padding: 10px 24px;
      background: #534AB7;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      transition: background 0.2s, transform 0.1s;
    }
    .btn:hover {
      background: #4339a0;
      transform: translateY(-2px);
    }
    .btn:active { transform: translateY(0); }

    /* Первый абзац */
    .card p:first-of-type { font-weight: bold; color: #333; }
  </style>
</head>
<body>
  <div class="card">
    <h2>CSS Селекторы</h2>
    <p class="text">Это первый абзац — он выделен жирным через :first-of-type.</p>
    <p class="text">Это второй абзац с обычным стилем.</p>
    <button class="btn">Наведи на меня!</button>
  </div>
</body>
</html>""",
        "solution": "<style>.title{color:red}.text{color:gray}.btn{background:blue;color:white;padding:8px 16px}.btn:hover{background:darkblue}</style><h1 class='title'>Заголовок</h1><p class='text'>Текст</p><button class='btn'>Кнопка</button>",
        "tests": "[]",
        "hints": json.dumps([
            ".className — селектор по классу, начинается с точки",
            ":hover — псевдокласс, стиль при наведении мыши",
            "Специфичность: #id > .class > тег"
        ]),
    },
    {
        "title": "Блочная модель CSS",
        "order": 7, "xp_reward": 25,
        "content": """## Блочная модель

Каждый HTML-элемент — прямоугольник из 4 слоёв:

```
┌─────────────────────────────┐  ← margin (внешний отступ)
│   ┌─────────────────────┐   │
│   │  border (рамка)     │   │
│   │  ┌───────────────┐  │   │
│   │  │ padding (внут)│  │   │
│   │  │ ┌───────────┐ │  │   │
│   │  │ │  content  │ │  │   │
│   │  │ └───────────┘ │  │   │
│   │  └───────────────┘  │   │
│   └─────────────────────┘   │
└─────────────────────────────┘
```

## Свойства

```css
.box {
  /* Размеры контента */
  width: 200px;
  height: 100px;

  /* Внутренний отступ */
  padding: 16px;             /* все стороны */
  padding: 10px 20px;        /* верх/низ  лево/право */
  padding: 5px 10px 15px 20px; /* верх право низ лево */

  /* Рамка */
  border: 2px solid #333;
  border-radius: 8px;        /* скругление */

  /* Внешний отступ */
  margin: 24px;
  margin: 0 auto;            /* центрирование по горизонтали */
}
```

## box-sizing

```css
/* По умолчанию width не включает padding и border */
.default { width: 200px; padding: 20px; } /* реальная ширина = 240px */

/* С border-box — width включает всё */
* { box-sizing: border-box; }
.better { width: 200px; padding: 20px; } /* реальная ширина = 200px */
```

## Задание

Создай три карточки с разными рамками, отступами и скруглениями. Используй `box-sizing: border-box`.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; padding: 24px; background: #f5f5f5; }

    .cards { display: flex; gap: 16px; flex-wrap: wrap; }

    .card {
      width: 200px;
      padding: 20px;
      background: white;
    }

    .card-1 {
      border: 2px solid #534AB7;
      border-radius: 8px;
    }

    .card-2 {
      border: 2px dashed #27ae60;
      border-radius: 50px;
      padding: 24px 32px;
    }

    .card-3 {
      border: 3px solid #e53e3e;
      border-radius: 0;
      box-shadow: 4px 4px 0 #e53e3e;
    }

    h3 { margin-bottom: 8px; font-size: 15px; }
    p { color: #888; font-size: 13px; line-height: 1.5; }
  </style>
</head>
<body>
  <h2 style="margin-bottom: 20px; color: #1a1a1a;">Блочная модель</h2>
  <div class="cards">
    <div class="card card-1">
      <h3>Скруглённая</h3>
      <p>border-radius: 8px, solid border</p>
    </div>
    <div class="card card-2">
      <h3>Пилюля</h3>
      <p>border-radius: 50px, dashed border</p>
    </div>
    <div class="card card-3">
      <h3>Ретро</h3>
      <p>Смещённая тень через box-shadow</p>
    </div>
  </div>
</body>
</html>""",
        "solution": "<style>*{box-sizing:border-box}.box{width:200px;padding:20px;margin:10px;border:2px solid blue;border-radius:8px}</style><div class='box'>Карточка 1</div><div class='box'>Карточка 2</div>",
        "tests": "[]",
        "hints": json.dumps([
            "padding — внутри элемента, margin — снаружи",
            "box-sizing: border-box — ширина включает padding и border",
            "margin: 0 auto — центрирует элемент по горизонтали"
        ]),
    },
    {
        "title": "Flexbox",
        "order": 8, "xp_reward": 30,
        "content": """## Что такое Flexbox?

Flexbox — способ расположить элементы в одну строку или столбец с гибким управлением пространством.

## Основные свойства контейнера

```css
.container {
  display: flex;

  /* Направление */
  flex-direction: row;       /* → строка (по умолчанию) */
  flex-direction: column;    /* ↓ столбец */

  /* Выравнивание по главной оси */
  justify-content: flex-start;   /* | ○ ○ ○       | */
  justify-content: center;       /* |    ○ ○ ○    | */
  justify-content: flex-end;     /* |       ○ ○ ○ | */
  justify-content: space-between;/* | ○    ○    ○ | */
  justify-content: space-around; /* |  ○   ○   ○  | */

  /* Выравнивание по поперечной оси */
  align-items: stretch;     /* растянуть */
  align-items: center;      /* по центру */
  align-items: flex-start;  /* сверху */

  /* Перенос */
  flex-wrap: wrap;
  gap: 16px;
}
```

## Свойства элементов

```css
.item {
  flex: 1;           /* занять всё свободное место */
  flex: 0 0 200px;   /* фиксированная ширина 200px */
  align-self: center; /* своё выравнивание */
}
```

## Задание

Создай навигационную панель с логотипом слева и ссылками справа, используя Flexbox.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; }

    /* Навбар */
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #534AB7;
      padding: 0 24px;
      height: 56px;
    }
    .logo { color: white; font-weight: bold; font-size: 18px; text-decoration: none; }
    .nav-links { display: flex; gap: 8px; list-style: none; }
    .nav-links a { color: rgba(255,255,255,0.85); text-decoration: none; padding: 6px 12px; border-radius: 6px; font-size: 14px; transition: background 0.2s; }
    .nav-links a:hover { background: rgba(255,255,255,0.15); }

    /* Карточки */
    .cards {
      display: flex;
      gap: 16px;
      padding: 32px 24px;
      flex-wrap: wrap;
    }
    .card {
      flex: 1;
      min-width: 180px;
      background: #f8f8fc;
      border-radius: 12px;
      padding: 24px;
      border: 1px solid #eee;
    }
    .card h3 { margin-bottom: 8px; color: #534AB7; }
    .card p { color: #666; font-size: 14px; line-height: 1.5; }

    /* Центрированный блок */
    .hero {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 160px;
      background: linear-gradient(135deg, #534AB7, #8B7FE8);
      color: white;
      text-align: center;
    }
    .hero h2 { font-size: 28px; }
  </style>
</head>
<body>
  <nav class="navbar">
    <a href="#" class="logo">&lt;/&gt; CodeLearn</a>
    <ul class="nav-links">
      <li><a href="#">Курсы</a></li>
      <li><a href="#">Рейтинг</a></li>
      <li><a href="#">Профиль</a></li>
    </ul>
  </nav>

  <div class="hero">
    <div>
      <h2>Flexbox — это просто!</h2>
      <p style="margin-top: 8px; opacity: 0.9;">justify-content: center + align-items: center</p>
    </div>
  </div>

  <div class="cards">
    <div class="card"><h3>flex: 1</h3><p>Все карточки занимают равное пространство благодаря flex: 1</p></div>
    <div class="card"><h3>gap: 16px</h3><p>Отступы между элементами через gap — удобнее чем margin</p></div>
    <div class="card"><h3>flex-wrap: wrap</h3><p>При нехватке места элементы переносятся на следующую строку</p></div>
  </div>
</body>
</html>""",
        "solution": "<style>.nav{display:flex;justify-content:space-between;align-items:center;background:#333;padding:16px}.logo{color:white}.links{display:flex;gap:16px;list-style:none}.links a{color:white;text-decoration:none}</style><nav class='nav'><span class='logo'>Logo</span><ul class='links'><li><a href='#'>Home</a></li><li><a href='#'>About</a></li></ul></nav>",
        "tests": "[]",
        "hints": json.dumps([
            "display: flex на контейнере — включает Flexbox для его дочерних элементов",
            "justify-content: space-between — первый элемент слева, последний справа",
            "align-items: center — выравнивает элементы по центру по вертикали"
        ]),
    },
    {
        "title": "CSS Grid",
        "order": 9, "xp_reward": 30,
        "content": """## Что такое CSS Grid?

Grid — двумерная система разметки (строки И столбцы одновременно).

**Flexbox** — одно направление (строка или столбец).
**Grid** — оба направления одновременно.

## Основы Grid

```css
.container {
  display: grid;

  /* 3 колонки: 200px, гибкая, 200px */
  grid-template-columns: 200px 1fr 200px;

  /* 2 строки: авто и фиксированная */
  grid-template-rows: auto 300px;

  gap: 16px; /* отступы между ячейками */
}
```

## fr — дробная единица

```css
/* 3 равные колонки */
grid-template-columns: 1fr 1fr 1fr;

/* Короче: */
grid-template-columns: repeat(3, 1fr);

/* Адаптивная сетка */
grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
```

## Растягивание элементов

```css
.wide { grid-column: span 2; }  /* занять 2 колонки */
.tall { grid-row: span 2; }     /* занять 2 строки */

/* Точное позиционирование */
.item { grid-column: 1 / 3; }   /* с 1-й по 3-ю линию */
```

## Задание

Создай сетку карточек 3 в ряд. На маленьких экранах — 1 в ряд.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; padding: 24px; background: #f5f5f5; }
    h2 { margin-bottom: 20px; }

    /* Адаптивная сетка */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 16px;
    }

    .card {
      background: white;
      border-radius: 12px;
      padding: 20px;
      border: 1px solid #eee;
    }

    /* Широкая карточка на 2 колонки */
    .card.wide {
      grid-column: span 2;
      background: linear-gradient(135deg, #534AB7, #8B7FE8);
      color: white;
    }

    .card h3 { margin-bottom: 8px; font-size: 15px; }
    .card p { color: #888; font-size: 13px; }
    .card.wide p { color: rgba(255,255,255,0.8); }

    .tag {
      display: inline-block;
      background: #EEEDFE;
      color: #534AB7;
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 11px;
      margin-bottom: 10px;
    }
    .card.wide .tag { background: rgba(255,255,255,0.2); color: white; }
  </style>
</head>
<body>
  <h2>CSS Grid — карточки</h2>
  <div class="grid">
    <div class="card wide">
      <span class="tag">Рекомендуем</span>
      <h3>CSS Grid — двумерная разметка</h3>
      <p>Управляй строками и столбцами одновременно. Идеально для сложных макетов.</p>
    </div>
    <div class="card">
      <span class="tag">Основы</span>
      <h3>display: grid</h3>
      <p>Включает Grid для дочерних элементов</p>
    </div>
    <div class="card">
      <span class="tag">Колонки</span>
      <h3>grid-template-columns</h3>
      <p>Определяет количество и ширину колонок</p>
    </div>
    <div class="card">
      <span class="tag">Единица</span>
      <h3>fr — fraction</h3>
      <p>Дробная часть свободного пространства</p>
    </div>
    <div class="card">
      <span class="tag">Адаптив</span>
      <h3>auto-fill + minmax</h3>
      <p>Автоматическое количество колонок</p>
    </div>
  </div>
</body>
</html>""",
        "solution": "<style>.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:#f5f5f5;padding:20px;border-radius:8px}</style><div class='grid'><div class='card'>1</div><div class='card'>2</div><div class='card'>3</div><div class='card'>4</div><div class='card'>5</div><div class='card'>6</div></div>",
        "tests": "[]",
        "hints": json.dumps([
            "display: grid на контейнере включает Grid",
            "repeat(3, 1fr) — 3 равные колонки",
            "grid-column: span 2 — элемент занимает 2 колонки"
        ]),
    },
    {
        "title": "Позиционирование",
        "order": 10, "xp_reward": 30,
        "content": """## position в CSS

```css
position: static;    /* по умолчанию, в потоке документа */
position: relative;  /* относительно своей позиции */
position: absolute;  /* относительно ближайшего positioned родителя */
position: fixed;     /* относительно viewport, не скроллится */
position: sticky;    /* прилипает при скролле */
```

## relative

```css
.box {
  position: relative;
  top: 20px;    /* сдвиг вниз от нормальной позиции */
  left: 10px;   /* сдвиг вправо */
}
```

## absolute

```css
.parent {
  position: relative; /* родитель должен быть positioned */
}
.child {
  position: absolute;
  top: 0;
  right: 0;   /* прижать к правому верхнему углу родителя */
}
```

## fixed — фиксированные элементы

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;    /* или width: 100% */
  z-index: 100;
}
```

## z-index — порядок слоёв

```css
.behind { z-index: 1; }
.above  { z-index: 10; }
```

## Задание

Создай карточку со значком в правом верхнем углу (position: absolute), и фиксированную кнопку «Наверх» (position: fixed).
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; padding: 24px; background: #f5f5f5; }

    /* Карточка с абсолютным бейджем */
    .card {
      position: relative; /* родитель для absolute дочерних */
      background: white;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 16px;
      border: 1px solid #eee;
      max-width: 360px;
    }

    .badge {
      position: absolute;
      top: -10px;
      right: -10px;
      background: #e53e3e;
      color: white;
      border-radius: 50%;
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: bold;
    }

    .card h3 { margin-bottom: 8px; }
    .card p { color: #666; font-size: 14px; }

    /* Фиксированная кнопка */
    .scroll-top {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 44px;
      height: 44px;
      background: #534AB7;
      color: white;
      border: none;
      border-radius: 50%;
      font-size: 20px;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(83,74,183,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .scroll-top:hover { background: #4339a0; }

    /* Sticky заголовок */
    .sticky-header {
      position: sticky;
      top: 0;
      background: white;
      padding: 12px 0;
      border-bottom: 1px solid #eee;
      margin-bottom: 16px;
      font-weight: bold;
      color: #534AB7;
    }
  </style>
</head>
<body>
  <div class="sticky-header">📌 Этот заголовок прилипает при скролле</div>

  <div class="card">
    <div class="badge">3</div>
    <h3>Уведомления</h3>
    <p>Бейдж в правом верхнем углу через <code>position: absolute</code></p>
  </div>

  <div class="card">
    <div class="badge" style="background: #27ae60;">✓</div>
    <h3>Выполнено</h3>
    <p>Родитель имеет <code>position: relative</code> — абсолютный дочерний прикрепляется к нему</p>
  </div>

  <button class="scroll-top" onclick="window.scrollTo(0,0)">↑</button>
</body>
</html>""",
        "solution": "<style>.parent{position:relative;padding:20px;background:#eee}.badge{position:absolute;top:-8px;right:-8px;background:red;color:white;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center}.fixed{position:fixed;bottom:20px;right:20px;background:blue;color:white;padding:10px;border:none;border-radius:50%;cursor:pointer}</style><div class='parent'>Карточка<span class='badge'>5</span></div><button class='fixed'>↑</button>",
        "tests": "[]",
        "hints": json.dumps([
            "Для position: absolute нужен родитель с position: relative",
            "position: fixed — не зависит от скролла, висит на экране",
            "z-index управляет слоями — больше значение = выше"
        ]),
    },
    {
        "title": "CSS анимации и переходы",
        "order": 11, "xp_reward": 30,
        "content": """## transition — плавный переход

```css
.btn {
  background: blue;
  transition: background 0.3s ease;
}
.btn:hover {
  background: darkblue; /* переход за 0.3 секунды */
}
```

## Несколько свойств

```css
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
```

## animation + @keyframes

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.element {
  animation: fadeIn 0.5s ease forwards;
}
```

## Параметры animation

```css
animation: name duration timing delay iteration direction;

animation: spin 1s linear infinite;  /* бесконечное вращение */
animation: pulse 2s ease-in-out alternate infinite; /* пульсация */
```

## Популярные трансформации

```css
transform: translateX(20px);   /* сдвиг по X */
transform: translateY(-10px);  /* сдвиг по Y */
transform: scale(1.1);         /* увеличение */
transform: rotate(45deg);      /* поворот */
```

## Задание

Создай карточки с hover-анимацией (подъём + тень) и кнопку с пульсирующей анимацией.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; padding: 32px; background: #f5f5f5; }

    /* Анимация появления */
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(30px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    /* Пульсация */
    @keyframes pulse {
      0%, 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(83,74,183,0.3); }
      50%       { transform: scale(1.05); box-shadow: 0 8px 25px rgba(83,74,183,0.5); }
    }

    /* Вращение */
    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    h2 { margin-bottom: 24px; }

    .cards { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 32px; }

    .card {
      background: white;
      border-radius: 12px;
      padding: 24px;
      flex: 1;
      min-width: 160px;
      border: 1px solid #eee;
      cursor: pointer;
      animation: fadeInUp 0.5s ease forwards;

      /* Плавный переход */
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .card:hover {
      transform: translateY(-6px);
      box-shadow: 0 12px 30px rgba(0,0,0,0.1);
    }
    .card:nth-child(2) { animation-delay: 0.1s; }
    .card:nth-child(3) { animation-delay: 0.2s; }

    .card-icon { font-size: 32px; margin-bottom: 12px; }
    .card h3 { font-size: 15px; margin-bottom: 6px; }
    .card p { color: #888; font-size: 13px; }

    /* Пульсирующая кнопка */
    .pulse-btn {
      padding: 14px 32px;
      background: #534AB7;
      color: white;
      border: none;
      border-radius: 50px;
      font-size: 15px;
      cursor: pointer;
      animation: pulse 2s ease-in-out infinite;
      margin-bottom: 24px;
      display: block;
    }

    /* Спиннер */
    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid #eee;
      border-top-color: #534AB7;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
  </style>
</head>
<body>
  <h2>CSS Анимации</h2>

  <div class="cards">
    <div class="card">
      <div class="card-icon">✨</div>
      <h3>Hover эффект</h3>
      <p>transform + transition</p>
    </div>
    <div class="card">
      <div class="card-icon">🎭</div>
      <h3>fadeInUp</h3>
      <p>@keyframes + animation</p>
    </div>
    <div class="card">
      <div class="card-icon">⚡</div>
      <h3>animation-delay</h3>
      <p>Последовательное появление</p>
    </div>
  </div>

  <button class="pulse-btn">💫 Пульсирующая кнопка</button>

  <p style="margin-bottom: 12px; color: #666; font-size: 14px;">Спиннер загрузки:</p>
  <div class="spinner"></div>
</body>
</html>""",
        "solution": "<style>@keyframes fadeIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}@keyframes spin{to{transform:rotate(360deg)}}.card{animation:fadeIn 0.5s ease;transition:transform 0.2s}.card:hover{transform:translateY(-4px)}.spinner{width:32px;height:32px;border:3px solid #eee;border-top-color:blue;border-radius:50%;animation:spin 0.8s linear infinite}</style><div class='card'><p>Наведи на меня</p></div><div class='spinner'></div>",
        "tests": "[]",
        "hints": json.dumps([
            "transition: свойство длительность плавность — плавно меняет свойство",
            "@keyframes имя { from{} to{} } — описывает анимацию",
            "animation: имя длительность — применяет анимацию к элементу"
        ]),
    },
    {
        "title": "Адаптивный дизайн (Media Queries)",
        "order": 12, "xp_reward": 35,
        "content": """## Что такое адаптивный дизайн?

Сайт должен хорошо выглядеть на любом устройстве — телефоне, планшете, компьютере.

## Viewport meta тег

Обязательно добавляй в `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

## Media Queries

```css
/* Стили для экранов до 768px (мобильные) */
@media (max-width: 768px) {
  .container { padding: 16px; }
  .sidebar { display: none; }
}

/* Стили для экранов от 768px до 1024px (планшеты) */
@media (min-width: 768px) and (max-width: 1024px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Стили для больших экранов */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```

## Mobile-first подход

Сначала пишем стили для мобильных, потом расширяем:

```css
/* Мобильный (по умолчанию) */
.grid { grid-template-columns: 1fr; }

/* Планшет */
@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Десктоп */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```

## Задание

Создай страницу которая на узком экране показывает колонки вертикально, а на широком — горизонтально. Попробуй изменить ширину окна браузера.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; background: #f5f5f5; }

    /* Навбар */
    .navbar {
      background: #534AB7;
      padding: 0 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 56px;
    }
    .logo { color: white; font-weight: bold; font-size: 16px; }
    .nav-links { display: flex; gap: 8px; list-style: none; }
    .nav-links a { color: rgba(255,255,255,0.9); text-decoration: none; padding: 6px 12px; border-radius: 6px; font-size: 14px; }
    .burger { display: none; background: none; border: none; color: white; font-size: 22px; cursor: pointer; }

    /* Герой */
    .hero {
      padding: 48px 24px;
      text-align: center;
      background: linear-gradient(135deg, #534AB7, #8B7FE8);
      color: white;
    }
    .hero h1 { font-size: 28px; margin-bottom: 12px; }
    .hero p { opacity: 0.9; font-size: 16px; }

    /* Карточки */
    .cards {
      display: grid;
      grid-template-columns: 1fr; /* мобильный: 1 колонка */
      gap: 16px;
      padding: 24px;
      max-width: 1100px;
      margin: 0 auto;
    }

    .card {
      background: white;
      border-radius: 12px;
      padding: 20px;
      border: 1px solid #eee;
    }
    .card h3 { margin-bottom: 8px; color: #534AB7; }
    .card p { color: #666; font-size: 14px; line-height: 1.5; }

    /* Индикатор размера */
    .size-indicator {
      text-align: center;
      padding: 10px;
      font-size: 13px;
      font-weight: bold;
      color: white;
    }

    /* === Media Queries === */

    /* Планшет: 2 колонки */
    @media (min-width: 640px) {
      .cards { grid-template-columns: repeat(2, 1fr); }
      .hero h1 { font-size: 36px; }
      .size-indicator { background: #27ae60; }
      .size-indicator::after { content: ' 📱 Планшет (≥640px)'; }
    }

    /* Десктоп: 3 колонки */
    @media (min-width: 1024px) {
      .cards { grid-template-columns: repeat(3, 1fr); }
      .hero h1 { font-size: 44px; }
      .nav-links { display: flex; }
      .size-indicator { background: #534AB7; }
      .size-indicator::after { content: ' 🖥 Десктоп (≥1024px)'; }
    }

    /* Мобильный */
    @media (max-width: 639px) {
      .nav-links { display: none; }
      .burger { display: block; }
      .size-indicator { background: #e53e3e; }
      .size-indicator::after { content: ' 📱 Мобильный (<640px)'; }
    }
  </style>
</head>
<body>
  <div class="size-indicator">Измени ширину окна браузера →</div>

  <nav class="navbar">
    <span class="logo">&lt;/&gt; CodeLearn</span>
    <ul class="nav-links">
      <li><a href="#">Курсы</a></li>
      <li><a href="#">Рейтинг</a></li>
      <li><a href="#">Профиль</a></li>
    </ul>
    <button class="burger">☰</button>
  </nav>

  <div class="hero">
    <h1>Адаптивный дизайн</h1>
    <p>Измени ширину окна чтобы увидеть изменения</p>
  </div>

  <div class="cards">
    <div class="card"><h3>📱 Мобильный</h3><p>1 колонка. Навигация скрыта, появляется бургер-меню.</p></div>
    <div class="card"><h3>📱 Планшет</h3><p>2 колонки при ширине от 640px. Больше информации.</p></div>
    <div class="card"><h3>🖥 Десктоп</h3><p>3 колонки при ширине от 1024px. Полная навигация.</p></div>
    <div class="card"><h3>🎯 Mobile First</h3><p>Сначала пишем для мобильных, потом расширяем через min-width.</p></div>
    <div class="card"><h3>📐 Breakpoints</h3><p>640px, 768px, 1024px, 1280px — стандартные точки перелома.</p></div>
    <div class="card"><h3>🔧 Viewport</h3><p>meta viewport обязателен для корректной работы на мобильных.</p></div>
  </div>
</body>
</html>""",
        "solution": "<style>.grid{display:grid;grid-template-columns:1fr;gap:16px}@media(min-width:640px){.grid{grid-template-columns:repeat(2,1fr)}}@media(min-width:1024px){.grid{grid-template-columns:repeat(3,1fr)}}.card{background:#f5f5f5;padding:20px;border-radius:8px}</style><div class='grid'><div class='card'>1</div><div class='card'>2</div><div class='card'>3</div></div>",
        "tests": "[]",
        "hints": json.dumps([
            "@media (max-width: 768px) — стили применяются только на экранах до 768px",
            "Mobile-first: пишем для мобильных, расширяем через min-width",
            "meta viewport обязателен — без него мобильный браузер масштабирует страницу"
        ]),
    },
    {
        "title": "Мини-проект: лендинг-страница",
        "order": 13, "xp_reward": 50,
        "content": """## Финальный проект курса HTML/CSS

Создай полноценную лендинг-страницу используя всё что изучил:

- **Семантический HTML** (header, main, section, footer)
- **Flexbox и Grid** для разметки
- **Анимации** и hover-эффекты
- **Адаптивность** — хорошо выглядит на телефоне

## Структура лендинга

```
┌──────────────────────────────┐
│          NAVBAR              │
├──────────────────────────────┤
│          HERO                │
│    Заголовок + кнопка        │
├──────────────────────────────┤
│         FEATURES             │
│  Карточка  Карточка  Карточка│
├──────────────────────────────┤
│          CTA                 │
│     Призыв к действию        │
├──────────────────────────────┤
│         FOOTER               │
└──────────────────────────────┘
```

## Задание

Код лендинга уже написан. Изучи его структуру и **измени содержимое** под свою идею: другое название, описание, цвета, иконки секций.
""",
        "starter_code": """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Мой лендинг</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; color: #1a1a1a; }

    /* ─── Navbar ─────────────────────────────── */
    .navbar {
      position: sticky; top: 0; z-index: 100;
      display: flex; justify-content: space-between; align-items: center;
      padding: 0 32px; height: 60px;
      background: rgba(255,255,255,0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid #eee;
    }
    .logo { font-weight: 800; font-size: 18px; color: #534AB7; }
    .nav-links { display: flex; gap: 4px; list-style: none; }
    .nav-links a { padding: 6px 14px; border-radius: 8px; text-decoration: none; color: #555; font-size: 14px; transition: background 0.15s; }
    .nav-links a:hover { background: #f0f0f0; }
    .nav-cta { padding: 8px 20px; background: #534AB7; color: white; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; transition: background 0.15s; }
    .nav-cta:hover { background: #4339a0; }

    /* ─── Hero ───────────────────────────────── */
    .hero {
      min-height: 90vh;
      display: flex; align-items: center; justify-content: center;
      text-align: center;
      background: linear-gradient(135deg, #f5f4ff 0%, #eef2ff 100%);
      padding: 60px 24px;
    }
    .hero-content { max-width: 680px; }
    .hero-badge { display: inline-block; background: #EEEDFE; color: #534AB7; padding: 6px 16px; border-radius: 50px; font-size: 13px; font-weight: 600; margin-bottom: 24px; }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: none; } }
    .hero h1 { font-size: 52px; font-weight: 800; line-height: 1.15; margin-bottom: 20px; animation: fadeInUp 0.7s ease; }
    .hero h1 span { color: #534AB7; }
    .hero p { font-size: 18px; color: #666; line-height: 1.7; margin-bottom: 36px; animation: fadeInUp 0.7s 0.1s ease both; }
    .hero-btns { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; animation: fadeInUp 0.7s 0.2s ease both; }
    .btn-primary { padding: 14px 32px; background: #534AB7; color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(83,74,183,0.35); }
    .btn-secondary { padding: 14px 32px; background: white; color: #534AB7; border: 2px solid #534AB7; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
    .btn-secondary:hover { background: #f5f4ff; }

    /* ─── Features ───────────────────────────── */
    .features { padding: 80px 24px; max-width: 1100px; margin: 0 auto; }
    .features h2 { text-align: center; font-size: 32px; margin-bottom: 12px; }
    .features-sub { text-align: center; color: #888; margin-bottom: 48px; font-size: 16px; }
    .features-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    .feature-card { padding: 28px; border: 1px solid #eee; border-radius: 16px; transition: transform 0.2s, box-shadow 0.2s; }
    .feature-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.07); }
    .feature-icon { font-size: 36px; margin-bottom: 16px; }
    .feature-card h3 { font-size: 17px; margin-bottom: 8px; }
    .feature-card p { color: #777; font-size: 14px; line-height: 1.6; }

    /* ─── CTA ────────────────────────────────── */
    .cta { background: linear-gradient(135deg, #534AB7, #8B7FE8); padding: 80px 24px; text-align: center; color: white; }
    .cta h2 { font-size: 36px; margin-bottom: 16px; }
    .cta p { font-size: 18px; opacity: 0.9; margin-bottom: 36px; }
    .btn-white { padding: 14px 36px; background: white; color: #534AB7; border: none; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; transition: transform 0.2s; }
    .btn-white:hover { transform: scale(1.05); }

    /* ─── Footer ─────────────────────────────── */
    footer { background: #1a1a1a; color: #888; padding: 32px 24px; text-align: center; font-size: 14px; }
    footer a { color: #aaa; text-decoration: none; margin: 0 8px; }
    footer a:hover { color: white; }

    /* ─── Responsive ──────────────────────────── */
    @media (max-width: 640px) {
      .hero h1 { font-size: 32px; }
      .nav-links { display: none; }
    }
  </style>
</head>
<body>

  <nav class="navbar">
    <div class="logo">&lt;/&gt; CodeLearn</div>
    <ul class="nav-links">
      <li><a href="#">Курсы</a></li>
      <li><a href="#">Рейтинг</a></li>
      <li><a href="#">О нас</a></li>
    </ul>
    <button class="nav-cta">Начать бесплатно</button>
  </nav>

  <section class="hero">
    <div class="hero-content">
      <span class="hero-badge">🚀 Учись программированию</span>
      <h1>Пиши код.<br>Решай задачи.<br><span>Расти</span> как разработчик.</h1>
      <p>Интерактивные курсы по Python, JavaScript и React. Запускай код прямо в браузере и получай мгновенный результат.</p>
      <div class="hero-btns">
        <button class="btn-primary">Начать обучение →</button>
        <button class="btn-secondary">Смотреть курсы</button>
      </div>
    </div>
  </section>

  <section class="features">
    <h2>Почему CodeLearn?</h2>
    <p class="features-sub">Всё что нужно для старта в программировании</p>
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">💻</div>
        <h3>Редактор в браузере</h3>
        <p>Пиши и запускай код без установки программ. Всё работает прямо на сайте.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>Практические задания</h3>
        <p>Каждый урок — конкретная задача с автоматической проверкой и подсказками.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Система XP</h3>
        <p>Зарабатывай опыт за каждый пройденный урок и поднимайся в рейтинге.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🐍</div>
        <h3>Python с нуля</h3>
        <p>От первой программы до ООП и FastAPI — полный путь разработчика.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">⚛️</div>
        <h3>React и JavaScript</h3>
        <p>Современный фронтенд: от основ JS до продвинутых хуков React.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🏆</div>
        <h3>Лидерборд</h3>
        <p>Соревнуйся с другими учениками и мотивируй себя учиться каждый день.</p>
      </div>
    </div>
  </section>

  <section class="cta">
    <h2>Готов начать?</h2>
    <p>Регистрация бесплатна. Первый урок — прямо сейчас.</p>
    <button class="btn-white">Зарегистрироваться бесплатно</button>
  </section>

  <footer>
    <p>&copy; 2024 CodeLearn &nbsp;·&nbsp; <a href="#">Условия</a> <a href="#">Контакты</a></p>
  </footer>

</body>
</html>""",
        "solution": "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,sans-serif}.hero{min-height:80vh;display:flex;align-items:center;justify-content:center;text-align:center;background:linear-gradient(135deg,#f5f4ff,#eef2ff);padding:40px}h1{font-size:40px;margin-bottom:16px}p{color:#666;margin-bottom:24px}.btn{padding:14px 32px;background:#534AB7;color:white;border:none;border-radius:10px;font-size:16px;cursor:pointer}.features{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:40px}.card{padding:24px;border:1px solid #eee;border-radius:12px}footer{background:#1a1a1a;color:#888;text-align:center;padding:24px}</style></head><body><section class='hero'><div><h1>Мой лендинг</h1><p>Описание продукта</p><button class='btn'>Начать</button></div></section><div class='features'><div class='card'>Фича 1</div><div class='card'>Фича 2</div><div class='card'>Фича 3</div></div><footer>© 2024</footer></body></html>",
        "tests": "[]",
        "hints": json.dumps([
            "Лендинг состоит из секций: hero, features, cta, footer",
            "position: sticky на navbar — прилипает при скролле",
            "Измени тексты, цвета и иконки чтобы сделать лендинг своим"
        ]),
    },
]


async def seed():
    async with Session() as db:
        result = await db.execute(
            select(Course).where(Course.title == "HTML/CSS для начинающих")
        )
        course = result.scalar_one_or_none()
        if not course:
            print("❌ Курс не найден")
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
            db.add(Lesson(course_id=course.id, **data))
            added += 1

        await db.commit()
        print(f"✅ Добавлено {added} уроков в '{course.title}'")


if __name__ == "__main__":
    asyncio.run(seed())
