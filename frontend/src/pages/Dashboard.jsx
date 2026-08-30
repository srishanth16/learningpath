import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getDashboard, generateLearningPath } from '../services/api';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';
import { Target, Flame, Clock, BookOpen, ArrowRight, Trophy, Sparkles, Route } from 'lucide-react';

export default function Dashboard({ user }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const fetchDashboard = () => {
    setLoading(true);
    getDashboard(user.id)
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchDashboard(); }, [user.id]);

  const handleGeneratePath = async () => {
    setGenerating(true);
    try {
      await generateLearningPath(user.id);
      fetchDashboard();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to generate path');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return (
    <div className="p-6 flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-3" />
        <p className="text-gray-500">Loading dashboard...</p>
      </div>
    </div>
  );

  const d = data || {};
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
  const radarData = (d.skills_developed || []).slice(0, 8).map(s => ({ skill: s.name, value: s.proficiency, fullMark: 100 }));

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto animate-fade-in">
      {/* Welcome */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">{greeting}, {d.user_name || user.name} 👋</h1>
        {d.current_goal && <p className="text-gray-500 mt-1">Goal: {d.current_goal}</p>}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard icon={Target} label="Progress" value={`${d.overall_progress || 0}%`} color="indigo" sub={`${d.completed_resources || 0}/${d.total_resources || 0} resources`} />
        <StatCard icon={Flame} label="Streak" value={`${d.learning_streak || 0} days`} color="orange" sub="Keep it up!" />
        <StatCard icon={Clock} label="Hours Learned" value={`${d.hours_learned || 0}h`} color="emerald" sub="Total study time" />
        <StatCard icon={BookOpen} label="Completed" value={d.completed_resources || 0} color="purple" sub="Resources finished" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Progress Ring */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Overall Progress</h3>
          <div className="flex items-center justify-center">
            <div className="relative w-40 h-40">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none" stroke="#e5e7eb" strokeWidth="10" />
                <circle cx="60" cy="60" r="50" fill="none" stroke="url(#gradient)" strokeWidth="10" strokeLinecap="round" strokeDasharray={`${(d.overall_progress || 0) * 3.14} 314`} />
                <defs><linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stopColor="#6366f1" /><stop offset="100%" stopColor="#a855f7" /></linearGradient></defs>
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl font-bold text-gray-800">{d.overall_progress || 0}%</span>
              </div>
            </div>
          </div>
          {d.current_milestone && (
            <p className="text-center text-sm text-gray-500 mt-3">
              <Trophy className="w-4 h-4 inline-block text-amber-500 mr-1" />
              Current: {d.current_milestone}
            </p>
          )}
        </div>

        {/* Skills Radar */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Skills Overview</h3>
          {radarData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="skill" tick={{ fontSize: 11, fill: '#6b7280' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.2} />
              </RadarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[200px] flex items-center justify-center text-gray-400 text-sm">
              Complete resources to see your skills
            </div>
          )}
          <button onClick={() => navigate('/app/skills')} className="w-full mt-3 text-sm text-indigo-600 hover:text-indigo-700 font-medium">
            View all skills →
          </button>
        </div>

        {/* Next Action */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Next Action</h3>
          {d.next_action ? (
            <div className="space-y-3">
              <div className="p-4 bg-indigo-50 rounded-xl">
                <p className="font-medium text-indigo-900 mb-1">{d.next_action.title}</p>
                <p className="text-sm text-indigo-600">
                  {d.next_action.type} · ~{d.next_action.estimated_hours}h · {d.next_action.skill}
                </p>
              </div>
              <button onClick={() => navigate('/app/learning-path')} className="w-full flex items-center justify-center gap-2 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition">
                Continue Learning <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="p-4 bg-gray-50 rounded-xl text-center">
                <Route className="w-8 h-8 mx-auto text-gray-300 mb-2" />
                <p className="text-sm text-gray-500">No learning path yet</p>
              </div>
              <button onClick={handleGeneratePath} disabled={generating} className="w-full flex items-center justify-center gap-2 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg text-sm font-medium hover:shadow-lg transition disabled:opacity-50">
                {generating ? 'Generating...' : 'Generate Learning Path'}
                {!generating && <Sparkles className="w-4 h-4" />}
              </button>
            </div>
          )}
          {d.upcoming_milestone && (
            <p className="text-sm text-gray-500 mt-4">
              <Trophy className="w-4 h-4 inline-block text-amber-500 mr-1" />
              Next milestone: {d.upcoming_milestone}
            </p>
          )}
        </div>
      </div>

      {/* Recommendations & Projects */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Recommendations */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-500" /> Recommended for You
          </h3>
          {(d.recommendations || []).length > 0 ? (
            <div className="space-y-3">
              {d.recommendations.slice(0, 4).map((rec, i) => (
                <div key={i} className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition">
                  <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-1 rounded">{rec.type}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-800 truncate">{rec.title}</p>
                    <p className="text-xs text-gray-500">{rec.skill} · {rec.difficulty} · ~{rec.estimated_hours}h</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-400">Set a goal and generate your path to see recommendations.</p>
          )}
        </div>

        {/* Projects */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-amber-500" /> Recommended Projects
          </h3>
          {(d.recommended_projects || []).length > 0 ? (
            <div className="space-y-3">
              {d.recommended_projects.map((p, i) => (
                <div key={i} className="p-3 rounded-lg border border-gray-100 hover:border-indigo-100 transition">
                  <p className="text-sm font-medium text-gray-800">{p.title}</p>
                  <p className="text-xs text-gray-500 mt-1">{p.description?.slice(0, 80)}...</p>
                  <div className="flex gap-2 mt-2">
                    <span className="text-xs bg-amber-50 text-amber-700 px-2 py-0.5 rounded">{p.difficulty}</span>
                    <span className="text-xs bg-gray-50 text-gray-600 px-2 py-0.5 rounded">~{p.estimated_hours}h</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-400">Projects will appear after generating your learning path.</p>
          )}
          <button onClick={() => navigate('/app/projects')} className="w-full mt-4 text-sm text-indigo-600 hover:text-indigo-700 font-medium">
            View all projects →
          </button>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color, sub }) {
  const colors = {
    indigo: 'bg-indigo-50 text-indigo-600',
    orange: 'bg-orange-50 text-orange-600',
    emerald: 'bg-emerald-50 text-emerald-600',
    purple: 'bg-purple-50 text-purple-600',
  };
  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-4 sm:p-5">
      <div className={`w-10 h-10 rounded-xl ${colors[color]} flex items-center justify-center mb-3`}>
        <Icon className="w-5 h-5" />
      </div>
      <p className="text-2xl font-bold text-gray-800">{value}</p>
      <p className="text-sm text-gray-500">{label}</p>
      {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
    </div>
  );
}
