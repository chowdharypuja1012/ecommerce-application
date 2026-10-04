import React, { useState } from 'react';
import type { Order } from '../types/orders';
import type { PaymentTransaction } from '../types/payments';
import { paymentsClient } from '../api/paymentsClient';

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  order: Order | null;
  onPaymentSuccess: (tx: PaymentTransaction) => void;
}

export const PaymentModal: React.FC<PaymentModalProps> = ({
  isOpen,
  onClose,
  order,
  onPaymentSuccess,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resultTx, setResultTx] = useState<PaymentTransaction | null>(null);

  if (!isOpen || !order) return null;

  const handleSimulatePayment = async (action: 'SUCCESS' | 'FAIL' | 'CANCEL') => {
    setLoading(true);
    setError(null);
    try {
      const tx = await paymentsClient.processPayment(
        order.id,
        order.total_amount,
        action,
        `IDEM-${order.id}-${Date.now()}`
      );
      setResultTx(tx);
      if (tx.status === 'SUCCESS') {
        onPaymentSuccess(tx);
      }
    } catch (err: any) {
      setError(err.message || 'Payment simulation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" id="payment-modal-overlay" onClick={onClose}>
      <div className="modal-content animate-fade-in" style={{ maxWidth: '580px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>💳 Payment Sandbox Simulator</h2>
          <button className="close-btn" id="close-payment-modal" onClick={onClose} aria-label="Close modal">
            &times;
          </button>
        </div>

        <div className="modal-body" id="payment-sandbox-body">
          {/* Sandbox Warning Banner */}
          <div
            className="cart-error-banner"
            style={{
              background: 'rgba(99, 102, 241, 0.12)',
              borderColor: 'rgba(99, 102, 241, 0.3)',
              color: '#fff',
              marginBottom: '1.25rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 600 }}>
              <span style={{ fontSize: '1.2rem' }}>🧪</span> Simulated Provider Sandbox Environment
            </div>
            <p style={{ margin: '0.3rem 0 0 0', fontSize: '0.86rem', color: 'var(--color-text-muted, #94a3b8)' }}>
              No real card credentials or financial charges are processed. Card data is strictly never collected or stored.
            </p>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem', fontSize: '0.92rem' }}>
              <span style={{ color: 'var(--color-text-muted, #94a3b8)' }}>Order Number:</span>
              <strong style={{ color: '#fff' }}>{order.order_number}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.1rem', fontWeight: 700 }}>
              <span>Total Payable Amount:</span>
              <span style={{ color: 'var(--color-primary-light, #818cf8)' }}>₹{parseFloat(order.total_amount).toLocaleString('en-IN')} INR</span>
            </div>
          </div>

          {error && (
            <div className="cart-error-banner" style={{ marginBottom: '1rem' }}>
              <p>{error}</p>
            </div>
          )}

          {resultTx ? (
            <div
              className="cart-error-banner"
              style={{
                background: resultTx.status === 'SUCCESS' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                borderColor: resultTx.status === 'SUCCESS' ? 'rgba(16, 185, 129, 0.4)' : 'rgba(239, 68, 68, 0.4)',
                textAlign: 'center',
                padding: '1.25rem',
              }}
            >
              <div style={{ fontSize: '2.5rem', marginBottom: '0.3rem' }}>
                {resultTx.status === 'SUCCESS' ? '✅' : resultTx.status === 'CANCELLED' ? '🟡' : '❌'}
              </div>
              <h3 style={{ margin: '0 0 0.25rem 0', color: '#fff' }}>
                Payment Status: {resultTx.status}
              </h3>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted, #94a3b8)', margin: '0 0 0.5rem 0' }}>
                Ref Token: <code style={{ color: '#fff', background: 'rgba(0,0,0,0.3)', padding: '0.2rem 0.4rem', borderRadius: '4px' }}>{resultTx.transaction_reference}</code>
              </p>
              <p style={{ fontSize: '0.9rem', color: '#fff', margin: 0 }}>
                {resultTx.provider_message}
              </p>

              <div style={{ marginTop: '1.25rem', display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                {resultTx.status !== 'SUCCESS' && (
                  <button
                    className="btn-secondary"
                    onClick={() => setResultTx(null)}
                    type="button"
                  >
                    Try Another Action
                  </button>
                )}
                <button className="btn-primary" onClick={onClose} type="button">
                  {resultTx.status === 'SUCCESS' ? 'Done' : 'Close'}
                </button>
              </div>
            </div>
          ) : (
            <div>
              <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted, #94a3b8)', marginBottom: '1rem' }}>
                Select a payment outcome to simulate:
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <button
                  id="simulate-payment-success-btn"
                  className="btn-primary"
                  disabled={loading}
                  onClick={() => handleSimulatePayment('SUCCESS')}
                  type="button"
                  style={{
                    backgroundColor: '#10b981',
                    borderColor: '#10b981',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    padding: '0.75rem',
                  }}
                >
                  🟢 Approve Payment (Simulate Success)
                </button>

                <button
                  id="simulate-payment-fail-btn"
                  className="btn-secondary"
                  disabled={loading}
                  onClick={() => handleSimulatePayment('FAIL')}
                  type="button"
                  style={{
                    borderColor: '#ef4444',
                    color: '#ef4444',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    padding: '0.75rem',
                  }}
                >
                  🔴 Decline Payment (Simulate Failure)
                </button>

                <button
                  id="simulate-payment-cancel-btn"
                  className="btn-secondary"
                  disabled={loading}
                  onClick={() => handleSimulatePayment('CANCEL')}
                  type="button"
                  style={{
                    borderColor: '#f59e0b',
                    color: '#f59e0b',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    padding: '0.75rem',
                  }}
                >
                  🟡 User Cancel Payment (Simulate Cancel)
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
