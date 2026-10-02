"""Prediction utilities for trained weather comfort models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd


class ComfortPredictor:
    """Load a trained model and predict comfort categories."""

    FEATURE_COLUMNS = ["temperature", "humidity", "wind_speed"]

    def __init__(self, model_path: str, encoder_path: str) -> None:
        """
        Initialize the predictor and load model artifacts.

        Args:
            model_path: Path to the trained Random Forest model artifact.
            encoder_path: Path to the trained LabelEncoder artifact.

        Raises:
            FileNotFoundError: If either artifact does not exist.
            RuntimeError: If model artifacts cannot be loaded.
        """
        self.model_path = Path(model_path)
        self.encoder_path = Path(encoder_path)
        self.model = self._load_artifact(self.model_path, "model")
        self.encoder = self._load_artifact(self.encoder_path, "encoder")

    def predict_comfort_category(
        self,
        temperature: float,
        humidity: float,
        wind_speed: float,
    ) -> dict[str, str | float]:
        """
        Predict comfort category and confidence for weather conditions.

        Args:
            temperature: Air temperature in degrees Celsius.
            humidity: Relative humidity percentage.
            wind_speed: Wind speed in kilometers per hour.

        Returns:
            Dictionary containing predicted_comfort_category and
            prediction_confidence.

        Raises:
            TypeError: If any input is not numeric.
            ValueError: If any input is outside a realistic accepted range.
            RuntimeError: If prediction fails.
        """
        self._validate_weather_inputs(
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
        )

        features = pd.DataFrame(
            [[temperature, humidity, wind_speed]],
            columns=self.FEATURE_COLUMNS,
        )

        try:
            encoded_prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            category = self.encoder.inverse_transform([encoded_prediction])[0]
            confidence = round(float(max(probabilities)) * 100, 2)
        except Exception as exc:
            raise RuntimeError("Failed to predict comfort category.") from exc

        return {
            "predicted_comfort_category": str(category),
            "prediction_confidence": confidence,
        }

    @staticmethod
    def _load_artifact(path: Path, artifact_name: str) -> Any:
        """
        Load a joblib model artifact.

        Args:
            path: Artifact path.
            artifact_name: Human-readable artifact name for errors.

        Returns:
            Loaded artifact object.

        Raises:
            FileNotFoundError: If the artifact path does not exist.
            RuntimeError: If joblib cannot load the artifact.
        """
        if not path.exists():
            raise FileNotFoundError(f"{artifact_name} artifact not found: {path}")

        try:
            return joblib.load(path)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load {artifact_name} artifact: {path}"
            ) from exc

    @staticmethod
    def _validate_weather_inputs(
        temperature: float,
        humidity: float,
        wind_speed: float,
    ) -> None:
        """Validate weather inputs before prediction."""
        ComfortPredictor._validate_numeric("temperature", temperature)
        ComfortPredictor._validate_numeric("humidity", humidity)
        ComfortPredictor._validate_numeric("wind_speed", wind_speed)

        if not -80 <= temperature <= 60:
            raise ValueError("temperature must be between -80 and 60 Celsius.")
        if not 0 <= humidity <= 100:
            raise ValueError("humidity must be between 0 and 100 percent.")
        if not 0 <= wind_speed <= 300:
            raise ValueError("wind_speed must be between 0 and 300 km/h.")

    @staticmethod
    def _validate_numeric(field_name: str, value: float) -> None:
        """Validate that a value is numeric and not boolean."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be a numeric value.")


if __name__ == "__main__":
    predictor = ComfortPredictor(
        model_path="ml/comfort_model.joblib",
        encoder_path="ml/comfort_model_encoder.joblib",
    )

    result = predictor.predict_comfort_category(
        temperature=25,
        humidity=50,
        wind_speed=10,
    )
    print(result)
