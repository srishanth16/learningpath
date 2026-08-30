import { useState, useEffect } from 'react';
import { getAssessments, getAssessment, submitAssessment, getAssessmentResults } from '../services/api';
import { ClipboardCheck, CheckCircle2, XCircle, Award, ArrowRight, RotateCcw } from 'lucide-react';

export default function AssessmentsPage({ user }) {
  const [assessments, setAssessments] = useState([]);
  const [results, setResults] = useState([]);
  const [activeQuiz, setActiveQuiz] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);

  useEffect(() => {
    Promise.all([
      getAssessments().then(r => setAssessments(r.data)),
      getAssessmentResults(user.id).then(r => setResults(r.data)),
    ]).finally(() => setLoading(false));
  }, [user.id]);

  const startQuiz = async (assessmentId) => {
    try {
      const res = await getAssessment(assessmentId);
      setActiveQuiz(res.data);
      setAnswers(new Array(res.data.questions.length).fill(-1));
      setCurrentQuestion(0);
      setQuizResult(null);
    } catch (err) {
      alert('Failed to load assessment');
    }
  };

  const selectAnswer = (qIndex, optionIndex) => {
    setAnswers(prev => { const n = [...prev]; n[qIndex] = optionIndex; return n; });
  };

  const handleSubmit = async () => {
    if (answers.some(a => a === -1)) {
      alert('Please answer all questions before submitting.');
      return;
    }
    setSubmitting(true);
    try {
      const res = await submitAssessment({ user_id: user.id, assessment_id: activeQuiz.id, answers });
      setQuizResult(res.data);
      // Refresh results
      getAssessmentResults(user.id).then(r => setResults(r.data));
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to submit');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return (
    <div className="p-6 flex items-center justify-center min-h-[60vh]">
      <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
    </div>
  );

  // Quiz result view
  if (quizResult) {
    return (
      <div className="p-4 sm:p-6 lg:p-8 max-w-3xl mx-auto animate-fade-in">
        <div className="bg-white rounded-2xl border border-gray-100 p-8 text-center mb-6">
          <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4 ${quizResult.passed ? 'bg-emerald-50' : 'bg-amber-50'}`}>
            {quizResult.passed ? <Award className="w-8 h-8 text-emerald-600" /> : <RotateCcw className="w-8 h-8 text-amber-600" />}
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">{quizResult.passed ? 'Great job!' : 'Keep practicing!'}</h2>
          <p className="text-4xl font-bold text-indigo-600 mb-2">{quizResult.score}/{quizResult.total}</p>
          <p className="text-lg text-gray-500 mb-4">{quizResult.percentage}%</p>
          <p className="text-sm text-gray-600 max-w-md mx-auto">{quizResult.feedback}</p>
        </div>

        {/* Detailed results */}
        <div className="space-y-3">
          {quizResult.details.map((detail, i) => (
            <div key={i} className={`bg-white rounded-xl border p-4 ${detail.is_correct ? 'border-emerald-200 bg-emerald-50/30' : 'border-red-200 bg-red-50/30'}`}>
              <div className="flex items-start gap-3">
                {detail.is_correct ? <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-0.5" /> : <XCircle className="w-5 h-5 text-red-500 mt-0.5" />}
                <div>
                  <p className="font-medium text-gray-800">{detail.question}</p>
                  {!detail.is_correct && <p className="text-sm text-gray-500 mt-1">{detail.explanation}</p>}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="flex gap-3 mt-6">
          <button onClick={() => { setActiveQuiz(null); setQuizResult(null); }} className="flex-1 py-3 border border-gray-200 rounded-xl font-medium text-gray-600 hover:bg-gray-50 transition">
            Back to Assessments
          </button>
          <button onClick={() => startQuiz(activeQuiz.id)} className="flex-1 py-3 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 transition">
            Retry Quiz
          </button>
        </div>
      </div>
    );
  }

  // Active quiz view
  if (activeQuiz) {
    const q = activeQuiz.questions[currentQuestion];
    return (
      <div className="p-4 sm:p-6 lg:p-8 max-w-3xl mx-auto animate-fade-in">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-bold text-gray-800">{activeQuiz.title}</h2>
          <span className="text-sm text-gray-500">Question {currentQuestion + 1} of {activeQuiz.questions.length}</span>
        </div>

        {/* Progress */}
        <div className="h-1.5 bg-gray-100 rounded-full mb-8">
          <div className="h-full bg-indigo-500 rounded-full transition-all" style={{ width: `${((currentQuestion + 1) / activeQuiz.questions.length) * 100}%` }} />
        </div>

        <div className="bg-white rounded-2xl border border-gray-100 p-6 sm:p-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-6">{q.question}</h3>
          <div className="space-y-3">
            {q.options.map((opt, i) => (
              <button key={i} onClick={() => selectAnswer(currentQuestion, i)} className={`w-full text-left p-4 rounded-xl border transition ${answers[currentQuestion] === i ? 'bg-indigo-50 border-indigo-300 text-indigo-700' : 'border-gray-200 text-gray-700 hover:border-gray-300 hover:bg-gray-50'}`}>
                <span className="font-medium mr-3 text-sm">{String.fromCharCode(65 + i)}.</span>
                {opt}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-between mt-6">
          <button onClick={() => setCurrentQuestion(c => Math.max(0, c - 1))} disabled={currentQuestion === 0} className="px-5 py-2.5 text-sm font-medium text-gray-600 hover:text-gray-800 disabled:opacity-30 transition">
            ← Previous
          </button>
          {currentQuestion < activeQuiz.questions.length - 1 ? (
            <button onClick={() => setCurrentQuestion(c => c + 1)} disabled={answers[currentQuestion] === -1} className="px-5 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition disabled:opacity-40 flex items-center gap-1">
              Next <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button onClick={handleSubmit} disabled={submitting || answers.some(a => a === -1)} className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg text-sm font-medium hover:shadow-lg transition disabled:opacity-40">
              {submitting ? 'Submitting...' : 'Submit Quiz'}
            </button>
          )}
        </div>

        {/* Question dots */}
        <div className="flex justify-center gap-2 mt-6">
          {activeQuiz.questions.map((_, i) => (
            <button key={i} onClick={() => setCurrentQuestion(i)} className={`w-3 h-3 rounded-full transition ${i === currentQuestion ? 'bg-indigo-600' : answers[i] !== -1 ? 'bg-indigo-200' : 'bg-gray-200'}`} />
          ))}
        </div>
      </div>
    );
  }

  // Assessment list
  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-4xl mx-auto animate-fade-in">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Assessments</h1>
      <p className="text-gray-500 mb-6">Test your knowledge and track your skill development.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {assessments.map(a => {
          const prevResult = results.find(r => r.assessment_id === a.id);
          return (
            <div key={a.id} className="bg-white rounded-2xl border border-gray-100 p-5 hover:border-indigo-100 hover:shadow-sm transition">
              <div className="flex items-start justify-between mb-3">
                <div className="w-10 h-10 rounded-xl bg-pink-50 flex items-center justify-center">
                  <ClipboardCheck className="w-5 h-5 text-pink-600" />
                </div>
                {prevResult && (
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${prevResult.percentage >= 60 ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
                    {prevResult.percentage}%
                  </span>
                )}
              </div>
              <h3 className="font-semibold text-gray-800 mb-1">{a.title}</h3>
              <p className="text-sm text-gray-500 mb-3">
                {a.question_count} questions · {a.skill} · {a.difficulty}
              </p>
              <button onClick={() => startQuiz(a.id)} className="w-full py-2.5 bg-indigo-50 text-indigo-600 rounded-lg text-sm font-medium hover:bg-indigo-100 transition">
                {prevResult ? 'Retake Quiz' : 'Start Quiz'}
              </button>
            </div>
          );
        })}
      </div>

      {assessments.length === 0 && (
        <div className="text-center py-16 text-gray-400">
          <ClipboardCheck className="w-12 h-12 mx-auto mb-3" />
          <p>No assessments available.</p>
        </div>
      )}
    </div>
  );
}
