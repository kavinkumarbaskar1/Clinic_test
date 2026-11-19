import { useEffect, useState } from 'react';

import routes, { getRouteByPath } from './routes/index.jsx';

const personas = [
  { id: 'patient', label: 'Patient' },
  { id: 'staff', label: 'Staff' },
];

function App() {
  const [pathname, setPathname] = useState(window.location.pathname);
  const [persona, setPersona] = useState('patient');
  const [isDarkTheme, setIsDarkTheme] = useState(false);

  const activeRoute = getRouteByPath(pathname);
  const visibleRoutes = routes.filter((route) => route.persona === persona);

  useEffect(() => {
    const handlePopState = () => {
      setPathname(window.location.pathname);
    };

    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const handleNavigation = (event, path) => {
    event.preventDefault();
    window.history.pushState({}, '', path);
    setPathname(path);
  };

  const handlePersonaChange = (event) => {
    const nextPersona = event.target.value;
    const nextRoute = routes.find((route) => route.persona === nextPersona);

    setPersona(nextPersona);

    if (nextRoute) {
      window.history.pushState({}, '', nextRoute.path);
      setPathname(nextRoute.path);
    }
  };

  return (
    <main className={isDarkTheme ? 'app app-dark' : 'app'}>
      <header className="topbar">
        <a className="brand" href="/" onClick={(event) => handleNavigation(event, '/')}>
          <span className="brand-mark" aria-hidden="true">+</span>
          <span>Clinic Booking</span>
        </a>
        <div className="toolbar">
          <label className="control">
            <span>Persona</span>
            <select value={persona} onChange={handlePersonaChange}>
              {personas.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <button
            className="theme-button"
            type="button"
            aria-pressed={isDarkTheme}
            onClick={() => setIsDarkTheme((currentValue) => !currentValue)}
          >
            {isDarkTheme ? 'Light' : 'Dark'}
          </button>
        </div>
      </header>

      <div className="workspace">
        <nav className="sidebar" aria-label="Clinic workflows">
          {visibleRoutes.map((route) => (
            <a
              className={route.path === pathname ? 'nav-link active' : 'nav-link'}
              href={route.path}
              key={route.path}
              onClick={(event) => handleNavigation(event, route.path)}
            >
              {route.label}
            </a>
          ))}
        </nav>

        <section className="content" aria-labelledby="page-title">
          <div className="notice">
            Development shell connected. Feature workflows will be layered in as routers
            and services are implemented.
          </div>
          <article className="panel">
            <p className="eyebrow">{activeRoute.persona}</p>
            <h1 id="page-title">{activeRoute.title}</h1>
            <p>{activeRoute.description}</p>
          </article>
        </section>
      </div>
    </main>
  );
}

export default App;
