import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { API_BASE_URL, getReports, getUsers } from './api/bugReportsApi'
import FiltersBar from './components/FiltersBar'
import ReportList from './components/ReportList'
import ThemeToggle from './components/ThemeToggle'

const THEME_STORAGE_KEY = 'bug-panel-theme'

const initialFilters = {
  query: '',
  nickname: '',
  accountId: '',
}

function getInitialTheme() {
  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY)
  if (savedTheme === 'light' || savedTheme === 'dark') {
    return savedTheme
  }

  return 'light'
}

function toTimestamp(value) {
  const timestamp = Date.parse(value)
  return Number.isNaN(timestamp) ? 0 : timestamp
}

function App() {
  const [theme, setTheme] = useState(getInitialTheme)
  const [reports, setReports] = useState([])
  const [usersById, setUsersById] = useState({})
  const [filters, setFilters] = useState(initialFilters)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    localStorage.setItem(THEME_STORAGE_KEY, theme)
  }, [theme])

  useEffect(() => {
    let isActive = true

    async function loadData() {
      setLoading(true)
      setError('')

      try {
        const [fetchedReports, fetchedUsers] = await Promise.all([getReports(), getUsers()])

        console.log('fetchedReports is ', fetchedUsers)
        console.log('fetchedUsers is ', fetchedUsers)


        if (!isActive) return

        const usersMap = Object.fromEntries(
          fetchedUsers.map((user) => [user.accountId, user.nickname]),
        )

        setUsersById(usersMap)
        setReports(fetchedReports)
      } catch (loadError) {
        if (!isActive) return
        setError(
          loadError instanceof Error
            ? `${loadError.message}. Проверьте VITE_API_BASE_URL и CORS на API.`
            : 'Не удалось загрузить данные.',
        )
      } finally {
        if (isActive) {
          setLoading(false)
        }
      }
    }

    loadData()

    return () => {
      isActive = false
    }
  }, [])

  const preparedReports = useMemo(() => {
    const query = filters.query.trim().toLowerCase()
    const nickname = filters.nickname.trim().toLowerCase()
    const accountId = filters.accountId.trim()

    return reports
      .map((report) => ({
        ...report,
        nickname: usersById[report.accountId] ?? report.nickname ?? '',
      }))
      .filter((report) => {
        if (query) {
          const haystack = `${report.title} ${report.text}`.toLowerCase()
          if (!haystack.includes(query)) return false
        }

        if (nickname) {
          if (!report.nickname.toLowerCase().includes(nickname)) return false
        }

        if (accountId) {
          if (!report.accountId.includes(accountId)) return false
        }

        return true
      })
      .sort((a, b) => toTimestamp(b.createdAt) - toTimestamp(a.createdAt))
  }, [filters, reports, usersById])

  function handleFilterChange(field, value) {
    setFilters((prev) => ({ ...prev, [field]: value }))
  }

  function toggleTheme() {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }

  return (
    <div className="app" data-theme={theme}>
      <header className="top-bar">
        <div>
          <h1>Bug Reports</h1>
          <p>Мир Танков • API: {API_BASE_URL}</p>
        </div>
        <ThemeToggle theme={theme} onToggle={toggleTheme} />
      </header>

      <main className="content">
        <FiltersBar
          filters={filters}
          onChange={handleFilterChange}
          onReset={() => setFilters(initialFilters)}
        />

        <div className="summary">Найдено репортов: {preparedReports.length}</div>

        <ReportList reports={preparedReports} loading={loading} error={error} />
      </main>
    </div>
  )
}

export default App
