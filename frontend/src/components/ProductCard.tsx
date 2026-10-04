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
  const stockText = isOutOfStock ? 'Sold Out' : `${product.stock} left`;

  const defaultImage = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200"><rect width="300" height="200" fill="%23FFF0F5"/><text x="50%" y="50%" fill="%23E8A0BF" font-family="serif" font-size="14" text-anchor="middle" dominant-baseline="middle">${encodeURIComponent(product.name)}</text></svg>`;

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
        <p className="product-desc">{product.description || 'A lovely little find for you.'}</p>

        <div className="card-footer">
          <div className="product-price">₹{parseFloat(product.price).toLocaleString('en-IN')}</div>
          <div style={{ display: 'flex', gap: '0.35rem' }}>
            <button
              className="btn-secondary"
              id={`view-detail-${product.id}`}
              onClick={handleCardClick}
              type="button"
              style={{ fontSize: '0.78rem', padding: '0.4rem 0.6rem' }}
            >
              View
            </button>
            <button
              className="btn-add-cart"
              id={`add-to-cart-${product.id}`}
              disabled={isOutOfStock}
              onClick={() => onAddToCart && onAddToCart(product)}
              type="button"
            >
              {isOutOfStock ? 'Sold Out' : '+ Add'}
            </button>
          </div>
        </div>
      </div>
    </article>
  );
};
