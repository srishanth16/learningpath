import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// ── Profile ──────────────────────────────────────────
export const createProfile = (data) => api.post('/profile', data);
export const getProfile = (userId) => api.get(`/profile/${userId}`);
export const getDemoProfile = () => api.get('/profile/demo/load');
export const updateProfile = (userId, data) => api.put(`/profile/${userId}`, data);

// ── Goals ────────────────────────────────────────────
export const createGoal = (data) => api.post('/goals', data);
export const getGoals = (userId) => api.get(`/goals/${userId}`);
export const analyzeGoal = (data) => api.post('/analyze-goal', data);

// ── Skills ───────────────────────────────────────────
export const getAllSkills = () => api.get('/skills');
export const getUserSkills = (userId) => api.get(`/skills/user/${userId}`);
export const updateUserSkills = (userId, skills) => api.put(`/skills/user/${userId}`, skills);

// ── Resources ────────────────────────────────────────
export const getResources = (params = {}) => api.get('/resources', { params });
export const getResource = (id) => api.get(`/resources/${id}`);

// ── Learning Path ────────────────────────────────────
export const generateLearningPath = (userId) => api.post('/learning-path/generate', { user_id: userId });
export const getLearningPath = (userId) => api.get(`/learning-path/${userId}`);
export const updatePathItem = (itemId, status) => api.put(`/learning-path/items/${itemId}`, { status });

// ── Progress ─────────────────────────────────────────
export const updateProgress = (data) => api.post('/progress', data);
export const getProgress = (userId) => api.get(`/progress/${userId}`);
export const getDashboard = (userId) => api.get(`/dashboard/${userId}`);

// ── Assessments ──────────────────────────────────────
export const getAssessments = () => api.get('/assessments');
export const getAssessment = (id) => api.get(`/assessments/${id}`);
export const submitAssessment = (data) => api.post('/assessments/submit', data);
export const getAssessmentResults = (userId) => api.get(`/assessments/results/${userId}`);

// ── Feedback ─────────────────────────────────────────
export const submitFeedback = (data) => api.post('/feedback', data);
export const getFeedback = (userId) => api.get(`/feedback/${userId}`);

// ── Chat ─────────────────────────────────────────────
export const sendChatMessage = (data) => api.post('/chat', data);
export const getChatHistory = (userId) => api.get(`/chat/${userId}`);

export default api;
