const API_URL = 'http://localhost:5000/api/timers'

async function readResponse(response) {
  try {
    return await response.json()
  } catch {
    return null
  }
}

function getErrorMessage(data, response) {
  return (
    data?.message ||
    data?.error ||
    `Request failed with status ${response.status}.`
  )
}

export async function createTimer(name, duration_seconds) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, duration_seconds }),
  })
  const data = await readResponse(response)

  if (!response.ok) {
    throw new Error(getErrorMessage(data, response))
  }

  if (!data?.timer) {
    throw new Error('The server response did not include a timer.')
  }

  return data.timer
}

export async function getTimers() {
  const response = await fetch(API_URL)
  const data = await readResponse(response)

  if (!response.ok) {
    throw new Error(getErrorMessage(data, response))
  }

  if (!Array.isArray(data)) {
    throw new Error('The server response did not include a timer list.')
  }

  return data
}
