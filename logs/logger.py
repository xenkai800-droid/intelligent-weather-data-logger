from __future__ import annotations

import logging
from pathlib import Path

from config.settings import Settings


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name: Logger name.

    Returns:
        Configured logger instance.
    """
    settings = Settings()
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    log_level = settings.get_log_level().upper()
    log_file = settings.get_log_file()

    log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(getattr(logging, log_level, logging.INFO))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger


if __name__ == "__main__":
    logger = get_logger("WeatherSystem")

    logger.info("Application started.")
    logger.warning("This is a warning message.")
    logger.error("This is a test error message.")

    print("Logger initialized successfully.")