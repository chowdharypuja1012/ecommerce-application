import { authClient } from './authClient';
import type { Cart } from '../types/cart';

const BASE_URL = import.meta.env?.VITE_API_GATEWAY_URL || 'http://127.0.0.1:8000';

export const cartClient = {
  /**
   * Fetch current authenticated user's active cart.
   */
  async getCart(): Promise<Cart> {
    const response = await fetch(`${BASE_URL}/api/v1/cart/`, {
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Authentication required to view shopping cart.');
      }
      throw new Error('Failed to fetch shopping cart from server.');
    }
    return await response.json();
  },

  /**
   * Add a product item to active cart.
   */
  async addItem(productId: number, quantity = 1): Promise<Cart> {
    const response = await fetch(`${BASE_URL}/api/v1/cart/items/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
      body: JSON.stringify({ product_id: productId, quantity }),
    });

    const data = await response.json();
    if (!response.ok) {
      const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Failed to add item to cart.';
      throw new Error(msg || 'Failed to add item to cart.');
    }
    return data;
  },

  /**
   * Update quantity of an item in active cart.
   */
  async updateItemQuantity(itemId: number, quantity: number): Promise<Cart> {
    const response = await fetch(`${BASE_URL}/api/v1/cart/items/${itemId}/`, {
      method: 'PATCH',
      headers: authClient.getAuthHeaders(),
      body: JSON.stringify({ quantity }),
    });

    const data = await response.json();
    if (!response.ok) {
      const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Failed to update item quantity.';
      throw new Error(msg || 'Failed to update item quantity.');
    }
    return data;
  },

  /**
   * Remove a specific item from active cart.
   */
  async removeItem(itemId: number): Promise<Cart> {
    const response = await fetch(`${BASE_URL}/api/v1/cart/items/${itemId}/`, {
      method: 'DELETE',
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to remove item from cart.');
    }
    return await response.json();
  },

  /**
   * Clear all items from active cart.
   */
  async clearCart(): Promise<Cart> {
    const response = await fetch(`${BASE_URL}/api/v1/cart/clear/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to clear shopping cart.');
    }
    return await response.json();
  },
};
