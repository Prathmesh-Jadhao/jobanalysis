import json
import pandas as pd
from pathlib import Path

def clean_jobs():
    #locate the latest raw file
    raw_dir = Path("data/raw")
    latest_file = sorted(raw_dir.glob("*.json"))[-1]

    # Load JSOn
    with open(latest_file, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    # Skip  metadata row
    jobs = jobs[1:]

    cleaned_jobs = []

    for job in jobs:
        cleaned_jobs.append({
            "id": job.get("id"),
            "postion": job.get("postion"),
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

    # Create processed folder
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_file = processed_dir / "clean_jobs.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved {len(df)} cleaned records to {output_file}")

if __name__ == "__main__":
    clean_jobs()