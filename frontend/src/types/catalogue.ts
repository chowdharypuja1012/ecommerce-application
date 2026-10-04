export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface CategorySummary {
  id: number;
  name: string;
  slug: string;
}

export interface Product {
  id: number;
  category: CategorySummary | null;
  name: string;
  slug: string;
  description: string;
  price: string;
  sku: string;
  stock: number;
  is_active: boolean;
  image_url: string;
  created_at: string;
  updated_at?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  total_pages: number;
  current_page: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ProductFilterParams {
  search?: string;
  category?: string;
  min_price?: string;
  max_price?: string;
  ordering?: string;
  page?: number;
  page_size?: number;
}
