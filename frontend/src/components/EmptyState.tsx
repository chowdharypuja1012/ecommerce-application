import React from 'react';

interface EmptyStateProps {
  onResetFilters: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onResetFilters }) => {
  return (
    <div className="empty-state animate-fade-in" id="empty-state">
      <div className="state-icon">🔍</div>
      <h2 className="state-title">No Products Found</h2>
      <p className="state-text">
        We couldn't find any products matching your selected search or filter criteria.
        Try adjusting your filters or search keywords.
      </p>
      <button
        id="empty-reset-btn"
        className="btn-action"
        onClick={onResetFilters}
        type="button"
      >
        Reset All Filters
      </button>
    </div>
  );
};
