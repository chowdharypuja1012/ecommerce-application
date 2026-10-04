import type { Address, AddressInput, AuthResponse, Profile, User } from '../types/auth';

const BASE_URL = import.meta.env?.VITE_API_GATEWAY_URL || 'http://127.0.0.1:8000';
const TOKEN_KEY = 'nexus_auth_token';

export const authClient = {
  getToken(): string | null {
    if (typeof localStorage === 'undefined') return null;
    return localStorage.getItem(TOKEN_KEY);
  },

  setToken(token: string): void {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(TOKEN_KEY, token);
    }
  },

  clearToken(): void {
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem(TOKEN_KEY);
    }
  },

  getAuthHeaders(): HeadersInit {
    const token = this.getToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Token ${token}`;
    }
    return headers;
  },

  async register(payload: Record<string, any>): Promise<AuthResponse> {
    const url = `${BASE_URL}/api/v1/auth/register/`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      const errorMsg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Registration failed.';
      throw new Error(errorMsg || 'Registration failed.');
    }

    if (data.token) {
      this.setToken(data.token);
    }
    return data;
  },

  async login(payload: Record<string, any>): Promise<AuthResponse> {
    const url = `${BASE_URL}/api/v1/auth/login/`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      const errorMsg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Login failed.';
      throw new Error(errorMsg || 'Invalid username or password.');
    }

    if (data.token) {
      this.setToken(data.token);
    }
    return data;
  },

  async logout(): Promise<void> {
    const token = this.getToken();
    if (token) {
      try {
        await fetch(`${BASE_URL}/api/v1/auth/logout/`, {
          method: 'POST',
          headers: this.getAuthHeaders(),
        });
      } catch (err) {
        console.warn('Logout API failed:', err);
      }
    }
    this.clearToken();
  },

  async getCurrentUser(): Promise<{ user: User; profile: Profile } | null> {
    const token = this.getToken();
    if (!token) return null;

    try {
      const response = await fetch(`${BASE_URL}/api/v1/auth/me/`, {
        headers: this.getAuthHeaders(),
      });
      if (response.ok) {
        return await response.json();
      }
    } catch (err) {
      console.warn('Failed to fetch current user:', err);
    }
    return null;
  },

  async updateProfile(payload: { full_name?: string; phone_number?: string }): Promise<Profile> {
    const response = await fetch(`${BASE_URL}/api/v1/profile/`, {
      method: 'PATCH',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error('Failed to update profile.');
    }
    return await response.json();
  },

  async getAddresses(): Promise<Address[]> {
    const response = await fetch(`${BASE_URL}/api/v1/profile/addresses/`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch addresses.');
    }
    return await response.json();
  },

  async createAddress(payload: AddressInput): Promise<Address> {
    const response = await fetch(`${BASE_URL}/api/v1/profile/addresses/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error('Failed to create address.');
    }
    return await response.json();
  },

  async deleteAddress(id: number): Promise<void> {
    const response = await fetch(`${BASE_URL}/api/v1/profile/addresses/${id}/`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to delete address.');
    }
  },
};
