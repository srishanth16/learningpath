import { useState, useEffect, useRef } from 'react';
import { sendChatMessage, getChatHistory } from '../services/api';
import { Bot, Send, User, Sparkles, Loader2 } from 'lucide-react';

const SUGGESTED_QUESTIONS = [
  "What should I learn next?",
  "What are my skill gaps?",
  "Can you recommend a project?",
  "How long will my roadmap take?",
  "Why was this resource recommended?",
  "I'm struggling with SQL. What should I do?",
  "Can I skip statistics?",
  "What should I learn this week?",
];

export default function AIAssistant({ user }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [suggestedQuestions, setSuggestedQuestions] = useState(SUGGESTED_QUESTIONS.slice(0, 4));
  const messagesEndRef = useRef(null);

  useEffect(() => {
    getChatHistory(user.id)
      .then(res => {
        if (res.data && res.data.length > 0) {
          setMessages(res.data.map(m => ({ role: m.role, content: m.content })));
        } else {
          setMessages([{
            role: 'assistant',
            content: `Hello ${user.name}! 👋 I'm your AI learning assistant. I can help you with:\n\n• **Learning path guidance** — what to learn next\n• **Skill gap analysis** — identify areas to improve\n• **Project recommendations** — hands-on practice ideas\n• **Study tips** — strategies for challenging topics\n• **Progress tracking** — how you're doing\n\nWhat would you like to know?`
          }]);
        }
      })
      .catch(() => {
        setMessages([{
          role: 'assistant',
          content: `Hello ${user.name}! 👋 I'm your AI learning assistant. How can I help you today?`
        }]);
      })
      .finally(() => setHistoryLoading(false));
  }, [user.id]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (text) => {
    const msg = text || input.trim();
    if (!msg || loading) return;

    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: msg }]);
    setLoading(true);

    try {
      const res = await sendChatMessage({ user_id: user.id, message: msg });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
      if (res.data.suggested_questions?.length > 0) {
        setSuggestedQuestions(res.data.suggested_questions);
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "I'm sorry, I couldn't process your message right now. Please try again."
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] lg:h-screen">
      {/* Header */}
      <div className="p-4 sm:p-6 border-b border-gray-100 bg-white">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-gray-800">AI Learning Assistant</h1>
            <p className="text-xs text-gray-400">Ask about your roadmap, skills, resources, and more</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-gray-50/50">
        {historyLoading ? (
          <div className="flex justify-center py-8">
            <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''} animate-fade-in`}>
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              )}
              <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white border border-gray-100 text-gray-700'}`}>
                <div className="text-sm whitespace-pre-wrap leading-relaxed" dangerouslySetInnerHTML={{
                  __html: msg.content
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\n/g, '<br/>')
                    .replace(/• /g, '• ')
                }} />
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center flex-shrink-0">
                  <User className="w-4 h-4 text-white" />
                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <div className="flex gap-3 animate-fade-in">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl px-4 py-3">
              <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions */}
      <div className="px-4 sm:px-6 py-2 border-t border-gray-100 bg-white overflow-x-auto">
        <div className="flex gap-2">
          {suggestedQuestions.map((q, i) => (
            <button key={i} onClick={() => handleSend(q)} disabled={loading} className="px-3 py-1.5 bg-gray-50 hover:bg-indigo-50 text-gray-600 hover:text-indigo-600 rounded-full text-xs font-medium whitespace-nowrap transition disabled:opacity-50">
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="p-4 sm:p-6 border-t border-gray-100 bg-white">
        <div className="flex gap-3 max-w-3xl mx-auto">
          <div className="flex-1 relative">
            <textarea
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything about your learning journey..."
              rows={1}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none resize-none text-sm"
            />
          </div>
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || loading}
            className="px-4 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition disabled:opacity-40 flex-shrink-0"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
