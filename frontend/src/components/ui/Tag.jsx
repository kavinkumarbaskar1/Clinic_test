function Tag({ children, tone = 'default' }) {
  return <span className={`ui-tag ui-tag--${tone}`}>{children}</span>;
}

export default Tag;
