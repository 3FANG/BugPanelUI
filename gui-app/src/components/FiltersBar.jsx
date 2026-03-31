function FiltersBar({ filters, onChange, onReset }) {
  return (
    <section className="filters" aria-label="Фильтры репортов">
      <input
        type="text"
        placeholder="Поиск по заголовку и тексту"
        value={filters.query}
        onChange={(event) => onChange('query', event.target.value)}
      />
      <input
        type="text"
        placeholder="Никнейм"
        value={filters.nickname}
        onChange={(event) => onChange('nickname', event.target.value)}
      />
      <input
        type="text"
        inputMode="numeric"
        placeholder="Account ID"
        value={filters.accountId}
        onChange={(event) => onChange('accountId', event.target.value)}
      />
      <button type="button" className="secondary" onClick={onReset}>
        Сбросить
      </button>
    </section>
  )
}

export default FiltersBar
