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
            <div className="logo-emblem">
              <svg viewBox="0 0 32 32" width="22" height="22" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M16 13C16 13 13 8 8.5 8C5.46 8 3 10.46 3 13.5C3 17.5 9 20 16 22C23 20 29 17.5 29 13.5C29 10.46 26.54 8 23.5 8C19 8 16 13 16 13Z"
                  fill="#FFF0F5"
                  stroke="#E85B86"
                  strokeWidth="1.8"
                  strokeLinejoin="round"
                />
                <circle cx="16" cy="13" r="2.8" fill="#E85B86" />
                <path
                  d="M13.5 15.5L8.5 24M18.5 15.5L23.5 24"
                  stroke="#E85B86"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                />
                <path
                  d="M26 4L26.8 6.2L29 7L26.8 7.8L26 10L25.2 7.8L23 7L25.2 6.2L26 4Z"
                  fill="#F59E0B"
                />
              </svg>
            </div>
            <div className="brand-text-wrap" style={{ textAlign: 'left' }}>
              <span className="brand-name-script" style={{ fontSize: '1.4rem' }}>
                Sweet <span className="brand-heart-dot">♡</span>
              </span>
              <span className="brand-name-sub">SENTIMENTS</span>
            </div>
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
            &copy; 2026 Sweet Sentiments. Cute Lifestyle & Gifting Store. Made with ♡
          </p>
        </div>
      </div>
    </footer>
  );
};
