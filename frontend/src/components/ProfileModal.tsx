import React, { useEffect, useState } from 'react';
import { authClient } from '../api/authClient';
import type { Address, Profile, User } from '../types/auth';

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: User;
  profile: Profile;
  onProfileUpdated: (updatedProfile: Profile) => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
  isOpen,
  onClose,
  user,
  profile,
  onProfileUpdated,
}) => {
  const [activeTab, setActiveTab] = useState<'profile' | 'addresses'>('profile');

  // Profile Form State
  const [fullName, setFullName] = useState(profile.full_name || '');
  const [phoneNumber, setPhoneNumber] = useState(profile.phone_number || '');
  const [savingProfile, setSavingProfile] = useState(false);
  const [profileMsg, setProfileMsg] = useState<string | null>(null);

  // Address State
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [loadingAddresses, setLoadingAddresses] = useState(false);
  const [showAddAddress, setShowAddAddress] = useState(false);

  // New Address Form State
  const [title, setTitle] = useState('Home');
  const [streetAddress, setStreetAddress] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [postalCode, setPostalCode] = useState('');
  const [country, setCountry] = useState('United States');
  const [isDefault, setIsDefault] = useState(false);
  const [creatingAddress, setCreatingAddress] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setFullName(profile.full_name || '');
      setPhoneNumber(profile.phone_number || '');
      fetchAddresses();
    }
  }, [isOpen, profile]);

  const fetchAddresses = async () => {
    setLoadingAddresses(true);
    try {
      const data = await authClient.getAddresses();
      setAddresses(data);
    } catch (err) {
      console.warn('Could not fetch addresses:', err);
    } finally {
      setLoadingAddresses(false);
    }
  };

  if (!isOpen) return null;

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingProfile(true);
    setProfileMsg(null);
    try {
      const updated = await authClient.updateProfile({
        full_name: fullName,
        phone_number: phoneNumber,
      });
      onProfileUpdated(updated);
      setProfileMsg('Profile updated successfully!');
    } catch {
      setProfileMsg('Failed to update profile.');
    } finally {
      setSavingProfile(false);
    }
  };

  const handleCreateAddress = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreatingAddress(true);
    try {
      await authClient.createAddress({
        title,
        street_address: streetAddress,
        city,
        state,
        postal_code: postalCode,
        country,
        is_default: isDefault,
      });
      setShowAddAddress(false);
      setStreetAddress('');
      setCity('');
      setState('');
      setPostalCode('');
      fetchAddresses();
    } catch {
      alert('Failed to save address.');
    } finally {
      setCreatingAddress(false);
    }
  };

  const handleDeleteAddress = async (id: number) => {
    if (!confirm('Are you sure you want to delete this address?')) return;
    try {
      await authClient.deleteAddress(id);
      fetchAddresses();
    } catch {
      alert('Failed to delete address.');
    }
  };

  return (
    <div className="modal-overlay" id="profile-modal-overlay" onClick={onClose}>
      <div className="modal-content profile-modal-content animate-fade-in" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="tab-buttons">
            <button
              id="tab-profile"
              type="button"
              className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              My Profile
            </button>
            <button
              id="tab-addresses"
              type="button"
              className={`tab-btn ${activeTab === 'addresses' ? 'active' : ''}`}
              onClick={() => setActiveTab('addresses')}
            >
              Addresses ({addresses.length})
            </button>
          </div>
          <button className="close-btn" id="close-profile-modal" onClick={onClose} aria-label="Close modal">
            &times;
          </button>
        </div>

        {activeTab === 'profile' ? (
          <form onSubmit={handleUpdateProfile} className="auth-form" id="profile-form">
            <div className="user-info-header">
              <div className="avatar-circle">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <div>
                <div className="user-username">@{user.username}</div>
                <div className="user-email">{user.email}</div>
              </div>
            </div>

            {profileMsg && <div className="profile-msg-banner">{profileMsg}</div>}

            <div className="form-group">
              <label htmlFor="profile-fullname">Full Name</label>
              <input
                id="profile-fullname"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="John Doe"
              />
            </div>

            <div className="form-group">
              <label htmlFor="profile-phone">Phone Number</label>
              <input
                id="profile-phone"
                type="text"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="+1 234 567 8900"
              />
            </div>

            <button id="save-profile-btn" type="submit" className="btn-primary" disabled={savingProfile}>
              {savingProfile ? 'Saving...' : 'Save Profile Changes'}
            </button>
          </form>
        ) : (
          <div className="address-tab-container">
            <div className="address-header-row">
              <h3>Saved Delivery Addresses</h3>
              {!showAddAddress && (
                <button
                  id="add-new-address-btn"
                  className="btn-secondary"
                  onClick={() => setShowAddAddress(true)}
                  type="button"
                >
                  + Add Address
                </button>
              )}
            </div>

            {showAddAddress && (
              <form onSubmit={handleCreateAddress} className="address-form animate-fade-in" id="add-address-form">
                <div className="form-row">
                  <div className="form-group">
                    <label>Title</label>
                    <input
                      type="text"
                      required
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      placeholder="Home / Work"
                    />
                  </div>
                  <div className="form-group">
                    <label>Country</label>
                    <input
                      type="text"
                      required
                      value={country}
                      onChange={(e) => setCountry(e.target.value)}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Street Address</label>
                  <input
                    type="text"
                    required
                    value={streetAddress}
                    onChange={(e) => setStreetAddress(e.target.value)}
                    placeholder="123 Main St, Apt 4B"
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>City</label>
                    <input
                      type="text"
                      required
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      placeholder="New York"
                    />
                  </div>
                  <div className="form-group">
                    <label>State</label>
                    <input
                      type="text"
                      value={state}
                      onChange={(e) => setState(e.target.value)}
                      placeholder="NY"
                    />
                  </div>
                  <div className="form-group">
                    <label>Postal Code</label>
                    <input
                      type="text"
                      required
                      value={postalCode}
                      onChange={(e) => setPostalCode(e.target.value)}
                      placeholder="10001"
                    />
                  </div>
                </div>

                <div className="form-checkbox">
                  <input
                    type="checkbox"
                    id="address-is-default"
                    checked={isDefault}
                    onChange={(e) => setIsDefault(e.target.checked)}
                  />
                  <label htmlFor="address-is-default">Set as default shipping address</label>
                </div>

                <div className="form-actions">
                  <button type="submit" className="btn-primary" disabled={creatingAddress}>
                    {creatingAddress ? 'Saving...' : 'Save Address'}
                  </button>
                  <button
                    type="button"
                    className="btn-cancel"
                    onClick={() => setShowAddAddress(false)}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}

            {loadingAddresses ? (
              <p>Loading addresses...</p>
            ) : addresses.length === 0 && !showAddAddress ? (
              <div className="no-address-box">
                <p>No addresses added yet.</p>
              </div>
            ) : (
              <div className="addresses-list">
                {addresses.map((addr) => (
                  <div key={addr.id} className="address-card" id={`address-card-${addr.id}`}>
                    <div className="address-card-header">
                      <span className="address-title-tag">{addr.title}</span>
                      {addr.is_default && <span className="default-badge">DEFAULT</span>}
                    </div>
                    <div className="address-body">
                      <p>{addr.street_address}</p>
                      <p>{addr.city}{addr.state ? `, ${addr.state}` : ''} {addr.postal_code}</p>
                      <p>{addr.country}</p>
                    </div>
                    <div className="address-card-actions">
                      <button
                        className="btn-delete-addr"
                        onClick={() => handleDeleteAddress(addr.id)}
                        type="button"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
