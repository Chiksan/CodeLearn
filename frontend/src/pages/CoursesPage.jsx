import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'
import styles from './CoursesPage.module.css'

const LANG_META = {
  python: {
    icon: '🐍',
    name: 'Python',
    color: '#3572A5',
    bg: '#3572A515',
    desc: 'Анализ данных, автоматизация, веб-бэкенд. Один из самых востребованных языков в мире.',
  },
  javascript: {
    icon: '⚡',
    name: 'JavaScript',
    color: '#D4A017',
    bg: '#F7DF1E18',
    desc: 'Язык веба: фронтенд, интерактивность, React. Работает прямо в браузере.',
  },
  html: {
    icon: '🎨',
    name: 'HTML / CSS',
    color: '#E34F26',
    bg: '#E34F2615',
    desc: 'Основа любого сайта. Разметка, стили, адаптивная вёрстка и красивые интерфейсы.',
  },
}

function pluralCourses(n) {
  if (n % 10 === 1 && n % 100 !== 11) return `${n} курс`
  if ([2,3,4].includes(n % 10) && ![12,13,14].includes(n % 100)) return `${n} курса`
  return `${n} курсов`
}

export default function CoursesPage() {
  const [grouped, setGrouped] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/api/courses/')
      .then(r => {
        const g = {}
        r.data.forEach(course => {
          if (!g[course.language]) g[course.language] = []
          g[course.language].push(course)
        })
        setGrouped(g)
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Выбери направление</h1>
        <p className={styles.subtitle}>Выбери язык программирования и начни учиться</p>
      </div>

      {loading ? (
        <div className={styles.loading}>Загружаем курсы...</div>
      ) : (
        <div className={styles.langGrid}>
          {Object.entries(LANG_META).map(([lang, meta]) => {
            const courses = grouped[lang] || []
            return (
              <Link key={lang} to={`/track/${lang}`} className={styles.langCard}>
                <div className={styles.langIcon} style={{ background: meta.bg }}>
                  {meta.icon}
                </div>
                <div className={styles.langBody}>
                  <div className={styles.langTop}>
                    <h2 className={styles.langName}>{meta.name}</h2>
                    <span className={styles.langBadge} style={{ color: meta.color, background: meta.bg }}>
                      {pluralCourses(courses.length)}
                    </span>
                  </div>
                  <p className={styles.langDesc}>{meta.desc}</p>
                  <ul className={styles.courseList}>
                    {courses.map(c => (
                      <li key={c.id} className={styles.courseItem}>
                        <span className={styles.courseCheck} style={{ color: meta.color }}>→</span>
                        {c.title}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className={styles.langArrow} style={{ color: meta.color }}>→</div>
              </Link>
            )
          })}
        </div>
      )}
    </div>
  )
}
