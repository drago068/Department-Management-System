/**
 * Profile API
 */
import { api } from './client';

/**
 * Get the logged-in user's own profile.
 */
export const getMyProfile = () => api.get('/profiles/me');

/**
 * Update the logged-in user's profile.
 */
export const updateMyProfile = (body) => api.patch('/profiles/me', body);

/**
 * Admin: get any user's profile by ID.
 */
export const getUserProfile = (userId) => api.get(`/profiles/${userId}`);
