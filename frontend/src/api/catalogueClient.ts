import type { Category, PaginatedResponse, Product, ProductFilterParams } from '../types/catalogue';

const BASE_URL = import.meta.env?.VITE_API_GATEWAY_URL || 'http://127.0.0.1:8000';

/**
 * Catalogue API Client
 * Interacts with the backend API Gateway / Catalogue Service.
 */
export const catalogueClient = {
  /**
   * Fetch all active categories.
   */
  async getCategories(): Promise<Category[]> {
    const urls = [
      `${BASE_URL}/api/v1/categories/`,
      `${BASE_URL}/api/v1/catalogue/categories/`,
    ];

    let lastError: Error | null = null;
    for (const url of urls) {
      try {
        const response = await fetch(url);
        if (response.ok) {
          return await response.json();
        }
      } catch (err) {
        lastError = err as Error;
      }
    }

    throw lastError || new Error('Failed to fetch categories from API.');
  },

  /**
   * Fetch paginated products with filter, search, sorting, and pagination parameters.
   */
  async getProducts(params: ProductFilterParams = {}): Promise<PaginatedResponse<Product>> {
    const query = new URLSearchParams();

    if (params.search?.trim()) {
      query.set('search', params.search.trim());
    }
    if (params.category?.trim()) {
      query.set('category', params.category.trim());
    }
    if (params.min_price?.trim()) {
      query.set('min_price', params.min_price.trim());
    }
    if (params.max_price?.trim()) {
      query.set('max_price', params.max_price.trim());
    }
    if (params.ordering?.trim()) {
      query.set('ordering', params.ordering.trim());
    }
    if (params.page && params.page > 1) {
      query.set('page', params.page.toString());
    }
    if (params.page_size) {
      query.set('page_size', params.page_size.toString());
    }

    const queryString = query.toString() ? `?${query.toString()}` : '';
    const urls = [
      `${BASE_URL}/api/v1/products/${queryString}`,
      `${BASE_URL}/api/v1/catalogue/products/${queryString}`,
    ];

    let lastError: Error | null = null;
    for (const url of urls) {
      try {
        const response = await fetch(url);
        if (response.ok) {
          return await response.json();
        } else if (response.status === 400) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Invalid filter criteria specified.');
        }
      } catch (err) {
        lastError = err as Error;
      }
    }

    throw lastError || new Error('Failed to fetch products from API.');
  },

  /**
   * Fetch single product detail by slug.
   */
  async getProductBySlug(slug: string): Promise<Product> {
    const urls = [
      `${BASE_URL}/api/v1/products/${slug}/`,
      `${BASE_URL}/api/v1/catalogue/products/${slug}/`,
    ];

    let lastError: Error | null = null;
    for (const url of urls) {
      try {
        const response = await fetch(url);
        if (response.ok) {
          return await response.json();
        } else if (response.status === 404) {
          throw new Error('Product not found.');
        }
      } catch (err) {
        lastError = err as Error;
      }
    }

    throw lastError || new Error(`Failed to fetch product details for ${slug}.`);
  },
};
