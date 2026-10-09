import json
from datetime import datetime

import requests

from config import RAW_DATA
from utils.logger import logger


def fetch_remoteok_jobs():
    """Fetch jobs from RemoteOK API."""

    url = "https://remoteok.com/api"
    headers = {
        "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        RAW_DATA.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        jobs = response.json()

        if not isinstance(jobs, list):
            raise ValueError("RemoteOK API returned an unexpected payload type.")

        records = jobs[1:] if jobs else []

        output_filename = f"jobs_{datetime.now().strftime('%Y-%m-%d')}.json"
        output_path = RAW_DATA / output_filename

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(jobs, file, indent=4, ensure_ascii=False)

        return {"records": len(records), "file": output_path}

    except requests.exceptions.HTTPError as exc:
        logger.error(f"HTTP error occurred: {exc}")
        raise
    except requests.exceptions.ConnectionError as exc:
        logger.error(f"Connection error: {exc}")
        raise
    except requests.exceptions.Timeout as exc:
        logger.error(f"Request timed out: {exc}")
        raise
    except requests.exceptions.RequestException as exc:
        logger.error(f"Request failed: {exc}")
        raise
    except ValueError as exc:
        logger.error(f"Invalid payload received from RemoteOK: {exc}")
        raise
    except Exception:
        logger.exception("Unexpected error while fetching jobs.")
        raise


if __name__ == "__main__":
    fetch_remoteok_jobs()
