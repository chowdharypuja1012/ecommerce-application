export interface WishlistProductDetails {
  id: number;
  sku: string;
  name: string;
  slug: string;
  price: string;
  stock: number;
  is_active: boolean;
  image_url?: string;
}

export interface WishlistItem {
  id: number;
  product_id: number;
  added_at: string;
  product_details: WishlistProductDetails;
}

export interface Wishlist {
  id: number;
  total_items: number;
  created_at: string;
  updated_at: string;
  items: WishlistItem[];
}
