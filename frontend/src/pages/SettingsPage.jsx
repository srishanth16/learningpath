import { useState } from 'react';
import { updateProfile } from '../services/api';
import { LEARNING_PREFERENCES, WEEKLY_HOURS } from '../data/constants';
import { Settings as SettingsIcon, Save, Check } from 'lucide-react';

export default function SettingsPage({ user, setUser }) {
  const [preferences, setPreferences] = useState(user.learning_preferences || []);
  const [weeklyHours, setWeeklyHours] = useState(user.weekly_hours || 7);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const togglePref = (pref) => {
    setPreferences(prev => prev.includes(pref) ? prev.filter(p => p !== pref) : [...prev, pref]);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await updateProfile(user.id, {
        learning_preferences: preferences,
        weekly_hours: weeklyHours,
      });
      setUser(res.data);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      alert('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-2xl mx-auto animate-fade-in">
      <h1 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <SettingsIcon className="w-6 h-6" /> Settings
      </h1>

      <div className="bg-white rounded-2xl border border-gray-100 p-6 space-y-6">
        {/* Learning Preferences */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-3">Learning Preferences</h3>
          <p className="text-sm text-gray-500 mb-3">Select how you prefer to learn. This affects your recommendations.</p>
          <div className="flex flex-wrap gap-2">
            {LEARNING_PREFERENCES.map(pref => (
              <button key={pref} onClick={() => togglePref(pref)} className={`px-4 py-2 rounded-full text-sm font-medium transition ${preferences.includes(pref) ? 'bg-indigo-100 text-indigo-700 border border-indigo-200' : 'bg-gray-50 text-gray-600 border border-gray-200 hover:border-gray-300'}`}>
                {pref}
              </button>
            ))}
          </div>
        </div>

        {/* Weekly Hours */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-3">Weekly Learning Time</h3>
          <p className="text-sm text-gray-500 mb-3">How much time can you dedicate to learning each week?</p>
          <div className="flex flex-wrap gap-3">
            {WEEKLY_HOURS.map(wh => (
              <button key={wh.value} onClick={() => setWeeklyHours(wh.value)} className={`px-4 py-2.5 rounded-lg border text-sm font-medium transition ${weeklyHours === wh.value ? 'bg-emerald-50 border-emerald-300 text-emerald-700' : 'border-gray-200 text-gray-600 hover:border-gray-300'}`}>
                {wh.label}
              </button>
            ))}
          </div>
        </div>

        {/* Save */}
        <button onClick={handleSave} disabled={saving} className="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition disabled:opacity-50">
          {saved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
          {saving ? 'Saving...' : saved ? 'Saved!' : 'Save Settings'}
        </button>
      </div>
    </div>
  );
}
