import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from models import Education, FormalEducation, LearningAdjusted, OutOfSchool, GenderGap
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


@pytest.fixture(autouse=True)
def clean_tables():
    yield
    for table in reversed(Base.metadata.sorted_tables):
        with test_engine.connect() as conn:
            conn.execute(table.delete())
            conn.commit()


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# --- Seed helpers ---
def seed_education(db, entity="Kenya", code="KEN", year=2020):
    edu = Education(Entity=entity, Code=code, Year=year)
    db.add(edu)
    db.flush()
    return edu

def seed_formal(db, edu):
    row = FormalEducation(education_id=edu.id, no_formal_education=0.3, some_formal_education=0.7)
    db.add(row)
    db.commit()

def seed_learning(db, edu):
    row = LearningAdjusted(education_id=edu.id, learning_adjusted_years=7.5)
    db.add(row)
    db.commit()

def seed_out_of_school(db, edu):
    row = OutOfSchool(education_id=edu.id, out_of_school_males=1000, out_of_school_females=1200)
    db.add(row)
    db.commit()

def seed_gender_gap(db, edu):
    row = GenderGap(
        education_id=edu.id,
        tertiary_female_enrollment=0.4,
        tertiary_male_enrollment=0.5,
        secondary_female_enrollment=0.6,
        secondary_male_enrollment=0.65,
        primary_female_enrollment=0.8,
        primary_male_enrollment=0.82,
    )
    db.add(row)
    db.commit()


# --- Root ---
def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Global Education API is running"}


# --- Formal Education ---
def test_formal_education_empty(client):
    res = client.get("/formal-education")
    assert res.status_code == 200
    assert res.json() == []

def test_formal_education_returns_data(client, db):
    edu = seed_education(db)
    seed_formal(db, edu)
    res = client.get("/formal-education")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["entity"] == "Kenya"
    assert data[0]["no_formal_education"] == 0.3
    assert data[0]["some_formal_education"] == 0.7

def test_formal_education_pagination(client, db):
    for i in range(5):
        edu = seed_education(db, entity=f"Country{i}", code=f"C{i}", year=2000+i)
        seed_formal(db, edu)
    res = client.get("/formal-education?skip=2&limit=2")
    assert res.status_code == 200
    assert len(res.json()) == 2


# --- Learning Adjusted ---
def test_learning_adjusted_empty(client):
    res = client.get("/learning-adjusted")
    assert res.status_code == 200
    assert res.json() == []

def test_learning_adjusted_returns_data(client, db):
    edu = seed_education(db)
    seed_learning(db, edu)
    res = client.get("/learning-adjusted")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["learning_adjusted_years"] == 7.5

def test_learning_adjusted_pagination(client, db):
    for i in range(5):
        edu = seed_education(db, entity=f"Country{i}", code=f"C{i}", year=2000+i)
        seed_learning(db, edu)
    res = client.get("/learning-adjusted?skip=0&limit=3")
    assert res.status_code == 200
    assert len(res.json()) == 3


# --- Out of School ---
def test_out_of_school_empty(client):
    res = client.get("/out-of-school")
    assert res.status_code == 200
    assert res.json() == []

def test_out_of_school_returns_data(client, db):
    edu = seed_education(db)
    seed_out_of_school(db, edu)
    res = client.get("/out-of-school")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["out_of_school_males"] == 1000
    assert data[0]["out_of_school_females"] == 1200

def test_out_of_school_pagination(client, db):
    for i in range(5):
        edu = seed_education(db, entity=f"Country{i}", code=f"C{i}", year=2000+i)
        seed_out_of_school(db, edu)
    res = client.get("/out-of-school?skip=1&limit=2")
    assert res.status_code == 200
    assert len(res.json()) == 2


# --- Gender Gap ---
def test_gender_gap_empty(client):
    res = client.get("/gender-gap")
    assert res.status_code == 200
    assert res.json() == []

def test_gender_gap_returns_data(client, db):
    edu = seed_education(db)
    seed_gender_gap(db, edu)
    res = client.get("/gender-gap")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["tertiary_female_enrollment"] == 0.4
    assert data[0]["primary_male_enrollment"] == 0.82

def test_gender_gap_pagination(client, db):
    for i in range(5):
        edu = seed_education(db, entity=f"Country{i}", code=f"C{i}", year=2000+i)
        seed_gender_gap(db, edu)
    res = client.get("/gender-gap?skip=0&limit=4")
    assert res.status_code == 200
    assert len(res.json()) == 4