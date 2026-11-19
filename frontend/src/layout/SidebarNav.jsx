function SidebarNav({ activePath, routes, onNavigate }) {
  return (
    <aside className="shell-sidebar">
      <nav className="shell-nav" aria-label="Clinic workflows">
        {routes.map((route) => (
          <a
            className={route.path === activePath ? 'shell-nav__link is-active' : 'shell-nav__link'}
            href={route.path}
            key={route.path}
            aria-current={route.path === activePath ? 'page' : undefined}
            onClick={(event) => onNavigate(event, route.path)}
          >
            <span>{route.label}</span>
            <span className="shell-nav__hint">{route.title}</span>
          </a>
        ))}
      </nav>
    </aside>
  );
}

export default SidebarNav;
