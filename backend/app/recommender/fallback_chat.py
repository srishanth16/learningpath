"""
Fallback chat engine for when no OpenAI API key is configured.
Uses pattern matching and learner context to generate helpful responses.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models.models import (
    User, UserSkill, Skill, LearningGoal, Resource, Progress,
    LearningPath, LearningPathItem, AssessmentResult
)
from .engine import detect_target_role, get_required_skills, analyze_skill_gaps, SKILL_ORDER


def generate_fallback_response(db: Session, user_id: int, message: str) -> Dict:
    """Generate a contextual response without an LLM."""
    msg = message.lower().strip()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {
            "response": "I don't have your profile yet. Please create a profile first so I can help you better!",
            "suggested_questions": ["How do I create my profile?"]
        }

    # Get context
    goal = db.query(LearningGoal).filter(
        LearningGoal.user_id == user_id,
        LearningGoal.is_active == True
    ).first()
    target_role = goal.target_role if goal else "your chosen career"
    if goal and not goal.target_role:
        target_role = detect_target_role(goal.goal_text).title()

    required_skills = get_required_skills(target_role.lower()) if goal else []
    gaps = analyze_skill_gaps(db, user_id, required_skills) if required_skills else {}

    # Get progress
    completed = db.query(Progress).filter(
        Progress.user_id == user_id, Progress.completed == True
    ).all()
    completed_ids = {p.resource_id for p in completed}

    # Get current learning path
    path = db.query(LearningPath).filter(LearningPath.user_id == user_id).order_by(
        LearningPath.created_at.desc()
    ).first()

    # ── Pattern matching ────────────────────────────
    suggested = [
        "What should I learn next?",
        "How long will my roadmap take?",
        "Can you recommend a project?",
        "What are my skill gaps?",
    ]

    # What to learn first / next
    if any(kw in msg for kw in ["learn first", "start with", "learn next", "what next", "what should i"]):
        if gaps and gaps.get("priority_skills"):
            next_skills = gaps["priority_skills"][:3]
            skill_names = [s["name"] for s in next_skills]
            response = (
                f"Based on your goal to become a {target_role}, I recommend focusing on these skills next:\n\n"
            )
            for i, s in enumerate(next_skills, 1):
                prof = s["proficiency"]
                status = "not started" if prof == 0 else f"{prof}% proficiency"
                response += f"{i}. **{s['name']}** — {status}\n"
            response += (
                f"\nStart with **{skill_names[0]}** as it's a key foundation for the other skills. "
                f"Check your Learning Path for specific resources!"
            )
            suggested = [
                f"Why do I need {skill_names[0]}?",
                "Can you recommend a project?",
                "How long will this take?",
            ]
        else:
            response = "You're making great progress! Check your Learning Path for the next recommended resources."
        return {"response": response, "suggested_questions": suggested}

    # Why do I need X?
    if "why" in msg and ("need" in msg or "learn" in msg or "important" in msg):
        # Try to extract skill name
        for skill_name in required_skills:
            if skill_name.lower() in msg:
                prereq_info = _get_skill_context(skill_name, target_role, required_skills)
                return {
                    "response": prereq_info,
                    "suggested_questions": [
                        f"Can I skip {skill_name}?",
                        "What should I learn next?",
                        "How long will my roadmap take?",
                    ]
                }
        response = (
            f"Each skill in your roadmap was selected because it's essential for becoming a {target_role}. "
            f"The skills build on each other — foundations like Python and SQL support more advanced topics like Machine Learning."
        )
        return {"response": response, "suggested_questions": suggested}

    # Can I skip X?
    if "skip" in msg:
        for skill_name in required_skills:
            if skill_name.lower() in msg:
                order = SKILL_ORDER.get(skill_name, 5)
                dependent_skills = [s for s in required_skills if SKILL_ORDER.get(s, 5) > order]
                if dependent_skills:
                    deps = ", ".join(dependent_skills[:3])
                    response = (
                        f"I wouldn't recommend skipping **{skill_name}**. "
                        f"Skills like {deps} depend on it. "
                        f"However, if you already have some knowledge, you could take the assessment to test your level "
                        f"and potentially move to more advanced resources."
                    )
                else:
                    response = (
                        f"**{skill_name}** is one of the later skills in your roadmap. "
                        f"While it's recommended for a complete {target_role} profile, "
                        f"you could potentially skip it initially and come back to it later."
                    )
                return {
                    "response": response,
                    "suggested_questions": [
                        "What should I learn next?",
                        f"How important is {skill_name}?",
                        "Can you recommend a project?",
                    ]
                }
        response = "Could you tell me which specific skill or topic you're thinking of skipping?"
        return {"response": response, "suggested_questions": suggested}

    # Project recommendation
    if any(kw in msg for kw in ["project", "build", "practice", "hands-on"]):
        projects = db.query(Resource).filter(Resource.type == "project").all()
        relevant = [p for p in projects if p.skill.lower() in [s.lower() for s in required_skills]]
        if relevant:
            response = f"Here are some projects I recommend for your {target_role} journey:\n\n"
            for p in relevant[:4]:
                response += f"• **{p.title}** — {p.description[:80]}... ({p.difficulty}, ~{p.estimated_hours}h)\n"
            response += "\nCheck the Projects page for full details!"
        else:
            response = "Check the Projects page for available projects that match your learning path."
        return {
            "response": response,
            "suggested_questions": [
                "What should I learn next?",
                "How long will my roadmap take?",
            ]
        }

    # How long will it take?
    if any(kw in msg for kw in ["how long", "duration", "time", "weeks", "months"]):
        if path and path.phases:
            total_hours = sum(p.get("estimated_hours", 0) for p in path.phases)
            weekly = user.weekly_hours or 5
            weeks = max(1, round(total_hours / weekly))
            response = (
                f"Based on your learning path and your commitment of **{weekly} hours/week**, "
                f"your roadmap should take approximately **{weeks} weeks** ({total_hours:.0f} total hours).\n\n"
                f"You've completed **{len(completed_ids)}** resources so far. Keep going!"
            )
        else:
            weekly = user.weekly_hours or 5
            gap_count = len(gaps.get("skill_gaps", [])) if gaps else 5
            est_weeks = gap_count * 3
            response = (
                f"With **{weekly} hours/week** of study, I estimate your roadmap will take "
                f"approximately **{est_weeks}–{est_weeks + 4} weeks**. "
                f"Generate your Learning Path for a more precise estimate!"
            )
        return {"response": response, "suggested_questions": suggested}

    # Struggling with X
    if any(kw in msg for kw in ["struggling", "difficult", "hard", "stuck", "don't understand", "confused"]):
        for skill_name in required_skills:
            if skill_name.lower() in msg:
                resources = db.query(Resource).filter(
                    Resource.skill == skill_name,
                    Resource.difficulty == "beginner"
                ).all()
                response = f"Don't worry — {skill_name} can be challenging at first! Here's what I suggest:\n\n"
                response += f"1. Review the fundamentals of {skill_name}\n"
                response += f"2. Practice with small exercises before moving to complex problems\n"
                if resources:
                    response += f"3. Try: **{resources[0].title}** — a beginner-friendly resource\n"
                response += f"4. Take the {skill_name} assessment to identify specific weak areas\n"
                response += f"\nRemember, it's completely normal to struggle with new concepts. Persistence pays off!"
                return {
                    "response": response,
                    "suggested_questions": [
                        f"What are the prerequisites for {skill_name}?",
                        "Can you recommend easier resources?",
                        "What should I learn next?",
                    ]
                }
        response = (
            "I understand you're finding things challenging. Here are some tips:\n\n"
            "1. Break down the topic into smaller parts\n"
            "2. Review prerequisite skills — sometimes the foundation needs strengthening\n"
            "3. Try different resource types (videos, tutorials, hands-on practice)\n"
            "4. Take assessments to identify specific weak areas\n\n"
            "Which specific topic are you struggling with?"
        )
        return {"response": response, "suggested_questions": suggested}

    # Skill gaps
    if any(kw in msg for kw in ["skill gap", "gaps", "missing skills", "what do i need"]):
        if gaps and gaps.get("skill_gaps"):
            response = f"Here's your skill gap analysis for becoming a {target_role}:\n\n"
            if gaps.get("strong"):
                response += "**Strong skills:** " + ", ".join(s["name"] for s in gaps["strong"]) + "\n"
            if gaps.get("intermediate"):
                response += "**Intermediate:** " + ", ".join(s["name"] for s in gaps["intermediate"]) + "\n"
            if gaps.get("needs_improvement"):
                response += "**Needs improvement:** " + ", ".join(s["name"] for s in gaps["needs_improvement"]) + "\n"
            if gaps.get("missing"):
                response += "**Not started:** " + ", ".join(s["name"] for s in gaps["missing"]) + "\n"
            response += "\nCheck the Skills page for a detailed visual breakdown!"
        else:
            response = "Set a learning goal first so I can analyze your skill gaps!"
        return {"response": response, "suggested_questions": suggested}

    # Why was X recommended?
    if "why" in msg and ("recommend" in msg or "suggested" in msg):
        response = (
            f"Every resource in your learning path is selected based on:\n\n"
            f"1. **Your goal** — becoming a {target_role}\n"
            f"2. **Your skill gaps** — skills you need but haven't mastered yet\n"
            f"3. **Prerequisites** — ensuring you learn foundations before advanced topics\n"
            f"4. **Your preferences** — matching your preferred learning style\n"
            f"5. **Difficulty** — appropriate challenge level for your experience\n\n"
            f"Click 'Why this recommendation?' on any resource for a specific explanation."
        )
        return {"response": response, "suggested_questions": suggested}

    # This week
    if any(kw in msg for kw in ["this week", "today", "now", "current"]):
        if path:
            current_items = db.query(LearningPathItem).filter(
                LearningPathItem.path_id == path.id,
                LearningPathItem.status.in_(["available", "in_progress"])
            ).order_by(LearningPathItem.phase, LearningPathItem.order).limit(3).all()
            if current_items:
                response = "Here's what I recommend for this week:\n\n"
                for item in current_items:
                    res = db.query(Resource).get(item.resource_id)
                    if res:
                        response += f"• **{res.title}** ({res.type}, ~{res.estimated_hours}h)\n"
                response += "\nFocus on completing these before moving on!"
            else:
                response = "You've completed all available items! Check your roadmap for the next phase."
        else:
            response = "Generate your Learning Path first, then I can tell you what to focus on this week!"
        return {"response": response, "suggested_questions": suggested}

    # Progress
    if any(kw in msg for kw in ["progress", "how am i doing", "status"]):
        total = db.query(Resource).count()
        done = len(completed_ids)
        pct = round((done / total) * 100) if total > 0 else 0
        response = (
            f"Here's your progress, {user.name}:\n\n"
            f"• **{done}/{total}** resources completed ({pct}%)\n"
        )
        if gaps:
            strong_count = len(gaps.get("strong", []))
            gap_count = len(gaps.get("skill_gaps", []))
            response += f"• **{strong_count}** skills mastered\n"
            response += f"• **{gap_count}** skill gaps remaining\n"
        response += "\nCheck your Dashboard for a full visual breakdown!"
        return {"response": response, "suggested_questions": suggested}

    # Greeting
    if any(kw in msg for kw in ["hello", "hi", "hey", "help", "what can you"]):
        response = (
            f"Hello {user.name}! 👋 I'm your learning assistant. I can help you with:\n\n"
            f"• **Learning path guidance** — what to learn next\n"
            f"• **Skill gap analysis** — identify areas to improve\n"
            f"• **Project recommendations** — hands-on practice ideas\n"
            f"• **Study tips** — strategies for challenging topics\n"
            f"• **Progress tracking** — how you're doing\n\n"
            f"What would you like to know?"
        )
        return {"response": response, "suggested_questions": suggested}

    # Default response
    response = (
        f"Thanks for your question, {user.name}! While I may not have a specific answer for that, "
        f"I can help you with:\n\n"
        f"• What to learn next\n"
        f"• Your skill gaps\n"
        f"• Project recommendations\n"
        f"• Study strategies\n"
        f"• Your learning progress\n\n"
        f"Try asking one of the suggested questions below!"
    )
    return {"response": response, "suggested_questions": suggested}


def _get_skill_context(skill_name: str, target_role: str, required_skills: list) -> str:
    """Explain why a specific skill matters for the target role."""
    contexts = {
        "Python": f"Python is the most widely used programming language in {target_role} roles. It's essential for data manipulation, analysis, machine learning, and automation.",
        "SQL": f"SQL is crucial for {target_role} because you'll constantly need to extract and analyze data from databases. Most companies store their data in relational databases.",
        "Statistics": f"Statistics is the mathematical foundation of data analysis. As a {target_role}, you'll use statistical concepts daily — from hypothesis testing to understanding model performance.",
        "Probability": f"Probability theory underpins many machine learning algorithms. Understanding distributions, Bayes' theorem, and expected values is essential for a {target_role}.",
        "NumPy": "NumPy provides the numerical computing foundation. It's the backbone of scientific Python — Pandas, scikit-learn, and TensorFlow all build on NumPy arrays.",
        "Pandas": "Pandas is the go-to tool for data manipulation. You'll use it to clean, transform, and analyze datasets in virtually every data project.",
        "Data Cleaning": "Real-world data is messy. Data cleaning typically takes 60-80% of a data professional's time. This skill is absolutely essential.",
        "Data Visualization": "Communicating insights through visualizations is a core skill. Charts and graphs make complex data understandable for stakeholders.",
        "Machine Learning": f"Machine Learning is the core technical skill for a {target_role}. It enables you to build predictive models and extract insights from data.",
        "Deep Learning": "Deep Learning extends ML with neural networks capable of handling complex patterns in images, text, and sequences.",
        "HTML": "HTML is the foundation of all web content. Every web page you see is built with HTML — it's the essential first step.",
        "CSS": "CSS controls how websites look. Modern CSS includes flexbox, grid, animations, and responsive design — all critical for professional web development.",
        "JavaScript": "JavaScript is the programming language of the web. It powers interactivity, dynamic content, and modern frontend frameworks.",
        "React": "React is the most popular frontend library. It's used by companies like Meta, Netflix, and Airbnb. Learning React makes you highly employable.",
        "Git": "Git is essential for any developer. It tracks code changes, enables collaboration, and is used in virtually every professional software project.",
        "REST APIs": "APIs connect frontend and backend systems. Understanding REST APIs is crucial for building and consuming web services.",
        "Testing": "Testing ensures your code works correctly. It's a professional skill that companies value highly.",
        "Deployment": "Knowing how to deploy applications means you can take projects from development to production — a complete skill set.",
        "NLP": "Natural Language Processing lets you work with text data — sentiment analysis, chatbots, text classification, and more.",
    }
    return contexts.get(skill_name, f"{skill_name} is an important skill for becoming a {target_role}. It builds on your existing knowledge and opens up new capabilities.")
