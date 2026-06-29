import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Create logs directory if it dosent exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

# Create Logger
logger = logging.getLogger("job_market_pipeline")
logger.setLevel(logging.INFO)
logger.propagate = False

# Avoid duplicate handlers if imported multiple times
if not logger.handlers:

    # File Handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    # Console Handler
    console_handler = logging.StreamHandler()

    # Common Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)