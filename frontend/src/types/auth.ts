export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Profile {
  id: number;
  user: User;
  full_name: string;
  phone_number: string;
  avatar_url: string;
  created_at?: string;
  updated_at?: string;
}

export interface Address {
  id: number;
  title: string;
  street_address: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_default: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface AuthResponse {
  message: string;
  token: string;
  user: User;
  profile: Profile;
}

export interface AddressInput {
  title?: string;
  street_address: string;
  city: string;
  state?: string;
  postal_code: string;
  country?: string;
  is_default?: boolean;
}
