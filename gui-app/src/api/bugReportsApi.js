const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

function extractArray(payload, fallbackKeys = []) {
  if (Array.isArray(payload)) return payload

  for (const key of fallbackKeys) {
    if (Array.isArray(payload?.[key])) {
      return payload[key]
    }
  }

  return []
}

async function fetchJson(path) {
  const url = `${API_BASE_URL}${path}`
  console.log(url)
  const response = await fetch(url)
  console.log(response)

  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${response.statusText}`)
  }

  return response.json()
}

export async function getReports() {
  const payload = await fetchJson('/reports/')
  const reports = extractArray(payload, ['reports', 'data', 'items'])

  return reports.map((report, index) => ({
    id: report.id ?? `${report.account_id ?? 'unknown'}-${report.created_at ?? index}`,
    accountId: String(report.account_id ?? ''),
    title: report.title ?? '',
    text: report.text ?? '',
    createdAt: report.created_at ?? '',
  }))
}

export async function getUsers() {
  const payload = await fetchJson('/users/')
  const users = extractArray(payload, ['users', 'data', 'items'])

  return users.map((user) => ({
    accountId: String(user.account_id ?? ''),
    nickname: user.nickname ?? '',
  }))
}

export { API_BASE_URL }
