import { useEffect, useState } from 'react';

import Button from '../components/ui/Button.jsx';
import Card from '../components/ui/Card.jsx';
import Dialog from '../components/ui/Dialog.jsx';
import Notice from '../components/ui/Notice.jsx';
import Tag from '../components/ui/Tag.jsx';
import routes, { getRouteByPath } from '../routes/index.jsx';
import SidebarNav from './SidebarNav.jsx';
import Topbar from './Topbar.jsx';

const personas = [
  {
    id: 'patient',
    label: 'Patient',
    description: 'Booking and rescheduling tools',
  },
  {
    id: 'staff',
    label: 'Staff',
    description: 'Daily clinic schedule',
  },
];

const mainContentId = 'main-content';
const defaultApiHealth = {
  message: 'Clinic API connection has not been checked.',
  status: 'unknown',
};

function getInitialPersona(pathname) {
  return getRouteByPath(pathname).persona;
}

function AppShell({ apiHealth = defaultApiHealth }) {
  const [pathname, setPathname] = useState(window.location.pathname);
  const [persona, setPersona] = useState(getInitialPersona(window.location.pathname));
  const [isDarkTheme, setIsDarkTheme] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const activeRoute = getRouteByPath(pathname);
  const visibleRoutes = routes.filter((route) => route.persona === persona);
  const themeLabel = isDarkTheme ? 'dark' : 'light';

  useEffect(() => {
    const handlePopState = () => {
      const nextPathname = window.location.pathname;

      setPathname(nextPathname);
      setPersona(getInitialPersona(nextPathname));
    };

    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const navigateTo = (path) => {
    if (path !== pathname) {
      window.history.pushState({}, '', path);
      setPathname(path);
    }
  };

  const handleNavigation = (event, path) => {
    event.preventDefault();
    navigateTo(path);
  };

  const handlePersonaChange = (event) => {
    const nextPersona = event.target.value;
    const nextRoute = routes.find((route) => route.persona === nextPersona);

    setPersona(nextPersona);

    if (nextRoute) {
      navigateTo(nextRoute.path);
    }
  };

  return (
    <div className="shell" data-theme={themeLabel}>
      <a className="skip-link" href={`#${mainContentId}`}>
        Skip to main content
      </a>
      <Topbar
        isDarkTheme={isDarkTheme}
        personas={personas}
        selectedPersona={persona}
        onNavigate={handleNavigation}
        onPersonaChange={handlePersonaChange}
        onToggleTheme={() => setIsDarkTheme((currentValue) => !currentValue)}
      />
      <div className="shell__workspace">
        <SidebarNav
          activePath={pathname}
          routes={visibleRoutes}
          onNavigate={handleNavigation}
        />
        <main
          className="shell__main"
          id={mainContentId}
          tabIndex="-1"
          aria-labelledby="page-title"
        >
          <Notice title="Prototype shell">
            Navigation, theme, and shared surfaces are ready for the booking,
            rescheduling, and daily schedule workflows. {apiHealth.message}
          </Notice>
          <Card className="route-card">
            <div className="route-card__header">
              <Tag>{activeRoute.persona}</Tag>
              <span className="route-card__path">{activeRoute.path}</span>
            </div>
            <h1 id="page-title">{activeRoute.title}</h1>
            <p>{activeRoute.description}</p>
            <div className="route-card__actions" aria-label="Page actions">
              <Button type="button" onClick={() => setIsDialogOpen(true)}>
                Preview dialog
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={(event) => handleNavigation(event, activeRoute.path)}
              >
                Refresh route
              </Button>
            </div>
          </Card>
        </main>
      </div>
      <Dialog
        isOpen={isDialogOpen}
        title="Shared dialog"
        onClose={() => setIsDialogOpen(false)}
      >
        <p>
          This reusable dialog shell is available for later appointment and
          schedule confirmations.
        </p>
      </Dialog>
    </div>
  );
}

export default AppShell;
