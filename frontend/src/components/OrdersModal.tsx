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
        return { color: 'var(--color-success, #10b981)', bg: 'rgba(16, 185, 129, 0.15)' };
      case 'SHIPPED':
        return { color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.15)' };
      case 'PAID':
        return { color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.15)' };
      case 'CANCELLED':
        return { color: 'var(--color-danger, #ef4444)', bg: 'rgba(239, 68, 68, 0.15)' };
      default: // PENDING
        return { color: 'var(--color-warning, #f59e0b)', bg: 'rgba(245, 158, 11, 0.15)' };
    }
  };

  return (
    <div className="modal-overlay" id="orders-modal-overlay" onClick={onClose}>
      <div className="modal-content animate-fade-in" style={{ maxWidth: '720px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>📜 Your Order History</h2>
          <button className="close-btn" id="close-orders-modal" onClick={onClose} aria-label="Close modal">
            &times;
          </button>
        </div>

        <div className="modal-body" id="orders-list-body">
          {loading ? (
            <div className="cart-loading-state">
              <div className="spinner" />
              <p>Fetching your order history...</p>
            </div>
          ) : error ? (
            <div className="cart-error-banner">
              <p>{error}</p>
            </div>
          ) : orders.length === 0 ? (
            <div className="empty-cart-view" id="empty-orders-view">
              <div className="empty-cart-icon">🛍️</div>
              <h3>No Orders Found</h3>
              <p>You haven't placed any orders yet. Start shopping and place your first order!</p>
              <button className="btn-primary" onClick={onClose} type="button">
                Start Shopping
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {orders.map((order) => {
                const badgeStyle = getStatusBadgeClass(order.status);
                const isExpanded = expandedOrderId === order.id;
                const canCancel = order.status === 'PENDING' || order.status === 'PAID';
                const canPay = order.status === 'PENDING';

                return (
                  <div
                    key={order.id}
                    className="cart-error-banner"
                    style={{
                      background: 'rgba(255, 255, 255, 0.03)',
                      borderColor: 'rgba(255, 255, 255, 0.1)',
                      color: 'inherit',
                      padding: '1.2rem',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div>
                        <div style={{ fontWeight: 600, fontSize: '1.05rem', color: '#fff' }}>
                          {order.order_number}
                        </div>
                        <div style={{ fontSize: '0.82rem', color: 'var(--color-text-muted, #94a3b8)', marginTop: '0.2rem' }}>
                          Placed on {new Date(order.created_at).toLocaleDateString()} at {new Date(order.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>

                      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <span
                          style={{
                            padding: '0.25rem 0.75rem',
                            borderRadius: '9999px',
                            fontSize: '0.8rem',
                            fontWeight: 600,
                            backgroundColor: badgeStyle.bg,
                            color: badgeStyle.color,
                          }}
                        >
                          {order.status}
                        </span>

                        <span style={{ fontWeight: 700, fontSize: '1.1rem', color: '#fff' }}>
                          ₹{parseFloat(order.total_amount).toLocaleString('en-IN')}
                        </span>
                      </div>
                    </div>

                    <div style={{ marginTop: '0.8rem', display: 'flex', gap: '0.6rem', justifyContent: 'flex-end' }}>
                      {canPay && onOpenPaymentModal && (
                        <button
                          className="btn-primary"
                          onClick={() => {
                            onClose();
                            onOpenPaymentModal(order);
                          }}
                          type="button"
                          style={{
                            fontSize: '0.82rem',
                            padding: '0.35rem 0.75rem',
                            backgroundColor: '#10b981',
                            borderColor: '#10b981',
                          }}
                        >
                          💳 Pay Now (Sandbox)
                        </button>
                      )}

                      <button
                        className="btn-secondary"
                        onClick={() => setExpandedOrderId(isExpanded ? null : order.id)}
                        type="button"
                        style={{ fontSize: '0.82rem', padding: '0.35rem 0.75rem' }}
                      >
                        {isExpanded ? 'Hide Details ▲' : 'View Details ▼'}
                      </button>

                      {canCancel && (
                        <button
                          className="btn-secondary"
                          onClick={() => handleCancelOrder(order.id)}
                          type="button"
                          style={{
                            fontSize: '0.82rem',
                            padding: '0.35rem 0.75rem',
                            borderColor: 'var(--color-danger, #ef4444)',
                            color: 'var(--color-danger, #ef4444)',
                          }}
                        >
                          Cancel Order
                        </button>
                      )}
                    </div>

                    {/* Order Details Accordion */}
                    {isExpanded && (
                      <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                        <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '0.92rem', color: '#fff' }}>Purchase Items:</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', marginBottom: '1rem' }}>
                          {order.items.map((item) => (
                            <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.86rem', color: 'var(--color-text-muted, #94a3b8)' }}>
                              <span>
                                <strong style={{ color: '#fff' }}>{item.product_name}</strong> ({item.product_sku}) &times; {item.quantity}
                              </span>
                              <span>₹{parseFloat(item.line_total).toLocaleString('en-IN')} (₹{parseFloat(item.unit_price).toLocaleString('en-IN')} ea)</span>
                            </div>
                          ))}
                        </div>

                        <h4 style={{ margin: '0 0 0.25rem 0', fontSize: '0.92rem', color: '#fff' }}>Shipping Destination:</h4>
                        <p style={{ margin: 0, fontSize: '0.86rem', color: 'var(--color-text-muted, #94a3b8)' }}>
                          {order.shipping_full_name} | {order.shipping_street_address}, {order.shipping_city}, {order.shipping_state} {order.shipping_postal_code}, {order.shipping_country}
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
