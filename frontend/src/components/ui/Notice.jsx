function Notice({ children, title }) {
  return (
    <section className="ui-notice" aria-label={title}>
      <strong>{title}</strong>
      <span>{children}</span>
    </section>
  );
}

export default Notice;
