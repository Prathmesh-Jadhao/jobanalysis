import pandas as pd
from sqlalchemy.orm import Session

from config import PROCESSED_DATA
from database.connection import engine
from database.models import Job, Skill, JobSkill
from utils.logger import logger


def load_jobs():
    input_file = PROCESSED_DATA / "jobs_with_skills.csv"

    try:
        jobs_df = pd.read_csv(input_file)
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        raise
    except Exception:
        logger.exception("Failed to read processed CSV.")
        raise

    inserted_jobs = 0
    inserted_skills = 0
    skipped_duplicates = 0

    with Session(engine) as session:
        try:
            existing_job_ids = {job_id for (job_id,) in session.query(Job.id).all()}
            existing_skill_map = {skill.skill_name: skill for skill in session.query(Skill).all()}

            for _, job_row in jobs_df.iterrows():
                job_id = int(job_row["id"])

                if job_id in existing_job_ids:
                    skipped_duplicates += 1
                    continue

                job = Job(
                    id=job_id,
                    position=job_row.get("position"),
                    company=job_row.get("company"),
                    location=job_row.get("location"),
                    salary_min=int(job_row["salary_min"]) if pd.notna(job_row.get("salary_min")) else None,
                    salary_max=int(job_row["salary_max"]) if pd.notna(job_row.get("salary_max")) else None,
                    date=str(job_row.get("date")) if pd.notna(job_row.get("date")) else None,
                    description=job_row.get("description"),
                )

                session.add(job)
                session.flush()
                inserted_jobs += 1
                existing_job_ids.add(job_id)

                raw_skills = str(job_row.get("skills", "")).split(",")
                skill_names = {skill_name.strip() for skill_name in raw_skills if skill_name.strip()}

                for skill_name in skill_names:
                    skill = existing_skill_map.get(skill_name)

                    if skill is None:
                        skill = Skill(skill_name=skill_name)
                        session.add(skill)
                        session.flush()
                        existing_skill_map[skill_name] = skill
                        inserted_skills += 1

                    session.add(JobSkill(job_id=job.id, skill_id=skill.id))

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
