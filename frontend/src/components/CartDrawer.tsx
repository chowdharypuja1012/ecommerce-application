import React from 'react';
import type { Cart, CartItem } from '../types/cart';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  cart: Cart | null;
  loading: boolean;
  error: string | null;
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
  onUpdateQuantity,
  onRemoveItem,
  onClearCart,
  onProceedToCheckout,
}) => {
  if (!isOpen) return null;

  const items = cart?.items || [];
  const subtotal = cart?.subtotal ? parseFloat(cart.subtotal).toFixed(2) : '0.00';
  const totalItems = cart?.total_items || 0;

  return (
    <div className="cart-drawer-overlay" id="cart-drawer-overlay" onClick={onClose}>
      <div className="cart-drawer-content animate-fade-in" onClick={(e) => e.stopPropagation()}>
        {/* Drawer Header */}
        <div className="cart-drawer-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <h2>Your Shopping Cart</h2>
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
              <p>Fetching your cart...</p>
            </div>
          ) : error ? (
            <div className="cart-error-banner">
              <p>{error}</p>
            </div>
          ) : items.length === 0 ? (
            <div className="empty-cart-view" id="empty-cart-view">
              <div className="empty-cart-icon">🛒</div>
              <h3>Your cart is empty</h3>
              <p>Looks like you haven't added any products to your cart yet.</p>
              <button className="btn-primary" onClick={onClose} type="button">
                Start Shopping
              </button>
            </div>
          ) : (
            <div className="cart-items-list" id="cart-items-list">
              {items.map((item: CartItem) => (
                <div key={item.id} className="cart-item-row" id={`cart-item-${item.id}`}>
                  <div className="cart-item-info">
                    <div className="cart-item-title">{item.product_name}</div>
                    <div className="cart-item-sku">SKU: {item.product_sku}</div>
                    <div className="cart-item-price">${parseFloat(item.unit_price).toFixed(2)} each</div>
                  </div>

                  <div className="cart-item-actions">
                    <div className="quantity-controls compact">
                      <button
                        type="button"
                        className="qty-btn"
                        onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                      >
                        -
                      </button>
                      <span>{item.quantity}</span>
                      <button
                        type="button"
                        className="qty-btn"
                        onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                      >
                        +
                      </button>
                    </div>

                    <div className="cart-item-line-total">
                      ${parseFloat(item.line_total).toFixed(2)}
                    </div>

                    <button
                      className="btn-remove-item"
                      id={`remove-item-${item.id}`}
                      onClick={() => onRemoveItem(item.id)}
                      title="Remove item"
                      type="button"
                    >
                      &times;
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Drawer Footer */}
        {items.length > 0 && !loading && (
          <div className="cart-drawer-footer">
            <div className="subtotal-row">
              <span>Server-Calculated Subtotal</span>
              <span className="subtotal-amount">${subtotal}</span>
            </div>
            <p className="subtotal-note">Taxes and shipping calculated at checkout.</p>

            <div className="drawer-footer-actions">
              <button
                id="clear-cart-btn"
                className="btn-secondary"
                onClick={onClearCart}
                type="button"
              >
                Clear Cart
              </button>
              <button
                id="checkout-btn"
                className="btn-primary btn-large"
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
