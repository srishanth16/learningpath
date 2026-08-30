"""
AI service module.
Uses OpenAI API if OPENAI_API_KEY is set, otherwise falls back to rule-based engine.
"""
import os
import json
from typing import Dict, Optional
from sqlalchemy.orm import Session
from ..models.models import User, LearningGoal, UserSkill, Skill, UserInterest
from ..recommender.engine import (
    detect_target_role, get_required_skills, analyze_skill_gaps,
    get_suggested_projects, get_suggested_assessments
)
from ..recommender.fallback_chat import generate_fallback_response


def _get_api_key() -> Optional[str]:
    key = os.getenv("OPENAI_API_KEY", "")
    if key and key != "your_openai_api_key_here" and len(key) > 10:
        return key
    return None


def _get_user_context(db: Session, user_id: int) -> str:
    """Build a context string about the user for the LLM."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return "No user profile found."

    goal = db.query(LearningGoal).filter(
        LearningGoal.user_id == user_id,
        LearningGoal.is_active == True
    ).first()

    skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    skill_info = []
    for us in skills:
        sk = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if sk:
            skill_info.append(f"{sk.name}: {us.proficiency}%")

    interests = db.query(UserInterest).filter(UserInterest.user_id == user_id).all()

    context = f"""Learner Profile:
- Name: {user.name}
- Experience Level: {user.experience_level}
- Education: {user.education}
- Current Role: {user.current_role}
- Weekly Learning Time: {user.weekly_hours} hours
- Learning Preferences: {', '.join(user.learning_preferences or [])}
- Interests: {', '.join(i.interest for i in interests)}
- Current Skills: {', '.join(skill_info) if skill_info else 'None listed'}
- Goal: {goal.goal_text if goal else 'Not set'}
- Target Role: {goal.target_role if goal else 'Not set'}"""

    if goal:
        target = goal.target_role or detect_target_role(goal.goal_text)
        required = get_required_skills(target)
        gaps = analyze_skill_gaps(db, user_id, required)
        context += f"\n- Skill Gaps: {', '.join(g['name'] for g in gaps.get('skill_gaps', []))}"

    return context


async def analyze_goal_with_ai(db: Session, user_id: int, goal_text: str) -> Dict:
    """Analyze a learning goal — tries OpenAI first, falls back to rules."""
    api_key = _get_api_key()

    if api_key:
        try:
            return await _openai_analyze_goal(api_key, db, user_id, goal_text)
        except Exception as e:
            print(f"OpenAI goal analysis failed, using fallback: {e}")

    # Fallback: rule-based analysis
    return _fallback_analyze_goal(db, user_id, goal_text)


def _fallback_analyze_goal(db: Session, user_id: int, goal_text: str) -> Dict:
    """Rule-based goal analysis."""
    target_role = detect_target_role(goal_text)
    required_skills = get_required_skills(target_role)
    gaps = analyze_skill_gaps(db, user_id, required_skills)

    # Determine difficulty
    gap_count = len(gaps.get("skill_gaps", []))
    total = len(required_skills)
    ratio = gap_count / total if total > 0 else 1

    if ratio > 0.8:
        difficulty = "Challenging — you have many skills to learn, but it's very achievable with consistent effort!"
    elif ratio > 0.5:
        difficulty = "Moderate — you have a solid foundation and need to fill some key gaps."
    else:
        difficulty = "Very doable — you already have most of the required skills!"

    return {
        "target_role": target_role.title(),
        "required_skills": required_skills,
        "current_skills": gaps.get("current_skills", []),
        "skill_gaps": [g["name"] for g in gaps.get("skill_gaps", [])],
        "suggested_sequence": [s["name"] for s in gaps.get("priority_skills", [])],
        "estimated_difficulty": difficulty,
        "suggested_projects": get_suggested_projects(target_role),
        "suggested_assessments": get_suggested_assessments(target_role),
    }


async def _openai_analyze_goal(api_key: str, db: Session, user_id: int, goal_text: str) -> Dict:
    """Use OpenAI to analyze the goal."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    context = _get_user_context(db, user_id)

    prompt = f"""You are a learning path advisor. Analyze this learner's goal and provide recommendations.

{context}

Goal: "{goal_text}"

Respond in this exact JSON format:
{{
    "target_role": "the career role they want",
    "required_skills": ["skill1", "skill2", ...],
    "skill_gaps": ["missing skill1", "missing skill2", ...],
    "suggested_sequence": ["first skill to learn", "second", ...],
    "estimated_difficulty": "brief difficulty assessment",
    "suggested_projects": ["project1", "project2", ...],
    "suggested_assessments": ["assessment1", "assessment2", ...]
}}"""

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert learning advisor. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    content = response.choices[0].message.content.strip()
    # Try to parse JSON from the response
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    result = json.loads(content)

    # Merge with rule-based data for robustness
    target_role = detect_target_role(goal_text)
    gaps = analyze_skill_gaps(db, user_id, get_required_skills(target_role))

    result["current_skills"] = gaps.get("current_skills", [])
    if not result.get("target_role"):
        result["target_role"] = target_role.title()

    return result


async def chat_with_ai(db: Session, user_id: int, message: str) -> Dict:
    """Handle chat messages — tries OpenAI first, falls back to rules."""
    api_key = _get_api_key()

    if api_key:
        try:
            return await _openai_chat(api_key, db, user_id, message)
        except Exception as e:
            print(f"OpenAI chat failed, using fallback: {e}")

    # Fallback
    return generate_fallback_response(db, user_id, message)


async def _openai_chat(api_key: str, db: Session, user_id: int, message: str) -> Dict:
    """Use OpenAI for chat responses."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    context = _get_user_context(db, user_id)

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly, knowledgeable learning assistant. "
                    "You help learners understand their roadmap, skills, and next steps. "
                    "Be specific to their profile and goals. Use markdown formatting. "
                    "Keep responses concise but helpful (2-4 paragraphs max).\n\n"
                    f"Learner context:\n{context}"
                )
            },
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=500
    )

    ai_response = response.choices[0].message.content.strip()

    return {
        "response": ai_response,
        "suggested_questions": [
            "What should I learn next?",
            "Can you recommend a project?",
            "How long will my roadmap take?",
            "What are my skill gaps?",
        ]
    }
