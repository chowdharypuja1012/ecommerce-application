import { cartClient } from './cartClient';
import type { Cart } from '../types/cart';

export async function runCartClientTests(): Promise<void> {
  console.log('Running cartClient unit tests...');

  const originalFetch = globalThis.fetch;

  try {
    // Test 1: getCart
    const mockCart: Cart = {
      id: 1,
      status: 'active',
      items: [
        {
          id: 10,
          product_id: 101,
          product_sku: 'LAPTOP-01',
          product_name: 'Pro Laptop',
          unit_price: '1200.00',
          quantity: 2,
          line_total: '2400.00',
        },
      ],
      subtotal: '2400.00',
      total_items: 2,
    };

    globalThis.fetch = (async () => {
      return new Response(JSON.stringify(mockCart), { status: 200 });
    }) as typeof fetch;

    const cartData = await cartClient.getCart();
    if (cartData.total_items !== 2 || cartData.subtotal !== '2400.00') {
      throw new Error('getCart test failed!');
    }
    console.log('✓ getCart test passed');

    // Test 2: addItem
    globalThis.fetch = (async (_input: RequestInfo | URL, init?: RequestInit) => {
      const body = JSON.parse(init?.body as string);
      if (body.product_id !== 101 || body.quantity !== 1) {
        throw new Error('addItem payload mismatch!');
      }
      return new Response(JSON.stringify(mockCart), { status: 200 });
    }) as typeof fetch;

    const addResp = await cartClient.addItem(101, 1);
    if (addResp.items.length !== 1) {
      throw new Error('addItem response handling failed!');
    }
    console.log('✓ addItem test passed');

    // Test 3: updateItemQuantity
    globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = input.toString();
      if (!url.includes('/cart/items/10/')) {
        throw new Error(`updateItemQuantity URL mismatch: ${url}`);
      }
      const body = JSON.parse(init?.body as string);
      if (body.quantity !== 5) {
        throw new Error('updateItemQuantity payload mismatch!');
      }
      return new Response(JSON.stringify({ ...mockCart, total_items: 5, subtotal: '6000.00' }), { status: 200 });
    }) as typeof fetch;

    const updateResp = await cartClient.updateItemQuantity(10, 5);
    if (updateResp.total_items !== 5) {
      throw new Error('updateItemQuantity response handling failed!');
    }
    console.log('✓ updateItemQuantity test passed');

    // Test 4: clearCart
    globalThis.fetch = (async () => {
      return new Response(JSON.stringify({ id: 1, status: 'active', items: [], subtotal: '0.00', total_items: 0 }), { status: 200 });
    }) as typeof fetch;

    const clearResp = await cartClient.clearCart();
    if (clearResp.total_items !== 0) {
      throw new Error('clearCart test failed!');
    }
    console.log('✓ clearCart test passed');

    console.log('All cartClient tests passed successfully!');
  } finally {
    globalThis.fetch = originalFetch;
  }
}

// Execute test suite when loaded via node/tsx
const globalProcess = (globalThis as any).process;
if (typeof globalProcess !== 'undefined' && globalProcess.argv?.[1]?.includes('cartClient.test')) {
  runCartClientTests().catch((err) => {
    console.error('Test run failed:', err);
    globalProcess.exit(1);
  });
}
