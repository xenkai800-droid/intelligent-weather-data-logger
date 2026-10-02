"""Automated weather collection scheduler."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import schedule

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.weather_client import WeatherClient
from config.settings import Settings
from database.database_manager import DatabaseManager
from logs.logger import get_logger
from scripts.populate_training_data import DataEnrichmentPipeline

logger = get_logger(__name__)


class WeatherScheduler:
    """Automated weather collection and enrichment scheduler."""

    def __init__(self) -> None:
        self.settings = Settings()

        self.weather_client = WeatherClient()

        self.database_manager = DatabaseManager(
            str(self.settings.get_database_path())
        )

        self.pipeline = DataEnrichmentPipeline(
            str(self.settings.get_database_path())
        )

    def collect_weather(self) -> None:
        """
        Execute one weather collection cycle.
        """

        logger.info("Starting scheduled weather collection.")

        try:
            latitude = self.settings.get_default_latitude()
            longitude = self.settings.get_default_longitude()
            city_name = self.settings.get_default_city()

            weather_data = self.weather_client.get_current_weather(
                latitude=latitude,
                longitude=longitude,
            )

            location_id = self.database_manager.add_location(
                city_name=city_name,
                latitude=latitude,
                longitude=longitude,
            )

            if self.database_manager.observation_exists(
                location_id=location_id,
                timestamp=weather_data["timestamp"],
            ):
                logger.info(
                    "Observation already exists for timestamp=%s. Skipping insert.",
                    weather_data["timestamp"],
                )
                return

            observation_id = (
                self.database_manager.add_weather_observation(
                    observation_data=weather_data,
                    location_id=location_id,
                )
            )

            logger.info(
                "Weather observation stored. id=%s",
                observation_id,
            )

            self.pipeline.run()

            logger.info(
                "Scheduled weather collection completed successfully."
            )

        except Exception as exc:
            logger.error(
                "Scheduled weather collection failed: %s",
                exc,
            )

    def start(self) -> None:
        """
        Start the scheduler loop.
        """

        interval_minutes = (
            self.settings.get_scheduler_interval()
        )

        logger.info(
            "Weather scheduler started. Interval=%s minutes",
            interval_minutes,
        )

        schedule.every(interval_minutes).minutes.do(
            self.collect_weather
        )

        self.collect_weather()

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    scheduler = WeatherScheduler()
    scheduler.start()