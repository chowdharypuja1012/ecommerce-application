import { paymentsClient } from './paymentsClient';

// Smoke test suite for paymentsClient API helper functions
console.log('Testing paymentsClient module exports...');

if (typeof paymentsClient.processPayment !== 'function') {
  throw new Error('paymentsClient.processPayment is not a function');
}
if (typeof paymentsClient.getOrderPayments !== 'function') {
  throw new Error('paymentsClient.getOrderPayments is not a function');
}

console.log('✅ paymentsClient unit tests passed successfully!');
