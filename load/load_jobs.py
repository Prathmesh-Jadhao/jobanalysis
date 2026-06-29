import pandas as pd
from sqlalchemy.orm import Session

from database.connection import engine
from database.models import Job, Skill, JobSkill
from config import PROCESSED_DATA
from utils.logger import logger

def load_jobs():

    input_file = PROCESSED_DATA / "jobs_with_skills.csv"

    try:
        jobs_df = pd.read_csv(input_file)
    
    except FileNotFoundError:
        logger.error(f"input files not found: {input_file}")
        raise

    except Exception:
        logger.exception("Failed to read processed CSV.")
        raise

    inserted_jobs = 0
    inserted_skills = 0
    skipped_duplicates = 0
    with Session(engine) as session:
        try:

            for _, job_row in jobs_df.iterrows():

                # Prevent duplicates
                existing_job = session.get(Job, int(job_row["id"]))

                if existing_job:
                    skipped_duplicates += 1
                    continue

                job = Job(
                    id=int(job_row["id"]),
                    position=job_row.get("position"),
                    company=job_row.get("company"),
                    location=job_row.get("location"),
                    salary_min=job_row.get("salary_min"),
                    salary_max=job_row.get("salary_max"),
                    date=str(job_row.get("date")),
                    description=job_row.get("description")
                )

                session.add(job)
                session.flush()

                inserted_jobs += 1

                # process skills
                skills = str(job_row.get("skills", "")).split(",")

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
                
                    session.add(
                        JobSkill(
                            job_id=job.id,
                            skill_id=skill.id
                        )
                    )

            session.commit()

            logger.info(f"Inserted {inserted_jobs} new jobs.")
            logger.info(f"Inserted {inserted_skills} unique skills.")
            logger.info(f"Skipped {skipped_duplicates} duplicate jobs.")

            return {
                "inserted_jobs": inserted_jobs,
                "inserted_skills": inserted_skills,
                "skipped_duplicates": skipped_duplicates,
            }

        except Exception:
            session.rollback()
            logger.exception("Failed to load jobs into PostgreSQL.")
            raise


if __name__ == "__main__":
    load_jobs()