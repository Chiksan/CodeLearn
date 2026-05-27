import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api/axios'
import { useAuthStore } from '../store/authStore'
import styles from './CoursePage.module.css'

const LANG_LABELS = { python: '🐍 Python', javascript: '⚡ JavaScript', html: '🎨 HTML/CSS' }
const LEVEL_LABELS = { beginner: 'Начинающий', intermediate: 'Средний', advanced: 'Продвинутый' }

export default function CoursePage() {
  const { id } = useParams()
  const { token } = useAuthStore()
  const [course, setCourse] = useState(null)
  const [lessons, setLessons] = useState([])
  const [progress, setProgress] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [courseRes, lessonsRes] = await Promise.all([
          api.get(`/api/courses/${id}`),
          api.get(`/api/lessons/course/${id}`),
        ])
        setCourse(courseRes.data)
        setLessons(lessonsRes.data)

        if (token) {
          const progressRes = await api.get(`/api/progress/me/course/${id}`)
          const map = {}
          for (const p of progressRes.data) map[p.lesson_id] = p
          setProgress(map)
        }
      } catch {
        // ignore
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [id, token])

  if (loading) return <div className={styles.loading}>Загружаем курс...</div>
  if (!course) return <div className={styles.loading}>Курс не найден</div>

  const completedCount = Object.values(progress).filter(p => p.completed).length

  return (
    <div className={styles.page}>
      <Link to="/courses" className={styles.back}>← Все курсы</Link>

      <div className={styles.header}>
        <div className={styles.langBadge}>{LANG_LABELS[course.language] || course.language}</div>
        <h1 className={styles.title}>{course.title}</h1>
        {course.description && <p className={styles.desc}>{course.description}</p>}
        <div className={styles.meta}>
          <span className={styles.level}>{LEVEL_LABELS[course.level]}</span>
          <span className={styles.count}>{lessons.length} уроков</span>
          {token && lessons.length > 0 && (
            <span className={styles.completed}>{completedCount} / {lessons.length} пройдено</span>
          )}
        </div>

        {token && lessons.length > 0 && (
          <div className={styles.progressBar}>
            <div
              className={styles.progressFill}
              style={{ width: `${(completedCount / lessons.length) * 100}%` }}
            />
          </div>
        )}
      </div>

      <div className={styles.lessons}>
        {lessons.length === 0 ? (
          <div className={styles.empty}>Уроки ещё не добавлены</div>
        ) : (
          lessons.map((lesson, i) => {
            const done = progress[lesson.id]?.completed
            return (
              <Link
                key={lesson.id}
                to={token ? `/lesson/${lesson.id}` : '/login'}
                className={`${styles.lessonCard} ${done ? styles.done : ''}`}
              >
                <div className={styles.lessonNum}>{done ? '✓' : i + 1}</div>
                <div className={styles.lessonInfo}>
                  <span className={styles.lessonTitle}>{lesson.title}</span>
                  <span className={styles.lessonXp}>+{lesson.xp_reward} XP</span>
                </div>
                <span className={styles.arrow}>{token ? '→' : '🔒'}</span>
              </Link>
            )
          })
        )}
      </div>

      {!token && (
        <div className={styles.loginPrompt}>
          <p>Войди в аккаунт чтобы начать обучение</p>
          <Link to="/login" className={styles.loginBtn}>Войти</Link>
        </div>
      )}
    </div>
  )
}
