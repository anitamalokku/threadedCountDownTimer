import { useState } from 'react'

const emptyForm = {
  name: '',
  hours: '',
  minutes: '',
  seconds: '',
}

function TimerForm({ onCreate }) {
  const [form, setForm] = useState(emptyForm)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  function handleChange(event) {
    const { name, value } = event.target
    setForm((currentForm) => ({ ...currentForm, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    const name = form.name.trim()
    const hours = Number(form.hours)
    const minutes = Number(form.minutes)
    const seconds = Number(form.seconds)

    if (!name) {
      setError('Please enter a timer name.')
      return
    }

    if (
      ![hours, minutes, seconds].every(
        (value) => Number.isFinite(value) && value >= 0,
      )
    ) {
      setError('Hours, minutes, and seconds must be valid non-negative numbers.')
      return
    }

    const duration_seconds = hours * 3600 + minutes * 60 + seconds
    if (duration_seconds <= 0) {
      setError('Enter a total time greater than zero.')
      return
    }

    setIsSubmitting(true)
    try {
      await onCreate({ name, duration_seconds })
      setForm(emptyForm)
      setError('')
    } catch (createError) {
      setError(createError.message || 'The timer could not be created.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form className="timer-form" onSubmit={handleSubmit} noValidate>
      <label>
        Name
        <input
          name="name"
          type="text"
          value={form.name}
          onChange={handleChange}
          placeholder="e.g. Study session"
        />
      </label>

      <div className="time-fields">
        <label>
          Hours
          <input
            name="hours"
            type="number"
            min="0"
            step="1"
            value={form.hours}
            onChange={handleChange}
            placeholder="0"
          />
        </label>
        <label>
          Minutes
          <input
            name="minutes"
            type="number"
            min="0"
            step="1"
            value={form.minutes}
            onChange={handleChange}
            placeholder="0"
          />
        </label>
        <label>
          Seconds
          <input
            name="seconds"
            type="number"
            min="0"
            step="1"
            value={form.seconds}
            onChange={handleChange}
            placeholder="0"
          />
        </label>
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create Timer'}
      </button>
      {error && <p className="form-error" role="alert">{error}</p>}
    </form>
  )
}

export default TimerForm