import { authClient } from './authClient';
import type { Review, ReviewSummaryResponse } from '../types/reviews';

const BASE_URL = import.meta.env?.VITE_API_GATEWAY_URL || 'http://127.0.0.1:8000';

export const reviewsClient = {
  /**
   * Fetch public approved reviews and aggregate rating summary for a product.
   */
  async getProductReviews(productId: number): Promise<ReviewSummaryResponse> {
    const response = await fetch(`${BASE_URL}/api/v1/reviews/product/${productId}/`);
    if (!response.ok) {
      throw new Error('Failed to fetch reviews for product.');
    }
    return await response.json();
  },

  /**
   * Submit a new customer review for a product.
   */
  async createReview(
    productId: number,
    rating: number,
    title: string,
    comment: string
  ): Promise<Review> {
    const response = await fetch(`${BASE_URL}/api/v1/reviews/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
      body: JSON.stringify({
        product_id: productId,
        rating,
        title,
        comment,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Failed to submit review.';
      throw new Error(msg || 'Failed to submit review.');
    }
    return data;
  },

  /**
   * Delete a customer review by ID.
   */
  async deleteReview(reviewId: number): Promise<void> {
    const response = await fetch(`${BASE_URL}/api/v1/reviews/${reviewId}/`, {
      method: 'DELETE',
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to delete review.');
    }
  },
};
