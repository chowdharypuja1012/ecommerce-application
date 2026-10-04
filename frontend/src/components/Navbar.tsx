import React from 'react';
import type { User, Profile } from '../types/auth';

interface NavbarProps {
  cartCount?: number;
  currentUser: { user: User; profile: Profile } | null;
  onOpenAuthModal: () => void;
  onOpenProfileModal: () => void;
  onOpenCartDrawer: () => void;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  cartCount = 0,
  currentUser,
  onOpenAuthModal,
  onOpenProfileModal,
  onOpenCartDrawer,
  onLogout,
}) => {
  return (
    <header className="navbar" role="banner">
      <div className="container navbar-inner">
        <a href="/" className="brand-logo" id="brand-logo-link">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="32" height="32" rx="8" fill="url(#logo-grad)"/>
            <path d="M10 11L16 17L22 11M10 21L16 15L22 21" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
            <defs>
              <linearGradient id="logo-grad" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
                <stop stopColor="#6366F1"/>
                <stop offset="1" stopColor="#4F46E5"/>
              </linearGradient>
            </defs>
          </svg>
          NexusShop <span className="brand-badge">Platform</span>
        </a>

        <div className="nav-actions">
          {currentUser ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
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
              className="btn-primary"
              id="signin-btn"
              onClick={onOpenAuthModal}
              type="button"
              style={{ padding: '0.45rem 1rem', fontSize: '0.9rem' }}
            >
              Sign In
            </button>
          )}

          <button
            className="cart-icon-btn"
            id="cart-btn"
            onClick={onOpenCartDrawer}
            aria-label={`Shopping Cart with ${cartCount} items`}
            title="Shopping Cart"
            type="button"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="9" cy="21" r="1"/>
              <circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
            {cartCount > 0 && (
              <span className="cart-count-badge" id="cart-count">{cartCount}</span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
