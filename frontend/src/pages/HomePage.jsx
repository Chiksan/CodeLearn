import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import styles from './HomePage.module.css'

const tracks = [
  { icon: '🐍', name: 'Python', desc: 'Анализ данных, автоматизация, бэкенд', badge: 'С нуля', color: '#3572A5', lang: 'python' },
  { icon: '⚡', name: 'JavaScript', desc: 'Веб, интерфейсы, Node.js', badge: 'Все уровни', color: '#F7DF1E', lang: 'javascript' },
  { icon: '🎨', name: 'HTML/CSS', desc: 'Разметка и стили страниц', badge: 'С нуля', color: '#E34F26', lang: 'html' },
  { icon: '⚙️', name: 'Алгоритмы', desc: 'Структуры данных и задачи', badge: 'Скоро', color: '#534AB7', lang: null },
]

const steps = [
  { num: '01', title: 'Выбери курс', desc: 'Python, JavaScript или HTML — выбирай по уровню и цели' },
  { num: '02', title: 'Читай теорию', desc: 'Краткое объяснение с примерами прямо в браузере' },
  { num: '03', title: 'Пиши код', desc: 'Редактор с подсветкой синтаксиса, запускай и видь результат' },
  { num: '04', title: 'Получай XP', desc: 'Следи за прогрессом и зарабатывай очки опыта' },
]

const CODE_PREVIEW = `def hello(name):
    print(f"Привет, {name}!")

hello("Мир")
# → Привет, Мир!`

export default function HomePage() {
  const { token } = useAuthStore()

  return (
    <div className={styles.page}>

      {/* ─── Hero ─────────────────────────────────────────── */}
      <section className={styles.hero}>
        <div className={styles.heroText}>
          <div className={styles.heroBadge}>Бесплатно · В браузере · Без установок</div>
          <h1>
            Учись программировать<br />
            <span className={styles.accent}>в интерактивном</span><br />
            формате
          </h1>
          <p>Python, JavaScript, HTML/CSS — пиши код прямо в браузере и получай мгновенный результат</p>
          <div className={styles.buttons}>
            <Link to="/courses" className={styles.btnPrimary}>
              Начать бесплатно →
            </Link>
            {!token && (
              <Link to="/register" className={styles.btnOutline}>Создать аккаунт</Link>
            )}
          </div>
        </div>

        <div className={styles.codeCard}>
          <div className={styles.codeBar}>
            <span className={styles.dot} style={{ background: '#ff5f57' }} />
            <span className={styles.dot} style={{ background: '#febc2e' }} />
            <span className={styles.dot} style={{ background: '#28c840' }} />
            <span className={styles.codeFilename}>solution.py</span>
          </div>
          <pre className={styles.code}>{CODE_PREVIEW}</pre>
          <div className={styles.codeOutput}>
            <span className={styles.outputLabel}>Вывод</span>
            <span>Привет, Мир!</span>
          </div>
        </div>
      </section>

      {/* ─── Stats ────────────────────────────────────────── */}
      <section className={styles.stats}>
        {[
          { value: '3', label: 'Языка' },
          { value: '48+', label: 'Уроков' },
          { value: '150+', label: 'Заданий' },
          { value: '100%', label: 'Бесплатно' },
        ].map(s => (
          <div key={s.label} className={styles.stat}>
            <strong>{s.value}</strong>
            <span>{s.label}</span>
          </div>
        ))}
      </section>

      {/* ─── Tracks ───────────────────────────────────────── */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Что ты выучишь</h2>
        <div className={styles.tracks}>
          {tracks.map(t => {
            const inner = (
              <>
                <div className={styles.trackTop}>
                  <span className={styles.trackIcon}>{t.icon}</span>
                  <span className={styles.trackBadge}>{t.badge}</span>
                </div>
                <h3 className={styles.trackName}>{t.name}</h3>
                <p className={styles.trackDesc}>{t.desc}</p>
                <div className={styles.trackBar} style={{ background: t.color + '22' }}>
                  <div className={styles.trackBarFill} style={{ background: t.color }} />
                </div>
              </>
            )
            return t.lang
              ? <Link key={t.name} to={`/track/${t.lang}`} className={`${styles.trackCard} ${styles.trackCardLink}`}>{inner}</Link>
              : <div key={t.name} className={styles.trackCard}>{inner}</div>
          })}
        </div>
      </section>

      {/* ─── How it works ─────────────────────────────────── */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Как это работает</h2>
        <div className={styles.steps}>
          {steps.map(s => (
            <div key={s.num} className={styles.step}>
              <div className={styles.stepNum}>{s.num}</div>
              <h3 className={styles.stepTitle}>{s.title}</h3>
              <p className={styles.stepDesc}>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ─── CTA ──────────────────────────────────────────── */}
      <section className={styles.cta}>
        <h2>Готов начать?</h2>
        <p>Присоединяйся и начни писать код уже сегодня</p>
        <Link to={token ? '/courses' : '/register'} className={styles.ctaBtn}>
          {token ? 'Перейти к курсам' : 'Зарегистрироваться бесплатно'}
        </Link>
      </section>

    </div>
  )
}
