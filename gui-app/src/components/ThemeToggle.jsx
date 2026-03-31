function ThemeToggle({ theme, onToggle }) {
  const isDark = theme === 'dark'

  return (
    <button className="theme-toggle" type="button" onClick={onToggle}>
      {isDark ? 'Светлая тема' : 'Темная тема'}
    </button>
  )
}

export default ThemeToggle
