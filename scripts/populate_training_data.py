"""Populate analytical fields for weather observations."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from analytics.anomaly_engine import AnomalyEngine
from analytics.comfort_engine import ComfortEngine
from analytics.recommendation_engine import RecommendationEngine
from analytics.risk_engine import RiskEngine


class DataEnrichmentPipeline:
    """Enrich raw weather observations with analytics and recommendations."""

    HISTORICAL_AVERAGE_TEMPERATURE = 28.0

    def __init__(self, db_path: str) -> None:
        """
        Initialize the data enrichment pipeline.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = Path(db_path)
        self.comfort_engine = ComfortEngine()
        self.risk_engine = RiskEngine()
        self.recommendation_engine = RecommendationEngine()
        self.anomaly_engine = AnomalyEngine()

    def get_unprocessed_observations(self) -> list[dict[str, Any]]:
        """
        Return weather observations that have not been enriched.

        Returns:
            List of observations where comfort_score is NULL.

        Raises:
            RuntimeError: If observations cannot be retrieved.
        """
        query = """
            SELECT
                observation_id,
                temperature,
                humidity,
                wind_speed,
                precipitation
            FROM weather_observations
            WHERE comfort_score IS NULL
            ORDER BY timestamp ASC, observation_id ASC;
        """

        try:
            with self._connect() as connection:
                rows = connection.execute(query).fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as exc:
            raise RuntimeError(
                "Failed to retrieve unprocessed observations."
            ) from exc

    def enrich_observation(self, observation: dict[str, Any]) -> dict[str, Any]:
        """
        Calculate analytics and recommendations for one observation.

        Args:
            observation: Raw weather observation dictionary.

        Returns:
            Dictionary containing calculated enrichment fields.

        Raises:
            KeyError: If required observation fields are missing.
            TypeError: If required values are not numeric.
            ValueError: If required values are invalid.
        """
        temperature = float(observation["temperature"])
        humidity = float(observation["humidity"])
        wind_speed = float(observation["wind_speed"])
        precipitation = float(observation["precipitation"])

        comfort_analysis = self.comfort_engine.analyze_weather(
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
        )
        risk_analysis = self.risk_engine.analyze_risks(
            temperature=temperature,
            humidity=humidity,
            precipitation=precipitation,
            wind_speed=wind_speed,
        )
        recommendations = self.recommendation_engine.generate_recommendations(
            temperature=temperature,
            dehydration_risk=str(risk_analysis["dehydration_risk"]),
            outdoor_activity_risk=str(risk_analysis["outdoor_activity_risk"]),
        )
        anomaly_analysis = self.anomaly_engine.analyze_temperature_anomaly(
            current_temperature=temperature,
            historical_average_temperature=self.HISTORICAL_AVERAGE_TEMPERATURE,
        )

        return {
            **comfort_analysis,
            **risk_analysis,
            **recommendations,
            "anomaly_score": anomaly_analysis["anomaly_score"],
            "anomaly_flag": int(bool(anomaly_analysis["anomaly_flag"])),
        }

    def update_observation(
        self,
        observation_id: int,
        enriched_data: dict[str, Any],
    ) -> None:
        """
        Update one observation with calculated enrichment data.

        Args:
            observation_id: Weather observation ID to update.
            enriched_data: Calculated enrichment field values.

        Raises:
            RuntimeError: If the observation cannot be updated.
        """
        query = """
            UPDATE weather_observations
            SET
                comfort_score = ?,
                comfort_category = ?,
                anomaly_score = ?,
                anomaly_flag = ?,
                heat_stress_risk = ?,
                dehydration_risk = ?,
                outdoor_activity_risk = ?,
                hydration_recommendation = ?,
                clothing_recommendation = ?,
                activity_recommendation = ?
            WHERE observation_id = ?;
        """
        values = (
            enriched_data["comfort_score"],
            enriched_data["comfort_category"],
            enriched_data["anomaly_score"],
            enriched_data["anomaly_flag"],
            enriched_data["heat_stress_risk"],
            enriched_data["dehydration_risk"],
            enriched_data["outdoor_activity_risk"],
            enriched_data["hydration_recommendation"],
            enriched_data["clothing_recommendation"],
            enriched_data["activity_recommendation"],
            observation_id,
        )

        try:
            with self._connect() as connection:
                connection.execute(query, values)
                connection.commit()
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to update observation {observation_id}."
            ) from exc

    def run(self) -> None:
        """
        Enrich all unprocessed weather observations.

        Prints each processed observation ID and a final processed count.

        Raises:
            RuntimeError: If enrichment cannot be completed.
        """
        processed_count = 0
        observations = self.get_unprocessed_observations()

        for observation in observations:
            observation_id = int(observation["observation_id"])

            try:
                enriched_data = self.enrich_observation(observation)
                self.update_observation(
                    observation_id=observation_id,
                    enriched_data=enriched_data,
                )
            except (KeyError, TypeError, ValueError, RuntimeError) as exc:
                raise RuntimeError(
                    f"Failed to process observation {observation_id}."
                ) from exc

            processed_count += 1
            print(f"Processed observation: {observation_id}")

        print(f"Processed {processed_count} observations.")

    def _connect(self) -> sqlite3.Connection:
        """
        Create a SQLite connection configured for row dictionaries.

        Returns:
            Configured SQLite connection.
        """
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection


if __name__ == "__main__":
    pipeline = DataEnrichmentPipeline("data/weather.db")
    pipeline.run()
