from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ── Profile ──────────────────────────────────────────
class SkillInput(BaseModel):
    name: str
    proficiency: int = 0  # 0-100


class ProfileCreate(BaseModel):
    name: str
    email: str
    education: str = ""
    experience_level: str = "beginner"
    weekly_hours: int = 5
    learning_preferences: List[str] = []
    current_role: str = ""
    interests: List[str] = []
    skills: List[SkillInput] = []
    goal: str = ""


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    education: Optional[str] = None
    experience_level: Optional[str] = None
    weekly_hours: Optional[int] = None
    learning_preferences: Optional[List[str]] = None
    current_role: Optional[str] = None
    interests: Optional[List[str]] = None
    skills: Optional[List[SkillInput]] = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    education: str
    experience_level: str
    weekly_hours: int
    learning_preferences: List[str]
    current_role: str
    interests: List[str]
    skills: List[dict]
    goals: List[dict]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Goals ────────────────────────────────────────────
class GoalCreate(BaseModel):
    user_id: int
    goal_text: str
    target_role: str = ""


class GoalAnalysisRequest(BaseModel):
    user_id: int
    goal_text: str


class GoalAnalysisResponse(BaseModel):
    target_role: str
    required_skills: List[str]
    current_skills: List[dict]
    skill_gaps: List[str]
    suggested_sequence: List[str]
    estimated_difficulty: str
    suggested_projects: List[str]
    suggested_assessments: List[str]


# ── Skills ───────────────────────────────────────────
class SkillGapResponse(BaseModel):
    current_skills: List[dict]
    skill_gaps: List[dict]
    priority_skills: List[dict]
    strong: List[dict]
    intermediate: List[dict]
    needs_improvement: List[dict]
    missing: List[dict]


# ── Resources ────────────────────────────────────────
class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str
    domain: str
    skill: str
    difficulty: str
    estimated_hours: float
    type: str
    prerequisites: List[str]
    url: str
    rating: float
    tags: List[str]

    class Config:
        from_attributes = True


# ── Learning Path ────────────────────────────────────
class GeneratePathRequest(BaseModel):
    user_id: int


class PathItemUpdate(BaseModel):
    status: str  # locked, available, in_progress, completed


class LearningPathItemResponse(BaseModel):
    id: int
    resource_id: int
    resource: Optional[ResourceResponse] = None
    phase: int
    order: int
    status: str
    reason: str

    class Config:
        from_attributes = True


class LearningPathResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    phases: List[dict]
    milestones: List[dict]
    items: List[LearningPathItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Progress ─────────────────────────────────────────
class ProgressUpdate(BaseModel):
    user_id: int
    resource_id: int
    progress_pct: int = 0
    completed: bool = False


class DashboardResponse(BaseModel):
    user_name: str
    overall_progress: float
    current_goal: Optional[str]
    current_milestone: Optional[str]
    skills_developed: List[dict]
    learning_streak: int
    hours_learned: float
    completed_resources: int
    total_resources: int
    next_action: Optional[dict]
    upcoming_milestone: Optional[str]
    recommended_projects: List[dict]


# ── Assessments ──────────────────────────────────────
class AssessmentSubmit(BaseModel):
    user_id: int
    assessment_id: int
    answers: List[int]  # indices of selected options


class AssessmentResultResponse(BaseModel):
    score: int
    total: int
    percentage: float
    passed: bool
    feedback: str
    details: List[dict]


# ── Feedback ─────────────────────────────────────────
class FeedbackCreate(BaseModel):
    user_id: int
    resource_id: int
    rating: int = 5
    difficulty_rating: str = "just_right"
    helpful: bool = True
    comment: str = ""


# ── Chat ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    user_id: int
    message: str


class ChatResponse(BaseModel):
    response: str
    suggested_questions: List[str] = []
