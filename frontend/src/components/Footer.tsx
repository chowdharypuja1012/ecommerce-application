import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="site-footer" role="contentinfo" id="store-footer">
      <div className="container footer-content">
        <div className="footer-logo">
          alldae<span className="logo-dot">.</span>
        </div>
        <p style={{ color: '#4B5563', fontSize: '0.9rem' }}>
          &copy; 2026 alldae. Superfruit Sparkling Beverages & Lifestyle. All rights reserved.
        </p>
      </div>
    </footer>
  );
};
