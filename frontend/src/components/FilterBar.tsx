import React from 'react';

interface FilterBarProps {
  search: string;
  minPrice: string;
  maxPrice: string;
  ordering: string;
  onSearchChange: (value: string) => void;
  onMinPriceChange: (value: string) => void;
  onMaxPriceChange: (value: string) => void;
  onOrderingChange: (value: string) => void;
  onResetFilters: () => void;
  hasActiveFilters: boolean;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  search,
  minPrice,
  maxPrice,
  ordering,
  onSearchChange,
  onMinPriceChange,
  onMaxPriceChange,
  onOrderingChange,
  onResetFilters,
  hasActiveFilters,
}) => {
  return (
    <div className="filter-bar" id="filter-bar">
      {/* Search Input */}
      <div className="search-box">
        <svg className="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          id="search-input"
          type="text"
          placeholder="Search products by name, SKU..."
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>

      {/* Price Filter Inputs */}
      <div className="price-filter-group">
        <input
          id="min-price-input"
          className="price-input"
          type="number"
          min="0"
          placeholder="Min ₹"
          value={minPrice}
          onChange={(e) => onMinPriceChange(e.target.value)}
        />
        <span style={{ color: 'var(--text-muted)' }}>–</span>
        <input
          id="max-price-input"
          className="price-input"
          type="number"
          min="0"
          placeholder="Max ₹"
          value={maxPrice}
          onChange={(e) => onMaxPriceChange(e.target.value)}
        />
      </div>

      {/* Sorting Dropdown */}
      <div className="select-box">
        <select
          id="sort-select"
          value={ordering}
          onChange={(e) => onOrderingChange(e.target.value)}
          aria-label="Sort products by"
        >
          <option value="-created_at">Newest First</option>
          <option value="created_at">Oldest First</option>
          <option value="price">Price: Low to High</option>
          <option value="-price">Price: High to Low</option>
          <option value="name">Name: A to Z</option>
          <option value="-name">Name: Z to A</option>
        </select>
      </div>

      {/* Reset Filters Button */}
      {hasActiveFilters && (
        <button
          id="reset-filters-btn"
          className="btn-reset-filters"
          onClick={onResetFilters}
          type="button"
        >
          Clear Filters
        </button>
      )}
    </div>
  );
};
