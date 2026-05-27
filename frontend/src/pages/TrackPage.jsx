import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api/axios'
import styles from './TrackPage.module.css'

const TRACK_META = {
  python: {
    icon: '🐍',
    name: 'Python',
    color: '#3572A5',
    desc: 'Полный путь от новичка до разработчика: основы языка, ООП, базы данных и FastAPI.',
  },
  javascript: {
    icon: '⚡',
    name: 'JavaScript',
    color: '#F0B429',
    desc: 'Язык веба: от переменных и функций до работы с массивами и DOM.',
  },
  html: {
    icon: '🎨',
    name: 'HTML / CSS',
    color: '#E34F26',
    desc: 'Основа любого сайта: разметка, стили и адаптивная вёрстка.',
  },
}

const LEVEL_LABELS = { beginner: 'Начинающий', intermediate: 'Средний', advanced: 'Продвинутый' }
const LEVEL_COLORS = { beginner: '#27ae60', intermediate: '#e67e22', advanced: '#8e44ad' }

export default function TrackPage() {
  const { lang } = useParams()
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)

  const meta = TRACK_META[lang]

  useEffect(() => {
    api.get('/api/courses/')
      .then(r => {
        const filtered = r.data
          .filter(c => c.language === lang)
          .sort((a, b) => {
            const order = { beginner: 0, intermediate: 1, advanced: 2 }
            return (order[a.level] ?? 3) - (order[b.level] ?? 3)
          })
        setCourses(filtered)
      })
      .catch(() => setCourses([]))
      .finally(() => setLoading(false))
  }, [lang])

  if (!meta) return (
    <div className={styles.notFound}>
      <p>Трек не найден</p>
      <Link to="/courses">← Все курсы</Link>
    </div>
  )

  if (loading) return <div className={styles.loading}>Загружаем...</div>

  return (
    <div className={styles.page}>

      {/* Hero */}
      <div className={styles.hero} style={{ borderColor: meta.color }}>
        <div className={styles.heroIcon} style={{ background: meta.color + '18' }}>
          {meta.icon}
        </div>
        <div>
          <div className={styles.heroLabel}>Трек</div>
          <h1 className={styles.heroTitle} style={{ color: meta.color }}>{meta.name}</h1>
          <p className={styles.heroDesc}>{meta.desc}</p>
          <div className={styles.heroStats}>
            <span>{courses.length} курсов</span>
            <span>·</span>
            <span>{courses.reduce((s, c) => s + (c.lesson_count || 0), 0)} уроков</span>
          </div>
        </div>
      </div>

      {/* Путь */}
      <div className={styles.pathWrap}>
        <h2 className={styles.pathTitle}>Учебный путь</h2>

        <div className={styles.path}>
          {courses.map((course, idx) => (
            <div key={course.id} className={styles.step}>

              {/* Линия соединения */}
              {idx < courses.length - 1 && (
                <div className={styles.connector}>
                  <div className={styles.connectorLine} style={{ background: meta.color + '40' }} />
                </div>
              )}

              {/* Номер шага */}
              <div className={styles.stepNum} style={{ background: meta.color, boxShadow: `0 4px 14px ${meta.color}40` }}>
                {idx + 1}
              </div>

              {/* Карточка курса */}
              <div className={styles.card}>
                <div className={styles.cardTop}>
                  <span
                    className={styles.level}
                    style={{ color: LEVEL_COLORS[course.level], background: LEVEL_COLORS[course.level] + '18' }}
                  >
                    {LEVEL_LABELS[course.level]}
                  </span>
                  <span className={styles.lessons}>{course.lesson_count} уроков</span>
                </div>

                <h3 className={styles.cardTitle}>{course.title}</h3>
                <p className={styles.cardDesc}>{course.description}</p>

                <Link
                  to={`/courses/${course.id}`}
                  className={styles.btn}
                  style={{ background: meta.color }}
                >
                  Перейти к курсу →
                </Link>
              </div>

            </div>
          ))}

          {courses.length === 0 && (
            <div className={styles.empty}>Курсы скоро появятся</div>
          )}
        </div>
      </div>

      <div className={styles.back}>
        <Link to="/courses" className={styles.backLink}>← Все курсы</Link>
      </div>
    </div>
  )
}
