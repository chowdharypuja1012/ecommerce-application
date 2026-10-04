import { authClient } from './authClient';
import type { PaymentTransaction } from '../types/payments';

const BASE_URL = import.meta.env?.VITE_API_GATEWAY_URL || 'http://127.0.0.1:8000';

export const paymentsClient = {
  /**
   * Process simulated payment sandbox request.
   */
  async processPayment(
    orderId: number,
    amount: string,
    simulatedAction: 'SUCCESS' | 'FAIL' | 'CANCEL' = 'SUCCESS',
    idempotencyKey?: string
  ): Promise<PaymentTransaction> {
    const response = await fetch(`${BASE_URL}/api/v1/payments/process/`, {
      method: 'POST',
      headers: authClient.getAuthHeaders(),
      body: JSON.stringify({
        order_id: orderId,
        amount,
        simulated_action: simulatedAction,
        idempotency_key: idempotencyKey,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Payment processing failed.';
      throw new Error(msg || 'Payment processing failed.');
    }
    return data;
  },

  /**
   * Fetch payment transaction history for a specific order.
   */
  async getOrderPayments(orderId: number): Promise<PaymentTransaction[]> {
    const response = await fetch(`${BASE_URL}/api/v1/payments/order/${orderId}/`, {
      headers: authClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch payment transactions for order.');
    }
    return await response.json();
  },
};
