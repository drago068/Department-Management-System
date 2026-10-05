/**
 * AuthContext
 * Global authentication state for the entire app.
 *
 * Provides:
 *  - user       : logged-in user profile (or null)
 *  - role       : 'STUDENT' | 'STAFF' | 'ADMIN' (or null)
 *  - isLoading  : true while restoring session from storage
 *  - signIn()   : called after successful login
 *  - signOut()  : clears session everywhere
 */

import React, { createContext, useContext, useEffect, useState } from 'react';
import { tokenStorage } from '../api/client';
import { logout as apiLogout } from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // ── Restore session on app launch ─────────────────────────────────────────
  useEffect(() => {
    (async () => {
      try {
        const { user: storedUser, refreshToken: storedRefresh } =
          await tokenStorage.getTokens();
        if (storedUser && storedRefresh) {
          setUser(storedUser);
          setRefreshToken(storedRefresh);
        }
      } catch (e) {
        // Corrupted storage — start fresh
        await tokenStorage.clearTokens();
      } finally {
        setIsLoading(false);
      }
    })();
  }, []);

  // ── signIn — called from login screens after API success ──────────────────
  const signIn = (tokenData) => {
    const { user: newUser, refresh_token } = tokenData;
    setUser(newUser);
    setRefreshToken(refresh_token);
  };

  // ── signOut ────────────────────────────────────────────────────────────────
  const signOut = async () => {
    await apiLogout(refreshToken);
    setUser(null);
    setRefreshToken(null);
  };

  const role = user?.role ?? null;

  return (
    <AuthContext.Provider value={{ user, role, isLoading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

/** Hook for consuming auth state in any screen */
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
