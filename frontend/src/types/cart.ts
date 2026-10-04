export interface CartItem {
  id: number;
  product_id: number;
  product_sku: string;
  product_name: string;
  unit_price: string;
  quantity: number;
  line_total: string;
  created_at?: string;
  updated_at?: string;
}

export interface Cart {
  id: number;
  status: string;
  items: CartItem[];
  subtotal: string;
  total_items: number;
  created_at?: string;
  updated_at?: string;
}
