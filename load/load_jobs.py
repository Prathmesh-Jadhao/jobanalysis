import pandas as pd
from sqlalchemy.orm import Session

from database.connection import engine
from database.models import Job, Skill, JobSkill

def load_jobs():

    input_file = "data/processed/jobs_with_skills.csv"

    df = pd.read_csv(input_file)

    with Session(engine) as session:

        inserted_jobs = 0
        inserted_skills = 0

        for _, row in df.iterrows():

            # Prevent duplicates
            existing_job = session.get(Job, int(row["id"]))

            if existing_job:
                continue

            job = Job(
                id=int(row["id"]),
                position=row.get("position"),
                company=row.get("company"),
                location=row.get("location"),
                salary_min=row.get("salary_min"),
                salary_max=row.get("salary_max"),
                date=str(row.get("date")),
                description=row.get("description")
            )

            session.add(job)
            session.flush()

            inserted_jobs += 1

            # process skills
            skills = str(row.get("skills", "")).split(",")

            for skill_name in skills:

                skill_name = skill_name.strip()

                if not skill_name:
                    continue

                # Check if skill exists
                skill = (
                    session.query(Skill)
                    .filter(Skill.skill_name == skill_name)
                    .first()
                )

                if skill is None:
                    skill = Skill(skill_name=skill_name)
                    session.add(skill)
                    session.flush()
                    inserted_skills += 1

                # Create relationship
                job_skill = JobSkill(
                    job_id=job.id,
                    skill_id=skill.id
                )
                
                session.add(job_skill)

        session.commit()

    print(f"Inserted {inserted_jobs} new jobs")
    print(f"Inserted {inserted_skills} unique skills")


if __name__ == "__main__":
    load_jobs()