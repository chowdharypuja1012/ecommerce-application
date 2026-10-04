import React, { useEffect, useState } from 'react';
import type { Order } from '../types/orders';
import { ordersClient } from '../api/ordersClient';

interface OrdersModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenPaymentModal?: (order: Order) => void;
}

export const OrdersModal: React.FC<OrdersModalProps> = ({ isOpen, onClose, onOpenPaymentModal }) => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedOrderId, setExpandedOrderId] = useState<number | null>(null);

  const loadOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await ordersClient.getOrders();
      setOrders(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load order history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadOrders();
    }
  }, [isOpen]);

  const handleCancelOrder = async (orderId: number) => {
    if (!confirm('Are you sure you want to cancel this order?')) return;
    try {
      const updated = await ordersClient.cancelOrder(orderId);
      setOrders((prev) => prev.map((o) => (o.id === orderId ? updated : o)));
    } catch (err: any) {
      alert(err.message || 'Could not cancel order.');
    }
  };

  if (!isOpen) return null;

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'DELIVERED':
        return { color: '#059669', bg: '#ECFDF5', border: '#A7F3D0' };
      case 'SHIPPED':
        return { color: '#2563EB', bg: '#EFF6FF', border: '#BFDBFE' };
      case 'PAID':
        return { color: '#7C3AED', bg: '#F5EEFF', border: '#DDD6FE' };
      case 'CANCELLED':
        return { color: '#DC2626', bg: '#FEF2F2', border: '#FECACA' };
      default: // PENDING
        return { color: '#D97706', bg: '#FFFBEB', border: '#FDE68A' };
    }
  };

  return (
    <div className="modal-overlay" id="orders-modal-overlay" onClick={onClose}>
      <div className="modal-content animate-fade-in" style={{ maxWidth: '760px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 style={{ color: 'var(--ruja-dark, #3D2F2F)', fontFamily: "'Cormorant Garamond', Georgia, serif", fontSize: '1.6rem' }}>
            📜 Your Order History
          </h2>
          <button className="close-btn" id="close-orders-modal" onClick={onClose} aria-label="Close modal">
            &times;
          </button>
        </div>

        <div className="modal-body" id="orders-list-body" style={{ maxHeight: '75vh', overflowY: 'auto' }}>
          {loading ? (
            <div className="cart-loading-state" style={{ padding: '3rem 0', textAlign: 'center' }}>
              <div className="spinner" />
              <p style={{ color: 'var(--text-secondary, #6B5B5B)', marginTop: '0.8rem' }}>Fetching your order history...</p>
            </div>
          ) : error ? (
            <div className="cart-error-banner" style={{ background: '#FEE2E2', borderColor: '#FECACA', color: '#DC2626', padding: '1rem', borderRadius: '12px' }}>
              <p>{error}</p>
            </div>
          ) : orders.length === 0 ? (
            <div className="empty-cart-view" id="empty-orders-view" style={{ padding: '3rem 1rem', textAlign: 'center' }}>
              <div className="empty-cart-icon" style={{ fontSize: '3rem', marginBottom: '1rem' }}>🛍️</div>
              <h3 style={{ color: 'var(--ruja-dark, #3D2F2F)', marginBottom: '0.5rem', fontFamily: "'Cormorant Garamond', Georgia, serif", fontSize: '1.5rem' }}>No Orders Found</h3>
              <p style={{ color: 'var(--text-secondary, #6B5B5B)', marginBottom: '1.5rem' }}>You haven't placed any orders yet. Start shopping and treat yourself!</p>
              <button className="btn-shop-now" onClick={onClose} type="button" style={{ margin: '0 auto' }}>
                Start Shopping →
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              {orders.map((order) => {
                const badgeStyle = getStatusBadgeClass(order.status);
                const isExpanded = expandedOrderId === order.id;
                const canCancel = order.status === 'PENDING' || order.status === 'PAID';
                const canPay = order.status === 'PENDING';

                return (
                  <div
                    key={order.id}
                    style={{
                      background: '#FFFFFF',
                      border: '1.5px solid var(--border-subtle, #F0E0E0)',
                      borderRadius: '18px',
                      padding: '1.35rem',
                      boxShadow: '0 4px 14px rgba(61, 47, 47, 0.04)',
                      transition: 'all 0.2s ease',
                    }}
                  >
                    {/* Header Row */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--ruja-dark, #3D2F2F)', letterSpacing: '0.3px' }}>
                          Order #{order.order_number}
                        </div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary, #6B5B5B)', marginTop: '0.25rem' }}>
                          Placed on {new Date(order.created_at).toLocaleDateString()} at {new Date(order.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>

                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                        <span
                          style={{
                            padding: '0.3rem 0.85rem',
                            borderRadius: '9999px',
                            fontSize: '0.78rem',
                            fontWeight: 700,
                            letterSpacing: '0.5px',
                            backgroundColor: badgeStyle.bg,
                            color: badgeStyle.color,
                            border: `1px solid ${badgeStyle.border}`,
                          }}
                        >
                          {order.status}
                        </span>

                        <span style={{ fontWeight: 700, fontSize: '1.25rem', color: 'var(--ruja-dark, #3D2F2F)' }}>
                          ₹{parseFloat(order.total_amount).toLocaleString('en-IN')}
                        </span>
                      </div>
                    </div>

                    {/* Action Buttons Row */}
                    <div style={{ marginTop: '1rem', display: 'flex', gap: '0.6rem', justifyContent: 'flex-end', flexWrap: 'wrap' }}>
                      {canPay && onOpenPaymentModal && (
                        <button
                          className="btn-primary"
                          onClick={() => {
                            onClose();
                            onOpenPaymentModal(order);
                          }}
                          type="button"
                          style={{
                            fontSize: '0.85rem',
                            padding: '0.45rem 0.95rem',
                            backgroundColor: '#10B981',
                            borderColor: '#10B981',
                            borderRadius: '9999px',
                            fontWeight: 600,
                            color: '#FFFFFF',
                          }}
                        >
                          💳 Pay Now (Sandbox)
                        </button>
                      )}

                      <button
                        type="button"
                        onClick={() => setExpandedOrderId(isExpanded ? null : order.id)}
                        style={{
                          fontSize: '0.85rem',
                          padding: '0.45rem 0.95rem',
                          borderRadius: '9999px',
                          background: isExpanded ? 'var(--ruja-pink, #E8A0BF)' : '#FFF0F5',
                          color: isExpanded ? '#FFFFFF' : 'var(--ruja-pink, #E8A0BF)',
                          border: '1px solid var(--ruja-pink-light, #F5D5E0)',
                          fontWeight: 600,
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                        }}
                      >
                        {isExpanded ? 'Hide Details ▲' : 'View Details ▼'}
                      </button>

                      {canCancel && (
                        <button
                          type="button"
                          onClick={() => handleCancelOrder(order.id)}
                          style={{
                            fontSize: '0.85rem',
                            padding: '0.45rem 0.95rem',
                            borderRadius: '9999px',
                            background: '#FEE2E2',
                            color: '#DC2626',
                            border: '1px solid #FECACA',
                            fontWeight: 600,
                            cursor: 'pointer',
                            transition: 'all 0.2s ease',
                          }}
                        >
                          Cancel Order
                        </button>
                      )}
                    </div>

                    {/* Order Details Accordion */}
                    {isExpanded && (
                      <div
                        style={{
                          marginTop: '1rem',
                          paddingTop: '1rem',
                          borderTop: '1.5px dashed var(--border-subtle, #F0E0E0)',
                          background: '#FFFAF5',
                          borderRadius: '12px',
                          padding: '1rem',
                        }}
                      >
                        <h4 style={{ margin: '0 0 0.6rem 0', fontSize: '0.95rem', fontWeight: 700, color: 'var(--ruja-dark, #3D2F2F)' }}>
                          🛍️ Purchased Items:
                        </h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginBottom: '1rem' }}>
                          {order.items.map((item) => (
                            <div
                              key={item.id}
                              style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: '0.5rem 0.75rem',
                                background: '#FFFFFF',
                                borderRadius: '10px',
                                border: '1px solid var(--border-subtle, #F0E0E0)',
                                fontSize: '0.9rem',
                              }}
                            >
                              <div>
                                <span style={{ fontWeight: 700, color: 'var(--ruja-dark, #3D2F2F)' }}>
                                  {item.product_name}
                                </span>
                                <span style={{ color: 'var(--text-secondary, #6B5B5B)', fontSize: '0.82rem', marginLeft: '0.4rem' }}>
                                  ({item.product_sku}) &times; {item.quantity}
                                </span>
                              </div>
                              <span style={{ fontWeight: 700, color: 'var(--ruja-dark, #3D2F2F)' }}>
                                ₹{parseFloat(item.line_total).toLocaleString('en-IN')}{' '}
                                <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary, #6B5B5B)', fontWeight: 400 }}>
                                  (₹{parseFloat(item.unit_price).toLocaleString('en-IN')} ea)
                                </span>
                              </span>
                            </div>
                          ))}
                        </div>

                        <h4 style={{ margin: '0 0 0.35rem 0', fontSize: '0.92rem', fontWeight: 700, color: 'var(--ruja-dark, #3D2F2F)' }}>
                          📍 Shipping Destination:
                        </h4>
                        <p style={{ margin: 0, fontSize: '0.88rem', color: 'var(--text-secondary, #6B5B5B)', lineHeight: 1.5 }}>
                          <strong style={{ color: 'var(--ruja-dark, #3D2F2F)' }}>{order.shipping_full_name}</strong> | {order.shipping_street_address}, {order.shipping_city}, {order.shipping_state} {order.shipping_postal_code}, {order.shipping_country}
                        </p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
