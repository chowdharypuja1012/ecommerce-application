import React from 'react';
import type { Wishlist, WishlistItem } from '../types/wishlist';

interface WishlistDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  wishlist: Wishlist | null;
  loading: boolean;
  error: string | null;
  onRemoveItem: (itemId: number) => void;
  onMoveToCart: (productId: number, itemId: number) => void;
  onClearWishlist: () => void;
}

export const WishlistDrawer: React.FC<WishlistDrawerProps> = ({
  isOpen,
  onClose,
  wishlist,
  loading,
  error,
  onRemoveItem,
  onMoveToCart,
  onClearWishlist,
}) => {
  if (!isOpen) return null;

  const items = wishlist?.items || [];
  const totalItems = wishlist?.total_items || 0;

  return (
    <div className="cart-drawer-overlay" id="wishlist-drawer-overlay" onClick={onClose}>
      <div className="cart-drawer-content animate-fade-in" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="cart-drawer-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <h2>Saved Wishlist</h2>
            {totalItems > 0 && <span className="cart-drawer-count">{totalItems}</span>}
          </div>
          <button className="close-btn" id="close-wishlist-drawer" onClick={onClose} aria-label="Close wishlist">
            &times;
          </button>
        </div>

        {/* Body */}
        <div className="cart-drawer-body">
          {loading ? (
            <div className="cart-loading-state">
              <div className="spinner" />
              <p>Loading your saved wishlist...</p>
            </div>
          ) : error ? (
            <div className="cart-error-banner">
              <p>{error}</p>
            </div>
          ) : items.length === 0 ? (
            <div className="empty-cart-view" id="empty-wishlist-view">
              <div className="empty-cart-icon">❤️</div>
              <h3>Your wishlist is empty</h3>
              <p>Explore products and click the heart icon to save items for later.</p>
              <button className="btn-primary" onClick={onClose} type="button">
                Discover Products
              </button>
            </div>
          ) : (
            <div className="cart-items-list" id="wishlist-items-list">
              {items.map((item: WishlistItem) => {
                const prod = item.product_details;
                const price = parseFloat(prod.price || '0').toFixed(2);
                const isOutOfStock = prod.stock <= 0;

                return (
                  <div key={item.id} className="cart-item-row" id={`wishlist-item-${item.id}`}>
                    <div className="cart-item-info">
                      <div className="cart-item-title">{prod.name}</div>
                      <div className="cart-item-sku">SKU: {prod.sku}</div>
                      <div className="cart-item-price">${price}</div>
                      {isOutOfStock ? (
                        <span style={{ color: 'var(--color-danger, #ef4444)', fontSize: '0.8rem' }}>
                          Out of stock
                        </span>
                      ) : (
                        <span style={{ color: 'var(--color-success, #10b981)', fontSize: '0.8rem' }}>
                          In stock ({prod.stock})
                        </span>
                      )}
                    </div>

                    <div className="cart-item-actions">
                      <button
                        className="btn-primary btn-sm"
                        disabled={isOutOfStock}
                        onClick={() => onMoveToCart(prod.id, item.id)}
                        type="button"
                        style={{ fontSize: '0.82rem', padding: '0.4rem 0.75rem' }}
                      >
                        {isOutOfStock ? 'Out of Stock' : 'Move to Cart'}
                      </button>

                      <button
                        className="btn-remove-item"
                        id={`remove-wishlist-item-${item.id}`}
                        onClick={() => onRemoveItem(item.id)}
                        title="Remove from wishlist"
                        type="button"
                      >
                        &times;
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer */}
        {items.length > 0 && !loading && (
          <div className="cart-drawer-footer">
            <button
              id="clear-wishlist-btn"
              className="btn-secondary"
              onClick={onClearWishlist}
              type="button"
              style={{ width: '100%' }}
            >
              Clear Entire Wishlist
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
