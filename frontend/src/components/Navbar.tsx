import React from 'react';
import type { User, Profile } from '../types/auth';

interface NavbarProps {
  cartCount?: number;
  wishlistCount?: number;
  currentUser: { user: User; profile: Profile } | null;
  onOpenAuthModal: () => void;
  onOpenProfileModal: () => void;
  onOpenCartDrawer: () => void;
  onOpenWishlistDrawer?: () => void;
  onOpenOrdersModal?: () => void;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  cartCount = 0,
  wishlistCount = 0,
  currentUser,
  onOpenAuthModal,
  onOpenProfileModal,
  onOpenCartDrawer,
  onOpenWishlistDrawer,
  onOpenOrdersModal,
  onLogout,
}) => {
  return (
    <>
      {/* Marquee Top Bar */}
      <div className="marquee-bar">
        <span>✨ A little treat for you — Enjoy discovering something lovely! ✨&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Free shipping on orders over ₹999 🎀&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✨ A little treat for you — Enjoy discovering something lovely! ✨</span>
      </div>

      <header className="navbar" role="banner">
        <div className="container navbar-inner">
          <a href="/" className="brand-logo" id="brand-logo-link">
            ruja <span className="logo-heart">♡</span>
          </a>

          <nav className="nav-center-links" aria-label="Main Navigation">
            <a href="#shop" className="nav-link">Home</a>
            <a href="#shop" className="nav-link">Shop All <span className="arrow-down">˅</span></a>
            <a href="#new" className="nav-link">New Arrivals</a>
            <a href="#best" className="nav-link">Best Sellers</a>
            <a href="#about" className="nav-link">Our Story</a>
          </nav>

          <div className="nav-actions">
            {currentUser ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <button
                  className="user-menu-btn"
                  id="user-orders-btn"
                  onClick={onOpenOrdersModal}
                  title="View Orders History"
                  type="button"
                >
                  Orders
                </button>

                <button
                  className="user-menu-btn"
                  id="user-profile-btn"
                  onClick={onOpenProfileModal}
                  title="View Profile & Addresses"
                  type="button"
                >
                  <div className="nav-avatar-pill">
                    {currentUser.user.username.charAt(0).toUpperCase()}
                  </div>
                  <span>{currentUser.profile.full_name || currentUser.user.username}</span>
                </button>

                <button
                  className="btn-signout"
                  id="signout-btn"
                  onClick={onLogout}
                  type="button"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <button
                className="user-menu-btn"
                id="signin-btn"
                onClick={onOpenAuthModal}
                type="button"
              >
                Sign In
              </button>
            )}

            {/* Wishlist Icon Button */}
            {onOpenWishlistDrawer && (
              <button
                className="cart-icon-btn"
                id="wishlist-btn"
                onClick={onOpenWishlistDrawer}
                aria-label={`Wishlist with ${wishlistCount} items`}
                title="Saved Wishlist"
                type="button"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
                {wishlistCount > 0 && (
                  <span className="cart-count-badge" id="wishlist-count">
                    {wishlistCount}
                  </span>
                )}
              </button>
            )}

            {/* Cart Icon Button */}
            <button
              className="cart-icon-btn"
              id="cart-btn"
              onClick={onOpenCartDrawer}
              aria-label={`Shopping Cart with ${cartCount} items`}
              title="Shopping Cart"
              type="button"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                <line x1="3" y1="6" x2="21" y2="6"/>
                <path d="M16 10a4 4 0 0 1-8 0"/>
              </svg>
              {cartCount > 0 && (
                <span className="cart-count-badge" id="cart-count">{cartCount}</span>
              )}
            </button>

            {/* Shop Now Action Button */}
            <button
              className="btn-shop-now"
              id="shop-now-btn"
              onClick={onOpenCartDrawer}
              type="button"
            >
              Shop Now <span className="btn-arrow">→</span>
            </button>
          </div>
        </div>
      </header>
    </>
  );
};
