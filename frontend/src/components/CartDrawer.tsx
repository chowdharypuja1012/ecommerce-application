import React from 'react';
import type { Cart, CartItem } from '../types/cart';
import type { Product } from '../types/catalogue';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  cart: Cart | null;
  loading: boolean;
  error: string | null;
  products?: Product[];
  onUpdateQuantity: (itemId: number, newQuantity: number) => void;
  onRemoveItem: (itemId: number) => void;
  onClearCart: () => void;
  onProceedToCheckout?: () => void;
}

export const CartDrawer: React.FC<CartDrawerProps> = ({
  isOpen,
  onClose,
  cart,
  loading,
  error,
  products = [],
  onUpdateQuantity,
  onRemoveItem,
  onClearCart,
  onProceedToCheckout,
}) => {
  if (!isOpen) return null;

  const items = cart?.items || [];
  const subtotal = cart?.subtotal ? parseFloat(cart.subtotal).toFixed(2) : '0.00';
  const totalItems = cart?.total_items || 0;

  // Helper to find matched product from catalogue for images
  const getProductImage = (productId: number, fallbackName: string) => {
    const prod = products.find((p) => p.id === productId);
    if (prod && prod.image_url) {
      return prod.image_url;
    }
    return `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120"><rect width="120" height="120" fill="%23FFF0F5"/><text x="50%" y="50%" fill="%23E8A0BF" font-family="sans-serif" font-size="11" text-anchor="middle" dominant-baseline="middle">${encodeURIComponent(fallbackName.slice(0, 10))}</text></svg>`;
  };

  return (
    <div className="cart-drawer-overlay" id="cart-drawer-overlay" onClick={onClose}>
      <div className="cart-drawer-content animate-fade-in" onClick={(e) => e.stopPropagation()}>
        {/* Drawer Header */}
        <div className="cart-drawer-header">
          <div className="cart-header-left">
            <h2 className="cart-drawer-title">Your Shopping Bag</h2>
            {totalItems > 0 && <span className="cart-drawer-count">{totalItems}</span>}
          </div>
          <button className="close-btn" id="close-cart-drawer" onClick={onClose} aria-label="Close cart">
            &times;
          </button>
        </div>

        {/* Drawer Body */}
        <div className="cart-drawer-body">
          {loading ? (
            <div className="cart-loading-state">
              <div className="spinner" />
              <p>Fetching your lovely bag...</p>
            </div>
          ) : error ? (
            <div className="cart-error-banner">
              <p>{error}</p>
            </div>
          ) : items.length === 0 ? (
            <div className="empty-cart-view" id="empty-cart-view">
              <div className="empty-cart-icon">🛍️</div>
              <h3>Your bag is empty</h3>
              <p>Looks like you haven't added any lovely items yet.</p>
              <button className="btn-primary" onClick={onClose} type="button" style={{ marginTop: '0.5rem' }}>
                Explore Collection ♡
              </button>
            </div>
          ) : (
            <div className="cart-items-list" id="cart-items-list">
              {items.map((item: CartItem) => {
                const imgUrl = getProductImage(item.product_id, item.product_name);
                return (
                  <div key={item.id} className="cart-item-row animate-fade-in" id={`cart-item-${item.id}`}>
                    <img
                      src={imgUrl}
                      alt={item.product_name}
                      className="cart-item-image"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120"><rect width="120" height="120" fill="%23FFF0F5"/><text x="50%" y="50%" fill="%23E8A0BF" font-family="sans-serif" font-size="11" text-anchor="middle" dominant-baseline="middle">♡</text></svg>`;
                      }}
                    />

                    <div className="cart-item-info">
                      <div className="cart-item-top">
                        <div className="cart-item-title" title={item.product_name}>
                          {item.product_name}
                        </div>
                        <button
                          className="btn-remove-item"
                          id={`remove-item-${item.id}`}
                          onClick={() => onRemoveItem(item.id)}
                          title="Remove item"
                          type="button"
                          aria-label="Remove item"
                        >
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                          </svg>
                        </button>
                      </div>

                      <div className="cart-item-meta">
                        <span className="cart-item-sku">SKU: {item.product_sku}</span>
                        <span className="cart-item-dot">•</span>
                        <span className="cart-item-unit-price">₹{parseFloat(item.unit_price).toLocaleString('en-IN')}</span>
                      </div>

                      <div className="cart-item-bottom-row">
                        <div className="quantity-controls compact">
                          <button
                            type="button"
                            className="qty-btn"
                            onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                            aria-label="Decrease quantity"
                          >
                            −
                          </button>
                          <span className="qty-value">{item.quantity}</span>
                          <button
                            type="button"
                            className="qty-btn"
                            onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                            aria-label="Increase quantity"
                          >
                            +
                          </button>
                        </div>

                        <div className="cart-item-line-total">
                          ₹{parseFloat(item.line_total).toLocaleString('en-IN')}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Drawer Footer */}
        {items.length > 0 && !loading && (
          <div className="cart-drawer-footer">
            <div className="subtotal-row">
              <span className="subtotal-label">Subtotal</span>
              <span className="subtotal-amount">₹{parseFloat(subtotal).toLocaleString('en-IN')}</span>
            </div>
            <p className="subtotal-note">Taxes & shipping calculated at checkout ✨</p>

            <div className="drawer-footer-actions">
              <button
                id="clear-cart-btn"
                className="btn-secondary"
                onClick={onClearCart}
                type="button"
              >
                Clear
              </button>
              <button
                id="checkout-btn"
                className="btn-primary"
                onClick={onProceedToCheckout}
                type="button"
              >
                Proceed to Checkout →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
