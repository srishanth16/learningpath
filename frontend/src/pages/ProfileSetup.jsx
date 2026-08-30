import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createProfile, getAllSkills } from '../services/api';
import { INTERESTS, EXPERIENCE_LEVELS, LEARNING_PREFERENCES, WEEKLY_HOURS, EXAMPLE_GOALS } from '../data/constants';
import { GraduationCap, ArrowRight, ArrowLeft, Lightbulb } from 'lucide-react';

export default function ProfileSetup({ setUser }) {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [availableSkills, setAvailableSkills] = useState([]);
  const [form, setForm] = useState({
    name: '', email: '', education: '', current_role: '',
    experience_level: 'beginner', interests: [], skills: [],
    learning_preferences: [], weekly_hours: 7, goal: '',
  });

  useEffect(() => {
    getAllSkills().then(res => setAvailableSkills(res.data)).catch(() => {});
  }, []);

  const updateForm = (key, value) => setForm(prev => ({ ...prev, [key]: value }));

  const toggleArray = (key, value) => {
    setForm(prev => ({
      ...prev,
      [key]: prev[key].includes(value) ? prev[key].filter(v => v !== value) : [...prev[key], value],
    }));
  };

  const toggleSkill = (skillName) => {
    setForm(prev => {
      const exists = prev.skills.find(s => s.name === skillName);
      if (exists) return { ...prev, skills: prev.skills.filter(s => s.name !== skillName) };
      return { ...prev, skills: [...prev.skills, { name: skillName, proficiency: 25 }] };
    });
  };

  const updateSkillProficiency = (skillName, proficiency) => {
    setForm(prev => ({
      ...prev,
      skills: prev.skills.map(s => s.name === skillName ? { ...s, proficiency } : s),
    }));
  };

  const handleSubmit = async () => {
    if (!form.name.trim() || !form.email.trim()) {
      setError('Name and email are required.');
      setStep(1);
      return;
    }
    if (!form.goal.trim()) {
      setError('Please enter your learning goal.');
      setStep(4);
      return;
    }

    setLoading(true);
    setError('');
    try {
      const res = await createProfile(form);
      setUser(res.data);
      navigate('/app/dashboard');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to create profile. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const canNext = () => {
    if (step === 1) return form.name.trim() && form.email.trim();
    if (step === 2) return form.interests.length > 0;
    if (step === 3) return true;
    if (step === 4) return form.goal.trim();
    return true;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-indigo-50/30 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-2xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <span className="font-bold text-xl text-gray-800">LearnPath AI</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-1">Set up your learning profile</h2>
          <p className="text-gray-500">Step {step} of 4</p>
          {/* Progress bar */}
          <div className="mt-4 h-1.5 bg-gray-200 rounded-full max-w-xs mx-auto">
            <div className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-300" style={{ width: `${(step / 4) * 100}%` }} />
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">{error}</div>
        )}

        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 sm:p-8 animate-fade-in">
          {/* Step 1: Basic Info */}
          {step === 1 && (
            <div className="space-y-5">
              <h3 className="text-lg font-semibold text-gray-800 mb-1">Basic Information</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                <input type="text" value={form.name} onChange={e => updateForm('name', e.target.value)} placeholder="Your name" className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                <input type="email" value={form.email} onChange={e => updateForm('email', e.target.value)} placeholder="you@example.com" className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Education</label>
                <input type="text" value={form.education} onChange={e => updateForm('education', e.target.value)} placeholder="e.g. Bachelor's in Computer Science" className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Current Role</label>
                <input type="text" value={form.current_role} onChange={e => updateForm('current_role', e.target.value)} placeholder="e.g. Student, Junior Developer" className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Experience Level</label>
                <div className="flex gap-3">
                  {EXPERIENCE_LEVELS.map(lvl => (
                    <button key={lvl.value} onClick={() => updateForm('experience_level', lvl.value)} className={`flex-1 py-2.5 rounded-lg border text-sm font-medium transition ${form.experience_level === lvl.value ? 'bg-indigo-50 border-indigo-300 text-indigo-700' : 'border-gray-200 text-gray-600 hover:border-gray-300'}`}>
                      {lvl.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Interests & Preferences */}
          {step === 2 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-1">Interests</h3>
                <p className="text-sm text-gray-500 mb-3">Select topics that interest you.</p>
                <div className="flex flex-wrap gap-2">
                  {INTERESTS.map(interest => (
                    <button key={interest} onClick={() => toggleArray('interests', interest)} className={`px-4 py-2 rounded-full text-sm font-medium transition ${form.interests.includes(interest) ? 'bg-indigo-100 text-indigo-700 border border-indigo-200' : 'bg-gray-50 text-gray-600 border border-gray-200 hover:border-gray-300'}`}>
                      {interest}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-1">Learning Preferences</h3>
                <p className="text-sm text-gray-500 mb-3">How do you prefer to learn?</p>
                <div className="flex flex-wrap gap-2">
                  {LEARNING_PREFERENCES.map(pref => (
                    <button key={pref} onClick={() => toggleArray('learning_preferences', pref)} className={`px-4 py-2 rounded-full text-sm font-medium transition ${form.learning_preferences.includes(pref) ? 'bg-purple-100 text-purple-700 border border-purple-200' : 'bg-gray-50 text-gray-600 border border-gray-200 hover:border-gray-300'}`}>
                      {pref}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-1">Weekly Learning Time</h3>
                <div className="flex flex-wrap gap-3">
                  {WEEKLY_HOURS.map(wh => (
                    <button key={wh.value} onClick={() => updateForm('weekly_hours', wh.value)} className={`px-4 py-2.5 rounded-lg border text-sm font-medium transition ${form.weekly_hours === wh.value ? 'bg-emerald-50 border-emerald-300 text-emerald-700' : 'border-gray-200 text-gray-600 hover:border-gray-300'}`}>
                      {wh.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Skills */}
          {step === 3 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-1">Current Skills</h3>
              <p className="text-sm text-gray-500 mb-3">Select skills you already know and rate your proficiency.</p>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-4">
                {availableSkills.map(skill => (
                  <button key={skill.name} onClick={() => toggleSkill(skill.name)} className={`px-3 py-2 rounded-lg text-sm font-medium transition text-left ${form.skills.find(s => s.name === skill.name) ? 'bg-indigo-50 border-indigo-300 text-indigo-700 border' : 'bg-gray-50 text-gray-600 border border-gray-200 hover:border-gray-300'}`}>
                    {skill.name}
                  </button>
                ))}
              </div>
              {form.skills.length > 0 && (
                <div className="space-y-3 pt-4 border-t border-gray-100">
                  <p className="text-sm font-medium text-gray-700">Set proficiency level:</p>
                  {form.skills.map(skill => (
                    <div key={skill.name} className="flex items-center gap-4">
                      <span className="w-24 text-sm text-gray-700 font-medium">{skill.name}</span>
                      <input type="range" min="5" max="100" value={skill.proficiency} onChange={e => updateSkillProficiency(skill.name, parseInt(e.target.value))} className="flex-1 accent-indigo-600" />
                      <span className="w-12 text-sm text-gray-500 text-right">{skill.proficiency}%</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Step 4: Goal */}
          {step === 4 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-1">Your Learning Goal</h3>
              <p className="text-sm text-gray-500 mb-3">What do you want to achieve?</p>
              <textarea
                value={form.goal}
                onChange={e => updateForm('goal', e.target.value)}
                placeholder="e.g. I want to become a machine learning engineer within 6 months."
                rows={4}
                className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition resize-none text-sm"
              />
              <div>
                <p className="text-sm text-gray-500 mb-2 flex items-center gap-1"><Lightbulb className="w-4 h-4" /> Example goals:</p>
                <div className="space-y-1.5">
                  {EXAMPLE_GOALS.map((goal, i) => (
                    <button key={i} onClick={() => updateForm('goal', goal)} className="w-full text-left px-3 py-2 bg-gray-50 hover:bg-indigo-50 rounded-lg text-sm text-gray-600 hover:text-indigo-700 transition">
                      {goal}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Navigation */}
          <div className="flex justify-between mt-8 pt-6 border-t border-gray-100">
            <button
              onClick={() => step > 1 ? setStep(step - 1) : navigate('/')}
              className="flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-gray-600 hover:text-gray-800 transition"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            {step < 4 ? (
              <button
                onClick={() => setStep(step + 1)}
                disabled={!canNext()}
                className="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Next <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={loading || !canNext()}
                className="flex items-center gap-2 px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg text-sm font-medium hover:shadow-lg transition disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {loading ? 'Creating...' : 'Create My Learning Path'}
                {!loading && <ArrowRight className="w-4 h-4" />}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
