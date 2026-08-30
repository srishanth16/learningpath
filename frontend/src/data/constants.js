export const INTERESTS = [
  'Artificial Intelligence', 'Machine Learning', 'Data Science',
  'Web Development', 'Mobile Development', 'Cloud Computing',
  'Cybersecurity', 'DevOps', 'UI/UX', 'Programming', 'Other'
];

export const EXPERIENCE_LEVELS = [
  { value: 'beginner', label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced', label: 'Advanced' },
];

export const LEARNING_PREFERENCES = [
  'Videos', 'Articles', 'Hands-on coding', 'Projects',
  'Quizzes', 'Reading', 'Interactive exercises'
];

export const WEEKLY_HOURS = [
  { value: 3, label: '2–5 hours' },
  { value: 7, label: '5–10 hours' },
  { value: 12, label: '10–15 hours' },
  { value: 18, label: '15+ hours' },
];

export const EXAMPLE_GOALS = [
  "I want to become a machine learning engineer within 6 months.",
  "I want to become a frontend developer.",
  "I want to transition into data science from a non-technical background.",
  "I want to become a full stack web developer.",
  "I want to learn AI and deep learning.",
  "I want to become a data analyst.",
];

export const DIFFICULTY_COLORS = {
  beginner: { bg: 'bg-emerald-100', text: 'text-emerald-700', border: 'border-emerald-200' },
  intermediate: { bg: 'bg-amber-100', text: 'text-amber-700', border: 'border-amber-200' },
  advanced: { bg: 'bg-rose-100', text: 'text-rose-700', border: 'border-rose-200' },
};

export const TYPE_COLORS = {
  course: { bg: 'bg-blue-100', text: 'text-blue-700' },
  video: { bg: 'bg-purple-100', text: 'text-purple-700' },
  article: { bg: 'bg-cyan-100', text: 'text-cyan-700' },
  tutorial: { bg: 'bg-indigo-100', text: 'text-indigo-700' },
  project: { bg: 'bg-orange-100', text: 'text-orange-700' },
  quiz: { bg: 'bg-pink-100', text: 'text-pink-700' },
  assessment: { bg: 'bg-pink-100', text: 'text-pink-700' },
};

export const STATUS_COLORS = {
  locked: { bg: 'bg-gray-100', text: 'text-gray-500', icon: '🔒' },
  available: { bg: 'bg-blue-50', text: 'text-blue-600', icon: '📘' },
  in_progress: { bg: 'bg-amber-50', text: 'text-amber-600', icon: '⏳' },
  completed: { bg: 'bg-emerald-50', text: 'text-emerald-600', icon: '✅' },
};
