import React from 'react';

export const LoadingState: React.FC = () => {
  return (
    <div className="products-grid" id="loading-state" aria-busy="true" aria-label="Loading products">
      {Array.from({ length: 8 }).map((_, idx) => (
        <div key={idx} className="skeleton skeleton-card" />
      ))}
    </div>
  );
};
