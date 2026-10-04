import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="footer" role="contentinfo" id="store-footer">
      <div className="container footer-content">
        <p>&copy; 2026 NexusShop Platform. All rights reserved.</p>
        <p style={{ fontSize: '0.8rem' }}>
          Microservices Powered • React + Vite + Django REST Framework
        </p>
      </div>
    </footer>
  );
};
