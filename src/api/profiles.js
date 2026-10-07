/**
 * Profile API
 */
import { api, BASE_URL } from './client';

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

/**
 * Admin: get cohort options (departments, batches, sections, mentors).
 */
export const getCohortOptions = () => api.get('/profiles/cohort-options');

/**
 * Admin: enroll a single student with predefined credentials.
 */
export const enrollStudent = (body) => api.post('/profiles/students', body);

/**
 * Admin: bulk enroll students with predefined credentials.
 */
export const bulkEnrollStudents = (body) => api.post('/profiles/students/bulk', body);

/**
 * Admin: get template download URL for student bulk enrollment.
 */
export const getStudentTemplateUrl = () => {
  return `${BASE_URL}/profiles/students/template`;
};


