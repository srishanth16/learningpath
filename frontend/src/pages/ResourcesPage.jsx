import { useState, useEffect } from 'react';
import { getResources } from '../services/api';
import { DIFFICULTY_COLORS, TYPE_COLORS } from '../data/constants';
import { Search, Filter, Star, Clock, ExternalLink } from 'lucide-react';

export default function ResourcesPage({ user }) {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterDiff, setFilterDiff] = useState('');

  useEffect(() => {
    getResources()
      .then(res => setResources(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = resources.filter(r => {
    if (search && !r.title.toLowerCase().includes(search.toLowerCase()) && !r.skill.toLowerCase().includes(search.toLowerCase())) return false;
    if (filterType && r.type !== filterType) return false;
    if (filterDiff && r.difficulty !== filterDiff) return false;
    return true;
  });

  const types = [...new Set(resources.map(r => r.type))];
  const difficulties = [...new Set(resources.map(r => r.difficulty))];

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto animate-fade-in">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Learning Resources</h1>
      <p className="text-gray-500 mb-6">Browse all available courses, tutorials, projects, and more.</p>

      {/* Filters */}
      <div className="bg-white rounded-2xl border border-gray-100 p-4 mb-6 flex flex-wrap gap-3 items-center">
        <div className="flex-1 min-w-[200px] relative">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search resources..." className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none" />
        </div>
        <select value={filterType} onChange={e => setFilterType(e.target.value)} className="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 focus:ring-2 focus:ring-indigo-500 outline-none">
          <option value="">All Types</option>
          {types.map(t => <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>)}
        </select>
        <select value={filterDiff} onChange={e => setFilterDiff(e.target.value)} className="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 focus:ring-2 focus:ring-indigo-500 outline-none">
          <option value="">All Levels</option>
          {difficulties.map(d => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
        </select>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
        </div>
      ) : (
        <>
          <p className="text-sm text-gray-500 mb-4">{filtered.length} resources found</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map(r => {
              const diffColors = DIFFICULTY_COLORS[r.difficulty] || {};
              const typeColors = TYPE_COLORS[r.type] || {};
              return (
                <div key={r.id} className="bg-white rounded-xl border border-gray-100 p-5 hover:border-indigo-100 hover:shadow-sm transition group">
                  <div className="flex items-center gap-2 mb-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${typeColors.bg} ${typeColors.text}`}>{r.type}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${diffColors.bg} ${diffColors.text}`}>{r.difficulty}</span>
                  </div>
                  <h3 className="font-semibold text-gray-800 mb-1 group-hover:text-indigo-600 transition">{r.title}</h3>
                  <p className="text-sm text-gray-500 line-clamp-2 mb-3">{r.description}</p>
                  <div className="flex items-center gap-3 text-xs text-gray-400">
                    <span className="flex items-center gap-1"><Star className="w-3 h-3 text-amber-400" /> {r.rating}</span>
                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {r.estimated_hours}h</span>
                    <span>{r.skill}</span>
                  </div>
                  {r.prerequisites?.length > 0 && (
                    <p className="text-xs text-gray-400 mt-2">Requires: {r.prerequisites.join(', ')}</p>
                  )}
                  {r.url && (
                    <a href={r.url} target="_blank" rel="noopener noreferrer" className="mt-3 inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-700 font-medium">
                      <ExternalLink className="w-3 h-3" /> Open Resource
                    </a>
                  )}
                </div>
              );
            })}
          </div>
          {filtered.length === 0 && (
            <div className="text-center py-12 text-gray-400">
              <p>No resources match your filters.</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
