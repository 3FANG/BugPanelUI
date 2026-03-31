import ReportCard from './ReportCard'

function ReportList({ reports, loading, error }) {
  if (loading) {
    return <div className="state-message">Загрузка репортов...</div>
  }

  if (error) {
    return <div className="state-message error">{error}</div>
  }

  if (reports.length === 0) {
    return <div className="state-message">По текущим фильтрам ничего не найдено.</div>
  }

  return (
    <section className="reports-list" aria-label="Список репортов">
      {reports.map((report) => (
        <ReportCard key={report.id} report={report} />
      ))}
    </section>
  )
}

export default ReportList
