import Button from './Button.jsx';

function Dialog({ children, isOpen, onClose, title }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="ui-dialog-backdrop" role="presentation">
      <section
        className="ui-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
      >
        <div className="ui-dialog__header">
          <h2 id="dialog-title">{title}</h2>
          <Button
            type="button"
            variant="ghost"
            aria-label="Close dialog"
            onClick={onClose}
          >
            Close
          </Button>
        </div>
        <div className="ui-dialog__body">{children}</div>
      </section>
    </div>
  );
}

export default Dialog;
