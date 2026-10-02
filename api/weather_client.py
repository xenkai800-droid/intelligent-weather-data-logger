"""Client for retrieving current weather data from the Open-Meteo API."""

from __future__ import annotations

from typing import Any

import requests

from logs.logger import get_logger

logger = get_logger(__name__)

class WeatherClient:
    """Fetch current weather observations from Open-Meteo."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    TIMEOUT_SECONDS = 10

    def __init__(self) -> None:
        """Initialize the weather client with a reusable HTTP session."""

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "WeatherDataLogger/1.0",
            }
        )

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, str | float]:
        """
        Retrieve current weather data for the given coordinates.

        Args:
            latitude: Location latitude in decimal degrees.
            longitude: Location longitude in decimal degrees.

        Returns:
            A dictionary containing timestamp, weather measurements,
            latitude, and longitude.

        Raises:
            ValueError: If coordinates are invalid or the API response is
                missing required current weather fields.
            RuntimeError: If the Open-Meteo request fails.
        """
        self._validate_coordinates(latitude, longitude)
        logger.info(
            "Fetching weather data for latitude=%s longitude=%s",
            latitude,
            longitude,
        )
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "pressure_msl",
                    "wind_speed_10m",
                    "precipitation",
                ]
            ),
        }

        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            payload = response.json()

            logger.info("Weather data retrieved successfully.")
        except requests.Timeout as exc:
            raise RuntimeError("Open-Meteo request timed out.") from exc
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Open-Meteo returned an HTTP error: {exc}"
            ) from exc
        except requests.RequestException as exc:
            logger.error("Weather API request failed: %s", exc)
            raise RuntimeError("Open-Meteo request failed.") from exc
        except ValueError as exc:
            raise RuntimeError("Open-Meteo returned invalid JSON.") from exc

        return self._parse_current_weather(payload, latitude, longitude)

    @staticmethod
    def _validate_coordinates(latitude: float, longitude: float) -> None:
        """Validate latitude and longitude ranges."""
        if not -90 <= latitude <= 90:
            raise ValueError("latitude must be between -90 and 90.")
        if not -180 <= longitude <= 180:
            raise ValueError("longitude must be between -180 and 180.")

    @staticmethod
    def _parse_current_weather(
        payload: dict[str, Any],
        latitude: float,
        longitude: float,
    ) -> dict[str, str | float]:
        """Parse and normalize the Open-Meteo current weather payload."""
        current = payload.get("current")
        if not isinstance(current, dict):
            raise ValueError("Open-Meteo response is missing current data.")

        required_fields = {
            "time": "timestamp",
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity",
            "pressure_msl": "pressure",
            "wind_speed_10m": "wind_speed",
            "precipitation": "precipitation",
        }

        missing_fields = [
            api_field for api_field in required_fields if api_field not in current
        ]
        if missing_fields:
            fields = ", ".join(missing_fields)
            raise ValueError(f"Open-Meteo response missing fields: {fields}.")

        return {
            "timestamp": str(current["time"]),
            "temperature": float(current["temperature_2m"]),
            "humidity": float(current["relative_humidity_2m"]),
            "pressure": float(current["pressure_msl"]),
            "wind_speed": float(current["wind_speed_10m"]),
            "precipitation": float(current["precipitation"]),
            "latitude": float(latitude),
            "longitude": float(longitude),
        }


if __name__ == "__main__":
    client = WeatherClient()
    bengaluru_latitude = 12.9716
    bengaluru_longitude = 77.5946

    weather = client.get_current_weather(
        latitude=bengaluru_latitude,
        longitude=bengaluru_longitude,
    )
    print(weather)
