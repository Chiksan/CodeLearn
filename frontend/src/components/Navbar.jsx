import { useState, useRef, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import styles from './Navbar.module.css'

export default function Navbar() {
  const { user, token, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const dropdownRef = useRef(null)

  const handleLogout = () => {
    logout()
    setDropdownOpen(false)
    navigate('/')
  }

  // Закрываем dropdown при клике вне
  useEffect(() => {
    const handler = e => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  // Закрываем мобильное меню при смене страницы
  useEffect(() => { setMobileOpen(false) }, [location.pathname])

  const isActive = path => location.pathname === path || location.pathname.startsWith(path + '/')

  return (
    <nav className={styles.nav}>
      {/* Логотип */}
      <Link to="/" className={styles.logo}>
        <span className={styles.logoIcon}>&lt;/&gt;</span>
        CodeLearn
      </Link>

      {/* Десктоп ссылки */}
      <div className={styles.links}>
        <Link
          to="/courses"
          className={`${styles.link} ${isActive('/courses') ? styles.linkActive : ''}`}
        >
          Курсы
        </Link>
        <Link
          to="/leaderboard"
          className={`${styles.link} ${isActive('/leaderboard') ? styles.linkActive : ''}`}
        >
          🏆 Рейтинг
        </Link>
      </div>

      {/* Правая часть */}
      <div className={styles.right}>
        {token && user ? (
          <div className={styles.userArea} ref={dropdownRef}>
            {/* Аватар кнопка с XP */}
            <button
              className={styles.avatarBtn}
              onClick={() => setDropdownOpen(o => !o)}
            >
              <div className={styles.avatar}>
                {user.username[0].toUpperCase()}
              </div>
              <span className={styles.username}>{user.username}</span>
              <span className={styles.xpInline}>⚡ {user.xp} XP</span>
              <span className={`${styles.chevron} ${dropdownOpen ? styles.chevronUp : ''}`}>▾</span>
            </button>

            {/* Dropdown */}
            {dropdownOpen && (
              <div className={styles.dropdown}>
                <div className={styles.dropdownHeader}>
                  <div className={styles.dropdownAvatar}>{user.username[0].toUpperCase()}</div>
                  <div>
                    <div className={styles.dropdownName}>{user.username}</div>
                    <div className={styles.dropdownEmail}>{user.email}</div>
                  </div>
                </div>
                <div className={styles.dropdownDivider} />
                <Link to="/profile" className={styles.dropdownItem} onClick={() => setDropdownOpen(false)}>
                  <span>👤</span> Профиль
                </Link>
                <Link to="/courses" className={styles.dropdownItem} onClick={() => setDropdownOpen(false)}>
                  <span>📚</span> Мои курсы
                </Link>
                <div className={styles.dropdownDivider} />
                <button className={styles.dropdownItemLogout} onClick={handleLogout}>
                  <span>🚪</span> Выйти
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className={styles.authBtns}>
            <Link to="/login" className={styles.btnLogin}>Войти</Link>
            <Link to="/register" className={styles.btnRegister}>Регистрация</Link>
          </div>
        )}

        {/* Мобильный бургер */}
        <button
          className={styles.burger}
          onClick={() => setMobileOpen(o => !o)}
          aria-label="Меню"
        >
          <span className={`${styles.burgerLine} ${mobileOpen ? styles.burgerLine1Open : ''}`} />
          <span className={`${styles.burgerLine} ${mobileOpen ? styles.burgerLineHide : ''}`} />
          <span className={`${styles.burgerLine} ${mobileOpen ? styles.burgerLine3Open : ''}`} />
        </button>
      </div>

      {/* Мобильное меню */}
      {mobileOpen && (
        <div className={styles.mobileMenu}>
          <Link to="/courses" className={styles.mobileLink}>Курсы</Link>
          <Link to="/leaderboard" className={styles.mobileLink}>🏆 Рейтинг</Link>
          {token ? (
            <>
              <Link to="/profile" className={styles.mobileLink}>Профиль</Link>
              <div className={styles.mobileDivider} />
              <button className={styles.mobileLinkBtn} onClick={handleLogout}>Выйти</button>
            </>
          ) : (
            <>
              <Link to="/login" className={styles.mobileLink}>Войти</Link>
              <Link to="/register" className={`${styles.mobileLink} ${styles.mobileLinkPrimary}`}>Регистрация</Link>
            </>
          )}
        </div>
      )}
    </nav>
  )
}
