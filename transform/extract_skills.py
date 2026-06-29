import pandas as pd
from config import PROCESSED_DATA
from utils.logger import logger

SKILLS = [
    "Python",
    "SQL",
    "AWS",
    "Spark",
    "Airflow",
    "Docker",
    "Kafka",
    "Power BI",
    "Tableau",
    "Pandas",
    "Snowflake",
    "dbt",
    "Azure",
    "GCP"
]


def extract_skills():
    input_file = PROCESSED_DATA / "clean_jobs.csv"

    try:
        df = pd.read_csv(input_file)

    except FileNotFoundError:
        logger.error("Clean jobs CSV not found.")
        raise

    except Exception:
        logger.exception("Failed to read cleaned jobs CSV.")
        raise

    extracted_skills = []

    for _, row in df.iterrows():

        text = (
            str(row.get("description", "")) + " " +
            str(row.get("tags", ""))
        ).lower()

        found = []

        for skill in SKILLS:
            if skill.lower() in text:
                found.append(skill)

        extracted_skills.append(", ".join(found))

    df["skills"] = extracted_skills

    output_file = PROCESSED_DATA / "jobs_with_skills.csv"

    try:
        df.to_csv(output_file, index=False)
        logger.info(
            f"Saved {len(df)} records with extracted skills to {output_file}"
        )
    except Exception:
        logger.exception("Failed to save jobs with extracted skills.")
        raise


if __name__ == "__main__":
    extract_skills()