"""Plotly chart utilities for weather analytics."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px


class WeatherCharts:
    """Create Plotly charts from weather observation data."""

    def __init__(self, db_path: str) -> None:
        """
        Initialize the chart service.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = Path(db_path)

    def load_data(self) -> pd.DataFrame:
        """
        Load weather observation data for visualization.

        Returns:
            DataFrame containing weather metrics and comfort fields sorted by
            timestamp ascending.

        Raises:
            RuntimeError: If data cannot be loaded from SQLite.
        """
        query = """
            SELECT
                timestamp,
                temperature,
                humidity,
                wind_speed,
                precipitation,
                comfort_score,
                comfort_category
            FROM weather_observations
            ORDER BY timestamp ASC;
        """

        return self._read_query(query)

    def temperature_trend(self) -> Any:
        """
        Create a temperature trend line chart.

        Returns:
            Plotly figure showing temperature over time.
        """
        data = self.load_data()
        return px.line(
            data,
            x="timestamp",
            y="temperature",
            title="Temperature Trend",
        )

    def humidity_trend(self) -> Any:
        """
        Create a humidity trend line chart.

        Returns:
            Plotly figure showing humidity over time.
        """
        data = self.load_data()
        return px.line(
            data,
            x="timestamp",
            y="humidity",
            title="Humidity Trend",
        )

    def comfort_score_trend(self) -> Any:
        """
        Create a comfort score trend line chart.

        Returns:
            Plotly figure showing comfort score over time.
        """
        data = self.load_data()
        return px.line(
            data,
            x="timestamp",
            y="comfort_score",
            title="Comfort Score Trend",
        )

    def comfort_category_distribution(self) -> Any:
        """
        Create a comfort category distribution bar chart.

        Returns:
            Plotly figure showing counts by comfort category.
        """
        data = self.load_data()
        category_counts = (
            data["comfort_category"]
            .dropna()
            .value_counts()
            .rename_axis("comfort_category")
            .reset_index(name="count")
        )

        return px.bar(
            category_counts,
            x="comfort_category",
            y="count",
            title="Comfort Category Distribution",
        )

    def precipitation_trend(self) -> Any:
        """
        Create a precipitation trend line chart.

        Returns:
            Plotly figure showing precipitation over time.
        """
        data = self.load_data()
        return px.line(
            data,
            x="timestamp",
            y="precipitation",
            title="Precipitation Trend",
        )

    def risk_distribution(self) -> Any:
        """
        Create a heat stress risk distribution bar chart.

        Returns:
            Plotly figure showing counts by heat stress risk level.

        Raises:
            RuntimeError: If risk data cannot be loaded from SQLite.
        """
        query = """
            SELECT heat_stress_risk
            FROM weather_observations
            WHERE heat_stress_risk IS NOT NULL;
        """
        data = self._read_query(query)
        risk_counts = (
            data["heat_stress_risk"]
            .value_counts()
            .rename_axis("heat_stress_risk")
            .reset_index(name="count")
        )

        return px.bar(
            risk_counts,
            x="heat_stress_risk",
            y="count",
            title="Heat Stress Risk Distribution",
        )

    def _read_query(self, query: str) -> pd.DataFrame:
        """
        Read a SQLite query into a pandas DataFrame.

        Args:
            query: SQL query to execute.

        Returns:
            Query results as a DataFrame.

        Raises:
            RuntimeError: If the query cannot be executed.
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                return pd.read_sql_query(query, connection)
        except (sqlite3.Error, pd.errors.DatabaseError) as exc:
            raise RuntimeError("Failed to load chart data from database.") from exc


if __name__ == "__main__":
    charts = WeatherCharts("data/weather.db")
    weather_data = charts.load_data()
    print(f"Number of rows loaded: {len(weather_data)}")

    charts.temperature_trend()
    print("Chart created successfully.")
