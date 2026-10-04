import React from 'react';

export const HeroBanner: React.FC = () => {
  return (
    <section className="hero-banner" id="hero-banner">
      <div className="container">
        <h1 className="hero-title">Explore Next-Gen Catalogue</h1>
        <p className="hero-subtitle">
          Discover premium products, curated categories, and real-time inventory backed by our microservices architecture.
        </p>
      </div>
    </section>
  );
};
