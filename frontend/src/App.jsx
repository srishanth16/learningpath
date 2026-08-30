import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import LandingPage from './pages/LandingPage';
import ProfileSetup from './pages/ProfileSetup';
import Dashboard from './pages/Dashboard';
import LearningPathPage from './pages/LearningPathPage';
import SkillsPage from './pages/SkillsPage';
import ResourcesPage from './pages/ResourcesPage';
import ProjectsPage from './pages/ProjectsPage';
import AssessmentsPage from './pages/AssessmentsPage';
import AIAssistant from './pages/AIAssistant';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';
import Sidebar from './components/Sidebar';
import './App.css';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem('learningPathUser');
    if (saved) {
      try { setUser(JSON.parse(saved)); } catch {}
    }
  }, []);

  const saveUser = (userData) => {
    setUser(userData);
    localStorage.setItem('learningPathUser', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('learningPathUser');
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage user={user} setUser={saveUser} />} />
        <Route path="/setup" element={<ProfileSetup setUser={saveUser} />} />
        <Route path="/app/*" element={
          user ? (
            <div className="flex min-h-screen bg-gray-50">
              <Sidebar user={user} logout={logout} />
              <main className="flex-1 lg:ml-64">
                <Routes>
                  <Route path="dashboard" element={<Dashboard user={user} />} />
                  <Route path="learning-path" element={<LearningPathPage user={user} />} />
                  <Route path="skills" element={<SkillsPage user={user} />} />
                  <Route path="resources" element={<ResourcesPage user={user} />} />
                  <Route path="projects" element={<ProjectsPage user={user} />} />
                  <Route path="assessments" element={<AssessmentsPage user={user} />} />
                  <Route path="assistant" element={<AIAssistant user={user} />} />
                  <Route path="profile" element={<ProfilePage user={user} setUser={saveUser} />} />
                  <Route path="settings" element={<SettingsPage user={user} setUser={saveUser} />} />
                </Routes>
              </main>
            </div>
          ) : (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
              <div className="text-center p-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Please create your profile first</h2>
                <a href="/setup" className="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
                  Create Profile
                </a>
              </div>
            </div>
          )
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
