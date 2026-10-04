import React from 'react';

export const HeroBanner: React.FC = () => {
  return (
    <section className="hero-banner" id="hero-banner">
      <div className="container">
        <div className="hero-card-banner">
          <div className="hero-left-content">
            <h1 className="hero-title">
              Savour <em>the Juicy</em> essence of fruit in every sip.
            </h1>
            <p className="hero-subtitle">
              Taste nature's best in every drop with real fruit and vibrant flavour
            </p>
            <a href="#product-grid" className="btn-hero-cta" id="hero-sip-fresh-btn">
              Sip Fresh <span className="btn-arrow">→</span>
            </a>
          </div>

          <div className="hero-center-media">
            <img
              src="https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=800&q=80"
              alt="alldae sparkling superfruit can splash"
              className="hero-can-img"
            />
          </div>

          <div className="hero-right-stat">
            <div className="hero-brand-badge">
              <span className="brand-dot-logo">alldae.</span>
              <span className="brand-subtext">POWERED BY</span>
            </div>
            <div className="hero-stat-number">78%</div>
            <div className="hero-stat-label">Natural ingredients used in flavour</div>
          </div>
        </div>
      </div>
    </section>
  );
};
