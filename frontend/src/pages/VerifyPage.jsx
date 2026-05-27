import { useEffect, useState } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import api from '../api/axios'
import styles from './VerifyPage.module.css'

export default function VerifyPage() {
  const [searchParams] = useSearchParams()
  const [status, setStatus] = useState('loading') // loading | success | error
  const [message, setMessage] = useState('')

  useEffect(() => {
    const token = searchParams.get('token')
    if (!token) { setStatus('error'); setMessage('Неверная ссылка'); return }

    api.get(`/api/auth/verify?token=${token}`)
      .then(r => { setStatus('success'); setMessage(r.data.message) })
      .catch(e => { setStatus('error'); setMessage(e.response?.data?.detail || 'Ошибка подтверждения') })
  }, [])

  return (
    <div className={styles.wrap}>
      <div className={styles.card}>
        {status === 'loading' && (
          <>
            <div className={styles.spinner} />
            <p className={styles.text}>Проверяем ссылку...</p>
          </>
        )}
        {status === 'success' && (
          <>
            <div className={styles.icon}>✅</div>
            <h2 className={styles.title}>Email подтверждён!</h2>
            <p className={styles.text}>{message}</p>
            <Link to="/login" className={styles.btn}>Войти в аккаунт</Link>
          </>
        )}
        {status === 'error' && (
          <>
            <div className={styles.icon}>❌</div>
            <h2 className={styles.title}>Ошибка</h2>
            <p className={styles.text}>{message}</p>
            <Link to="/register" className={styles.btn}>Зарегистрироваться снова</Link>
          </>
        )}
      </div>
    </div>
  )
}
