import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import api from '../api/axios'
import styles from './ProfilePage.module.css'

const LEVELS = [
  { level: 1, min: 0,    max: 100,  title: 'Новичок' },
  { level: 2, min: 100,  max: 300,  title: 'Ученик' },
  { level: 3, min: 300,  max: 600,  title: 'Практик' },
  { level: 4, min: 600,  max: 1000, title: 'Знаток' },
  { level: 5, min: 1000, max: 2000, title: 'Эксперт' },
  { level: 6, min: 2000, max: 9999, title: 'Мастер' },
]

function getLevel(xp) {
  return LEVELS.findLast(l => xp >= l.min) || LEVELS[0]
}

const LANG_LABELS = { python: '🐍 Python', javascript: '⚡ JavaScript', html: '🎨 HTML/CSS' }

export default function ProfilePage() {
  const { user } = useAuthStore()
  const [progress, setProgress] = useState([])
  const [courses, setCourses]   = useState([])
  const [loading, setLoading]   = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/api/progress/me'),
      api.get('/api/courses/'),
    ]).then(([pRes, cRes]) => {
      setProgress(pRes.data)
      setCourses(cRes.data)
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (!user) return null

  const lvl        = getLevel(user.xp)
  const nextLvl    = LEVELS.find(l => l.level === lvl.level + 1)
  const xpInLevel  = user.xp - lvl.min
  const xpNeeded   = (nextLvl?.min ?? lvl.max) - lvl.min
  const pct        = Math.min(100, Math.round((xpInLevel / xpNeeded) * 100))

  const completedLessons = progress.filter(p => p.completed).length
  const totalAttempts    = progress.reduce((s, p) => s + p.attempts, 0)

  // Прогресс по курсам
  const courseProgress = courses.map(c => {
    const lessons  = progress.filter(p => p.lesson_id) // все записи
    // нет course_id в ProgressOut, считаем по lesson_count
    const done = progress.filter(p => p.completed).length
    return c
  })

  // группируем прогресс по course_id через lesson_id — нужен другой подход
  // используем /api/progress/me/course/:id для каждого курса — это дорого
  // поэтому просто показываем курсы с кнопкой "Продолжить"

  const joinDate = new Date(user.created_at).toLocaleDateString('ru-RU', {
    year: 'numeric', month: 'long', day: 'numeric'
  })

  return (
    <div className={styles.page}>

      {/* ─── Шапка профиля ─── */}
      <div className={styles.hero}>
        <div className={styles.avatarWrap}>
          <div className={styles.avatar}>{user.username[0].toUpperCase()}</div>
          <div className={styles.levelBadge}>Ур. {lvl.level}</div>
        </div>
        <div className={styles.heroInfo}>
          <div className={styles.heroTop}>
            <h1 className={styles.name}>{user.username}</h1>
            <span className={styles.levelTitle}>{lvl.title}</span>
          </div>
          <p className={styles.email}>{user.email}</p>
          {user.created_at && <p className={styles.joined}>На платформе с {joinDate}</p>}

          {/* XP прогресс */}
          <div className={styles.xpSection}>
            <div className={styles.xpRow}>
              <span className={styles.xpLabel}>⚡ {user.xp} XP</span>
              {nextLvl && (
                <span className={styles.xpNext}>до ур. {lvl.level + 1}: {nextLvl.min - user.xp} XP</span>
              )}
            </div>
            <div className={styles.xpBar}>
              <div className={styles.xpFill} style={{ width: `${pct}%` }} />
            </div>
          </div>
        </div>
      </div>

      {/* ─── Статистика ─── */}
      <div className={styles.stats}>
        {[
          { icon: '✅', value: completedLessons, label: 'Уроков пройдено' },
          { icon: '📚', value: courses.length,   label: 'Доступных курсов' },
          { icon: '🔁', value: totalAttempts,    label: 'Попыток сдачи' },
          { icon: '⚡', value: user.xp,          label: 'Очков опыта' },
        ].map(s => (
          <div key={s.label} className={styles.statCard}>
            <span className={styles.statIcon}>{s.icon}</span>
            <strong className={styles.statValue}>{s.value}</strong>
            <span className={styles.statLabel}>{s.label}</span>
          </div>
        ))}
      </div>

      {/* ─── Курсы ─── */}
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Курсы платформы</h2>
        {loading ? (
          <div className={styles.loadingText}>Загружаем...</div>
        ) : courses.length === 0 ? (
          <div className={styles.emptyText}>Курсы ещё не добавлены</div>
        ) : (
          <div className={styles.courseList}>
            {courses.map(c => (
              <Link key={c.id} to={`/courses/${c.id}`} className={styles.courseCard}>
                <div className={styles.courseLang}>{LANG_LABELS[c.language] || c.language}</div>
                <div className={styles.courseTitle}>{c.title}</div>
                <span className={styles.courseArrow}>→</span>
              </Link>
            ))}
          </div>
        )}
      </div>

    </div>
  )
}
