# LearnPath AI — AI-Powered Personalized Learning Path Recommender

An intelligent learning assistant that understands your goals, current skills, interests, and learning preferences to generate a personalized learning roadmap.

## Features

- **AI Goal Analysis** — Analyzes your career goal and identifies required skills
- **Skill Gap Detection** — Compares your skills against target role requirements
- **Personalized Roadmaps** — Generates phased learning paths with prerequisites
- **50+ Learning Resources** — Courses, tutorials, projects, videos, and articles
- **10 Assessments** — Multiple-choice quizzes with scoring and feedback
- **Progress Tracking** — Track completion, hours learned, and streaks
- **Adaptive Recommendations** — Adjusts based on feedback and performance
- **AI Chat Assistant** — Ask questions about your learning journey
- **Visual Dashboard** — Charts, progress rings, and skill radar
- **Demo Mode** — Pre-populated demo user for instant demonstration

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + Tailwind CSS v4 + React Router + Recharts + Lucide React |
| Backend | Python + FastAPI + SQLAlchemy |
| Database | SQLite |
| AI | OpenAI API (optional) + Rule-based fallback engine |

## Project Structure

```
nextpulse/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── database/
│   │   │   ├── db.py            # SQLAlchemy engine + session
│   │   │   └── seed.py          # Seed data (50+ resources, 10 quizzes)
│   │   ├── models/
│   │   │   └── models.py        # ORM models
│   │   ├── schemas/
│   │   │   └── schemas.py       # Pydantic schemas
│   │   ├── routes/
│   │   │   ├── profile.py       # Profile CRUD
│   │   │   ├── goals.py         # Goal management + analysis
│   │   │   ├── skills.py        # Skills + gap analysis
│   │   │   ├── resources.py     # Resource browsing
│   │   │   ├── learning_path.py # Path generation + management
│   │   │   ├── progress.py      # Progress + dashboard
│   │   │   ├── assessments.py   # Quiz system
│   │   │   ├── feedback.py      # Feedback collection
│   │   │   └── chat.py          # AI chat
│   │   ├── ai/
│   │   │   └── ai_service.py    # OpenAI + fallback routing
│   │   └── recommender/
│   │       ├── engine.py        # Recommendation scoring engine
│   │       └── fallback_chat.py # Rule-based chat responses
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/               # All page components
│   │   ├── components/          # Sidebar, shared components
│   │   ├── services/api.js      # API service layer
│   │   ├── data/constants.js    # Static configuration
│   │   ├── App.jsx              # Router + layout
│   │   └── main.jsx             # Entry point
│   ├── index.html
│   └── vite.config.js
├── .env.example
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm

### 1. Clone & Navigate
```bash
cd nextpulse
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Variables (Optional)
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key (optional)
# The app works fully without it using the built-in recommendation engine
OPENAI_API_KEY=your_key_here
```

## How to Run

### Start Backend (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

## How It Works

### AI Integration
When `OPENAI_API_KEY` is set:
- Goal analysis uses GPT for intelligent skill extraction
- Chat assistant provides contextual, conversational responses
- Recommendations are enhanced with LLM reasoning

### Fallback Recommendation Engine
When no API key is configured (default):
- **Goal analysis**: Keyword matching maps goals to career roles
- **Skill gaps**: Compares user skills vs. role requirements
- **Scoring**: `score = goal_relevance × gap_relevance × prereq_match × interest_match × pref_match × difficulty_fit`
- **Path generation**: Orders resources by prerequisite dependencies, groups into phases
- **Chat**: Pattern matching with learner context for helpful responses
- **Adaptation**: Feedback signals adjust difficulty, type preferences, and resource ordering

### Recommendation Score Formula
Each resource is scored based on:
1. **Goal relevance** (0-30) — Does this teach a needed skill?
2. **Interest match** (0-10) — Does this match user interests?
3. **Preference match** (0-10) — Is the resource type preferred?
4. **Difficulty suitability** (0-15) — Appropriate for experience level?
5. **Rating bonus** (0-10) — Higher-rated resources score better
6. **Feedback adaptation** — Adjusts based on "too difficult" / "not helpful" feedback

## Example User Flow

1. **Landing Page** → Click "Create My Learning Path" or "Explore Demo"
2. **Profile Setup** → Enter name, skills, interests, goal
3. **Dashboard** → See overview, generate learning path
4. **Learning Path** → View phased roadmap, start/complete resources
5. **Assessments** → Take quizzes, get scored, see explanations
6. **Skills** → View skill progress charts
7. **AI Assistant** → Ask "What should I learn next?"
8. **Feedback** → Rate completed resources
9. **Dashboard** → See updated progress

## Demo User

Click **"Explore Demo"** on the landing page to load a pre-configured user:
- **Name**: Alex
- **Experience**: Beginner
- **Skills**: Python (25%), SQL (20%)
- **Goal**: Become a Data Scientist
- **Interests**: Data Science, Machine Learning, Programming
- **Preferences**: Projects, Videos
- **Weekly Time**: 8 hours

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/profile | Create learner profile |
| GET | /api/profile/{id} | Get profile |
| GET | /api/profile/demo/load | Load demo user |
| PUT | /api/profile/{id} | Update profile |
| POST | /api/goals | Create learning goal |
| GET | /api/goals/{user_id} | Get goals |
| POST | /api/analyze-goal | AI goal analysis |
| GET | /api/skills | List all skills |
| GET | /api/skills/user/{id} | Get user skills + gaps |
| GET | /api/resources | List resources (filterable) |
| POST | /api/learning-path/generate | Generate learning path |
| GET | /api/learning-path/{user_id} | Get learning path |
| PUT | /api/learning-path/items/{id} | Update item status |
| POST | /api/progress | Update progress |
| GET | /api/dashboard/{user_id} | Dashboard data |
| GET | /api/assessments | List assessments |
| GET | /api/assessments/{id} | Get quiz questions |
| POST | /api/assessments/submit | Submit quiz answers |
| POST | /api/feedback | Submit feedback |
| POST | /api/chat | Send chat message |
| GET | /api/chat/{user_id} | Get chat history |

## Future Improvements

- User authentication with JWT
- External course API integration
- Spaced repetition for assessments
- Learning path sharing/export
- Mobile app with React Native
- Collaborative learning features
- Certificate generation
- Advanced analytics dashboard
