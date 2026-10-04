import { authClient } from './authClient';

export async function runAuthClientTests(): Promise<void> {
  console.log('Running authClient unit tests...');

  const originalFetch = globalThis.fetch;
  const originalLocalStorage = globalThis.localStorage;

  // Mock localStorage
  const mockStorage: Record<string, string> = {};
  const fakeLocalStorage = {
    getItem: (key: string) => mockStorage[key] || null,
    setItem: (key: string, val: string) => { mockStorage[key] = val; },
    removeItem: (key: string) => { delete mockStorage[key]; },
    clear: () => { Object.keys(mockStorage).forEach(k => delete mockStorage[k]); },
  };

  (globalThis as any).localStorage = fakeLocalStorage;

  try {
    // Test 1: login saves token
    globalThis.fetch = (async () => {
      return new Response(
        JSON.stringify({
          token: 'test-token-123',
          user: { id: 1, username: 'testuser', email: 'test@example.com' },
          profile: { id: 1, full_name: 'Test User' },
        }),
        { status: 200 }
      );
    }) as typeof fetch;

    const authResp = await authClient.login({ username: 'testuser', password: 'Password123!' });
    if (authResp.token !== 'test-token-123') {
      throw new Error('Login token mismatch!');
    }
    if (authClient.getToken() !== 'test-token-123') {
      throw new Error('Token was not saved to localStorage!');
    }
    console.log('✓ login and token storage test passed');

    // Test 2: auth headers include Token
    const headers = authClient.getAuthHeaders() as Record<string, string>;
    if (headers['Authorization'] !== 'Token test-token-123') {
      throw new Error(`Auth header mismatch: ${headers['Authorization']}`);
    }
    console.log('✓ getAuthHeaders test passed');

    // Test 3: logout clears token
    globalThis.fetch = (async () => {
      return new Response(JSON.stringify({ message: 'Logged out' }), { status: 200 });
    }) as typeof fetch;

    await authClient.logout();
    if (authClient.getToken() !== null) {
      throw new Error('Logout failed to clear token from localStorage!');
    }
    console.log('✓ logout clears token test passed');

    console.log('All authClient tests passed successfully!');
  } finally {
    globalThis.fetch = originalFetch;
    Object.defineProperty(globalThis, 'localStorage', {
      value: originalLocalStorage,
      writable: true,
    });
  }
}

// Execute test suite when loaded via node/tsx
const globalProcess = (globalThis as any).process;
if (typeof globalProcess !== 'undefined' && globalProcess.argv?.[1]?.includes('authClient.test')) {
  runAuthClientTests().catch((err) => {
    console.error('Test run failed:', err);
    globalProcess.exit(1);
  });
}
