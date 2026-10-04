import { authClient } from './authClient';
import type { CheckoutAddress, CheckoutPreviewResponse, Order } from '../types/orders';

const BASE_URL = import.meta.env?.VITE_API_GATEWAY_URL || 'http://127.0.0.1:8000';

export const ordersClient = {
  /**
   * Generates order preview, re-checking stock and price snapshots.
   */
  async previewCheckout(address: CheckoutAddress): Promise<CheckoutPreviewResponse> {
    const response = await fetch(`${BASE_URL}/api/v1/checkout/preview/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
      body: JSON.stringify(address),
    });

    const data = await response.json();
    if (!response.ok) {
      const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Failed to preview checkout.';
      throw new Error(msg || 'Failed to preview checkout.');
    }
    return data;
  },

  /**
   * Submits checkout to create a pending order and clear active cart.
   */
  async createOrder(address: CheckoutAddress): Promise<Order> {
    const response = await fetch(`${BASE_URL}/api/v1/checkout/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
      body: JSON.stringify(address),
    });

    const data = await response.json();
    if (!response.ok) {
      const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Checkout failed.';
      throw new Error(msg || 'Checkout failed.');
    }
    return data;
  },

  /**
   * Fetches customer order history.
   */
  async getOrders(): Promise<Order[]> {
    const response = await fetch(`${BASE_URL}/api/v1/orders/`, {
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch order history.');
    }
    return await response.json();
  },

  /**
   * Fetches detailed information for a single order by ID.
   */
  async getOrderDetails(orderId: number): Promise<Order> {
    const response = await fetch(`${BASE_URL}/api/v1/orders/${orderId}/`, {
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch order details.');
    }
    return await response.json();
  },
};
