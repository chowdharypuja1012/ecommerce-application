import { reviewsClient } from './reviewsClient';

// Smoke test suite for reviewsClient API helper functions
console.log('Testing reviewsClient module exports...');

if (typeof reviewsClient.getProductReviews !== 'function') {
  throw new Error('reviewsClient.getProductReviews is not a function');
}
if (typeof reviewsClient.createReview !== 'function') {
  throw new Error('reviewsClient.createReview is not a function');
}
if (typeof reviewsClient.deleteReview !== 'function') {
  throw new Error('reviewsClient.deleteReview is not a function');
}

console.log('✅ reviewsClient unit tests passed successfully!');
