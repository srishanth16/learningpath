from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import Assessment, AssessmentResult, User, Progress, Resource, UserSkill, Skill
from ..schemas.schemas import AssessmentSubmit
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Assessments"])


@router.get("/assessments")
def list_assessments(db: Session = Depends(get_db)):
    assessments = db.query(Assessment).all()
    return [
        {
            "id": a.id,
            "title": a.title,
            "skill": a.skill,
            "difficulty": a.difficulty,
            "question_count": len(a.questions) if a.questions else 0,
        }
        for a in assessments
    ]


@router.get("/assessments/{assessment_id}")
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Return questions without correct answers for the quiz
    questions = []
    for q in (assessment.questions or []):
        questions.append({
            "question": q["question"],
            "options": q["options"],
        })

    return {
        "id": assessment.id,
        "title": assessment.title,
        "skill": assessment.skill,
        "difficulty": assessment.difficulty,
        "questions": questions,
    }


@router.post("/assessments/submit")
def submit_assessment(data: AssessmentSubmit, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    assessment = db.query(Assessment).filter(Assessment.id == data.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    questions = assessment.questions or []
    total = len(questions)

    if len(data.answers) != total:
        raise HTTPException(status_code=400, detail=f"Expected {total} answers, got {len(data.answers)}")

    # Grade
    score = 0
    details = []
    for i, q in enumerate(questions):
        is_correct = data.answers[i] == q["correct"]
        if is_correct:
            score += 1
        details.append({
            "question": q["question"],
            "selected": data.answers[i],
            "correct": q["correct"],
            "is_correct": is_correct,
            "explanation": q.get("explanation", ""),
        })

    percentage = round((score / total) * 100) if total > 0 else 0
    passed = percentage >= 60

    # Save result
    result = AssessmentResult(
        user_id=data.user_id,
        assessment_id=data.assessment_id,
        score=score,
        total=total,
        answers=data.answers,
        completed_at=datetime.utcnow(),
    )
    db.add(result)

    # Update skill proficiency based on score
    skill = db.query(Skill).filter(Skill.name == assessment.skill).first()
    if skill:
        user_skill = db.query(UserSkill).filter(
            UserSkill.user_id == data.user_id,
            UserSkill.skill_id == skill.id
        ).first()

        if percentage >= 80:
            boost = 20
        elif percentage >= 60:
            boost = 10
        else:
            boost = 5

        if user_skill:
            user_skill.proficiency = min(100, user_skill.proficiency + boost)
        else:
            db.add(UserSkill(
                user_id=data.user_id,
                skill_id=skill.id,
                proficiency=min(100, boost)
            ))

    db.commit()

    # Generate feedback message
    if percentage >= 80:
        feedback = f"Excellent work! You scored {score}/{total} ({percentage}%). You have a strong understanding of {assessment.skill}. You're ready to move on to the next topic!"
    elif percentage >= 60:
        feedback = f"Good job! You scored {score}/{total} ({percentage}%). You have a decent grasp of {assessment.skill}, but some additional practice would help solidify your understanding."
    else:
        feedback = f"You scored {score}/{total} ({percentage}%). It looks like {assessment.skill} needs more review. I recommend going back to the foundational resources before moving on."

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "passed": passed,
        "feedback": feedback,
        "details": details,
    }


@router.get("/assessments/results/{user_id}")
def get_user_results(user_id: int, db: Session = Depends(get_db)):
    results = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).all()
    return [
        {
            "id": r.id,
            "assessment_id": r.assessment_id,
            "assessment_title": db.query(Assessment).filter(Assessment.id == r.assessment_id).first().title if db.query(Assessment).filter(Assessment.id == r.assessment_id).first() else "",
            "score": r.score,
            "total": r.total,
            "percentage": round((r.score / r.total) * 100) if r.total > 0 else 0,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
        }
        for r in results
    ]
