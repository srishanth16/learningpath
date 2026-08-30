import { useState, useEffect } from 'react';
import { getUserSkills } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { BarChart3, TrendingUp, AlertTriangle, CheckCircle2, Target } from 'lucide-react';

export default function SkillsPage({ user }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getUserSkills(user.id)
      .then(res => setData(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user.id]);

  if (loading) return (
    <div className="p-6 flex items-center justify-center min-h-[60vh]">
      <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
    </div>
  );

  const d = data || {};
  const allSkills = [...(d.strong || []), ...(d.intermediate || []), ...(d.needs_improvement || []), ...(d.missing || [])];
  const barData = allSkills.map(s => ({ name: s.name, proficiency: s.proficiency }));
  const radarData = allSkills.slice(0, 10).map(s => ({ skill: s.name, value: s.proficiency, fullMark: 100 }));

  const classify = (prof) => {
    if (prof >= 70) return { label: 'Strong', color: 'text-emerald-600', bg: 'bg-emerald-50' };
    if (prof >= 40) return { label: 'Intermediate', color: 'text-amber-600', bg: 'bg-amber-50' };
    if (prof > 0) return { label: 'Needs Work', color: 'text-orange-600', bg: 'bg-orange-50' };
    return { label: 'Missing', color: 'text-red-500', bg: 'bg-red-50' };
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto animate-fade-in">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Skills Dashboard</h1>
      <p className="text-gray-500 mb-6">Track your skill development and identify gaps.</p>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-xl border border-gray-100 p-4">
          <CheckCircle2 className="w-5 h-5 text-emerald-500 mb-2" />
          <p className="text-2xl font-bold text-gray-800">{(d.strong || []).length}</p>
          <p className="text-sm text-gray-500">Strong Skills</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 p-4">
          <TrendingUp className="w-5 h-5 text-amber-500 mb-2" />
          <p className="text-2xl font-bold text-gray-800">{(d.intermediate || []).length}</p>
          <p className="text-sm text-gray-500">Intermediate</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 p-4">
          <AlertTriangle className="w-5 h-5 text-orange-500 mb-2" />
          <p className="text-2xl font-bold text-gray-800">{(d.needs_improvement || []).length}</p>
          <p className="text-sm text-gray-500">Needs Work</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 p-4">
          <Target className="w-5 h-5 text-red-500 mb-2" />
          <p className="text-2xl font-bold text-gray-800">{(d.missing || []).length}</p>
          <p className="text-sm text-gray-500">Missing</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Bar Chart */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-indigo-500" /> Skill Proficiency
          </h3>
          {barData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData} layout="vertical" margin={{ left: 80 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 12 }} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 12 }} width={75} />
                <Tooltip />
                <Bar dataKey="proficiency" fill="#6366f1" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-400 text-sm">No skill data yet</div>
          )}
        </div>

        {/* Radar */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Skills Overview</h3>
          {radarData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="skill" tick={{ fontSize: 11, fill: '#6b7280' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.2} />
              </RadarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-400 text-sm">No skill data yet</div>
          )}
        </div>
      </div>

      {/* Skill Cards */}
      <div className="bg-white rounded-2xl border border-gray-100 p-6">
        <h3 className="font-semibold text-gray-800 mb-4">All Required Skills</h3>
        <div className="space-y-3">
          {allSkills.map((skill, i) => {
            const cls = classify(skill.proficiency);
            return (
              <div key={i} className="flex items-center gap-4">
                <span className="w-28 text-sm font-medium text-gray-700">{skill.name}</span>
                <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all" style={{ width: `${skill.proficiency}%` }} />
                </div>
                <span className="w-12 text-sm text-gray-500 text-right">{skill.proficiency}%</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${cls.bg} ${cls.color} font-medium`}>{cls.label}</span>
              </div>
            );
          })}
          {allSkills.length === 0 && <p className="text-sm text-gray-400">Set a goal to see your required skills and gaps.</p>}
        </div>
      </div>

      {/* Priority Skills */}
      {(d.priority_skills || []).length > 0 && (
        <div className="bg-white rounded-2xl border border-gray-100 p-6 mt-6">
          <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-red-500" /> Priority Skills to Learn
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {d.priority_skills.map((skill, i) => (
              <div key={i} className="p-4 rounded-xl border border-gray-100 bg-red-50/30">
                <p className="font-medium text-gray-800">{skill.name}</p>
                <p className="text-sm text-gray-500 mt-1">
                  {skill.proficiency === 0 ? 'Not started — learn this next' : `${skill.proficiency}% — keep improving`}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
