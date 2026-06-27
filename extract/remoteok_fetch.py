import requests
import json
from datetime import datetime
from pathlib import Path

def fetch_remoteok_jobs():
    """Fetch jobs from RemoteOK API"""

    url = "https://remoteok.com/api"

    headers = {
        "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        jobs = response.json()

        # create raw data directory if it doesn't exist
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)

        # create filename with todays date
        file_name = f"jobs_{datetime.now().strftime('%Y-%m-%d')}.json"

        output_path = raw_dir / file_name

        # save raw JSON
        with open(output_path, "w") as f:
            json.dump(jobs, f, indent=4)

        print(f"Saved {len(jobs)} jobs to {output_path}")

    else:
        print(f"Failed to fetch jobs. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_remoteok_jobs()