import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="site-footer" role="contentinfo" id="store-footer">
      <div className="container footer-content">
        <p style={{ fontFamily: 'Fredoka, sans-serif', fontSize: '1.05rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.3rem' }}>
          🌸 Maison Pastel Boutique
        </p>
        <p>&copy; 2026 Maison Pastel. Crafted with ♡ for aesthetic living & workspace inspiration.</p>
      </div>
    </footer>
  );
};
