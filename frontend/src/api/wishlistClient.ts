import { authClient } from './authClient';
import type { Wishlist } from '../types/wishlist';

const BASE_URL = import.meta.env?.VITE_API_GATEWAY_URL || 'http://127.0.0.1:8000';

export const wishlistClient = {
  /**
   * Fetch current authenticated user's wishlist.
   */
  async getWishlist(): Promise<Wishlist> {
    const response = await fetch(`${BASE_URL}/api/v1/wishlist/`, {
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Authentication required to view wishlist.');
      }
      throw new Error('Failed to fetch wishlist from server.');
    }
    return await response.json();
  },

  /**
   * Add a product to wishlist.
   */
  async addItem(productId: number): Promise<Wishlist> {
    const response = await fetch(`${BASE_URL}/api/v1/wishlist/items/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
      body: JSON.stringify({ product_id: productId }),
    });

    const data = await response.json();
    if (!response.ok) {
      const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Failed to add item to wishlist.';
      throw new Error(msg || 'Failed to add item to wishlist.');
    }
    return data;
  },

  /**
   * Remove item from wishlist by item ID.
   */
  async removeItem(itemId: number): Promise<Wishlist> {
    const response = await fetch(`${BASE_URL}/api/v1/wishlist/items/${itemId}/`, {
      method: 'DELETE',
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to remove item from wishlist.');
    }
    return await response.json();
  },

  /**
   * Remove item from wishlist by product ID.
   */
  async removeItemByProductId(productId: number): Promise<Wishlist> {
    const response = await fetch(`${BASE_URL}/api/v1/wishlist/items/by-product/${productId}/`, {
      method: 'DELETE',
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to remove product from wishlist.');
    }
    return await response.json();
  },

  /**
   * Clear all items in wishlist.
   */
  async clearWishlist(): Promise<Wishlist> {
    const response = await fetch(`${BASE_URL}/api/v1/wishlist/clear/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to clear wishlist.');
    }
    return await response.json();
  },
};
