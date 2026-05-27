import { useEffect, useState, useCallback, useMemo } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import Editor from '@monaco-editor/react'
import ReactMarkdown from 'react-markdown'
import api from '../api/axios'
import styles from './LessonPage.module.css'

const LANG_MAP = { python: 'python', javascript: 'javascript', html: 'html' }
const EXT_MAP  = { python: 'solution.py', javascript: 'solution.js', html: 'index.html' }

export default function LessonPage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [lesson, setLesson]       = useState(null)
  const [siblings, setSiblings]   = useState([])   // все уроки курса
  const [code, setCode]           = useState('')
  const [result, setResult]       = useState(null)
  const [running, setRunning]     = useState(false)
  const [tab, setTab]             = useState('theory')
  const [outTab, setOutTab]       = useState('output')  // 'output' | 'tests'
  const [outputOpen, setOutputOpen] = useState(false)
  const [hintsRevealed, setHintsRevealed] = useState(0)
  const [xpAnim, setXpAnim] = useState(null)
  const [htmlPreview, setHtmlPreview] = useState('')

  useEffect(() => {
    setResult(null)
    setOutputOpen(false)
    setHintsRevealed(0)
    api.get(`/api/lessons/${id}`).then(async r => {
      const l = r.data
      setLesson(l)
      setCode(l.starter_code || '')
      // загружаем список уроков курса для навигации
      try {
        const sibs = await api.get(`/api/lessons/course/${l.course_id}`)
        setSiblings(sibs.data)
      } catch { /* ignore */ }
    })
  }, [id])

  // Живое превью для HTML уроков и React (код начинается с <!DOCTYPE)
  const isHtmlLike = lesson?.language === 'html' || code.trimStart().startsWith('<!DOCTYPE')

  useEffect(() => {
    if (!isHtmlLike) return
    const t = setTimeout(() => setHtmlPreview(code), 400)
    return () => clearTimeout(t)
  }, [code, isHtmlLike])

  const runCode = useCallback(async () => {
    if (running || !lesson) return
    setRunning(true)
    setResult(null)
    setOutputOpen(true)
    setOutTab('output')
    try {
      const { data } = await api.post('/api/code/run', {
        lesson_id: parseInt(id),
        language: lesson.language || 'python',
        code,
      })
      setResult(data)
      if (data.total_tests > 0) setOutTab('tests')
      if (data.xp_earned > 0) {
        setXpAnim(data.xp_earned)
        setTimeout(() => setXpAnim(null), 1800)
      }
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Ошибка соединения с сервером'
      setResult({ success: false, error: msg })
    } finally {
      setRunning(false)
    }
  }, [running, lesson, id, code])

  // Ctrl+Enter — запустить
  useEffect(() => {
    const handler = e => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') runCode()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [runCode])

  const hints = useMemo(() => {
    if (!lesson?.hints) return []
    try { return JSON.parse(lesson.hints) } catch { return [] }
  }, [lesson?.hints])

  if (!lesson) return <div className={styles.loading}>Загружаем урок...</div>

  const idx     = siblings.findIndex(l => l.id === lesson.id)
  const prevLesson = siblings[idx - 1] ?? null
  const nextLesson = siblings[idx + 1] ?? null
  const filename   = EXT_MAP[lesson.language] || 'solution.py'

  // разбираем вывод тестов построчно
  const testLines = result?.output
    ? result.output.split('\n').filter(l => l.startsWith('✓') || l.startsWith('✗'))
    : []
  const stdout = result?.output
    ? result.output.split('\n').filter(l => !l.startsWith('✓') && !l.startsWith('✗')).join('\n').trim()
    : ''

  return (
    <>
    <div className={styles.wrap}>

      {/* ─── Top bar ─── */}
      <div className={styles.topbar}>
        <Link to={`/courses/${lesson.course_id}`} className={styles.backLink}>
          ← Назад к курсу
        </Link>
        <div className={styles.lessonTitle}>
          {idx >= 0 && <span className={styles.lessonNum}>Урок {idx + 1}</span>}
          <span className={styles.lessonName}>{lesson.title}</span>
        </div>
        <div className={styles.navBtns}>
          <button
            className={styles.navBtn}
            disabled={!prevLesson}
            onClick={() => prevLesson && navigate(`/lesson/${prevLesson.id}`)}
          >← Пред.</button>
          <span className={styles.navCounter}>
            {idx >= 0 ? `${idx + 1} / ${siblings.length}` : ''}
          </span>
          <button
            className={styles.navBtn}
            disabled={!nextLesson}
            onClick={() => nextLesson && navigate(`/lesson/${nextLesson.id}`)}
          >След. →</button>
        </div>
      </div>

      {/* ─── Main ─── */}
      <div className={styles.page}>

        {/* Левая панель */}
        <div className={styles.left}>
          <div className={styles.tabs}>
            <button
              className={tab === 'theory' ? styles.activeTab : styles.tab}
              onClick={() => setTab('theory')}
            >📖 Теория</button>
            <button
              className={tab === 'task' ? styles.activeTab : styles.tab}
              onClick={() => setTab('task')}
            >✏️ Задание</button>
          </div>

          <div className={styles.content}>
            {tab === 'theory' ? (
              <div className={styles.markdown}>
                <ReactMarkdown>{lesson.content || 'Теория скоро появится.'}</ReactMarkdown>
              </div>
            ) : (
              <div className={styles.task}>
                <div className={styles.taskHeader}>
                  <h3>Задание</h3>
                  <span className={styles.xpBadge}>+{lesson.xp_reward} XP</span>
                </div>
                <p className={styles.taskDesc}>{lesson.title}</p>

                {hints.length > 0 && (
                  <div className={styles.hintsSection}>
                    {hints.slice(0, hintsRevealed).map((hint, i) => (
                      <div key={i} className={styles.hintCard}>
                        <span className={styles.hintIcon}>💡</span>
                        <div>
                          <div className={styles.hintLabel}>Подсказка {i + 1}</div>
                          <div className={styles.hintText}>{hint}</div>
                        </div>
                      </div>
                    ))}
                    {hintsRevealed < hints.length && (
                      <button
                        className={styles.hintBtn}
                        onClick={() => setHintsRevealed(r => r + 1)}
                      >
                        💡 {hintsRevealed === 0 ? 'Показать подсказку' : 'Следующая подсказка'}
                        <span className={styles.hintCounter}>{hintsRevealed}/{hints.length}</span>
                      </button>
                    )}
                  </div>
                )}

                {result && (
                  <div className={result.success ? styles.successBox : styles.errorBox}>
                    <div className={styles.resultIcon}>{result.success ? '✓' : '✗'}</div>
                    <div>
                      <div className={styles.resultTitle}>
                        {result.success ? 'Отлично! Задание выполнено' : 'Попробуй ещё раз'}
                      </div>
                      {result.success && result.xp_earned > 0 && (
                        <div className={styles.xpEarned}>+{result.xp_earned} XP заработано</div>
                      )}
                      {!result.success && result.error && (
                        <div className={styles.errorMsg}>{result.error}</div>
                      )}
                    </div>
                  </div>
                )}

                {result?.success && nextLesson && (
                  <button
                    className={styles.nextBtn}
                    onClick={() => navigate(`/lesson/${nextLesson.id}`)}
                  >
                    Следующий урок →
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Правая панель */}
        <div className={styles.right}>
          <div className={styles.editorHeader}>
            <div className={styles.editorLeft}>
              <span className={styles.fileTab}>{filename}</span>
            </div>
            <div className={styles.editorRight}>
              <span className={styles.shortcut}>Ctrl+Enter</span>
              <button
                className={`${styles.runBtn} ${running ? styles.runBtnRunning : ''}`}
                onClick={runCode}
                disabled={running}
              >
                {running ? <><span className={styles.spinner} /> Выполняется...</> : '▶ Запустить'}
              </button>
            </div>
          </div>

          {/* Редактор */}
          <div className={styles.editorWrap}>
            <Editor
              language={LANG_MAP[lesson.language] || 'python'}
              value={code}
              onChange={val => setCode(val || '')}
              theme="vs-dark"
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                lineNumbers: 'on',
                renderLineHighlight: 'all',
                padding: { top: 12 },
              }}
            />
          </div>

          {/* HTML превью или терминал */}
          {isHtmlLike ? (
            <div className={styles.htmlPreviewPanel}>
              <div className={styles.htmlPreviewHeader}>
                <span>🌐 Превью</span>
                {result?.success && <span className={styles.htmlPreviewOk}>✓ Засчитано</span>}
              </div>
              <iframe
                className={styles.htmlFrame}
                srcDoc={htmlPreview}
                title="HTML Preview"
                sandbox="allow-scripts"
              />
            </div>
          ) : (
          <div className={`${styles.terminal} ${outputOpen ? styles.terminalOpen : ''}`}>
            <div className={styles.terminalHeader} onClick={() => setOutputOpen(o => !o)}>
              <div className={styles.terminalTabs}>
                <button
                  className={outTab === 'output' ? styles.termTabActive : styles.termTab}
                  onClick={e => { e.stopPropagation(); setOutTab('output') }}
                >Вывод</button>
                {result?.total_tests > 0 && (
                  <button
                    className={outTab === 'tests' ? styles.termTabActive : styles.termTab}
                    onClick={e => { e.stopPropagation(); setOutTab('tests') }}
                  >
                    Тесты
                    <span className={result.passed_tests === result.total_tests
                      ? styles.testsBadgeOk : styles.testsBadgeFail}>
                      {result.passed_tests}/{result.total_tests}
                    </span>
                  </button>
                )}
              </div>
              <span className={styles.terminalToggle}>{outputOpen ? '▼' : '▲'}</span>
            </div>

            {outputOpen && (
              <div className={styles.terminalBody}>
                {outTab === 'output' ? (
                  <pre className={styles.termOutput}>
                    {running && <span className={styles.termRunning}>● Выполняется...</span>}
                    {!running && !result && <span className={styles.termHint}>Запусти код чтобы увидеть вывод</span>}
                    {result?.error && !result.success && (
                      <span className={styles.termError}>{result.error}</span>
                    )}
                    {stdout && <span>{stdout}</span>}
                  </pre>
                ) : (
                  <div className={styles.testsList}>
                    {testLines.map((line, i) => (
                      <div key={i} className={line.startsWith('✓') ? styles.testPass : styles.testFail}>
                        {line}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
          )}
        </div>
      </div>
    </div>

    {xpAnim && (
      <div className={styles.xpPopup}>
        <span className={styles.xpPopupIcon}>⭐</span>
        +{xpAnim} XP
      </div>
    )}
    </>
  )
}
