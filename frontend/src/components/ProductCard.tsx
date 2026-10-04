import React from 'react';
import type { Product } from '../types/catalogue';

interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  onSelectProduct?: (product: Product) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onAddToCart,
  onSelectProduct,
}) => {
  const isOutOfStock = product.stock <= 0;
  const stockClass = isOutOfStock ? 'stock-out' : 'stock-in';
  const stockText = isOutOfStock ? 'Out of Stock' : `${product.stock} in Stock`;

  const defaultImage = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200" fill="%231f293d"><rect width="300" height="200"/><text x="50%" y="50%" fill="%239ca3af" font-family="sans-serif" font-size="16" text-anchor="middle" dominant-baseline="middle">${encodeURIComponent(product.name)}</text></svg>`;

  const handleCardClick = () => {
    if (onSelectProduct) {
      onSelectProduct(product);
    }
  };

  return (
    <article className="product-card animate-fade-in" id={`product-card-${product.id}`}>
      <div className="card-image-wrapper" onClick={handleCardClick} style={{ cursor: 'pointer' }}>
        <img
          src={product.image_url || defaultImage}
          alt={product.name}
          className="product-image"
          onError={(e) => {
            (e.target as HTMLImageElement).src = defaultImage;
          }}
          loading="lazy"
        />
        {product.category && (
          <span className="card-category-tag">{product.category.name}</span>
        )}
        <span className={`stock-badge ${stockClass}`}>{stockText}</span>
      </div>

      <div className="card-body">
        <h3
          className="product-title clickable-title"
          title={product.name}
          onClick={handleCardClick}
          style={{ cursor: 'pointer' }}
        >
          {product.name}
        </h3>
        <div className="product-sku">SKU: {product.sku}</div>
        <p className="product-desc">{product.description || 'No detailed description available.'}</p>

        <div className="card-footer">
          <div className="product-price">${parseFloat(product.price).toFixed(2)}</div>
          <div style={{ display: 'flex', gap: '0.4rem' }}>
            <button
              className="btn-secondary"
              id={`view-detail-${product.id}`}
              onClick={handleCardClick}
              type="button"
              style={{ fontSize: '0.8rem', padding: '0.45rem 0.65rem' }}
            >
              Details
            </button>
            <button
              className="btn-add-cart"
              id={`add-to-cart-${product.id}`}
              disabled={isOutOfStock}
              onClick={() => onAddToCart && onAddToCart(product)}
              type="button"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="9" cy="21" r="1"/>
                <circle cx="20" cy="21" r="1"/>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
              </svg>
              {isOutOfStock ? 'Sold Out' : 'Add'}
            </button>
          </div>
        </div>
      </div>
    </article>
  );
};
