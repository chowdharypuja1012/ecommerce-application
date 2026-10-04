import React, { useState } from 'react';
import type { Cart } from '../types/cart';
import type { Address } from '../types/auth';
import type { CheckoutAddress, Order } from '../types/orders';
import { ordersClient } from '../api/ordersClient';

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  cart: Cart | null;
  savedAddresses: Address[];
  onOrderSuccess: (order: Order) => void;
  onOpenPaymentModal?: (order: Order) => void;
}

export const CheckoutModal: React.FC<CheckoutModalProps> = ({
  isOpen,
  onClose,
  cart,
  savedAddresses,
  onOrderSuccess,
  onOpenPaymentModal,
}) => {
  const [selectedAddressId, setSelectedAddressId] = useState<number | 'new'>(
    savedAddresses.find((a) => a.is_default)?.id || (savedAddresses.length > 0 ? savedAddresses[0].id : 'new')
  );

  const defaultAddr = savedAddresses.find((a) => a.id === selectedAddressId);

  const [fullName, setFullName] = useState('');
  const [streetAddress, setStreetAddress] = useState(defaultAddr?.street_address || '');
  const [city, setCity] = useState(defaultAddr?.city || '');
  const [state, setState] = useState(defaultAddr?.state || '');
  const [postalCode, setPostalCode] = useState(defaultAddr?.postal_code || '');
  const [country, setCountry] = useState(defaultAddr?.country || 'United States');
  const [phone, setPhone] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [placedOrder, setPlacedOrder] = useState<Order | null>(null);

  if (!isOpen) return null;

  const handleSelectAddress = (idStr: string) => {
    if (idStr === 'new') {
      setSelectedAddressId('new');
      setStreetAddress('');
      setCity('');
      setState('');
      setPostalCode('');
      return;
    }
    const addrId = parseInt(idStr, 10);
    setSelectedAddressId(addrId);
    const addr = savedAddresses.find((a) => a.id === addrId);
    if (addr) {
      setStreetAddress(addr.street_address);
      setCity(addr.city);
      setState(addr.state);
      setPostalCode(addr.postal_code);
      setCountry(addr.country);
    }
  };

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cart || cart.items.length === 0) {
      setError('Your shopping cart is empty.');
      return;
    }

    setLoading(true);
    setError(null);

    const addressData: CheckoutAddress = {
      shipping_full_name: fullName,
      shipping_street_address: streetAddress,
      shipping_city: city,
      shipping_state: state,
      shipping_postal_code: postalCode,
      shipping_country: country,
      shipping_phone: phone,
    };

    try {
      const newOrder = await ordersClient.createOrder(addressData);
      setPlacedOrder(newOrder);
      onOrderSuccess(newOrder);
    } catch (err: any) {
      setError(err.message || 'Checkout failed. Please re-check inventory or address details.');
    } finally {
      setLoading(false);
    }
  };

  const cartItems = cart?.items || [];
  const subtotal = cart?.subtotal ? parseFloat(cart.subtotal).toFixed(2) : '0.00';

  return (
    <div className="modal-overlay" id="checkout-modal-overlay" onClick={onClose}>
      <div className="modal-content animate-fade-in" style={{ maxWidth: '640px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{placedOrder ? '🎉 Order Placed Successfully!' : 'Checkout & Shipping Address'}</h2>
          <button className="close-btn" id="close-checkout-modal" onClick={onClose} aria-label="Close modal">
            &times;
          </button>
        </div>

        {placedOrder ? (
          <div className="modal-body" id="order-confirmation-view">
            <div style={{ textAlign: 'center', padding: '1.25rem 0 1rem' }}>
              <div style={{ fontSize: '3.2rem', marginBottom: '0.4rem' }}>📦</div>
              <h3 style={{
                fontFamily: "'Cormorant Garamond', Georgia, serif",
                fontSize: '1.65rem',
                fontWeight: 700,
                color: 'var(--ruja-dark, #3D2F2F)',
                margin: '0 0 0.4rem 0'
              }}>
                Thank you for your order!
              </h3>
              <p style={{ color: 'var(--text-secondary, #6B5E5E)', fontSize: '0.92rem', margin: '0 0 0.5rem 0' }}>
                Order Number: <strong style={{ color: 'var(--ruja-dark, #3D2F2F)', background: 'var(--ruja-pink-light, #FFE4E1)', padding: '2px 8px', borderRadius: '6px' }}>{placedOrder.order_number}</strong>
              </p>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted, #9C8E8E)' }}>Status:</span>
                <span style={{
                  background: '#FEF3C7',
                  color: '#B45309',
                  padding: '3px 10px',
                  borderRadius: '9999px',
                  fontWeight: 700,
                  fontSize: '0.78rem',
                  letterSpacing: '0.04em'
                }}>
                  {placedOrder.status}
                </span>
              </div>
            </div>

            <div style={{
              background: 'var(--ruja-pink-pale, #FFF0F5)',
              border: '1px solid rgba(232, 160, 191, 0.35)',
              borderRadius: '16px',
              padding: '1.15rem 1.25rem',
              margin: '0.5rem 0 1rem'
            }}>
              <h4 style={{ margin: '0 0 0.45rem 0', color: 'var(--ruja-dark, #3D2F2F)', fontSize: '0.92rem', fontWeight: 700 }}>
                📍 Shipping To:
              </h4>
              <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary, #6B5E5E)', lineHeight: 1.5 }}>
                <strong style={{ color: 'var(--ruja-dark, #3D2F2F)' }}>{placedOrder.shipping_full_name}</strong><br />
                {placedOrder.shipping_street_address}, {placedOrder.shipping_city}, {placedOrder.shipping_state} {placedOrder.shipping_postal_code}<br />
                {placedOrder.shipping_country}
              </p>
            </div>

            <div className="subtotal-row" style={{
              marginTop: '0.5rem',
              paddingTop: '0.85rem',
              borderTop: '1px solid var(--border-subtle, rgba(232, 160, 191, 0.25))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <span style={{ color: 'var(--ruja-dark, #3D2F2F)', fontWeight: 600, fontSize: '1rem' }}>
                Total Amount Pending:
              </span>
              <span className="subtotal-amount" style={{ color: 'var(--ruja-dark, #3D2F2F)', fontSize: '1.45rem', fontWeight: 800 }}>
                ₹{parseFloat(placedOrder.total_amount).toLocaleString('en-IN')}
              </span>
            </div>

            <div style={{ marginTop: '1.25rem', display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', alignItems: 'center' }}>
              <button
                className="btn-secondary"
                onClick={onClose}
                type="button"
                style={{
                  padding: '0.75rem 1.3rem',
                  borderRadius: '9999px',
                  background: 'var(--ruja-pink-pale, #FFF0F5)',
                  border: '1px solid rgba(232, 160, 191, 0.45)',
                  color: 'var(--ruja-pink, #E8A0BF)',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                Continue Shopping
              </button>
              {onOpenPaymentModal && (
                <button
                  id="checkout-pay-now-btn"
                  onClick={() => {
                    const currentOrd = placedOrder;
                    onClose();
                    onOpenPaymentModal(currentOrd);
                  }}
                  type="button"
                  style={{
                    backgroundColor: '#D1FAE5',
                    color: '#065F46',
                    border: '1.5px solid #A7F3D0',
                    borderRadius: '9999px',
                    padding: '0.75rem 1.4rem',
                    fontWeight: 700,
                    fontSize: '0.92rem',
                    cursor: 'pointer',
                    boxShadow: '0 2px 8px rgba(16, 185, 129, 0.12)',
                    transition: 'all 0.2s ease',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.4rem'
                  }}
                >
                  💳 Pay Now (Sandbox Simulation)
                </button>
              )}
            </div>
          </div>
        ) : (
          <form onSubmit={handlePlaceOrder} className="modal-body" id="checkout-form">
            {error && (
              <div className="cart-error-banner">
                <p>{error}</p>
              </div>
            )}

            {/* Saved Address Selector */}
            {savedAddresses.length > 0 && (
              <div className="form-group" style={{ marginBottom: '1.25rem' }}>
                <label htmlFor="address-select-dropdown">Select Saved Shipping Address</label>
                <select
                  id="address-select-dropdown"
                  value={selectedAddressId}
                  onChange={(e) => handleSelectAddress(e.target.value)}
                  className="filter-select"
                  style={{ width: '100%', padding: '0.6rem' }}
                >
                  {savedAddresses.map((addr) => (
                    <option key={addr.id} value={addr.id}>
                      {addr.title || 'Address'} — {addr.street_address}, {addr.city} {addr.is_default ? '(Default)' : ''}
                    </option>
                  ))}
                  <option value="new">+ Enter New Address</option>
                </select>
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label htmlFor="shipping-full-name">Full Name *</label>
                <input
                  id="shipping-full-name"
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="John Doe"
                />
              </div>

              <div className="form-group">
                <label htmlFor="shipping-phone">Phone Number</label>
                <input
                  id="shipping-phone"
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+1-555-0199"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="shipping-street">Street Address *</label>
              <input
                id="shipping-street"
                type="text"
                required
                value={streetAddress}
                onChange={(e) => setStreetAddress(e.target.value)}
                placeholder="123 Main St, Apt 4B"
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label htmlFor="shipping-city">City *</label>
                <input
                  id="shipping-city"
                  type="text"
                  required
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="City"
                />
              </div>

              <div className="form-group">
                <label htmlFor="shipping-state">State / Province *</label>
                <input
                  id="shipping-state"
                  type="text"
                  required
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  placeholder="State"
                />
              </div>

              <div className="form-group">
                <label htmlFor="shipping-postal">Postal Code *</label>
                <input
                  id="shipping-postal"
                  type="text"
                  required
                  value={postalCode}
                  onChange={(e) => setPostalCode(e.target.value)}
                  placeholder="90210"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="shipping-country">Country *</label>
              <input
                id="shipping-country"
                type="text"
                required
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                placeholder="United States"
              />
            </div>

            {/* Order Items Preview */}
            <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
              <h4 style={{ margin: '0 0 0.75rem 0' }}>Order Summary ({cartItems.length} items)</h4>
              <div style={{ maxHeight: '140px', overflowY: 'auto', paddingRight: '0.5rem' }}>
                {cartItems.map((item) => (
                  <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', padding: '0.3rem 0', color: 'var(--color-text-muted, #94a3b8)' }}>
                    <span>{item.product_name} &times; {item.quantity}</span>
                    <span>₹{parseFloat(item.line_total).toLocaleString('en-IN')}</span>
                  </div>
                ))}
              </div>

              <div className="subtotal-row" style={{ marginTop: '0.75rem' }}>
                <span>Subtotal (Server Calculated):</span>
                <span className="subtotal-amount">₹{parseFloat(subtotal).toLocaleString('en-IN')}</span>
              </div>
            </div>

            <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
              <button className="btn-secondary" onClick={onClose} type="button" disabled={loading}>
                Cancel
              </button>
              <button
                id="submit-order-btn"
                className="btn-primary"
                type="submit"
                disabled={loading || cartItems.length === 0}
              >
                {loading ? 'Submitting Order...' : 'Place Order & Proceed'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
