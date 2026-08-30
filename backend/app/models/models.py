from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    education = Column(String(100), default="")
    experience_level = Column(String(50), default="beginner")
    weekly_hours = Column(Integer, default=5)
    learning_preferences = Column(JSON, default=list)
    current_role = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    interests = relationship("UserInterest", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("LearningGoal", back_populates="user", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")


class UserInterest(Base):
    __tablename__ = "user_interests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interest = Column(String(100), nullable=False)

    user = relationship("User", back_populates="interests")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    domain = Column(String(100), nullable=False)
    description = Column(Text, default="")

    user_skills = relationship("UserSkill", back_populates="skill")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency = Column(Integer, default=0)  # 0-100

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")


class LearningGoal(Base):
    __tablename__ = "learning_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal_text = Column(Text, nullable=False)
    target_role = Column(String(200), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="goals")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, default="")
    domain = Column(String(100), nullable=False)
    skill = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)  # beginner, intermediate, advanced
    estimated_hours = Column(Float, default=1.0)
    type = Column(String(50), nullable=False)  # course, video, article, tutorial, project, quiz, assessment
    prerequisites = Column(JSON, default=list)
    url = Column(String(500), default="")
    rating = Column(Float, default=4.0)
    tags = Column(JSON, default=list)


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, default="")
    phases = Column(JSON, default=list)
    milestones = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="learning_paths")
    items = relationship("LearningPathItem", back_populates="learning_path", cascade="all, delete-orphan")


class LearningPathItem(Base):
    __tablename__ = "learning_path_items"

    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    phase = Column(Integer, default=1)
    order = Column(Integer, default=0)
    status = Column(String(50), default="locked")  # locked, available, in_progress, completed
    reason = Column(Text, default="")

    learning_path = relationship("LearningPath", back_populates="items")
    resource = relationship("Resource")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    progress_pct = Column(Integer, default=0)  # 0-100
    completed = Column(Boolean, default=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progress")
    resource = relationship("Resource")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    skill = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="beginner")
    questions = Column(JSON, default=list)
    # questions format: [{"question": "...", "options": ["a","b","c","d"], "correct": 0, "explanation": "..."}]


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    score = Column(Integer, default=0)
    total = Column(Integer, default=0)
    answers = Column(JSON, default=list)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessment_results")
    assessment = relationship("Assessment")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    rating = Column(Integer, default=5)  # 1-5
    difficulty_rating = Column(String(50), default="just_right")  # too_easy, just_right, too_difficult
    helpful = Column(Boolean, default=True)
    comment = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
    resource = relationship("Resource")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_messages")
