import { useEffect, useState } from 'react'
import api from '../api/axios'
import { useAuthStore } from '../store/authStore'
import styles from './LeaderboardPage.module.css'

const MEDALS = ['🥇', '🥈', '🥉']
const MEDAL_LABELS = ['1-е место', '2-е место', '3-е место']

export default function LeaderboardPage() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const { user: me } = useAuthStore()

  useEffect(() => {
    api.get('/api/users/leaderboard')
      .then(r => setUsers(r.data))
      .finally(() => setLoading(false))
  }, [])

  const top3 = users.slice(0, 3)
  const rest = users.slice(3)

  return (
    <div className={styles.page}>
      <div className={styles.hero}>
        <div className={styles.heroIcon}>🏆</div>
        <h1 className={styles.heroTitle}>Лидерборд</h1>
        <p className={styles.heroSub}>Топ учеников по заработанному XP</p>
      </div>

      {loading ? (
        <div className={styles.loading}>
          <div className={styles.spinner} />
          <p>Загружаем рейтинг...</p>
        </div>
      ) : (
        <div className={styles.content}>

          {/* Подиум топ-3 */}
          {top3.length > 0 && (
            <div className={styles.podium}>
              {/* Перестановка: 2-й, 1-й, 3-й для визуального подиума */}
              {[top3[1], top3[0], top3[2]].map((u, visualIdx) => {
                if (!u) return <div key={visualIdx} className={styles.podiumSlot} />
                const rank = u.rank - 1
                const heights = [80, 110, 60]
                const isMe = me?.id === u.id
                return (
                  <div
                    key={u.id}
                    className={`${styles.podiumCard} ${styles[`podium${rank + 1}`]} ${isMe ? styles.podiumMe : ''}`}
                    style={{ '--bar-height': heights[visualIdx] + 'px' }}
                  >
                    <div className={styles.podiumMedal}>{MEDALS[rank]}</div>
                    <div className={styles.podiumAvatar}>
                      {u.username[0].toUpperCase()}
                    </div>
                    <div className={styles.podiumName}>{u.username}{isMe && ' (ты)'}</div>
                    <div className={styles.podiumXp}>⚡ {u.xp} XP</div>
                    <div className={styles.podiumLabel}>{MEDAL_LABELS[rank]}</div>
                    <div className={styles.podiumBar} />
                  </div>
                )
              })}
            </div>
          )}

          {/* Остальные места */}
          {rest.length > 0 && (
            <div className={styles.list}>
              {rest.map(u => {
                const isMe = me?.id === u.id
                return (
                  <div
                    key={u.id}
                    className={`${styles.row} ${isMe ? styles.rowMe : ''}`}
                  >
                    <div className={styles.rowRank}>#{u.rank}</div>
                    <div className={styles.rowAvatar}>
                      {u.username[0].toUpperCase()}
                    </div>
                    <div className={styles.rowInfo}>
                      <span className={styles.rowName}>
                        {u.username}{isMe && <span className={styles.meBadge}>ты</span>}
                      </span>
                      <span className={styles.rowJoined}>С {u.joined}</span>
                    </div>
                    <div className={styles.rowXp}>⚡ {u.xp} XP</div>
                  </div>
                )
              })}
            </div>
          )}

          {users.length === 0 && (
            <div className={styles.empty}>
              <div style={{ fontSize: 48, marginBottom: 12 }}>🌱</div>
              <p>Ещё никто не заработал XP. Стань первым!</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
