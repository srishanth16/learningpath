import { useNavigate } from 'react-router-dom';
import { getDemoProfile } from '../services/api';
import {
  GraduationCap, Brain, Target, Route, BarChart3, Bot, Sparkles,
  ArrowRight, CheckCircle2, Zap
} from 'lucide-react';

const features = [
  { icon: Brain, title: 'AI Goal Analysis', desc: 'Our AI understands your career goals and maps out what you need to learn.' },
  { icon: Target, title: 'Skill Gap Detection', desc: 'Identifies the exact skills you need to develop for your target role.' },
  { icon: Route, title: 'Personalized Roadmaps', desc: 'Get a step-by-step learning path tailored to your pace and style.' },
  { icon: BarChart3, title: 'Progress Tracking', desc: 'Track your learning journey with visual dashboards and milestones.' },
  { icon: Bot, title: 'AI Learning Assistant', desc: 'Ask questions about your roadmap, skills, and next steps anytime.' },
  { icon: Sparkles, title: 'Adaptive Recommendations', desc: 'Your path evolves based on your progress, feedback, and performance.' },
];

const steps = [
  { num: '01', title: 'Tell us your goal', desc: 'Describe what you want to achieve — "I want to become a data scientist"' },
  { num: '02', title: 'Build your profile', desc: 'Share your current skills, experience level, and learning preferences.' },
  { num: '03', title: 'Identify skill gaps', desc: 'We analyze what you know vs. what you need and find the gaps.' },
  { num: '04', title: 'Generate your roadmap', desc: 'Get a phased learning path with courses, projects, and assessments.' },
  { num: '05', title: 'Learn & track progress', desc: 'Complete resources, take quizzes, and watch your skills grow.' },
  { num: '06', title: 'Adapt your path', desc: 'Your roadmap updates based on your progress and feedback.' },
];

export default function LandingPage({ user, setUser }) {
  const navigate = useNavigate();

  const handleDemo = async () => {
    try {
      const res = await getDemoProfile();
      setUser(res.data);
      navigate('/app/dashboard');
    } catch (err) {
      console.error('Failed to load demo:', err);
      navigate('/setup');
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <GraduationCap className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg text-gray-800">LearnPath AI</span>
          </div>
          <nav className="hidden md:flex items-center gap-6 text-sm text-gray-600">
            <a href="#features" className="hover:text-indigo-600 transition">Features</a>
            <a href="#how-it-works" className="hover:text-indigo-600 transition">How It Works</a>
          </nav>
          <div className="flex items-center gap-3">
            {user ? (
              <button onClick={() => navigate('/app/dashboard')} className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition">
                Dashboard
              </button>
            ) : (
              <button onClick={() => navigate('/setup')} className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition">
                Get Started
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="pt-28 pb-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 text-indigo-600 text-sm font-medium mb-6">
            <Zap className="w-4 h-4" />
            AI-Powered Learning Paths
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
            Your Personalized Learning{' '}
            <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Journey Starts Here
            </span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-500 max-w-2xl mx-auto mb-10 leading-relaxed">
            Tell us your goals, current skills, and learning preferences. Our AI creates a tailored roadmap with courses, projects, assessments, and milestones — all personalized just for you.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => navigate('/setup')}
              className="w-full sm:w-auto px-8 py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl text-base font-semibold hover:shadow-lg hover:shadow-indigo-200 transition-all flex items-center justify-center gap-2"
            >
              Create My Learning Path
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={handleDemo}
              className="w-full sm:w-auto px-8 py-3.5 bg-white border-2 border-gray-200 text-gray-700 rounded-xl text-base font-semibold hover:border-indigo-300 hover:text-indigo-600 transition-all"
            >
              Explore Demo
            </button>
          </div>
          <div className="flex items-center justify-center gap-6 mt-8 text-sm text-gray-400">
            <span className="flex items-center gap-1"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Free to use</span>
            <span className="flex items-center gap-1"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> No sign-up required</span>
            <span className="flex items-center gap-1"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Works offline</span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-4 sm:px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">Powerful Features</h2>
            <p className="text-gray-500 text-lg max-w-xl mx-auto">Everything you need for an intelligent, personalized learning experience.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <div key={i} className="bg-white rounded-2xl p-6 border border-gray-100 hover:border-indigo-100 hover:shadow-md transition-all group">
                <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-4 group-hover:bg-indigo-100 transition">
                  <f.icon className="w-6 h-6 text-indigo-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-gray-500 text-lg">Six simple steps to your personalized learning path.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {steps.map((s, i) => (
              <div key={i} className="relative p-6 rounded-2xl bg-gradient-to-br from-white to-gray-50 border border-gray-100">
                <span className="text-4xl font-black text-indigo-100">{s.num}</span>
                <h3 className="text-base font-semibold text-gray-800 mt-2 mb-1">{s.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 sm:px-6 bg-gradient-to-br from-indigo-600 to-purple-700">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Ready to start learning?</h2>
          <p className="text-indigo-100 text-lg mb-8">Create your personalized learning path in minutes.</p>
          <button
            onClick={() => navigate('/setup')}
            className="px-8 py-3.5 bg-white text-indigo-600 rounded-xl font-semibold hover:shadow-lg transition-all"
          >
            Get Started Free
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 sm:px-6 bg-gray-900 text-gray-400 text-sm text-center">
        <p>© 2024 LearnPath AI — AI-Powered Personalized Learning Path Recommender</p>
      </footer>
    </div>
  );
}
