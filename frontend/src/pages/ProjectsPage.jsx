import { useState, useEffect } from 'react';
import { getResources } from '../services/api';
import { DIFFICULTY_COLORS } from '../data/constants';
import { FolderKanban, Clock, Wrench, BarChart3 } from 'lucide-react';

export default function ProjectsPage({ user }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getResources({ type: 'project' })
      .then(res => setProjects(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="p-6 flex items-center justify-center min-h-[60vh]">
      <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto animate-fade-in">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Projects</h1>
      <p className="text-gray-500 mb-6">Build real-world projects to apply and solidify your skills.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {projects.map(p => {
          const diffColors = DIFFICULTY_COLORS[p.difficulty] || {};
          return (
            <div key={p.id} className="bg-white rounded-2xl border border-gray-100 p-6 hover:border-indigo-100 hover:shadow-md transition">
              <div className="flex items-start justify-between mb-3">
                <div className="w-10 h-10 rounded-xl bg-orange-50 flex items-center justify-center">
                  <FolderKanban className="w-5 h-5 text-orange-600" />
                </div>
                <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${diffColors.bg} ${diffColors.text}`}>{p.difficulty}</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">{p.title}</h3>
              <p className="text-sm text-gray-500 mb-4 leading-relaxed">{p.description}</p>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2 text-gray-500">
                  <Wrench className="w-4 h-4 text-gray-400" />
                  <span>Skills: {p.skill}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-500">
                  <Clock className="w-4 h-4 text-gray-400" />
                  <span>~{p.estimated_hours} hours</span>
                </div>
                <div className="flex items-center gap-2 text-gray-500">
                  <BarChart3 className="w-4 h-4 text-gray-400" />
                  <span>Rating: ★ {p.rating}</span>
                </div>
              </div>
              {p.prerequisites?.length > 0 && (
                <div className="mt-4 pt-3 border-t border-gray-100">
                  <p className="text-xs text-gray-400 mb-1">Prerequisites:</p>
                  <div className="flex flex-wrap gap-1">
                    {p.prerequisites.map((pr, i) => (
                      <span key={i} className="text-xs bg-gray-50 text-gray-600 px-2 py-0.5 rounded">{pr}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {projects.length === 0 && (
        <div className="text-center py-16 text-gray-400">
          <FolderKanban className="w-12 h-12 mx-auto mb-3" />
          <p>No projects available yet.</p>
        </div>
      )}
    </div>
  );
}
