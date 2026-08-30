import { useState, useEffect } from 'react';
import { getLearningPath, generateLearningPath, updatePathItem, submitFeedback } from '../services/api';
import { STATUS_COLORS, DIFFICULTY_COLORS, TYPE_COLORS } from '../data/constants';
import { Sparkles, ChevronDown, ChevronUp, Lock, CheckCircle2, Play, Info, Star, MessageSquare } from 'lucide-react';

export default function LearningPathPage({ user }) {
  const [path, setPath] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [expandedPhase, setExpandedPhase] = useState(null);
  const [feedbackItem, setFeedbackItem] = useState(null);
  const [feedbackData, setFeedbackData] = useState({ rating: 5, difficulty_rating: 'just_right', helpful: true, comment: '' });
  const [showReason, setShowReason] = useState(null);

  const fetchPath = () => {
    setLoading(true);
    getLearningPath(user.id)
      .then(res => {
        setPath(res.data);
        // Auto-expand first in-progress phase
        if (res.data?.phases) {
          const firstActive = res.data.phases.find(p => {
            const phaseItems = (res.data.items || []).filter(i => i.phase === p.phase);
            return phaseItems.some(i => i.status !== 'completed');
          });
          if (firstActive) setExpandedPhase(firstActive.phase);
        }
      })
      .catch(() => setPath(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchPath(); }, [user.id]);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const res = await generateLearningPath(user.id);
      setPath(res.data);
      if (res.data?.phases?.[0]) setExpandedPhase(res.data.phases[0].phase);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to generate path');
    } finally {
      setGenerating(false);
    }
  };

  const handleUpdateStatus = async (itemId, status) => {
    try {
      await updatePathItem(itemId, status);
      fetchPath();
    } catch (err) {
      alert('Failed to update status');
    }
  };

  const handleFeedback = async () => {
    if (!feedbackItem) return;
    try {
      await submitFeedback({ user_id: user.id, resource_id: feedbackItem.resource_id, ...feedbackData });
      setFeedbackItem(null);
      setFeedbackData({ rating: 5, difficulty_rating: 'just_right', helpful: true, comment: '' });
    } catch (err) {
      alert('Failed to submit feedback');
    }
  };

  if (loading) return (
    <div className="p-6 flex items-center justify-center min-h-[60vh]">
      <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
    </div>
  );

  if (!path) return (
    <div className="p-4 sm:p-8 max-w-3xl mx-auto animate-fade-in">
      <div className="text-center py-16">
        <Sparkles className="w-12 h-12 text-indigo-300 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-2">No learning path yet</h2>
        <p className="text-gray-500 mb-6">Generate a personalized roadmap based on your goal and skills.</p>
        <button onClick={handleGenerate} disabled={generating} className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-medium hover:shadow-lg transition disabled:opacity-50">
          {generating ? 'Generating...' : 'Generate My Learning Path'}
        </button>
      </div>
    </div>
  );

  const phases = path.phases || [];
  const items = path.items || [];
  const milestones = path.milestones || [];

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-4xl mx-auto animate-fade-in">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{path.title}</h1>
          <p className="text-gray-500 mt-1">{path.description}</p>
        </div>
        <button onClick={handleGenerate} disabled={generating} className="px-4 py-2 text-sm bg-indigo-50 text-indigo-600 rounded-lg hover:bg-indigo-100 transition font-medium disabled:opacity-50">
          {generating ? '...' : 'Regenerate'}
        </button>
      </div>

      {/* Milestone Progress */}
      <div className="bg-white rounded-2xl border border-gray-100 p-5 mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Milestones</h3>
        <div className="flex items-center gap-1 overflow-x-auto pb-2">
          {milestones.map((ms, i) => {
            const phaseItems = items.filter(it => it.phase === ms.phase);
            const allDone = phaseItems.length > 0 && phaseItems.every(it => it.status === 'completed');
            const hasProgress = phaseItems.some(it => it.status === 'completed' || it.status === 'in_progress');
            return (
              <div key={i} className="flex items-center">
                <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap ${allDone ? 'bg-emerald-50 text-emerald-700' : hasProgress ? 'bg-amber-50 text-amber-700' : 'bg-gray-50 text-gray-500'}`}>
                  {allDone ? <CheckCircle2 className="w-3.5 h-3.5" /> : hasProgress ? <Play className="w-3.5 h-3.5" /> : <Lock className="w-3.5 h-3.5" />}
                  {ms.title}
                </div>
                {i < milestones.length - 1 && <div className="w-6 h-px bg-gray-200 mx-1" />}
              </div>
            );
          })}
        </div>
      </div>

      {/* Phases Timeline */}
      <div className="space-y-4">
        {phases.map((phase) => {
          const phaseItems = items.filter(it => it.phase === phase.phase);
          const completedCount = phaseItems.filter(it => it.status === 'completed').length;
          const isExpanded = expandedPhase === phase.phase;
          const allDone = phaseItems.length > 0 && completedCount === phaseItems.length;

          return (
            <div key={phase.phase} className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
              <button onClick={() => setExpandedPhase(isExpanded ? null : phase.phase)} className="w-full flex items-center gap-4 p-5 text-left hover:bg-gray-50/50 transition">
                {/* Timeline dot */}
                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${allDone ? 'bg-emerald-100 text-emerald-600' : 'bg-indigo-100 text-indigo-600'}`}>
                  {allDone ? <CheckCircle2 className="w-5 h-5" /> : <span className="text-sm font-bold">{phase.phase}</span>}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-800">{phase.title}</h3>
                  <p className="text-sm text-gray-500">{phase.week_range} · {completedCount}/{phaseItems.length} completed · ~{phase.estimated_hours}h</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-20 h-1.5 bg-gray-100 rounded-full">
                    <div className="h-full bg-indigo-500 rounded-full transition-all" style={{ width: `${phaseItems.length > 0 ? (completedCount / phaseItems.length) * 100 : 0}%` }} />
                  </div>
                  {isExpanded ? <ChevronUp className="w-5 h-5 text-gray-400" /> : <ChevronDown className="w-5 h-5 text-gray-400" />}
                </div>
              </button>

              {isExpanded && (
                <div className="px-5 pb-5 space-y-3 border-t border-gray-50 pt-3">
                  {phaseItems.map((item) => {
                    const res = item.resource;
                    if (!res) return null;
                    const statusInfo = STATUS_COLORS[item.status] || STATUS_COLORS.locked;
                    const diffColors = DIFFICULTY_COLORS[res.difficulty] || {};
                    const typeColors = TYPE_COLORS[res.type] || {};

                    return (
                      <div key={item.id} className={`rounded-xl border p-4 ${statusInfo.bg} border-gray-100 transition`}>
                        <div className="flex items-start gap-3">
                          <span className="text-lg mt-0.5">{statusInfo.icon}</span>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-start justify-between gap-2">
                              <h4 className="font-medium text-gray-800">{res.title}</h4>
                              <div className="flex gap-1.5 flex-shrink-0">
                                <span className={`text-xs px-2 py-0.5 rounded-full ${typeColors.bg} ${typeColors.text}`}>{res.type}</span>
                                <span className={`text-xs px-2 py-0.5 rounded-full ${diffColors.bg} ${diffColors.text}`}>{res.difficulty}</span>
                              </div>
                            </div>
                            <p className="text-sm text-gray-500 mt-1 line-clamp-2">{res.description}</p>
                            <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                              <span>~{res.estimated_hours}h</span>
                              <span>{res.skill}</span>
                              <span>★ {res.rating}</span>
                              {res.prerequisites?.length > 0 && <span>Requires: {res.prerequisites.join(', ')}</span>}
                            </div>

                            {/* Actions */}
                            <div className="flex flex-wrap items-center gap-2 mt-3">
                              {item.status === 'available' && (
                                <button onClick={() => handleUpdateStatus(item.id, 'in_progress')} className="px-3 py-1.5 text-xs font-medium bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
                                  Start Learning
                                </button>
                              )}
                              {item.status === 'in_progress' && (
                                <button onClick={() => handleUpdateStatus(item.id, 'completed')} className="px-3 py-1.5 text-xs font-medium bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition">
                                  Mark Complete
                                </button>
                              )}
                              {item.status === 'completed' && (
                                <button onClick={() => { setFeedbackItem(item); }} className="px-3 py-1.5 text-xs font-medium bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition flex items-center gap-1">
                                  <Star className="w-3 h-3" /> Give Feedback
                                </button>
                              )}
                              <button onClick={() => setShowReason(showReason === item.id ? null : item.id)} className="px-3 py-1.5 text-xs font-medium text-gray-500 hover:text-indigo-600 transition flex items-center gap-1">
                                <Info className="w-3 h-3" /> Why this?
                              </button>
                              {res.url && (
                                <a href={res.url} target="_blank" rel="noopener noreferrer" className="px-3 py-1.5 text-xs font-medium text-indigo-600 hover:text-indigo-700 transition">
                                  Open Resource ↗
                                </a>
                              )}
                            </div>

                            {/* Reason */}
                            {showReason === item.id && item.reason && (
                              <div className="mt-3 p-3 bg-indigo-50 rounded-lg text-sm text-indigo-800">
                                <p className="font-medium mb-1">Why this recommendation?</p>
                                <p>{item.reason}</p>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Feedback Modal */}
      {feedbackItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={() => setFeedbackItem(null)}>
          <div className="bg-white rounded-2xl max-w-md w-full p-6 animate-fade-in" onClick={e => e.stopPropagation()}>
            <h3 className="text-lg font-semibold text-gray-800 mb-1">Give Feedback</h3>
            <p className="text-sm text-gray-500 mb-4">{feedbackItem.resource?.title}</p>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">How useful was this resource?</label>
                <div className="flex gap-1">
                  {[1,2,3,4,5].map(n => (
                    <button key={n} onClick={() => setFeedbackData(d => ({ ...d, rating: n }))} className={`text-2xl ${n <= feedbackData.rating ? 'text-amber-400' : 'text-gray-200'} hover:scale-110 transition`}>★</button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">Difficulty</label>
                <div className="flex gap-2">
                  {['too_easy', 'just_right', 'too_difficult'].map(d => (
                    <button key={d} onClick={() => setFeedbackData(prev => ({ ...prev, difficulty_rating: d }))} className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${feedbackData.difficulty_rating === d ? 'bg-indigo-50 border-indigo-300 text-indigo-700 border' : 'border border-gray-200 text-gray-600'}`}>
                      {d === 'too_easy' ? 'Too Easy' : d === 'just_right' ? 'Just Right' : 'Too Difficult'}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">Was it helpful?</label>
                <div className="flex gap-2">
                  <button onClick={() => setFeedbackData(d => ({ ...d, helpful: true }))} className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${feedbackData.helpful ? 'bg-emerald-50 border-emerald-300 text-emerald-700 border' : 'border border-gray-200 text-gray-600'}`}>Helpful</button>
                  <button onClick={() => setFeedbackData(d => ({ ...d, helpful: false }))} className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${!feedbackData.helpful ? 'bg-red-50 border-red-300 text-red-700 border' : 'border border-gray-200 text-gray-600'}`}>Not Helpful</button>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-1 block">Comments (optional)</label>
                <textarea value={feedbackData.comment} onChange={e => setFeedbackData(d => ({ ...d, comment: e.target.value }))} rows={3} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none" placeholder="Any additional thoughts..." />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button onClick={() => setFeedbackItem(null)} className="flex-1 py-2.5 border border-gray-200 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition">Cancel</button>
              <button onClick={handleFeedback} className="flex-1 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition">Submit Feedback</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
