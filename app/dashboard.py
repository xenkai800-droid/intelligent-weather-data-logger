"""Streamlit dashboard for the Weather Analytics and Prediction System."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from analytics.comfort_engine import ComfortEngine
from analytics.recommendation_engine import RecommendationEngine
from analytics.risk_engine import RiskEngine
from api.weather_client import WeatherClient
from database.database_manager import DatabaseManager
from database.schema import create_database
from ml.predictor import ComfortPredictor
from visualizations.charts import WeatherCharts


DB_PATH = "data/weather.db"
MODEL_PATH = "ml/comfort_model.joblib"
ENCODER_PATH = "ml/comfort_model_encoder.joblib"


class WeatherDashboard:
    """Coordinate dashboard UI, data access, analytics, and visualizations."""

    def __init__(self, db_path: str) -> None:
        """
        Initialize dashboard dependencies.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = Path(db_path)
        create_database(str(self.db_path))
        self.database_manager = DatabaseManager(str(self.db_path))
        self.weather_client = WeatherClient()
        self.comfort_engine = ComfortEngine()
        self.risk_engine = RiskEngine()
        self.recommendation_engine = RecommendationEngine()
        self.charts = WeatherCharts(str(self.db_path))

    def render(self) -> None:
        """Render the full Streamlit dashboard."""
        st.set_page_config(
            page_title="Weather Analytics & Prediction System",
            layout="wide",
        )

        st.title("Weather Analytics & Prediction System")
        latitude, longitude, fetch_weather = self._render_sidebar()

        if fetch_weather:
            self._render_current_weather(latitude, longitude)

        self._render_historical_analytics()
        self._render_database_summary()

    @staticmethod
    def _render_sidebar() -> tuple[float, float, bool]:
        """
        Render location input controls.

        Returns:
            Latitude, longitude, and whether the fetch button was clicked.
        """

        city_coordinates = {
            "Bengaluru": (12.9716, 77.5946),
            "Mumbai": (19.0760, 72.8777),
            "Chennai": (13.0827, 80.2707),
            "Delhi": (28.6139, 77.2090),
            "Hyderabad": (17.3850, 78.4867),
            "Kolkata": (22.5726, 88.3639),
        }

        st.sidebar.header("Location Input")

        selected_city = st.sidebar.selectbox(
            "Select City",
            list(city_coordinates.keys()),
        )

        latitude, longitude = city_coordinates[selected_city]

        st.sidebar.write(f"Latitude: {latitude}")
        st.sidebar.write(f"Longitude: {longitude}")

        fetch_weather = st.sidebar.button(
            "Fetch Current Weather"
        )

        return latitude, longitude, fetch_weather

    def _render_current_weather(self, latitude: float, longitude: float) -> None:
        """
        Fetch and render current weather plus derived analytics.

        Args:
            latitude: Selected latitude.
            longitude: Selected longitude.
        """
        try:
            weather = self.weather_client.get_current_weather(
                latitude=latitude,
                longitude=longitude,
            )

        except (RuntimeError, ValueError) as exc:
            st.error(f"Unable to fetch current weather: {exc}")
            return

        st.header("Current Weather")
        metric_columns = st.columns(5)
        metric_columns[0].metric("Temperature", f"{weather['temperature']} C")
        metric_columns[1].metric("Humidity", f"{weather['humidity']}%")
        metric_columns[2].metric("Pressure", f"{weather['pressure']} hPa")
        metric_columns[3].metric("Wind Speed", f"{weather['wind_speed']} km/h")
        metric_columns[4].metric(
            "Precipitation",
            f"{weather['precipitation']} mm",
        )

        self._render_weather_analytics(weather)
        self._render_ml_prediction(weather)

    def _render_weather_analytics(self, weather: dict[str, float | str]) -> None:
        """
        Render rule-based analytics, risks, and recommendations.

        Args:
            weather: Current weather dictionary returned by WeatherClient.
        """
        temperature = float(weather["temperature"])
        humidity = float(weather["humidity"])
        wind_speed = float(weather["wind_speed"])
        precipitation = float(weather["precipitation"])

        try:
            comfort = self.comfort_engine.analyze_weather(
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
            )
            risks = self.risk_engine.analyze_risks(
                temperature=temperature,
                humidity=humidity,
                precipitation=precipitation,
                wind_speed=wind_speed,
            )
            recommendations = self.recommendation_engine.generate_recommendations(
                temperature=temperature,
                dehydration_risk=str(risks["dehydration_risk"]),
                outdoor_activity_risk=str(risks["outdoor_activity_risk"]),
            )
        except (TypeError, ValueError) as exc:
            st.error(f"Unable to analyze current weather: {exc}")
            return

        st.header("Analytics")
        analytics_columns = st.columns(2)
        analytics_columns[0].metric("Comfort Score", comfort["comfort_score"])
        analytics_columns[1].metric(
            "Comfort Category",
            str(comfort["comfort_category"]),
        )

        st.header("Risk Assessment")
        risk_columns = st.columns(3)
        risk_columns[0].metric("Heat Stress Risk", risks["heat_stress_risk"])
        risk_columns[1].metric("Dehydration Risk", risks["dehydration_risk"])
        risk_columns[2].metric(
            "Outdoor Activity Risk",
            risks["outdoor_activity_risk"],
        )

        st.header("Recommendations")
        recommendation_columns = st.columns(3)
        recommendation_columns[0].info(
            recommendations["hydration_recommendation"]
        )
        recommendation_columns[1].info(
            recommendations["clothing_recommendation"]
        )
        recommendation_columns[2].info(
            recommendations["activity_recommendation"]
        )

    @staticmethod
    def _render_ml_prediction(weather: dict[str, float | str]) -> None:
        """
        Render ML comfort prediction for current weather.

        Args:
            weather: Current weather dictionary returned by WeatherClient.
        """
        st.header("ML Prediction")

        try:
            predictor = ComfortPredictor(
                model_path=MODEL_PATH,
                encoder_path=ENCODER_PATH,
            )
            prediction = predictor.predict_comfort_category(
                temperature=float(weather["temperature"]),
                humidity=float(weather["humidity"]),
                wind_speed=float(weather["wind_speed"]),
            )
        except (FileNotFoundError, RuntimeError, TypeError, ValueError) as exc:
            st.error(f"Unable to generate ML prediction: {exc}")
            return

        prediction_columns = st.columns(2)
        prediction_columns[0].metric(
            "Predicted Comfort Category",
            prediction["predicted_comfort_category"],
        )
        prediction_columns[1].metric(
            "Prediction Confidence",
            f"{prediction['prediction_confidence']}%",
        )

    def _render_historical_analytics(self) -> None:
        """Render historical Plotly analytics charts."""
        st.header("Historical Analytics")

        try:
            temperature_chart = self.charts.temperature_trend()
            comfort_score_chart = self.charts.comfort_score_trend()
            category_chart = self.charts.comfort_category_distribution()
            risk_chart = self.charts.risk_distribution()
        except RuntimeError as exc:
            st.error(f"Unable to load historical analytics: {exc}")
            return

        chart_left, chart_right = st.columns(2)
        chart_left.plotly_chart(temperature_chart, use_container_width=True)
        chart_right.plotly_chart(comfort_score_chart, use_container_width=True)

        distribution_left, distribution_right = st.columns(2)
        distribution_left.plotly_chart(category_chart, use_container_width=True)
        distribution_right.plotly_chart(risk_chart, use_container_width=True)

    def _render_database_summary(self) -> None:
        """Render database summary metrics."""
        st.header("Database Summary")

        try:
            summary = self._get_database_summary()
        except RuntimeError as exc:
            st.error(f"Unable to load database summary: {exc}")
            return

        summary_columns = st.columns(3)
        summary_columns[0].metric(
            "Total Observations",
            summary["total_observations"],
        )
        summary_columns[1].metric(
            "Number of Locations",
            summary["location_count"],
        )
        summary_columns[2].metric(
            "Latest Observation Timestamp",
            summary["latest_timestamp"] or "N/A",
        )

    def _get_database_summary(self) -> dict[str, Any]:
        """
        Load database summary statistics.

        Returns:
            Dictionary containing observation count, location count, and latest
            observation timestamp.

        Raises:
            RuntimeError: If summary data cannot be loaded.
        """
        try:
            total_observations = len(
                self.database_manager.get_all_observations()
            )

            with sqlite3.connect(self.db_path) as connection:
                location_count = pd.read_sql_query(
                    "SELECT COUNT(*) AS count FROM locations;",
                    connection,
                ).iloc[0]["count"]
                latest_timestamp = pd.read_sql_query(
                    """
                    SELECT MAX(timestamp) AS latest_timestamp
                    FROM weather_observations;
                    """,
                    connection,
                ).iloc[0]["latest_timestamp"]
        except (RuntimeError, sqlite3.Error, pd.errors.DatabaseError) as exc:
            raise RuntimeError("Failed to load database summary.") from exc

        return {
            "total_observations": int(total_observations),
            "location_count": int(location_count),
            "latest_timestamp": latest_timestamp,
        }


if __name__ == "__main__":
    dashboard = WeatherDashboard(DB_PATH)
    dashboard.render()
