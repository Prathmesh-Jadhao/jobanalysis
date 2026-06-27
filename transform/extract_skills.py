import pandas as pd
from pathlib import Path

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
    input_file = Path("data/processed/clean_jobs.csv")

    df = pd.read_csv(input_file)

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

    output_file = Path("data/processed/jobs_with_skills.csv")

    df.to_csv(output_file, index=False)

    print(f"Saved {len(df)} records to {output_file}")


if __name__ == "__main__":
    extract_skills()