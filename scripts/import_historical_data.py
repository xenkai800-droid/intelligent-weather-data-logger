"""Import historical Open-Meteo weather records into SQLite."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.historical_weather_client import HistoricalWeatherClient
from database.database_manager import DatabaseManager


class HistoricalDataImporter:
    """Import historical weather observations into the local database."""

    CITIES = [
        {
            "city_name": "Bengaluru",
            "latitude": 12.9716,
            "longitude": 77.5946,
        },
        {
            "city_name": "Delhi",
            "latitude": 28.6139,
            "longitude": 77.2090,
        },
        {
            "city_name": "Mumbai",
            "latitude": 19.0760,
            "longitude": 72.8777,
        },
        {
            "city_name": "Chennai",
            "latitude": 13.0827,
            "longitude": 80.2707,
        },
        {
            "city_name": "Kolkata",
            "latitude": 22.5726,
            "longitude": 88.3639,
        },
        {
            "city_name": "Hyderabad",
            "latitude": 17.3850,
            "longitude": 78.4867,
        },
    ]
    START_DATE = "2024-01-01"
    END_DATE = "2025-12-31"

    def __init__(self, db_path: str) -> None:
        """
        Initialize the historical data importer.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = Path(db_path)
        self.weather_client = HistoricalWeatherClient()
        self.database_manager = DatabaseManager(str(self.db_path))

    def import_city_history(self, city_config: dict[str, str | float]) -> int:
        """
        Fetch and import historical weather observations for one city.

        Args:
            city_config: City configuration with city_name, latitude, and
                longitude values.

        Existing observations for the same location and timestamp are skipped.

        Returns:
            Number of newly inserted observations.

        Raises:
            RuntimeError: If importing city records fails.
        """
        city_name = str(city_config["city_name"])
        latitude = float(city_config["latitude"])
        longitude = float(city_config["longitude"])

        print(f"Importing {city_name}...")

        try:
            records = self.weather_client.get_historical_weather(
                latitude=latitude,
                longitude=longitude,
                start_date=self.START_DATE,
                end_date=self.END_DATE,
            )
            location_id = self.database_manager.add_location(
                city_name=city_name,
                latitude=latitude,
                longitude=longitude,
            )

            inserted_count = 0
            for record in records:
                timestamp = str(record["timestamp"])

                if self._observation_exists(
                    location_id=location_id,
                    timestamp=timestamp,
                ):
                    continue

                observation_id = self.database_manager.add_weather_observation(
                    observation_data=record,
                    location_id=location_id,
                )
                inserted_count += 1
                print(f"Inserted observation: {observation_id}")

            return inserted_count
        except (KeyError, RuntimeError, ValueError, sqlite3.Error) as exc:
            raise RuntimeError(f"Failed to import data for {city_name}.") from exc

    def import_all_city_histories(self) -> None:
        """
        Import historical weather observations for all configured cities.

        Raises:
            RuntimeError: If any city import fails.
        """
        summary: dict[str, int] = {}

        for city_config in self.CITIES:
            city_name = str(city_config["city_name"])
            inserted_count = self.import_city_history(city_config)
            summary[city_name] = inserted_count

        total_inserted = sum(summary.values())

        print("## Import Summary")
        print()
        for city_name, inserted_count in summary.items():
            print(f"{city_name}: {inserted_count} inserted")
        print()
        print(f"Total inserted: {total_inserted}")

    def import_bengaluru_history(self) -> None:
        """
        Import Bengaluru historical weather observations.

        This method is retained for compatibility with older scripts.
        """
        bengaluru_config = next(
            city
            for city in self.CITIES
            if city["city_name"] == "Bengaluru"
        )
        inserted_count = self.import_city_history(bengaluru_config)
        print(f"Imported {inserted_count} historical observations.")

    def _observation_exists(self, location_id: int, timestamp: str) -> bool:
        """
        Check whether an observation already exists for a location and time.

        Args:
            location_id: Location ID to check.
            timestamp: Observation timestamp to check.

        Returns:
            True if a matching observation exists, otherwise False.

        Raises:
            sqlite3.Error: If the lookup query fails.
        """
        query = """
            SELECT 1
            FROM weather_observations
            WHERE location_id = ? AND timestamp = ?
            LIMIT 1;
        """

        with self._connect() as connection:
            row = connection.execute(query, (location_id, timestamp)).fetchone()
            return row is not None

    def _connect(self) -> sqlite3.Connection:
        """
        Create a SQLite connection with foreign keys enabled.

        Returns:
            Configured SQLite connection.
        """
        connection = sqlite3.connect(self.db_path)
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection


if __name__ == "__main__":
    importer = HistoricalDataImporter("data/weather.db")
    importer.import_all_city_histories()
