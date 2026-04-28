from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from src.backend.database import SessionLocal, engine, get_db
import uvicorn
from src.backend.models import Base, Education, FormalEducation, LearningAdjusted, OutOfSchool, GenderGap


app = FastAPI(title="Global Education API")

@app.get("/")
def root():
    return {"message": "Global Education API is running"}


@app.get("/formal-education")
def get_formal_education(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rows = (
        db.query(FormalEducation)
        .options(joinedload(FormalEducation.education))
        .offset(skip).limit(limit).all()
    )
    return [
        {
            "entity": r.education.Entity,
            "code":   r.education.Code,
            "year":   r.education.Year,
            "no_formal_education":   r.no_formal_education,
            "some_formal_education": r.some_formal_education,
        }
        for r in rows
    ]


@app.get("/learning-adjusted")
def get_learning_adjusted(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rows = (
        db.query(LearningAdjusted)
        .options(joinedload(LearningAdjusted.education))
        .offset(skip).limit(limit).all()
    )
    return [
        {
            "entity": r.education.Entity,
            "code":   r.education.Code,
            "year":   r.education.Year,
            "learning_adjusted_years": r.learning_adjusted_years,
        }
        for r in rows
    ]


@app.get("/out-of-school")
def get_out_of_school(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rows = (
        db.query(OutOfSchool)
        .options(joinedload(OutOfSchool.education))
        .offset(skip).limit(limit).all()
    )
    return [
        {
            "entity": r.education.Entity,
            "code":   r.education.Code,
            "year":   r.education.Year,
            "out_of_school_males":   r.out_of_school_males,
            "out_of_school_females": r.out_of_school_females,
        }
        for r in rows
    ]


@app.get("/gender-gap")
def get_gender_gap(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rows = (
        db.query(GenderGap)
        .options(joinedload(GenderGap.education))
        .offset(skip).limit(limit).all()
    )
    return [
        {
            "entity": r.education.Entity,
            "code":   r.education.Code,
            "year":   r.education.Year,
            "tertiary_female_enrollment":  r.tertiary_female_enrollment,
            "tertiary_male_enrollment":    r.tertiary_male_enrollment,
            "secondary_female_enrollment": r.secondary_female_enrollment,
            "secondary_male_enrollment":   r.secondary_male_enrollment,
            "primary_female_enrollment":   r.primary_female_enrollment,
            "primary_male_enrollment":     r.primary_male_enrollment,
        }
        for r in rows
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)