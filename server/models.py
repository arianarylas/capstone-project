from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Education(Base):
    __tablename__ = "education"

    id     = Column(Integer, primary_key=True, index=True)
    Entity = Column(String, index=True)
    Code   = Column(String, index=True)
    Year   = Column(Integer, index=True)

    # Relationships (optional, for easy ORM access)
    formal_education    = relationship("FormalEducation",    back_populates="education", uselist=False)
    learning_adjusted   = relationship("LearningAdjusted",   back_populates="education", uselist=False)
    out_of_school       = relationship("OutOfSchool",        back_populates="education", uselist=False)
    gender_gap          = relationship("GenderGap",          back_populates="education", uselist=False)


class FormalEducation(Base):
    __tablename__ = "formal_education"

    id           = Column(Integer, primary_key=True, index=True)
    education_id = Column(Integer, ForeignKey("education.id"), nullable=False, unique=True)

    no_formal_education   = Column(Float, nullable=True)
    some_formal_education = Column(Float, nullable=True)

    education = relationship("Education", back_populates="formal_education")


class LearningAdjusted(Base):
    __tablename__ = "learning_adjusted"

    id           = Column(Integer, primary_key=True, index=True)
    education_id = Column(Integer, ForeignKey("education.id"), nullable=False, unique=True)

    learning_adjusted_years = Column(Float, nullable=True)

    education = relationship("Education", back_populates="learning_adjusted")


class OutOfSchool(Base):
    __tablename__ = "out_of_school"

    id           = Column(Integer, primary_key=True, index=True)
    education_id = Column(Integer, ForeignKey("education.id"), nullable=False, unique=True)

    out_of_school_males   = Column(Float, nullable=True)
    out_of_school_females = Column(Float, nullable=True)

    education = relationship("Education", back_populates="out_of_school")


class GenderGap(Base):
    __tablename__ = "gender_gap"

    id           = Column(Integer, primary_key=True, index=True)
    education_id = Column(Integer, ForeignKey("education.id"), nullable=False, unique=True)

    tertiary_female_enrollment  = Column(Float, nullable=True)
    tertiary_male_enrollment    = Column(Float, nullable=True)
    secondary_female_enrollment = Column(Float, nullable=True)
    secondary_male_enrollment   = Column(Float, nullable=True)
    primary_female_enrollment   = Column(Float, nullable=True)
    primary_male_enrollment     = Column(Float, nullable=True)

    education = relationship("Education", back_populates="gender_gap")