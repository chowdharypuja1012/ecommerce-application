import React from 'react';
import type { Category } from '../types/catalogue';

interface CategoryNavProps {
  categories: Category[];
  selectedCategory: string;
  onSelectCategory: (categorySlug: string) => void;
}

export const CategoryNav: React.FC<CategoryNavProps> = ({
  categories,
  selectedCategory,
  onSelectCategory,
}) => {
  return (
    <nav className="category-nav-wrapper" aria-label="Product Categories" id="category-navigation">
      <div className="container category-nav-header-row">
        <h2 className="section-serif-title">
          Discover <em>our range -</em>
        </h2>

        <div className="category-pills">
          <button
            id="cat-pill-all"
            className={`category-pill ${selectedCategory === '' ? 'active' : ''}`}
            onClick={() => onSelectCategory('')}
            type="button"
          >
            Best Seller
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              id={`cat-pill-${cat.slug}`}
              className={`category-pill ${selectedCategory === cat.slug ? 'active' : ''}`}
              onClick={() => onSelectCategory(cat.slug)}
              type="button"
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
};
