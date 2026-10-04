import { ordersClient } from './ordersClient';

// Smoke test suite for ordersClient API helper functions
console.log('Testing ordersClient module exports...');

if (typeof ordersClient.previewCheckout !== 'function') {
  throw new Error('ordersClient.previewCheckout is not a function');
}
if (typeof ordersClient.createOrder !== 'function') {
  throw new Error('ordersClient.createOrder is not a function');
}
if (typeof ordersClient.getOrders !== 'function') {
  throw new Error('ordersClient.getOrders is not a function');
}
if (typeof ordersClient.getOrderDetails !== 'function') {
  throw new Error('ordersClient.getOrderDetails is not a function');
}

console.log('✅ ordersClient unit tests passed successfully!');
