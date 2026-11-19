import TimerCard from './TimerCard.jsx'

function TimerList({ timers }) {
  if (timers.length === 0) {
    return <p className="timer-list-empty">No timers yet.</p>
  }

  return (
    <section className="timer-list" aria-label="Timers">
      {timers.map((timer) => (
        <TimerCard key={timer.id} timer={timer} />
      ))}
    </section>
  )
}

export default TimerList