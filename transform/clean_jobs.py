import json
from pathlib import Path

import pandas as pd

from config import RAW_DATA, PROCESSED_DATA
from utils.logger import logger


def clean_jobs():
    RAW_DATA.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)

    try:
        json_files = sorted(RAW_DATA.glob("*.json"))

        if not json_files:
            raise FileNotFoundError("No raw JSON files found.")

        latest_file = json_files[-1]

        with open(latest_file, "r", encoding="utf-8") as file:
            jobs = json.load(file)

    except FileNotFoundError:
        logger.error("Raw JSON file not found.")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON format.")
        raise

    jobs = jobs[1:] if isinstance(jobs, list) and jobs else []

    cleaned_jobs = []
    for job in jobs:
        tags = job.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)] if tags else []

        cleaned_jobs.append(
            {
                "id": job.get("id"),
                "position": job.get("position"),
                "company": job.get("company"),
                "location": job.get("location"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "date": job.get("date"),
                "tags": ", ".join(tags),
                "description": job.get("description"),
            }
        )

    df = pd.DataFrame(cleaned_jobs)
    df.drop_duplicates(subset=["id"], inplace=True)

    output_file = PROCESSED_DATA / "clean_jobs.csv"

    try:
        df.to_csv(output_file, index=False)
    except Exception:
        logger.exception("Failed to save cleaned CSV.")
        raise

    logger.info(f"Saved {len(df)} cleaned records to {output_file}")


if __name__ == "__main__":
    clean_jobs()
