function formatDate(value) {
  if (!value) return 'Дата не указана'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return date.toLocaleString('ru-RU')
}

function ReportCard({ report }) {
  return (
    <article className="report-card">
      <header>
        <h3>{report.title || 'Без заголовка'}</h3>
        <time dateTime={report.createdAt || undefined}>{formatDate(report.createdAt)}</time>
      </header>

      <p>{report.text || 'Текст репорта отсутствует'}</p>

      <footer>
        <span className="pill">{report.nickname || 'Unknown'}</span>
        <span className="muted">account_id: {report.accountId || '—'}</span>
      </footer>
    </article>
  )
}

export default ReportCard
