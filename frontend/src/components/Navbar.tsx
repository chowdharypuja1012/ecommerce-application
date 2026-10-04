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
    <header className="navbar" role="banner">
      <div className="container navbar-inner">
        <a href="/" className="brand-logo" id="brand-logo-link">
          alldae<span className="logo-dot">.</span>
        </a>

        <nav className="nav-center-links" aria-label="Main Navigation">
          <a href="#shop" className="nav-link">Shop All <span className="arrow-down">˅</span></a>
          <a href="#flavours" className="nav-link">Flavours</a>
          <a href="#about" className="nav-link">About Us</a>
          <a href="#recipes" className="nav-link">Recipes <span className="arrow-down">˅</span></a>
          <a href="#mission" className="nav-link">Our Mission</a>
        </nav>

        <div className="nav-actions">
          {currentUser ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
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
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l8.78-8.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
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
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="9" cy="21" r="1"/>
              <circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
            {cartCount > 0 && (
              <span className="cart-count-badge" id="cart-count">{cartCount}</span>
            )}
          </button>

          {/* Juice Up Yellow Pill Action Button */}
          <button
            className="btn-juice-up"
            id="juice-up-btn"
            onClick={onOpenCartDrawer}
            type="button"
          >
            Juice Up <span className="btn-arrow">→</span>
          </button>
        </div>
      </div>
    </header>
  );
};
