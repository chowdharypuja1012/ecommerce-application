import React from 'react';

interface ErrorStateProps {
  message: string;
  onRetry: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ message, onRetry }) => {
  return (
    <div className="error-state animate-fade-in" id="error-state">
      <div className="state-icon">⚠️</div>
      <h2 className="state-title">Unable to Load Catalogue</h2>
      <p className="state-text">{message}</p>
      <button
        id="retry-btn"
        className="btn-action"
        onClick={onRetry}
        type="button"
      >
        Retry Connection
      </button>
    </div>
  );
};
