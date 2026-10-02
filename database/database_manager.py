"""Database operations for weather locations and observations."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from logs.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manage SQLite reads and writes for the weather application."""

    def __init__(self, db_path: str) -> None:
        """
        Initialize the database manager.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def add_location(
        self,
        city_name: str,
        latitude: float,
        longitude: float,
    ) -> int:
        """
        Insert a location if it does not exist and return its ID.

        Args:
            city_name: City name for the location.
            latitude: Location latitude in decimal degrees.
            longitude: Location longitude in decimal degrees.

        Returns:
            The existing or newly created location ID.

        Raises:
            RuntimeError: If the location cannot be saved.
        """
        try:
            with self._connect() as connection:
                logger.info(
                    "Adding location: %s (%s, %s)",
                    city_name,
                    latitude,
                    longitude,
                )

                existing_location = connection.execute(
                    """
                    SELECT location_id
                    FROM locations
                    WHERE LOWER(city_name) = LOWER(?)
                        AND latitude = ?
                        AND longitude = ?;
                    """,
                    (city_name, latitude, longitude),
                ).fetchone()

                if existing_location is not None:
                    logger.info(
                        "Using existing location id=%s",
                        existing_location["location_id"],
                    )
                    return int(existing_location["location_id"])

                existing_coordinates = connection.execute(
                    """
                    SELECT location_id
                    FROM locations
                    WHERE latitude = ? AND longitude = ?;
                    """,
                    (latitude, longitude),
                ).fetchone()

                if existing_coordinates is not None:
                    logger.info(
                        "Using existing coordinates id=%s",
                        existing_coordinates["location_id"],
                    )
                    return int(existing_coordinates["location_id"])

                cursor = connection.execute(
                    """
                    INSERT INTO locations (city_name, latitude, longitude)
                    VALUES (?, ?, ?);
                    """,
                    (city_name, latitude, longitude),
                )

                connection.commit()

                logger.info(
                    "Location created with id=%s",
                    cursor.lastrowid,
                )

                return int(cursor.lastrowid)

        except sqlite3.Error as exc:
            logger.error(
                "Failed to add location to database: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to add location to database."
            ) from exc

    def add_weather_observation(
        self,
        observation_data: dict[str, Any],
        location_id: int,
    ) -> int:
        """
        Insert a weather observation and return its ID.

        Args:
            observation_data: Weather data with timestamp, temperature,
                humidity, pressure, wind_speed, and precipitation keys.
            location_id: ID of the related location.

        Returns:
            The newly created observation ID.

        Raises:
            ValueError: If required observation fields are missing.
            RuntimeError: If the observation cannot be saved.
        """
        required_fields = (
            "timestamp",
            "temperature",
            "humidity",
            "pressure",
            "wind_speed",
            "precipitation",
        )

        missing_fields = [
            field for field in required_fields
            if field not in observation_data
        ]

        if missing_fields:
            fields = ", ".join(missing_fields)
            raise ValueError(
                f"Observation data missing fields: {fields}."
            )

        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO weather_observations (
                        location_id,
                        timestamp,
                        data_source,
                        temperature,
                        humidity,
                        pressure,
                        wind_speed,
                        precipitation
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        location_id,
                        observation_data["timestamp"],
                        "Open-Meteo",
                        observation_data["temperature"],
                        observation_data["humidity"],
                        observation_data["pressure"],
                        observation_data["wind_speed"],
                        observation_data["precipitation"],
                    ),
                )

                connection.commit()

                logger.info(
                    "Weather observation inserted with id=%s",
                    cursor.lastrowid,
                )

                return int(cursor.lastrowid)

        except sqlite3.Error as exc:
            logger.error(
                "Failed to add weather observation: %s",
                exc,
            )
            raise RuntimeError(
                "Failed to add weather observation to database."
            ) from exc

    def get_recent_observations(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Return the most recent weather observation records.

        Args:
            limit: Maximum number of records to return.

        Returns:
            A list of weather observation records.

        Raises:
            ValueError: If limit is less than one.
            RuntimeError: If records cannot be retrieved.
        """
        if limit < 1:
            raise ValueError("limit must be greater than zero.")

        try:
            with self._connect() as connection:
                rows = connection.execute(
                    """
                    SELECT
                        observation_id,
                        location_id,
                        timestamp,
                        data_source,
                        temperature,
                        humidity,
                        pressure,
                        wind_speed,
                        precipitation,
                        comfort_score,
                        comfort_category,
                        anomaly_score,
                        anomaly_flag,
                        heat_stress_risk,
                        dehydration_risk,
                        outdoor_activity_risk,
                        hydration_recommendation,
                        clothing_recommendation,
                        activity_recommendation
                    FROM weather_observations
                    ORDER BY timestamp DESC, observation_id DESC
                    LIMIT ?;
                    """,
                    (limit,),
                ).fetchall()

                return [dict(row) for row in rows]

        except sqlite3.Error as exc:
            raise RuntimeError(
                "Failed to retrieve recent observations."
            ) from exc

    def get_all_observations(self) -> list[dict[str, Any]]:
        """
        Return all weather observation records.

        Returns:
            A list of all weather observation records.

        Raises:
            RuntimeError: If records cannot be retrieved.
        """
        try:
            with self._connect() as connection:
                rows = connection.execute(
                    """
                    SELECT
                        observation_id,
                        location_id,
                        timestamp,
                        data_source,
                        temperature,
                        humidity,
                        pressure,
                        wind_speed,
                        precipitation,
                        comfort_score,
                        comfort_category,
                        anomaly_score,
                        anomaly_flag,
                        heat_stress_risk,
                        dehydration_risk,
                        outdoor_activity_risk,
                        hydration_recommendation,
                        clothing_recommendation,
                        activity_recommendation
                    FROM weather_observations
                    ORDER BY timestamp ASC, observation_id ASC;
                    """
                ).fetchall()

                return [dict(row) for row in rows]

        except sqlite3.Error as exc:
            raise RuntimeError(
                "Failed to retrieve observations."
            ) from exc
    def observation_exists(
        self,
        location_id: int,
        timestamp: str,
    ) -> bool:
        """
        Check whether an observation already exists for a location
        and timestamp.

        Args:
            location_id: Location identifier.
            timestamp: Observation timestamp.

        Returns:
            True if an observation exists, otherwise False.

        Raises:
            RuntimeError: If the lookup fails.
        """
        try:
            with self._connect() as connection:
                row = connection.execute(
                    """
                    SELECT observation_id
                    FROM weather_observations
                    WHERE location_id = ?
                    AND timestamp = ?
                    LIMIT 1;
                    """,
                    (
                        location_id,
                        timestamp,
                    ),
                ).fetchone()

                return row is not None

        except sqlite3.Error as exc:
            raise RuntimeError(
                "Failed to check existing observation."
            ) from exc
    def _connect(self) -> sqlite3.Connection:
        """
        Create a SQLite connection with foreign keys enabled.

        Returns:
            A configured SQLite connection.

        Raises:
            sqlite3.Error: If the database connection cannot be created.
        """
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection


if __name__ == "__main__":
    manager = DatabaseManager("data/weather.db")

    location_id = manager.add_location(
        city_name="Bengaluru",
        latitude=12.9716,
        longitude=77.5946,
    )

    observation_id = manager.add_weather_observation(
        observation_data={
            "timestamp": "2026-01-01T10:00",
            "temperature": 25.0,
            "humidity": 60.0,
            "pressure": 1013.0,
            "wind_speed": 10.0,
            "precipitation": 0.0,
        },
        location_id=location_id,
    )

    recent_observations = manager.get_recent_observations()

    print(f"location_id: {location_id}")
    print(f"observation_id: {observation_id}")
    print(f"recent observations: {recent_observations}")