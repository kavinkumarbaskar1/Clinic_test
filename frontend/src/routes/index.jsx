const routes = [
  {
    path: '/',
    label: 'Overview',
    persona: 'patient',
    title: 'Clinic booking',
    description: 'Start a booking, check next steps, or switch to staff tools.',
  },
  {
    path: '/book',
    label: 'Book',
    persona: 'patient',
    title: 'Book an appointment',
    description: 'A guided booking flow will collect visit details in a later task.',
  },
  {
    path: '/reschedule',
    label: 'Reschedule',
    persona: 'patient',
    title: 'Reschedule a visit',
    description: 'Patients will manage existing appointment requests here.',
  },
  {
    path: '/staff/schedule',
    label: 'Staff schedule',
    persona: 'staff',
    title: 'Staff schedule',
    description: 'Authorized staff scheduling controls will be added behind role checks.',
  },
];

const routeFallback = {
  path: '/',
  label: 'Overview',
  persona: 'patient',
  title: 'Page not found',
  description: 'Choose a clinic workflow from the navigation.',
};

export function getRouteByPath(pathname) {
  return routes.find((route) => route.path === pathname) ?? routeFallback;
}

export default routes;
