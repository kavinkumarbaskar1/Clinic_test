import { useEffect, useState } from 'react';

import AppShell from './layout/AppShell.jsx';
import { getHealth, normalizeApiError } from './services/apiClient.js';
import './styles/tokens.css';

function App() {
  const [apiHealth, setApiHealth] = useState({
    message: 'Checking clinic API connection...',
    status: 'checking',
  });

  useEffect(() => {
    let isActive = true;

    getHealth()
      .then((health) => {
        if (isActive) {
          setApiHealth({
            message: `Clinic API status: ${health.status}`,
            status: health.status,
          });
        }
      })
      .catch((error) => {
        if (isActive) {
          const normalizedError = normalizeApiError(error);

          setApiHealth({
            message: normalizedError.message,
            status: 'unavailable',
          });
        }
      });

    return () => {
      isActive = false;
    };
  }, []);

  return <AppShell apiHealth={apiHealth} />;
}

export default App;
