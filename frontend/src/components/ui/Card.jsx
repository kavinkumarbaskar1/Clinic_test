function Card({ children, className = '' }) {
  const classes = ['ui-card', className].filter(Boolean).join(' ');

  return <article className={classes}>{children}</article>;
}

export default Card;
