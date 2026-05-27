import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import styles from './Auth.module.css'

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', username: '', password: '' })
  const [showPass, setShowPass] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState('register') // 'register' | 'verify'
  const [code, setCode] = useState('')
  const [verified, setVerified] = useState(false)
  const navigate = useNavigate()

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await api.post('/api/auth/register', {
        email: form.email,
        username: form.username,
        password: form.password,
      })
      if (res.data?.auto_verified) {
        setVerified(true)
        setTimeout(() => navigate('/login'), 2000)
      } else {
        setStep('verify')
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка при регистрации')
    } finally {
      setLoading(false)
    }
  }

  const handleVerify = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await api.post('/api/auth/verify-code', { email: form.email, code })
      setVerified(true)
      setTimeout(() => navigate('/login'), 2000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Неверный код')
    } finally {
      setLoading(false)
    }
  }

  if (verified) return (
    <div className={styles.page}>
      <div className={styles.left}>
        <Link to="/" className={styles.brand}>&lt;/&gt; CodeLearn</Link>
      </div>
      <div className={styles.right}>
        <div className={styles.formWrap} style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 56, marginBottom: 16 }}>✅</div>
          <h2 className={styles.formTitle}>Email подтверждён!</h2>
          <p className={styles.formSub} style={{ marginTop: 10 }}>Перенаправляем ко входу...</p>
        </div>
      </div>
    </div>
  )

  if (step === 'verify') return (
    <div className={styles.page}>
      <div className={styles.left}>
        <Link to="/" className={styles.brand}>&lt;/&gt; CodeLearn</Link>
        <div className={styles.leftContent}>
          <h2 className={styles.leftTitle}>Почти готово!</h2>
          <p className={styles.leftSub}>Осталось подтвердить email</p>
        </div>
      </div>
      <div className={styles.right}>
        <div className={styles.formWrap}>
          <div className={styles.formHeader}>
            <div style={{ fontSize: 48, marginBottom: 12 }}>📧</div>
            <h1 className={styles.formTitle}>Введи код</h1>
            <p className={styles.formSub}>
              Мы отправили 6-значный код на <strong>{form.email}</strong>
            </p>
          </div>

          {error && (
            <div className={styles.errorBox}>
              <span>⚠</span> {error}
            </div>
          )}

          <form onSubmit={handleVerify} className={styles.form}>
            <div className={styles.field}>
              <label className={styles.label}>Код из письма</label>
              <input
                className={styles.input}
                type="text"
                placeholder="123456"
                value={code}
                onChange={e => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                required
                autoFocus
                maxLength={6}
                style={{ fontSize: 28, letterSpacing: 8, textAlign: 'center' }}
              />
            </div>

            <button className={styles.submitBtn} type="submit" disabled={loading || code.length !== 6}>
              {loading ? <><span className={styles.spinner} /> Проверяем...</> : 'Подтвердить →'}
            </button>
          </form>

          <p style={{ fontSize: 13, color: '#aaa', marginTop: 20, textAlign: 'center' }}>
            Не пришло? Проверь папку <strong>Спам</strong>.
          </p>
        </div>
      </div>
    </div>
  )

  return (
    <div className={styles.page}>
      {/* Левая панель */}
      <div className={styles.left}>
        <Link to="/" className={styles.brand}>&lt;/&gt; CodeLearn</Link>
        <div className={styles.leftContent}>
          <h2 className={styles.leftTitle}>Начни учиться бесплатно</h2>
          <p className={styles.leftSub}>Присоединяйся и пиши код уже сегодня</p>
          <div className={styles.features}>
            {[
              { icon: '🐍', text: 'Python, JavaScript, HTML/CSS' },
              { icon: '💻', text: 'Редактор кода прямо в браузере' },
              { icon: '🎯', text: 'Интерактивные задания с тестами' },
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
            <h1 className={styles.formTitle}>Создать аккаунт</h1>
            <p className={styles.formSub}>
              Уже есть аккаунт? <Link to="/login" className={styles.link}>Войти</Link>
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
                name="email"
                placeholder="you@example.com"
                value={form.email}
                onChange={handleChange}
                required
                autoFocus
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Имя пользователя</label>
              <input
                className={styles.input}
                type="text"
                name="username"
                placeholder="chiksan"
                value={form.username}
                onChange={handleChange}
                required
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Пароль</label>
              <div className={styles.inputWrap}>
                <input
                  className={styles.input}
                  type={showPass ? 'text' : 'password'}
                  name="password"
                  placeholder="Минимум 6 символов"
                  value={form.password}
                  onChange={handleChange}
                  required
                  minLength={6}
                />
                <button type="button" className={styles.eyeBtn} onClick={() => setShowPass(p => !p)}>
                  {showPass ? '🙈' : '👁'}
                </button>
              </div>
            </div>

            <button className={styles.submitBtn} type="submit" disabled={loading}>
              {loading
                ? <><span className={styles.spinner} /> Создаём аккаунт...</>
                : 'Зарегистрироваться →'
              }
            </button>
          </form>

          <p className={styles.terms}>
            Регистрируясь, ты соглашаешься с условиями использования платформы
          </p>
        </div>
      </div>
    </div>
  )
}
