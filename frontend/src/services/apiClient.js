const DEFAULT_API_BASE_URL = 'http://localhost:8000';

function getConfiguredBaseUrl() {
  const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL;

  return configuredBaseUrl.replace(/\/+$/, '');
}

export class ApiClientError extends Error {
  constructor(message, { code, status } = {}) {
    super(message);
    this.name = 'ApiClientError';
    this.code = code;
    this.status = status;
  }
}

export function normalizeApiError(error) {
  if (error instanceof ApiClientError) {
    return {
      code: error.code ?? 'api_error',
      message: error.message,
      status: error.status,
    };
  }

  return {
    code: 'network_error',
    message: 'The clinic service is unavailable. Please try again shortly.',
    status: undefined,
  };
}

async function request(path, options = {}) {
  const url = `${getConfiguredBaseUrl()}${path}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        Accept: 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new ApiClientError(
        'The clinic service returned an error. Please try again shortly.',
        {
          code: 'api_error',
          status: response.status,
        },
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }

    throw new ApiClientError(
      'The clinic service is unavailable. Please try again shortly.',
      { code: 'network_error' },
    );
  }
}

export function getHealth() {
  return request('/api/health');
}
