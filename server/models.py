from sqlalchemy import Column, Integer, String, Float
from database import Base

class BaseEducation(Base):
    __abstract__ = True

    id     = Column(Integer, primary_key=True, index=True)
    Entity = Column(String, index=True)
    Code   = Column(String, index=True)
    Year   = Column(Integer, index=True)

class FormalEducation(BaseEducation):
    __tablename__ = "formal_education"

    no_formal_education   = Column(Float, nullable=True)
    some_formal_education = Column(Float, nullable=True)

class LearningAdjusted(BaseEducation):
    __tablename__ = "learning_adjusted"

    learning_adjusted_years = Column(Float, nullable=True)

class OutOfSchool(BaseEducation):
    __tablename__ = "out_of_school"

    out_of_school_males   = Column(Float, nullable=True)
    out_of_school_females = Column(Float, nullable=True)

class GenderGap(BaseEducation):
    __tablename__ = "gender_gap"

    tertiary_female_enrollment = Column(Float, nullable=True)
    tertiary_male_enrollment   = Column(Float, nullable=True)
    secondary_female_enrollment = Column(Float, nullable=True)
    secondary_male_enrollment   = Column(Float, nullable=True)
    primary_female_enrollment     = Column(Float, nullable=True)
    primary_male_enrollment       = Column(Float, nullable=True)