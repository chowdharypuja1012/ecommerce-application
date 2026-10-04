import React from 'react';
import type { Category } from '../types/catalogue';

interface CategoryNavProps {
  categories: Category[];
  selectedCategory: string;
  onSelectCategory: (categorySlug: string) => void;
}

const CATEGORY_IMAGES: Record<string, string> = {
  'stationery': '/images/categories/stationery.jpg',
  'accessories': '/images/categories/accessories.jpg',
  'home-decor': '/images/categories/home-decor.jpg',
  'gifts': '/images/categories/gifts.jpg',
  'self-care': '/images/categories/self-care.jpg',
  'flowers-and-wrapping': '/images/categories/flowers-and-wrapping.jpg',
};

const CATEGORY_DEFAULT_IMAGE = '/images/categories/stationery.jpg';

export const CategoryNav: React.FC<CategoryNavProps> = ({
  categories,
  selectedCategory,
  onSelectCategory,
}) => {
  return (
    <section className="category-section" aria-label="Product Categories" id="category-navigation">
      <div className="category-header-center">
        <h2 className="shop-by-mood-title">
          Shop by mood <span className="mood-heart">♡</span>
        </h2>
      </div>

      <div className="category-cards-grid">
        {categories.map((cat) => {
          const isSelected = selectedCategory === cat.slug;
          const imageSrc = CATEGORY_IMAGES[cat.slug] || CATEGORY_DEFAULT_IMAGE;

          return (
            <div
              key={cat.id}
              id={`cat-card-${cat.slug}`}
              className={`category-card-item ${isSelected ? 'active' : ''}`}
              onClick={() => onSelectCategory(isSelected ? '' : cat.slug)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  onSelectCategory(isSelected ? '' : cat.slug);
                }
              }}
            >
              <div className="category-card-image-box">
                <img
                  src={imageSrc}
                  alt={cat.name}
                  className="category-card-img"
                  loading="lazy"
                />
                {isSelected && (
                  <div className="category-active-badge">Selected ✓</div>
                )}
              </div>
              <span className="category-card-name">{cat.name}</span>
            </div>
          );
        })}
      </div>

      {selectedCategory && (
        <div className="category-clear-filter-row">
          <button
            type="button"
            className="btn-clear-category-pill"
            onClick={() => onSelectCategory('')}
          >
            ✕ Clear Category Filter (Show All)
          </button>
        </div>
      )}
    </section>
  );
};

