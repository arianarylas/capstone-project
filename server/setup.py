import pandas as pd
from database import engine, SessionLocal
from models import Base, Education, FormalEducation, LearningAdjusted, OutOfSchool, GenderGap

def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("%", "pct", regex=False)
    )
    return df

def make_education(db, row):
    """Get or create an Education record for a given Entity/Code/Year combo."""
    edu = db.query(Education).filter_by(
        Entity=row.get("entity"),
        Code=row.get("code"),
        Year=row.get("year"),
    ).first()
    if not edu:
        edu = Education(
            Entity=row.get("entity"),
            Code=row.get("code"),
            Year=row.get("year"),
        )
        db.add(edu)
        db.flush()  # populate edu.id
    return edu

def load_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Sheet 1 - Formal Education
    if db.query(FormalEducation).first() is None:
        df = pd.read_csv("data/1- share-of-the-world-population-with-at-least-basic-education.csv")
        df = clean_columns(df)
        df = df.rename(columns={
            "share_of_population_with_no_formal_education_1820-2020":   "no_formal_education",
            "share_of_population_with_some_formal_education_1820-2020": "some_formal_education",
        })
        for _, row in df.iterrows():
            edu = make_education(db, row)
            db.add(FormalEducation(
                education_id=edu.id,
                no_formal_education=row.get("no_formal_education"),
                some_formal_education=row.get("some_formal_education"),
            ))
        db.commit()
        print("Formal Education loaded!")

    # Sheet 2 - Learning Adjusted
    if db.query(LearningAdjusted).first() is None:
        df = pd.read_csv("data/2- learning-adjusted-years-of-school-lays.csv")
        df = clean_columns(df)
        df = df.rename(columns={
            "learning-adjusted_years_of_school": "learning_adjusted_years",
        })
        for _, row in df.iterrows():
            edu = make_education(db, row)
            db.add(LearningAdjusted(
                education_id=edu.id,
                learning_adjusted_years=row.get("learning_adjusted_years"),
            ))
        db.commit()
        print("Learning Adjusted loaded!")

    # Sheet 3 - Out of School
    if db.query(OutOfSchool).first() is None:
        df = pd.read_csv("data/3- number-of-out-of-school-children.csv")
        df = clean_columns(df)
        df = df.rename(columns={
            "out-of-school_children_adolescents_and_youth_of_primary_and_secondary_school_age_male_number":   "out_of_school_males",
            "out-of-school_children_adolescents_and_youth_of_primary_and_secondary_school_age_female_number": "out_of_school_females",
        })
        for _, row in df.iterrows():
            edu = make_education(db, row)
            db.add(OutOfSchool(
                education_id=edu.id,
                out_of_school_males=row.get("out_of_school_males"),
                out_of_school_females=row.get("out_of_school_females"),
            ))
        db.commit()
        print("Out of School loaded!")

    # Sheet 4 - Gender Gap
    if db.query(GenderGap).first() is None:
        df = pd.read_csv("data/4- gender-gap-education-levels.csv")
        df = clean_columns(df)
        df = df.rename(columns={
            "combined_gross_enrolment_ratio_for_tertiary_education_female": "tertiary_female_enrollment",
            "combined_gross_enrolment_ratio_for_tertiary_education_male":   "tertiary_male_enrollment",
            "combined_total_net_enrolment_rate_secondary_male":             "secondary_male_enrollment",
            "combined_total_net_enrolment_rate_secondary_female":           "secondary_female_enrollment",
            "combined_total_net_enrolment_rate_primary_female":             "primary_female_enrollment",
            "combined_total_net_enrolment_rate_primary_male":               "primary_male_enrollment",
        })
        for _, row in df.iterrows():
            edu = make_education(db, row)
            db.add(GenderGap(
                education_id=edu.id,
                tertiary_female_enrollment=row.get("tertiary_female_enrollment"),
                tertiary_male_enrollment=row.get("tertiary_male_enrollment"),
                secondary_male_enrollment=row.get("secondary_male_enrollment"),
                secondary_female_enrollment=row.get("secondary_female_enrollment"),
                primary_female_enrollment=row.get("primary_female_enrollment"),
                primary_male_enrollment=row.get("primary_male_enrollment"),
            ))
        db.commit()
        print("Gender Gap loaded!")

    db.close()
    print("All data loaded successfully!")

if __name__ == "__main__":
    load_data()