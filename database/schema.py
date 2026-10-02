"""SQLite schema management for the weather application."""

from __future__ import annotations

import sqlite3
from pathlib import Path


def create_database(db_path: str) -> None:
    """
    Create the weather application database schema.

    The function creates all required tables if they do not already exist,
    commits the schema changes, and closes the database connection safely.

    Args:
        db_path: Path to the SQLite database file.

    Raises:
        sqlite3.Error: If SQLite fails to create or update the schema.
    """
    database_path = Path(db_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON;")

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS locations (
                location_id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                UNIQUE(latitude, longitude)
            );
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_observations (
                observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_id INTEGER,
                timestamp TEXT,
                data_source TEXT,
                temperature REAL,
                humidity REAL,
                pressure REAL,
                wind_speed REAL,
                precipitation REAL,
                comfort_score REAL,
                comfort_category TEXT,
                anomaly_score REAL,
                anomaly_flag INTEGER,
                heat_stress_risk TEXT,
                dehydration_risk TEXT,
                outdoor_activity_risk TEXT,
                hydration_recommendation TEXT,
                clothing_recommendation TEXT,
                activity_recommendation TEXT,
                FOREIGN KEY (location_id)
                    REFERENCES locations (location_id)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS ml_predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER,
                prediction_timestamp TEXT,
                predicted_comfort_category TEXT,
                prediction_confidence REAL,
                FOREIGN KEY (observation_id)
                    REFERENCES weather_observations (observation_id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            """
        )

        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    create_database("data/weather.db")
    print("Database schema created successfully.")
