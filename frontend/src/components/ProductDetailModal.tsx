import React, { useState, useEffect } from 'react';
import type { Product } from '../types/catalogue';
import type { ReviewSummaryResponse } from '../types/reviews';
import { reviewsClient } from '../api/reviewsClient';
import { authClient } from '../api/authClient';

interface ProductDetailModalProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onAddToCart: (product: Product, quantity: number) => void;
}

export const ProductDetailModal: React.FC<ProductDetailModalProps> = ({
  product,
  isOpen,
  onClose,
  onAddToCart,
}) => {
  const [quantity, setQuantity] = useState(1);
  const [addedNotice, setAddedNotice] = useState(false);

  // Review states
  const [reviewSummary, setReviewSummary] = useState<ReviewSummaryResponse | null>(null);
  const [loadingReviews, setLoadingReviews] = useState(false);
  const [rating, setRating] = useState(5);
  const [reviewTitle, setReviewTitle] = useState('');
  const [reviewComment, setReviewComment] = useState('');
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewError, setReviewError] = useState<string | null>(null);
  const [reviewSuccess, setReviewSuccess] = useState<string | null>(null);

  const isLoggedIn = !!authClient.getToken();

  const loadReviews = async () => {
    if (!product) return;
    setLoadingReviews(true);
    try {
      const data = await reviewsClient.getProductReviews(product.id);
      setReviewSummary(data);
    } catch {
      // Non-blocking error for review loading
    } finally {
      setLoadingReviews(false);
    }
  };

  useEffect(() => {
    if (isOpen && product) {
      setQuantity(1);
      setAddedNotice(false);
      setReviewError(null);
      setReviewSuccess(null);
      setReviewTitle('');
      setReviewComment('');
      setRating(5);
      loadReviews();
    }
  }, [isOpen, product?.id]);

  if (!isOpen || !product) return null;

  const isOutOfStock = product.stock <= 0;
  const defaultImage = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400" fill="%231f293d"><rect width="600" height="400"/><text x="50%" y="50%" fill="%239ca3af" font-family="sans-serif" font-size="20" text-anchor="middle" dominant-baseline="middle">${encodeURIComponent(product.name)}</text></svg>`;

  const handleAdd = () => {
    onAddToCart(product, quantity);
    setAddedNotice(true);
    setTimeout(() => setAddedNotice(false), 2000);
  };

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewTitle.trim() || !reviewComment.trim()) {
      setReviewError('Please provide both a title and review text.');
      return;
    }
    setSubmittingReview(true);
    setReviewError(null);
    setReviewSuccess(null);
    try {
      await reviewsClient.createReview(product.id, rating, reviewTitle, reviewComment);
      setReviewSuccess('Thank you! Your review has been submitted for moderation.');
      setReviewTitle('');
      setReviewComment('');
      setRating(5);
      await loadReviews();
    } catch (err: any) {
      setReviewError(err.message || 'Failed to submit review.');
    } finally {
      setSubmittingReview(false);
    }
  };

  const renderStars = (score: number, max: number = 5) => {
    const stars = [];
    for (let i = 1; i <= max; i++) {
      stars.push(
        <span key={i} className={i <= Math.round(score) ? 'star-gold' : 'star-muted'}>
          ★
        </span>
      );
    }
    return stars;
  };

  return (
    <div className="modal-overlay" id="product-detail-overlay" onClick={onClose}>
      <div className="modal-content product-detail-modal-content animate-fade-in" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <span className="detail-modal-title">Product Details</span>
          <button className="close-btn" id="close-product-detail-modal" onClick={onClose} aria-label="Close product detail">
            &times;
          </button>
        </div>

        <div className="product-detail-scroll-container">
          <div className="product-detail-body">
            <div className="detail-image-wrapper">
              <img
                src={product.image_url || defaultImage}
                alt={product.name}
                className="detail-product-image"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = defaultImage;
                }}
              />
              {product.category && (
                <span className="card-category-tag">{product.category.name}</span>
              )}
            </div>

            <div className="detail-info-col">
              <h2 className="detail-title">{product.name}</h2>
              <div className="detail-sku-badge">SKU: <code>{product.sku}</code></div>

              <div className="detail-price-row">
                <span className="detail-price">₹{parseFloat(product.price).toLocaleString('en-IN')}</span>
                <span className={`stock-badge ${isOutOfStock ? 'stock-out' : 'stock-in'}`}>
                  {isOutOfStock ? 'Out of Stock' : `${product.stock} in stock`}
                </span>
              </div>

              {reviewSummary && (
                <div className="detail-rating-quick">
                  <div className="rating-stars">{renderStars(reviewSummary.average_rating)}</div>
                  <span className="rating-score">{reviewSummary.average_rating.toFixed(1)}</span>
                  <span className="rating-count">({reviewSummary.total_reviews} {reviewSummary.total_reviews === 1 ? 'review' : 'reviews'})</span>
                </div>
              )}

              <div className="detail-section">
                <h4>Description</h4>
                <p className="detail-description">{product.description || 'A curated aesthetic piece crafted with love.'}</p>
              </div>

              {!isOutOfStock && (
                <div className="quantity-row">
                  <label htmlFor="detail-quantity">Quantity</label>
                  <div className="quantity-controls">
                    <button
                      type="button"
                      className="qty-btn"
                      onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                      disabled={quantity <= 1}
                      aria-label="Decrease quantity"
                    >
                      −
                    </button>
                    <span className="qty-value">{quantity}</span>
                    <button
                      type="button"
                      className="qty-btn"
                      onClick={() => setQuantity((q) => Math.min(product.stock, q + 1))}
                      disabled={quantity >= product.stock}
                      aria-label="Increase quantity"
                    >
                      +
                    </button>
                  </div>
                </div>
              )}

              {addedNotice && (
                <div className="add-success-banner animate-fade-in">
                  ✓ Added {quantity} item(s) to your bag!
                </div>
              )}

              <div className="detail-actions">
                <button
                  id="detail-add-to-cart-btn"
                  className="btn-primary"
                  disabled={isOutOfStock}
                  onClick={handleAdd}
                  type="button"
                >
                  {isOutOfStock ? 'Currently Unavailable' : `Add to Bag — ₹${(parseFloat(product.price) * quantity).toLocaleString('en-IN')}`}
                </button>
              </div>
            </div>
          </div>

          {/* ── Customer Reviews Section ── */}
          <div className="reviews-modal-section">
            <h3 className="reviews-section-title">Customer Reviews & Ratings</h3>

          {loadingReviews ? (
            <div className="reviews-loading">Loading customer reviews...</div>
          ) : (
            <>
              {reviewSummary && (
                <div className="review-summary-card">
                  <div className="summary-left">
                    <span className="big-rating">{reviewSummary.average_rating.toFixed(1)}</span>
                    <div className="summary-stars">{renderStars(reviewSummary.average_rating)}</div>
                    <span className="summary-total">Based on {reviewSummary.total_reviews} review(s)</span>
                  </div>

                  <div className="summary-bars">
                    {[5, 4, 3, 2, 1].map((star) => {
                      const count = reviewSummary.rating_distribution[star.toString()] || 0;
                      const percent = reviewSummary.total_reviews > 0 ? (count / reviewSummary.total_reviews) * 100 : 0;
                      return (
                        <div key={star} className="rating-bar-row">
                          <span className="bar-label">{star} ★</span>
                          <div className="bar-track">
                            <div className="bar-fill" style={{ width: `${percent}%` }} />
                          </div>
                          <span className="bar-count">{count}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Review Submission Form */}
              <div className="review-form-container">
                <h4>Write a Product Review</h4>
                {isLoggedIn ? (
                  <form onSubmit={handleReviewSubmit} className="review-form">
                    {reviewError && <div className="review-alert alert-error">{reviewError}</div>}
                    {reviewSuccess && <div className="review-alert alert-success">{reviewSuccess}</div>}

                    <div className="rating-select-group">
                      <label>Your Rating:</label>
                      <div className="star-picker">
                        {[1, 2, 3, 4, 5].map((s) => (
                          <button
                            key={s}
                            type="button"
                            className={`star-pick-btn ${s <= rating ? 'active' : ''}`}
                            onClick={() => setRating(s)}
                            aria-label={`Rate ${s} star${s > 1 ? 's' : ''}`}
                          >
                            ★
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="form-group">
                      <label htmlFor="review-title-input">Review Headline</label>
                      <input
                        id="review-title-input"
                        type="text"
                        placeholder="e.g. Excellent quality & fast shipping!"
                        value={reviewTitle}
                        onChange={(e) => setReviewTitle(e.target.value)}
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="review-comment-input">Review Details</label>
                      <textarea
                        id="review-comment-input"
                        rows={3}
                        placeholder="Tell others what you liked or disliked about this product..."
                        value={reviewComment}
                        onChange={(e) => setReviewComment(e.target.value)}
                        required
                      />
                    </div>

                    <button
                      type="submit"
                      id="submit-review-btn"
                      className="btn-primary"
                      disabled={submittingReview}
                    >
                      {submittingReview ? 'Submitting...' : 'Submit Review'}
                    </button>
                  </form>
                ) : (
                  <div className="login-prompt-banner">
                    Please log in to submit a review for this product.
                  </div>
                )}
              </div>

              {/* Existing Reviews List */}
              <div className="review-list">
                <h4>Customer Feedback</h4>
                {reviewSummary && reviewSummary.reviews.length > 0 ? (
                  reviewSummary.reviews.map((rev) => (
                    <div key={rev.id} className="review-card">
                      <div className="review-card-header">
                        <div className="review-author-info">
                          <span className="review-author">{rev.username}</span>
                          <span className="review-date">{new Date(rev.created_at).toLocaleDateString()}</span>
                        </div>
                        <div className="review-stars">{renderStars(rev.rating)}</div>
                      </div>
                      <h5 className="review-card-title">{rev.title}</h5>
                      <p className="review-card-comment">{rev.comment}</p>
                    </div>
                  ))
                ) : (
                  <div className="no-reviews-msg">No customer reviews yet. Be the first to review this product!</div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  </div>
);
};

