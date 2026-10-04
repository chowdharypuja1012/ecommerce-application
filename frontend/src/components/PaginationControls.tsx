import React from 'react';

interface PaginationControlsProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const PaginationControls: React.FC<PaginationControlsProps> = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  if (totalPages <= 1) return null;

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <nav className="pagination" aria-label="Product Pagination" id="pagination-controls">
      <button
        id="prev-page-btn"
        className="page-btn"
        disabled={currentPage <= 1}
        onClick={() => onPageChange(currentPage - 1)}
        type="button"
      >
        ← Previous
      </button>

      {pages.map((p) => (
        <button
          key={p}
          id={`page-btn-${p}`}
          className={`page-btn ${p === currentPage ? 'active' : ''}`}
          onClick={() => onPageChange(p)}
          type="button"
        >
          {p}
        </button>
      ))}

      <button
        id="next-page-btn"
        className="page-btn"
        disabled={currentPage >= totalPages}
        onClick={() => onPageChange(currentPage + 1)}
        type="button"
      >
        Next →
      </button>
    </nav>
  );
};
