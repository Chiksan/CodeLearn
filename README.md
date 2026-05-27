# CodeLearn — Интерактивная платформа обучения программированию

## Быстрый старт

### Требования
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — скачай и установи

### Запуск (одна команда)
```bash
docker-compose up --build
```

После запуска открой:
- **Фронтенд:** http://localhost:3000
- **Бэкенд API:** http://localhost:8000
- **Документация API:** http://localhost:8000/docs

---

## Структура проекта

```
codelearn/
├── docker-compose.yml        # Запуск всех сервисов
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py           # Точка входа FastAPI
│       ├── core/
│       │   ├── config.py     # Настройки
│       │   └── security.py   # JWT, хэширование паролей
│       ├── db/
│       │   └── database.py   # Подключение к PostgreSQL
│       ├── models/
│       │   └── user.py       # Модели БД (User, Course, Lesson, Progress)
│       ├── schemas/
│       │   └── schemas.py    # Pydantic схемы
│       └── api/routes/
│           ├── auth.py       # Регистрация / логин
│           ├── courses.py    # CRUD курсов
│           ├── lessons.py    # CRUD уроков
│           ├── code_runner.py # Запуск кода
│           └── progress.py   # Прогресс пользователя
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx          # Точка входа React
        ├── App.jsx           # Роутинг
        ├── index.css         # Глобальные стили
        ├── api/
        │   └── axios.js      # HTTP клиент
        ├── store/
        │   └── authStore.js  # Zustand (авторизация)
        ├── components/
        │   ├── Navbar.jsx
        │   └── Navbar.module.css
        └── pages/
            ├── HomePage.jsx
            ├── LoginPage.jsx
            ├── RegisterPage.jsx
            ├── CoursesPage.jsx
            ├── LessonPage.jsx  # Monaco Editor + запуск кода
            └── ProfilePage.jsx
```

## Следующие шаги

1. Добавить курсы через API: `POST /api/courses/`
2. Добавить уроки: `POST /api/lessons/course/{id}`
3. Настроить `.env` для продакшена (сменить SECRET_KEY!)
