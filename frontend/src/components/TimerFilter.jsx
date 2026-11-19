const FILTERS = ["All", "Started", "Paused", "Finished"];

function TimerFilter({ value, onChange }) {
  return (
    <div className="timer-filter" role="group" aria-label="Filter timers by status">
      {FILTERS.map((f) => (
        <button
          key={f}
          type="button"
          className={f === value ? "active" : ""}
          aria-pressed={f === value}
          onClick={() => onChange(f)}
        >
          {f}
        </button>
      ))}
    </div>
  );
}

export default TimerFilter;