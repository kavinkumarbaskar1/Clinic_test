import Button from '../components/ui/Button.jsx';

function Topbar({
  isDarkTheme,
  personas,
  selectedPersona,
  onNavigate,
  onPersonaChange,
  onToggleTheme,
}) {
  return (
    <header className="shell-topbar">
      <a
        className="shell-brand"
        href="/"
        onClick={(event) => onNavigate(event, '/')}
      >
        <span className="shell-brand__mark" aria-hidden="true">
          +
        </span>
        <span>
          <span className="shell-brand__name">Clinic Booking</span>
          <span className="shell-brand__tagline">Care access desk</span>
        </span>
      </a>
      <div className="shell-topbar__tools">
        <label className="persona-picker">
          <span>Persona</span>
          <select value={selectedPersona} onChange={onPersonaChange}>
            {personas.map((persona) => (
              <option key={persona.id} value={persona.id}>
                {persona.label}
              </option>
            ))}
          </select>
        </label>
        <Button
          type="button"
          variant="secondary"
          aria-pressed={isDarkTheme}
          onClick={onToggleTheme}
        >
          {isDarkTheme ? 'Light theme' : 'Dark theme'}
        </Button>
      </div>
    </header>
  );
}

export default Topbar;
