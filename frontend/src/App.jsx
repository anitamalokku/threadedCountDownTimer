import { useEffect, useState } from 'react'
import TimerForm from './components/TimerForm.jsx'
import TimerList from './components/TimerList.jsx'
import { createTimer, getTimers } from './services/timerApi.js'
import './App.css'

function App() {
  const [timers, setTimers] = useState([])
  const [listError, setListError] = useState('')
  const [isFormOpen, setIsFormOpen] = useState(false)

  useEffect(() => {
    getTimers()
      .then(setTimers)
      .catch((error) => setListError(error.message))
  }, [])

  useEffect(() => {
    if (!isFormOpen) {
      return
    }

    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        setIsFormOpen(false)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isFormOpen])

  async function handleCreate({ name, duration_seconds }) {
    await createTimer(name, duration_seconds)
    setIsFormOpen(false)

    try {
      const updatedTimers = await getTimers()
      setTimers(updatedTimers)
      setListError('')
    } catch (error) {
      setListError(`Timer created, but the list could not be refreshed: ${error.message}`)
    }
  }

  return (
    <main className="app">
      <header className="page-title">
        <h1>TickDown Timer</h1>
      </header>
      <section className="app-header" aria-label="Timer actions">
        <p className="timer-intro">Set a duration and create a countdown timer.</p>
        <button
          className="add-timer-button"
          type="button"
          onClick={() => setIsFormOpen(true)}
        >
          Add timer
        </button>
      </section>
      <TimerList timers={timers} />

      {isFormOpen && (
        <div
          className="modal-backdrop"
          onClick={(event) => {
            if (event.target === event.currentTarget) {
              setIsFormOpen(false)
            }
          }}
        >
          <section
            className="timer-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="timer-modal-title"
          >
            <div className="modal-header">
              <h2 id="timer-modal-title">Create a timer</h2>
              <button
                className="close-modal-button"
                type="button"
                aria-label="Close"
                onClick={() => setIsFormOpen(false)}
              >
                ×
              </button>
            </div>
            <TimerForm onCreate={handleCreate} />
          </section>
        </div>
      )}
    </main>
  )
}

export default App
