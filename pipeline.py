import time

from extract.remoteok_fetch import fetch_remoteok_jobs
from transform.clean_jobs import clean_jobs
from transform.extract_skills import extract_skills
from load.load_jobs import load_jobs
from utils.logger import logger


def run_pipeline():
    start_time = time.perf_counter()

    logger.info("=" * 60)
    logger.info("Starting Job Market Analytics Pipeline")
    logger.info("=" * 60)

    try:
        fetch_remoteok_jobs()
        clean_jobs()
        extract_skills()
        load_jobs()

        elapsed = time.perf_counter() - start_time

        logger.info("=" * 60)
        logger.info("Pipeline completed successfully.")
        logger.info(f"Execution time: {elapsed:.2f} seconds")
        logger.info("=" * 60)

    except Exception:
        logger.exception("Pipeline execution failed.")
        raise


if __name__ == "__main__":
    run_pipeline()