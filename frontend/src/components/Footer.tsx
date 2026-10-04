import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="site-footer" role="contentinfo" id="store-footer">
      {/* Pink CTA Banner */}
      <div className="footer-top-cta">
        <div className="container">
          <h3 className="footer-cta-title">A little love, from us to you 🤍</h3>
          <p className="footer-cta-text">
            Discover lovely finds, curate your aesthetic, and make everyday a little more special.
          </p>
        </div>
      </div>

      {/* Main Footer */}
      <div className="footer-main">
        <div className="container">
          <div className="footer-logo">
            ruja <span className="logo-heart" style={{ color: 'var(--ruja-pink)', fontSize: '1rem' }}>♡</span>
          </div>
          <div className="footer-links">
            <a href="#shop" className="footer-link">Shop</a>
            <a href="#about" className="footer-link">About Us</a>
            <a href="#faq" className="footer-link">FAQ</a>
            <a href="#contact" className="footer-link">Contact</a>
            <a href="#shipping" className="footer-link">Shipping</a>
            <a href="#returns" className="footer-link">Returns</a>
          </div>
          <p className="footer-copy">
            &copy; 2026 ruja. Cute Lifestyle & Gifting Store. Made with ♡
          </p>
        </div>
      </div>
    </footer>
  );
};
