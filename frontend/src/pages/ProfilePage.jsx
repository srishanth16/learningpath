import { useState, useEffect } from 'react';
import { getProfile, analyzeGoal } from '../services/api';
import { User, Mail, GraduationCap, Briefcase, Target, Clock, Heart, Wrench, Sparkles, Loader2 } from 'lucide-react';

export default function ProfilePage({ user, setUser }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    getProfile(user.id)
      .then(res => setProfile(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user.id]);

  const handleAnalyze = async () => {
    const activeGoal = profile?.goals?.find(g => g.is_active);
    if (!activeGoal) return alert('No active goal found');

    setAnalyzing(true);
    try {
      const res = await analyzeGoal({ user_id: user.id, goal_text: activeGoal.goal_text });
      setAnalysis(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) return (
    <div className="p-6 flex items-center justify-center min-h-[60vh]">
      <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
    </div>
  );

  const p = profile || user;
  const activeGoal = p.goals?.find(g => g.is_active);

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-4xl mx-auto animate-fade-in">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Profile</h1>

      {/* Profile Card */}
      <div className="bg-white rounded-2xl border border-gray-100 p-6 mb-6">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white text-2xl font-bold">
            {p.name?.[0] || 'U'}
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-800">{p.name}</h2>
            <p className="text-gray-500">{p.email}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <InfoRow icon={GraduationCap} label="Education" value={p.education || 'Not set'} />
          <InfoRow icon={Briefcase} label="Current Role" value={p.current_role || 'Not set'} />
          <InfoRow icon={Target} label="Experience" value={(p.experience_level || 'beginner').charAt(0).toUpperCase() + (p.experience_level || 'beginner').slice(1)} />
          <InfoRow icon={Clock} label="Weekly Hours" value={`${p.weekly_hours || 0} hours/week`} />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
        {/* Interests */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <Heart className="w-5 h-5 text-pink-500" /> Interests
          </h3>
          <div className="flex flex-wrap gap-2">
            {(p.interests || []).map((interest, i) => (
              <span key={i} className="px-3 py-1 bg-pink-50 text-pink-700 rounded-full text-sm">{interest}</span>
            ))}
            {(p.interests || []).length === 0 && <span className="text-sm text-gray-400">No interests set</span>}
          </div>
        </div>

        {/* Preferences */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <Wrench className="w-5 h-5 text-indigo-500" /> Learning Preferences
          </h3>
          <div className="flex flex-wrap gap-2">
            {(p.learning_preferences || []).map((pref, i) => (
              <span key={i} className="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-sm">{pref}</span>
            ))}
            {(p.learning_preferences || []).length === 0 && <span className="text-sm text-gray-400">No preferences set</span>}
          </div>
        </div>
      </div>

      {/* Skills */}
      <div className="bg-white rounded-2xl border border-gray-100 p-6 mb-6">
        <h3 className="font-semibold text-gray-800 mb-4">Current Skills</h3>
        {(p.skills || []).length > 0 ? (
          <div className="space-y-3">
            {p.skills.map((skill, i) => (
              <div key={i} className="flex items-center gap-4">
                <span className="w-24 text-sm font-medium text-gray-700">{skill.name}</span>
                <div className="flex-1 h-2.5 bg-gray-100 rounded-full">
                  <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${skill.proficiency}%` }} />
                </div>
                <span className="text-sm text-gray-500 w-12 text-right">{skill.proficiency}%</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-400">No skills added yet.</p>
        )}
      </div>

      {/* Goal & Analysis */}
      {activeGoal && (
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-500" /> Active Goal
          </h3>
          <p className="text-gray-700 mb-2">"{activeGoal.goal_text}"</p>
          {activeGoal.target_role && (
            <p className="text-sm text-gray-500 mb-4">Target: {activeGoal.target_role}</p>
          )}
          <button onClick={handleAnalyze} disabled={analyzing} className="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-lg text-sm font-medium hover:bg-indigo-100 transition disabled:opacity-50 flex items-center gap-2">
            {analyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
            {analyzing ? 'Analyzing...' : 'Analyze Goal'}
          </button>

          {analysis && (
            <div className="mt-6 space-y-4 border-t border-gray-100 pt-4">
              <div>
                <h4 className="font-medium text-gray-800 mb-1">Target Role</h4>
                <p className="text-indigo-600 font-semibold">{analysis.target_role}</p>
              </div>
              <div>
                <h4 className="font-medium text-gray-800 mb-1">Difficulty Assessment</h4>
                <p className="text-sm text-gray-600">{analysis.estimated_difficulty}</p>
              </div>
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Required Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {(analysis.required_skills || []).map((s, i) => (
                    <span key={i} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">{s}</span>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Skill Gaps</h4>
                <div className="flex flex-wrap gap-2">
                  {(analysis.skill_gaps || []).map((s, i) => (
                    <span key={i} className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm">{s}</span>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Suggested Sequence</h4>
                <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                  {(analysis.suggested_sequence || []).map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ol>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function InfoRow({ icon: Icon, label, value }) {
  return (
    <div className="flex items-center gap-3">
      <Icon className="w-5 h-5 text-gray-400" />
      <div>
        <p className="text-xs text-gray-400">{label}</p>
        <p className="text-sm font-medium text-gray-700">{value}</p>
      </div>
    </div>
  );
}
