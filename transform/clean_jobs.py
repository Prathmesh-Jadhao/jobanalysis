import json
import pandas as pd
from config import RAW_DATA, PROCESSED_DATA
from utils.logger import logger

def clean_jobs():
    

    # Load JSOn
    try:
        json_files = sorted(RAW_DATA.glob("*.json"))

        if not json_files:
            raise FileNotFoundError("No raw JSON files found.")

        latest_file = json_files[-1]
        
        with open(latest_file, "r", encoding="utf-8") as f:
            jobs = json.load(f)

    except FileNotFoundError:
        logger.error("Raw JSON file not found.")
        raise

    except json.JSONDecodeError:
        logger.error("Invalid JSON format.")
        raise

    # RemoteOK API returns metadata as the first element.
    # Skip it before processing job records.
    jobs = jobs[1:] if jobs else []

    cleaned_jobs = []

    for job in jobs:
        cleaned_jobs.append({
            "id": job.get("id"),
            "position": job.get("position"),
            "company": job.get("company"),
            "location": job.get("location"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "date": job.get("date"),
            "tags": ", ".join(job.get("tags", [])),
            "description": job.get("description")
        })

    df =  pd.DataFrame(cleaned_jobs)

    # Remove duplicates
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