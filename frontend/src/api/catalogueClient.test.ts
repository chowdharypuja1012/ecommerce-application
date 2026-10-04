import { catalogueClient } from './catalogueClient';
import type { Category, PaginatedResponse, Product } from '../types/catalogue';

/**
 * Catalogue API Client Unit Verification Test Script.
 * Verifies category fetching, product filter URL query building, and error responses.
 */
export async function runCatalogueClientTests(): Promise<void> {
  console.log('Running catalogueClient tests...');

  // Mock global fetch
  const originalFetch = globalThis.fetch;

  try {
    // Test 1: getCategories
    const mockCategories: Category[] = [
      { id: 1, name: 'Electronics', slug: 'electronics', description: 'Gadgets', is_active: true },
    ];
    globalThis.fetch = (async () => {
      return new Response(JSON.stringify(mockCategories), { status: 200 });
    }) as typeof fetch;

    const categories = await catalogueClient.getCategories();
    if (categories.length !== 1 || categories[0].slug !== 'electronics') {
      throw new Error('getCategories test failed!');
    }
    console.log('✓ getCategories test passed');

    // Test 2: getProducts with query parameters
    const mockProducts: PaginatedResponse<Product> = {
      count: 1,
      total_pages: 1,
      current_page: 1,
      next: null,
      previous: null,
      results: [
        {
          id: 10,
          category: { id: 1, name: 'Electronics', slug: 'electronics' },
          name: 'Pro Laptop',
          slug: 'pro-laptop',
          description: 'Laptop',
          price: '999.00',
          sku: 'LAPTOP-10',
          stock: 5,
          is_active: true,
          image_url: '',
          created_at: '2026-10-04T10:00:00Z',
        },
      ],
    };

    let requestedUrl = '';
    globalThis.fetch = (async (input: RequestInfo | URL) => {
      requestedUrl = input.toString();
      return new Response(JSON.stringify(mockProducts), { status: 200 });
    }) as typeof fetch;

    const productsResp = await catalogueClient.getProducts({
      search: 'laptop',
      category: 'electronics',
      min_price: '500',
      ordering: '-price',
      page: 1,
    });

    if (!requestedUrl.includes('search=laptop') || !requestedUrl.includes('min_price=500')) {
      throw new Error(`getProducts query string missing expected params: ${requestedUrl}`);
    }
    if (productsResp.results.length !== 1) {
      throw new Error('getProducts results length mismatch!');
    }
    console.log('✓ getProducts query building test passed');

    // Test 3: 400 Bad Request error handling
    globalThis.fetch = (async () => {
      return new Response(JSON.stringify({ error: 'Invalid min_price parameter' }), { status: 400 });
    }) as typeof fetch;

    let errorCaught = false;
    try {
      await catalogueClient.getProducts({ min_price: '-10' });
    } catch (err: any) {
      if (err.message.includes('Invalid min_price')) {
        errorCaught = true;
      }
    }

    if (!errorCaught) {
      throw new Error('Failed to handle 400 Bad Request response!');
    }
    console.log('✓ 400 Bad Request error handling test passed');

    console.log('All catalogueClient tests passed successfully!');
  } finally {
    globalThis.fetch = originalFetch;
  }
}

// Execute test suite when loaded
const globalProcess = (globalThis as any).process;
if (typeof globalProcess !== 'undefined' && globalProcess.argv?.[1]?.includes('catalogueClient.test')) {
  runCatalogueClientTests().catch((err) => {
    console.error('Test run failed:', err);
    globalProcess.exit(1);
  });
}
