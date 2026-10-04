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
            style={{
              background: 'var(--ruja-pink-pale, #FFF0F5)',
              border: '1px solid rgba(232, 160, 191, 0.4)',
              borderRadius: '16px',
              padding: '1rem 1.25rem',
              color: 'var(--ruja-dark, #3D2F2F)',
              marginBottom: '1.25rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 700, fontSize: '0.95rem' }}>
              <span style={{ fontSize: '1.2rem' }}>🧪</span> Simulated Provider Sandbox Environment
            </div>
            <p style={{ margin: '0.3rem 0 0 0', fontSize: '0.85rem', color: 'var(--text-secondary, #6B5E5E)', lineHeight: 1.4 }}>
              No real card credentials or financial charges are processed. Card data is strictly never collected or stored.
            </p>
          </div>

          <div style={{
            background: '#FAF6F0',
            border: '1px solid var(--border-subtle, rgba(232, 160, 191, 0.25))',
            padding: '1.15rem 1.25rem',
            borderRadius: '16px',
            marginBottom: '1.25rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem', fontSize: '0.92rem' }}>
              <span style={{ color: 'var(--text-muted, #9C8E8E)' }}>Order Number:</span>
              <strong style={{ color: 'var(--ruja-dark, #3D2F2F)', background: 'var(--ruja-pink-light, #FFE4E1)', padding: '2px 8px', borderRadius: '6px' }}>
                {order.order_number}
              </strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '1.05rem', fontWeight: 700, marginTop: '0.5rem' }}>
              <span style={{ color: 'var(--ruja-dark, #3D2F2F)' }}>Total Payable Amount:</span>
              <span style={{ color: 'var(--ruja-dark, #3D2F2F)', fontSize: '1.35rem', fontWeight: 800 }}>
                ₹{parseFloat(order.total_amount).toLocaleString('en-IN')} INR
              </span>
            </div>
          </div>

          {error && (
            <div className="auth-error-banner" style={{ marginBottom: '1rem' }}>
              <p style={{ margin: 0 }}>{error}</p>
            </div>
          )}

          {resultTx ? (
            <div
              style={{
                background: resultTx.status === 'SUCCESS' ? '#ECFDF5' : '#FEF2F2',
                border: `1.5px solid ${resultTx.status === 'SUCCESS' ? '#A7F3D0' : '#FECACA'}`,
                borderRadius: '16px',
                textAlign: 'center',
                padding: '1.5rem',
              }}
            >
              <div style={{ fontSize: '2.5rem', marginBottom: '0.3rem' }}>
                {resultTx.status === 'SUCCESS' ? '✅' : resultTx.status === 'CANCELLED' ? '🟡' : '❌'}
              </div>
              <h3 style={{ margin: '0 0 0.35rem 0', color: resultTx.status === 'SUCCESS' ? '#065F46' : '#991B1B', fontWeight: 700 }}>
                Payment Status: {resultTx.status}
              </h3>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary, #6B5E5E)', margin: '0 0 0.5rem 0' }}>
                Ref Token: <code style={{ color: 'var(--ruja-dark, #3D2F2F)', background: '#FFFFFF', padding: '0.2rem 0.5rem', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>{resultTx.transaction_reference}</code>
              </p>
              <p style={{ fontSize: '0.9rem', color: 'var(--ruja-dark, #3D2F2F)', margin: 0, fontWeight: 500 }}>
                {resultTx.provider_message}
              </p>

              <div style={{ marginTop: '1.25rem', display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                {resultTx.status !== 'SUCCESS' && (
                  <button
                    className="btn-secondary"
                    onClick={() => setResultTx(null)}
                    type="button"
                    style={{ borderRadius: '9999px', padding: '0.75rem 1.25rem' }}
                  >
                    Try Another Action
                  </button>
                )}
                <button
                  className="btn-primary"
                  onClick={onClose}
                  type="button"
                  style={{ borderRadius: '9999px', padding: '0.75rem 1.4rem' }}
                >
                  {resultTx.status === 'SUCCESS' ? 'Done ✨' : 'Close'}
                </button>
              </div>
            </div>
          ) : (
            <div>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary, #6B5E5E)', marginBottom: '0.85rem', fontWeight: 500 }}>
                Select a payment outcome to simulate:
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <button
                  id="simulate-payment-success-btn"
                  disabled={loading}
                  onClick={() => handleSimulatePayment('SUCCESS')}
                  type="button"
                  style={{
                    backgroundColor: '#D1FAE5',
                    color: '#065F46',
                    border: '1.5px solid #A7F3D0',
                    borderRadius: '9999px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    padding: '0.8rem 1.25rem',
                    fontWeight: 700,
                    fontSize: '0.92rem',
                    cursor: 'pointer',
                    boxShadow: '0 2px 8px rgba(16, 185, 129, 0.12)',
                    transition: 'all 0.2s ease'
                  }}
                >
                  🟢 Approve Payment (Simulate Success)
                </button>

                <button
                  id="simulate-payment-fail-btn"
                  disabled={loading}
                  onClick={() => handleSimulatePayment('FAIL')}
                  type="button"
                  style={{
                    backgroundColor: '#FEE2E2',
                    color: '#991B1B',
                    border: '1.5px solid #FECACA',
                    borderRadius: '9999px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    padding: '0.8rem 1.25rem',
                    fontWeight: 700,
                    fontSize: '0.92rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                >
                  🔴 Decline Payment (Simulate Failure)
                </button>

                <button
                  id="simulate-payment-cancel-btn"
                  disabled={loading}
                  onClick={() => handleSimulatePayment('CANCEL')}
                  type="button"
                  style={{
                    backgroundColor: '#FEF3C7',
                    color: '#92400E',
                    border: '1.5px solid #FDE68A',
                    borderRadius: '9999px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    padding: '0.8rem 1.25rem',
                    fontWeight: 700,
                    fontSize: '0.92rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
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
