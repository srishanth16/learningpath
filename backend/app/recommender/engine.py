"""
Rule-based recommendation engine.
Scores resources based on learner profile, goals, skill gaps, and feedback.
Works entirely without an LLM — this is the core fallback engine.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models.models import (
    User, UserSkill, UserInterest, LearningGoal, Skill,
    Resource, Progress, Feedback, LearningPath, LearningPathItem,
    AssessmentResult
)

# ── Career → Required Skills Mapping ────────────────
ROLE_SKILLS = {
    "data scientist": [
        "Python", "SQL", "Statistics", "Probability", "NumPy", "Pandas",
        "Data Cleaning", "Data Visualization", "Machine Learning", "Deep Learning"
    ],
    "machine learning engineer": [
        "Python", "NumPy", "Pandas", "Statistics", "Probability",
        "Machine Learning", "Deep Learning", "Git", "Docker", "Cloud Computing"
    ],
    "frontend developer": [
        "HTML", "CSS", "JavaScript", "React", "TypeScript",
        "Git", "REST APIs", "Testing", "Deployment", "UI/UX Design"
    ],
    "backend developer": [
        "Python", "SQL", "REST APIs", "Git", "Linux",
        "Docker", "Testing", "Deployment", "Algorithms"
    ],
    "full stack developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "SQL",
        "REST APIs", "Git", "Testing", "Deployment"
    ],
    "data analyst": [
        "Python", "SQL", "Statistics", "Pandas", "Data Visualization",
        "Data Cleaning", "NumPy"
    ],
    "devops engineer": [
        "Linux", "Git", "Docker", "Cloud Computing", "Python",
        "Deployment", "Testing"
    ],
    "cybersecurity analyst": [
        "Linux", "Cybersecurity", "Python", "Algorithms", "Cloud Computing"
    ],
    "ai engineer": [
        "Python", "NumPy", "Pandas", "Statistics", "Machine Learning",
        "Deep Learning", "NLP", "Git", "Docker"
    ],
    "web developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js",
        "REST APIs", "Git", "Testing", "Deployment"
    ],
}

# ── Skill prerequisite ordering (higher index = more advanced) ──
SKILL_ORDER = {
    # Data Science track
    "Python": 1, "SQL": 1, "Git": 1,
    "Statistics": 2, "NumPy": 2,
    "Probability": 3, "Pandas": 3,
    "Data Cleaning": 4, "Data Visualization": 4,
    "Machine Learning": 5,
    "Deep Learning": 6, "NLP": 6,
    # Web track
    "HTML": 1, "CSS": 1,
    "JavaScript": 2,
    "React": 3, "Node.js": 3, "TypeScript": 3, "REST APIs": 3,
    "Testing": 4, "Deployment": 4,
    # Other
    "Linux": 1, "Algorithms": 2,
    "Docker": 3, "Cloud Computing": 3,
    "Cybersecurity": 2, "UI/UX Design": 1, "Agile": 1,
}


def detect_target_role(goal_text: str) -> str:
    """Extract target role from free-text goal using keyword matching."""
    goal_lower = goal_text.lower()
    for role in ROLE_SKILLS:
        if role in goal_lower:
            return role
    # Fuzzy matching
    keyword_map = {
        "data scien": "data scientist",
        "ml engineer": "machine learning engineer",
        "machine learning": "machine learning engineer",
        "frontend": "frontend developer",
        "front-end": "frontend developer",
        "front end": "frontend developer",
        "backend": "backend developer",
        "back-end": "backend developer",
        "back end": "backend developer",
        "full stack": "full stack developer",
        "fullstack": "full stack developer",
        "data analy": "data analyst",
        "devops": "devops engineer",
        "cybersec": "cybersecurity analyst",
        "security": "cybersecurity analyst",
        "ai ": "ai engineer",
        "artificial intelligence": "ai engineer",
        "web dev": "web developer",
        "nlp": "ai engineer",
        "deep learning": "machine learning engineer",
    }
    for keyword, role in keyword_map.items():
        if keyword in goal_lower:
            return role
    return "data scientist"  # default


def get_required_skills(target_role: str) -> List[str]:
    """Get the list of required skills for a target role."""
    return ROLE_SKILLS.get(target_role.lower(), ROLE_SKILLS["data scientist"])


def analyze_skill_gaps(db: Session, user_id: int, required_skills: List[str]) -> Dict:
    """Compare user skills against required skills and classify them."""
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    skill_map = {}
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            skill_map[skill.name] = us.proficiency

    current_skills = []
    skill_gaps = []
    strong = []
    intermediate = []
    needs_improvement = []
    missing = []

    for skill_name in required_skills:
        prof = skill_map.get(skill_name, 0)
        entry = {"name": skill_name, "proficiency": prof, "order": SKILL_ORDER.get(skill_name, 5)}

        if prof > 0:
            current_skills.append(entry)

        if prof >= 70:
            strong.append(entry)
        elif prof >= 40:
            intermediate.append(entry)
        elif prof > 0:
            needs_improvement.append(entry)
            skill_gaps.append(entry)
        else:
            missing.append(entry)
            skill_gaps.append(entry)

    # Priority skills = gaps sorted by prerequisite order (learn foundations first)
    priority_skills = sorted(skill_gaps, key=lambda x: x["order"])

    return {
        "current_skills": current_skills,
        "skill_gaps": skill_gaps,
        "priority_skills": priority_skills,
        "strong": strong,
        "intermediate": intermediate,
        "needs_improvement": needs_improvement,
        "missing": missing,
    }


def score_resource(resource: Resource, user: User, skill_gaps: List[Dict],
                   interests: List[str], feedback_data: Dict, completed_ids: set) -> float:
    """Score a resource for recommendation relevance (0-100)."""
    if resource.id in completed_ids:
        return -1  # Already completed

    score = 0.0

    # Goal relevance — does this resource teach a needed skill?
    gap_names = {g["name"].lower() for g in skill_gaps}
    if resource.skill.lower() in gap_names:
        score += 30
    elif resource.skill.lower() in {s.lower() for s in get_required_skills(
            detect_target_role(user.goals[0].goal_text if user.goals else ""))}:
        score += 15

    # Interest match
    interest_names = {i.lower() for i in interests}
    resource_domain_lower = resource.domain.lower()
    resource_tags = {t.lower() for t in (resource.tags or [])}
    for interest in interest_names:
        if interest in resource_domain_lower or interest in resource_tags:
            score += 10
            break

    # Learning preference match
    prefs = {p.lower() for p in (user.learning_preferences or [])}
    type_pref_map = {
        "videos": ["video"],
        "articles": ["article"],
        "hands-on coding": ["tutorial", "project"],
        "projects": ["project"],
        "quizzes": ["quiz", "assessment"],
        "reading": ["article", "course"],
        "interactive exercises": ["tutorial", "project"],
    }
    for pref in prefs:
        matched_types = type_pref_map.get(pref, [])
        if resource.type.lower() in matched_types:
            score += 10
            break

    # Difficulty suitability
    exp = user.experience_level.lower() if user.experience_level else "beginner"
    diff = resource.difficulty.lower()
    difficulty_match = {
        ("beginner", "beginner"): 15,
        ("beginner", "intermediate"): 8,
        ("beginner", "advanced"): 2,
        ("intermediate", "beginner"): 5,
        ("intermediate", "intermediate"): 15,
        ("intermediate", "advanced"): 10,
        ("advanced", "beginner"): 2,
        ("advanced", "intermediate"): 8,
        ("advanced", "advanced"): 15,
    }
    score += difficulty_match.get((exp, diff), 5)

    # Rating bonus
    score += (resource.rating or 4.0) * 2  # up to ~10

    # Feedback adaptation — reduce score for resources similar to those rated "too difficult"
    if feedback_data.get("reduce_difficulty"):
        if diff == "advanced":
            score -= 10
        elif diff == "intermediate":
            score -= 5

    # Reduce video recommendations if user said they don't like videos
    if feedback_data.get("reduce_videos") and resource.type.lower() == "video":
        score -= 15

    # Boost projects if user prefers project-based learning
    if feedback_data.get("boost_projects") and resource.type.lower() == "project":
        score += 10

    return max(score, 0)


def check_prerequisites_met(resource: Resource, completed_titles: set) -> bool:
    """Check if all prerequisites for a resource are completed."""
    prereqs = resource.prerequisites or []
    if not prereqs:
        return True
    return all(p in completed_titles for p in prereqs)


def get_feedback_signals(db: Session, user_id: int) -> Dict:
    """Analyze feedback to determine adaptation signals."""
    feedbacks = db.query(Feedback).filter(Feedback.user_id == user_id).all()
    signals = {
        "reduce_difficulty": False,
        "reduce_videos": False,
        "boost_projects": False,
    }

    difficult_count = sum(1 for f in feedbacks if f.difficulty_rating == "too_difficult")
    if difficult_count >= 2:
        signals["reduce_difficulty"] = True

    not_helpful_videos = sum(
        1 for f in feedbacks
        if not f.helpful and f.resource and db.query(Resource).get(f.resource_id)
        and db.query(Resource).get(f.resource_id).type == "video"
    )
    if not_helpful_videos >= 1:
        signals["reduce_videos"] = True

    # Check assessment scores — if low, reduce difficulty
    results = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).all()
    low_scores = sum(1 for r in results if r.total > 0 and (r.score / r.total) < 0.6)
    if low_scores >= 1:
        signals["reduce_difficulty"] = True

    # Check preferences
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.learning_preferences:
        if "projects" in [p.lower() for p in user.learning_preferences]:
            signals["boost_projects"] = True

    return signals


def generate_recommendations(db: Session, user_id: int) -> List[Dict]:
    """Generate ranked resource recommendations for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []

    # Get active goal
    goal = db.query(LearningGoal).filter(
        LearningGoal.user_id == user_id,
        LearningGoal.is_active == True
    ).first()
    if not goal:
        return []

    target_role = goal.target_role or detect_target_role(goal.goal_text)
    required_skills = get_required_skills(target_role)

    # Analyze gaps
    gaps = analyze_skill_gaps(db, user_id, required_skills)

    # Get interests
    interests_objs = db.query(UserInterest).filter(UserInterest.user_id == user_id).all()
    interests = [i.interest for i in interests_objs]

    # Get completed resources
    completed = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.completed == True
    ).all()
    completed_ids = {p.resource_id for p in completed}
    completed_resources = [db.query(Resource).get(rid) for rid in completed_ids]
    completed_titles = {r.title for r in completed_resources if r}

    # Get feedback signals
    feedback_signals = get_feedback_signals(db, user_id)

    # Score all resources
    all_resources = db.query(Resource).all()
    scored = []
    for resource in all_resources:
        s = score_resource(resource, user, gaps["skill_gaps"], interests, feedback_signals, completed_ids)
        if s >= 0:
            prereqs_met = check_prerequisites_met(resource, completed_titles)
            scored.append({
                "resource": resource,
                "score": s,
                "prerequisites_met": prereqs_met,
                "reason": _generate_reason(resource, user, gaps, target_role)
            })

    # Sort by score, prereqs met first
    scored.sort(key=lambda x: (x["prerequisites_met"], x["score"]), reverse=True)

    return scored[:20]


def _generate_reason(resource: Resource, user: User, gaps: Dict, target_role: str) -> str:
    """Generate a human-readable explanation for why a resource is recommended."""
    skill = resource.skill
    gap_names = [g["name"] for g in gaps["skill_gaps"]]
    user_name = user.name

    if skill in gap_names:
        return (
            f"This {resource.type} was recommended because {skill} is a key skill gap "
            f"in your journey to become a {target_role.title()}. "
            f"Completing this will bring you closer to your goal."
        )
    else:
        return (
            f"This {resource.type} covers {skill}, which is valuable for "
            f"a {target_role.title()} career path. It will strengthen your overall skill set."
        )


def generate_learning_path(db: Session, user_id: int) -> Dict:
    """Generate a complete, phased learning path with milestones."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {}

    goal = db.query(LearningGoal).filter(
        LearningGoal.user_id == user_id,
        LearningGoal.is_active == True
    ).first()
    if not goal:
        return {}

    target_role = goal.target_role or detect_target_role(goal.goal_text)
    required_skills = get_required_skills(target_role)
    gaps = analyze_skill_gaps(db, user_id, required_skills)

    # Get completed resources
    completed = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.completed == True
    ).all()
    completed_ids = {p.resource_id for p in completed}
    completed_resources = [db.query(Resource).get(rid) for rid in completed_ids]
    completed_titles = {r.title for r in completed_resources if r}

    # Get feedback signals for adaptation
    feedback_signals = get_feedback_signals(db, user_id)

    # Group required skills by order to create phases
    skill_phases = {}
    for skill_name in required_skills:
        order = SKILL_ORDER.get(skill_name, 5)
        if order not in skill_phases:
            skill_phases[order] = []
        skill_phases[order].append(skill_name)

    # Build phases
    phases = []
    milestones = []
    items = []
    phase_num = 0

    # Calculate weekly hours
    weekly_hours = user.weekly_hours or 5
    current_week = 1

    for order in sorted(skill_phases.keys()):
        phase_skills = skill_phases[order]
        phase_num += 1

        # Find resources for these skills
        phase_resources = []
        for skill_name in phase_skills:
            # Check if user already knows this skill well enough
            is_strong = any(s["name"] == skill_name and s["proficiency"] >= 70 for s in gaps["strong"])
            if is_strong:
                continue

            # Find matching resources
            skill_resources = db.query(Resource).filter(
                Resource.skill == skill_name
            ).all()

            for res in skill_resources:
                if res.id in completed_ids:
                    continue

                # Filter by difficulty preference
                if feedback_signals.get("reduce_difficulty") and res.difficulty == "advanced":
                    continue

                # Filter by type preference
                if feedback_signals.get("reduce_videos") and res.type == "video":
                    continue

                phase_resources.append(res)

        if not phase_resources:
            continue

        # Sort resources within phase: courses first, then tutorials, then projects
        type_order = {"course": 0, "video": 1, "article": 2, "tutorial": 3, "project": 4, "quiz": 5, "assessment": 5}
        phase_resources.sort(key=lambda r: (type_order.get(r.type, 3), -r.rating))

        # Calculate phase duration
        phase_hours = sum(r.estimated_hours for r in phase_resources)
        phase_weeks = max(1, round(phase_hours / weekly_hours))
        week_range = f"Week {current_week}" if phase_weeks == 1 else f"Week {current_week}–{current_week + phase_weeks - 1}"

        phase_info = {
            "phase": phase_num,
            "title": f"Phase {phase_num} — {', '.join(phase_skills)}",
            "skills": phase_skills,
            "week_range": week_range,
            "estimated_hours": phase_hours,
            "resource_count": len(phase_resources),
        }
        phases.append(phase_info)

        # Add milestone
        milestones.append({
            "phase": phase_num,
            "title": f"{', '.join(phase_skills)} Foundation" if phase_num <= 3 else f"{', '.join(phase_skills)} Mastery",
            "description": f"Complete all {', '.join(phase_skills)} resources",
        })

        # Create path items
        for idx, res in enumerate(phase_resources):
            prereqs_met = check_prerequisites_met(res, completed_titles)
            status = "available" if (phase_num == 1 and prereqs_met) else "locked"

            items.append({
                "resource": res,
                "phase": phase_num,
                "order": idx,
                "status": status,
                "reason": _generate_reason(res, user, gaps, target_role),
            })

        current_week += phase_weeks

    # Add final milestone
    milestones.append({
        "phase": phase_num + 1,
        "title": "Career Ready",
        "description": f"You've completed all the core skills needed for a {target_role.title()} role!",
    })

    return {
        "title": f"Learning Path: {target_role.title()}",
        "description": f"A personalized learning roadmap to help {user.name} become a {target_role.title()}.",
        "target_role": target_role,
        "phases": phases,
        "milestones": milestones,
        "items": items,
        "estimated_weeks": current_week - 1,
    }


def get_suggested_projects(target_role: str) -> List[str]:
    """Get project suggestions for a target role."""
    projects = {
        "data scientist": [
            "Exploratory Data Analysis Project",
            "Customer Churn Prediction",
            "Sales Forecasting",
            "Sentiment Analysis",
        ],
        "machine learning engineer": [
            "Customer Churn Prediction",
            "Image Classification",
            "Recommendation System",
            "NLP Text Classifier",
        ],
        "frontend developer": [
            "Portfolio Website",
            "Task Manager App",
            "E-commerce Website",
            "Real-time Chat Application",
        ],
        "backend developer": [
            "REST API Project",
            "Authentication System",
            "Job Board API",
            "Real-time Chat Backend",
        ],
        "full stack developer": [
            "Task Manager App",
            "E-commerce Website",
            "Social Media Dashboard",
            "Real-time Chat Application",
        ],
        "data analyst": [
            "Exploratory Data Analysis",
            "Dashboard with Visualization",
            "A/B Testing Analysis",
            "Survey Data Analysis",
        ],
    }
    return projects.get(target_role.lower(), projects["data scientist"])


def get_suggested_assessments(target_role: str) -> List[str]:
    """Get assessment suggestions for a target role."""
    assessments = {
        "data scientist": ["Python Basics Quiz", "SQL Fundamentals Quiz", "Statistics Quiz", "Machine Learning Basics Quiz"],
        "machine learning engineer": ["Python Basics Quiz", "Statistics Quiz", "Machine Learning Basics Quiz", "NumPy Quiz"],
        "frontend developer": ["HTML & CSS Quiz", "JavaScript Fundamentals Quiz", "React Basics Quiz"],
        "backend developer": ["Python Basics Quiz", "SQL Fundamentals Quiz", "Git Basics Quiz"],
        "full stack developer": ["HTML & CSS Quiz", "JavaScript Fundamentals Quiz", "React Basics Quiz", "SQL Fundamentals Quiz"],
        "data analyst": ["Python Basics Quiz", "SQL Fundamentals Quiz", "Statistics Quiz", "Pandas Quiz"],
    }
    return assessments.get(target_role.lower(), assessments["data scientist"])
