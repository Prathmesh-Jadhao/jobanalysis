import requests
import json
from datetime import datetime
from pathlib import Path
from config import RAW_DATA
from utils.logger import logger

def fetch_remoteok_jobs():
    """Fetch jobs from RemoteOK API"""

    url = "https://remoteok.com/api"

    headers = {
        "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        jobs = response.json()

        # Create filename with today's date
        output_filename = f"jobs_{datetime.now().strftime('%Y-%m-%d')}.json"
        output_path = RAW_DATA / output_filename

        # Save raw JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4, ensure_ascii=False)

        return {
            "records": len(jobs),
            "file": output_path
        }

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise

    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise

    except requests.exceptions.Timeout as e:
        logger.error(f"Request timed out: {e}")
        raise

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error while fetching jobs.")
        raise

if __name__ == "__main__":
    fetch_remoteok_jobs()