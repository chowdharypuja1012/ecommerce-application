import React, { useState } from 'react';
import type { Product } from '../types/catalogue';

interface ProductDetailModalProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onAddToCart: (product: Product, quantity: number) => void;
}

export const ProductDetailModal: React.FC<ProductDetailModalProps> = ({
  product,
  isOpen,
  onClose,
  onAddToCart,
}) => {
  const [quantity, setQuantity] = useState(1);
  const [addedNotice, setAddedNotice] = useState(false);

  if (!isOpen || !product) return null;

  const isOutOfStock = product.stock <= 0;
  const defaultImage = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400" fill="%231f293d"><rect width="600" height="400"/><text x="50%" y="50%" fill="%239ca3af" font-family="sans-serif" font-size="20" text-anchor="middle" dominant-baseline="middle">${encodeURIComponent(product.name)}</text></svg>`;

  const handleAdd = () => {
    onAddToCart(product, quantity);
    setAddedNotice(true);
    setTimeout(() => setAddedNotice(false), 2000);
  };

  return (
    <div className="modal-overlay" id="product-detail-overlay" onClick={onClose}>
      <div className="modal-content product-detail-modal-content animate-fade-in" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <span className="detail-modal-title">Product Details</span>
          <button className="close-btn" id="close-product-detail-modal" onClick={onClose} aria-label="Close product detail">
            &times;
          </button>
        </div>

        <div className="product-detail-body">
          <div className="detail-image-wrapper">
            <img
              src={product.image_url || defaultImage}
              alt={product.name}
              className="detail-product-image"
              onError={(e) => {
                (e.target as HTMLImageElement).src = defaultImage;
              }}
            />
            {product.category && (
              <span className="card-category-tag">{product.category.name}</span>
            )}
          </div>

          <div className="detail-info-col">
            <h2 className="detail-title">{product.name}</h2>
            <div className="detail-sku-badge">SKU: <code>{product.sku}</code></div>

            <div className="detail-price-row">
              <span className="detail-price">${parseFloat(product.price).toFixed(2)}</span>
              <span className={`stock-badge ${isOutOfStock ? 'stock-out' : 'stock-in'}`}>
                {isOutOfStock ? 'Out of Stock' : `${product.stock} Units Available`}
              </span>
            </div>

            <div className="detail-section">
              <h4>Description</h4>
              <p className="detail-description">{product.description || 'No detailed description available.'}</p>
            </div>

            {!isOutOfStock && (
              <div className="quantity-row">
                <label htmlFor="detail-quantity">Quantity:</label>
                <div className="quantity-controls">
                  <button
                    type="button"
                    className="qty-btn"
                    onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                    disabled={quantity <= 1}
                  >
                    -
                  </button>
                  <input
                    id="detail-quantity"
                    type="number"
                    min="1"
                    max={product.stock}
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, Math.min(product.stock, parseInt(e.target.value) || 1)))}
                  />
                  <button
                    type="button"
                    className="qty-btn"
                    onClick={() => setQuantity((q) => Math.min(product.stock, q + 1))}
                    disabled={quantity >= product.stock}
                  >
                    +
                  </button>
                </div>
              </div>
            )}

            {addedNotice && (
              <div className="add-success-banner animate-fade-in">
                ✓ Added {quantity} item(s) to your cart!
              </div>
            )}

            <div className="detail-actions">
              <button
                id="detail-add-to-cart-btn"
                className="btn-primary btn-large"
                disabled={isOutOfStock}
                onClick={handleAdd}
                type="button"
              >
                {isOutOfStock ? 'Currently Unavailable' : `Add ${quantity} to Cart — $${(parseFloat(product.price) * quantity).toFixed(2)}`}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
