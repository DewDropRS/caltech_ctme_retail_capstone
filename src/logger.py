# ============================================================
# logger.py
# Configures structured JSON logging with a rotating file handler.
# Import get_logger() in any module to get a named logger instance.
# ============================================================

import logging
import logging.handlers
from pythonjsonlogger import jsonlogger

from src.config import LOG_FILE, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def get_logger(name: str) -> logging.Logger:
    # Create a logger with the given module name (e.g. "data_cleaning")
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger is called more than once
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Rotating file handler — writes logs to pipeline.log, rotates at 5MB,
    # keeps the 3 most recent log files
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )

    # JSON formatter — each log entry is a structured JSON object with
    # timestamp, log level, module name, and message
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    # Console handler — also print logs to terminal during development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger