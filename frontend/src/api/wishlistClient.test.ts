import { wishlistClient } from './wishlistClient';

// Smoke test suite for wishlistClient API helper functions
console.log('Testing wishlistClient module exports...');

if (typeof wishlistClient.getWishlist !== 'function') {
  throw new Error('wishlistClient.getWishlist is not a function');
}
if (typeof wishlistClient.addItem !== 'function') {
  throw new Error('wishlistClient.addItem is not a function');
}
if (typeof wishlistClient.removeItem !== 'function') {
  throw new Error('wishlistClient.removeItem is not a function');
}
if (typeof wishlistClient.removeItemByProductId !== 'function') {
  throw new Error('wishlistClient.removeItemByProductId is not a function');
}
if (typeof wishlistClient.clearWishlist !== 'function') {
  throw new Error('wishlistClient.clearWishlist is not a function');
}

console.log('✅ wishlistClient unit tests passed successfully!');
