import React from 'react';

export const HeroBanner: React.FC = () => {
  return (
    <section className="hero-banner" id="hero-banner">
      <div className="hero-card-banner">
        <div className="hero-left-content">
          <span className="hero-eyebrow">little things, big happiness</span>
          <h1 className="hero-title">
            Find your kind of <em>lovely.</em>
          </h1>
          <p className="hero-subtitle">
            A happy place for all the little things that bring you joy. 
            Curated gifts, stationery, and lifestyle treats.
          </p>
          <a href="#product-grid" className="btn-hero-cta" id="hero-shop-btn">
            Shop now <span className="btn-arrow">→</span>
          </a>
        </div>

        <div className="hero-image-collage">
          <div className="hero-img-item">
            <img
              src="/images/products/a-box-of-joy-birthday-hamper.jpg"
              alt="Curated gift box with flowers"
            />
            <span className="hero-decorative-badge">🎀 Gift Ready</span>
          </div>
          <div className="hero-img-item">
            <img
              src="/images/products/soy-wax-candle-vanilla-peony.jpg"
              alt="Aesthetic pink candle"
            />
          </div>
          <div className="hero-img-item">
            <img
              src="/images/products/sunday-morning-mug-lavender.jpg"
              alt="Pastel ceramic mug"
            />
          </div>
        </div>
      </div>
    </section>
  );
};
