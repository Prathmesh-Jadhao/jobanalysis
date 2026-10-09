import re
from pathlib import Path

import pandas as pd

from config import PROCESSED_DATA
from utils.logger import logger

SKILL_PATTERNS = [
    ("Python", re.compile(r"\bpython\b", re.IGNORECASE)),
    ("SQL", re.compile(r"\bsql\b", re.IGNORECASE)),
    ("AWS", re.compile(r"\baws\b", re.IGNORECASE)),
    ("Spark", re.compile(r"\bspark\b", re.IGNORECASE)),
    ("Airflow", re.compile(r"\bairflow\b", re.IGNORECASE)),
    ("Docker", re.compile(r"\bdocker\b", re.IGNORECASE)),
    ("Kafka", re.compile(r"\bkafka\b", re.IGNORECASE)),
    ("Power BI", re.compile(r"\bpower\s*bi\b", re.IGNORECASE)),
    ("Tableau", re.compile(r"\btableau\b", re.IGNORECASE)),
    ("Pandas", re.compile(r"\bpandas\b", re.IGNORECASE)),
    ("Snowflake", re.compile(r"\bsnowflake\b", re.IGNORECASE)),
    ("dbt", re.compile(r"\bdbt\b", re.IGNORECASE)),
    ("Azure", re.compile(r"\bazure\b", re.IGNORECASE)),
    ("GCP", re.compile(r"\bgcp\b", re.IGNORECASE)),
]


def extract_skills():
    input_file = PROCESSED_DATA / "clean_jobs.csv"
    output_file = PROCESSED_DATA / "jobs_with_skills.csv"

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
        text = f"{row.get('description', '')} {row.get('tags', '')}".lower()
        found = []

        for skill_name, pattern in SKILL_PATTERNS:
            if pattern.search(text):
                found.append(skill_name)

        extracted_skills.append(", ".join(found))

    df["skills"] = extracted_skills

    try:
        df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(df)} records with extracted skills to {output_file}")
    except Exception:
        logger.exception("Failed to save jobs with extracted skills.")
        raise


if __name__ == "__main__":
    extract_skills()
