export interface PaymentTransaction {
  id: number;
  order_id: number;
  transaction_reference: string;
  idempotency_key?: string;
  amount: string;
  currency: string;
  payment_method: string;
  status: 'INITIATED' | 'SUCCESS' | 'FAILED' | 'CANCELLED';
  provider_status_code: string;
  provider_message: string;
  created_at: string;
  updated_at: string;
}
