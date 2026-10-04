export interface CheckoutAddress {
  shipping_full_name: string;
  shipping_street_address: string;
  shipping_city: string;
  shipping_state: string;
  shipping_postal_code: string;
  shipping_country: string;
  shipping_phone?: string;
}

export interface OrderItem {
  id: number;
  product_id: number;
  product_sku: string;
  product_name: string;
  unit_price: string;
  quantity: number;
  line_total: string;
}

export interface Order {
  id: number;
  order_number: string;
  status: 'PENDING' | 'PAID' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED';
  total_amount: string;
  shipping_full_name: string;
  shipping_street_address: string;
  shipping_city: string;
  shipping_state: string;
  shipping_postal_code: string;
  shipping_country: string;
  shipping_phone?: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface CheckoutPreviewResponse {
  shipping_address: CheckoutAddress;
  items: OrderItem[];
  total_amount: string;
  status: string;
}
