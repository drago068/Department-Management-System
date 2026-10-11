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

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { tokenStorage } from '../../../services/api/client';
import { logout as apiLogout } from '../../../services/api/auth';
import { getMyProfile } from '../../../services/api/profiles';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // ── Fetch fresh full profile from backend ───────────────────────────────────
  const fetchProfile = useCallback(async () => {
    try {
      const data = await getMyProfile();
      if (data) {
        setProfile(data);
        return data;
      }
    } catch {
      // Backend offline or error; profile fallback
    }
    return null;
  }, []);

  // ── Restore session on app launch ─────────────────────────────────────────
  useEffect(() => {
    (async () => {
      try {
        const { user: storedUser, refreshToken: storedRefresh } =
          await tokenStorage.getTokens();
        if (storedUser && storedRefresh) {
          setUser(storedUser);
          setRefreshToken(storedRefresh);
          // Load full profile
          try {
            const prof = await getMyProfile();
            if (prof) setProfile(prof);
          } catch {}
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
  const signIn = async (tokenData) => {
    const { user: newUser, refresh_token } = tokenData;
    setUser(newUser);
    setRefreshToken(refresh_token);
    // Fetch full profile immediately
    try {
      const prof = await getMyProfile();
      if (prof) setProfile(prof);
    } catch {}
  };

  // ── signOut ────────────────────────────────────────────────────────────────
  const signOut = async () => {
    await apiLogout(refreshToken);
    setUser(null);
    setProfile(null);
    setRefreshToken(null);
  };

  const updateProfileState = (newProfile) => {
    setProfile((prev) => ({ ...(prev || {}), ...newProfile }));
  };

  const role = user?.role ?? profile?.role ?? null;

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        role,
        isLoading,
        signIn,
        signOut,
        refreshProfile: fetchProfile,
        updateProfile: updateProfileState,
      }}
    >
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

