import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.db import engine, SessionLocal, Base
from .models.models import *
from .database.seed import get_skills, get_resources, get_assessments, create_demo_user
from .routes import profile, goals, skills, resources, learning_path, progress, assessments, feedback, chat

app = FastAPI(
    title="AI Learning Path Recommender",
    description="Personalized learning path recommendation engine",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(profile.router)
app.include_router(goals.router)
app.include_router(skills.router)
app.include_router(resources.router)
app.include_router(learning_path.router)
app.include_router(progress.router)
app.include_router(assessments.router)
app.include_router(feedback.router)
app.include_router(chat.router)


@app.on_event("startup")
def startup():
    """Create tables and seed data on startup."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Seed skills if empty
        from .models.models import Skill as SkillModel
        if db.query(SkillModel).count() == 0:
            print("Seeding database...")
            for skill in get_skills():
                db.add(skill)
            db.commit()

            for resource in get_resources():
                db.add(resource)
            db.commit()

            for assessment in get_assessments():
                db.add(assessment)
            db.commit()

            create_demo_user(db)
            print("Database seeded successfully!")
        else:
            print("Database already seeded.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "AI Learning Path Recommender API", "version": "1.0.0"}


@app.get("/api/health")
def health():
    return {"status": "ok"}
