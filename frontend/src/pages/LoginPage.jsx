import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import styles from './Auth.module.css'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await login(email, password)
      navigate('/courses')
    } catch (err) {
      setError(err.response?.data?.detail || 'Неверный email или пароль')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      {/* Левая панель */}
      <div className={styles.left}>
        <Link to="/" className={styles.brand}>&lt;/&gt; CodeLearn</Link>
        <div className={styles.leftContent}>
          <h2 className={styles.leftTitle}>Добро пожаловать обратно!</h2>
          <p className={styles.leftSub}>Продолжай учиться и зарабатывать XP</p>
          <div className={styles.features}>
            {[
              { icon: '⚡', text: 'Запускай код прямо в браузере' },
              { icon: '📈', text: 'Отслеживай свой прогресс' },
              { icon: '🏆', text: 'Зарабатывай XP за каждый урок' },
            ].map(f => (
              <div key={f.text} className={styles.feature}>
                <span className={styles.featureIcon}>{f.icon}</span>
                <span>{f.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Правая панель — форма */}
      <div className={styles.right}>
        <div className={styles.formWrap}>
          <div className={styles.formHeader}>
            <h1 className={styles.formTitle}>Вход в аккаунт</h1>
            <p className={styles.formSub}>
              Нет аккаунта? <Link to="/register" className={styles.link}>Зарегистрироваться</Link>
            </p>
          </div>

          {error && (
            <div className={styles.errorBox}>
              <span>⚠</span> {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.field}>
              <label className={styles.label}>Email</label>
              <input
                className={styles.input}
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                autoFocus
              />
            </div>

            <div className={styles.field}>
              <div className={styles.labelRow}>
                <label className={styles.label}>Пароль</label>
              </div>
              <div className={styles.inputWrap}>
                <input
                  className={styles.input}
                  type={showPass ? 'text' : 'password'}
                  placeholder="••••••••"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                />
                <button type="button" className={styles.eyeBtn} onClick={() => setShowPass(p => !p)}>
                  {showPass ? '🙈' : '👁'}
                </button>
              </div>
            </div>

            <button className={styles.submitBtn} type="submit" disabled={loading}>
              {loading
                ? <><span className={styles.spinner} /> Входим...</>
                : 'Войти →'
              }
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
