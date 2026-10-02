"""Client for retrieving historical weather data from Open-Meteo."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import requests


class HistoricalWeatherClient:
    """Fetch daily historical weather observations from Open-Meteo."""

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
    TIMEOUT_SECONDS = 15
    DEFAULT_HUMIDITY = 50.0
    DEFAULT_PRESSURE = 1013.0
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self) -> None:
        """Initialize the historical weather client."""
        self.session = requests.Session()

    def get_historical_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, float | str]]:
        """
        Retrieve daily historical weather records for a location and date range.

        Args:
            latitude: Location latitude in decimal degrees.
            longitude: Location longitude in decimal degrees.
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.

        Returns:
            List of daily weather dictionaries ready for database insertion.

        Raises:
            ValueError: If coordinates or dates are invalid.
            RuntimeError: If the API request or response parsing fails.
        """
        self._validate_coordinates(latitude, longitude)
        self._validate_dates(start_date, end_date)

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ",".join(
                [
                    "temperature_2m_mean",
                    "precipitation_sum",
                    "wind_speed_10m_max",
                ]
            ),
            "timezone": "auto",
        }

        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.Timeout as exc:
            raise RuntimeError(
                "Open-Meteo historical archive request timed out."
            ) from exc
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Open-Meteo historical archive returned an HTTP error: {exc}"
            ) from exc
        except requests.RequestException as exc:
            raise RuntimeError(
                "Open-Meteo historical archive request failed."
            ) from exc
        except ValueError as exc:
            raise RuntimeError(
                "Open-Meteo historical archive returned invalid JSON."
            ) from exc

        return self._parse_response(payload)

    @staticmethod
    def _validate_coordinates(latitude: float, longitude: float) -> None:
        """
        Validate latitude and longitude values.

        Args:
            latitude: Location latitude in decimal degrees.
            longitude: Location longitude in decimal degrees.

        Raises:
            TypeError: If either coordinate is not numeric.
            ValueError: If either coordinate is outside its valid range.
        """
        HistoricalWeatherClient._validate_numeric("latitude", latitude)
        HistoricalWeatherClient._validate_numeric("longitude", longitude)

        if not -90 <= latitude <= 90:
            raise ValueError("latitude must be between -90 and 90.")
        if not -180 <= longitude <= 180:
            raise ValueError("longitude must be between -180 and 180.")

    @staticmethod
    def _validate_dates(start_date: str, end_date: str) -> None:
        """
        Validate date strings and date order.

        Args:
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.

        Raises:
            TypeError: If either date is not a string.
            ValueError: If dates are incorrectly formatted or ordered.
        """
        parsed_start_date = HistoricalWeatherClient._parse_date(
            "start_date",
            start_date,
        )
        parsed_end_date = HistoricalWeatherClient._parse_date(
            "end_date",
            end_date,
        )

        if parsed_start_date > parsed_end_date:
            raise ValueError("start_date must be before or equal to end_date.")

    @staticmethod
    def _parse_response(payload: dict[str, Any]) -> list[dict[str, float | str]]:
        """
        Parse the Open-Meteo historical archive response.

        Args:
            payload: JSON payload returned by Open-Meteo.

        Returns:
            List of normalized daily weather dictionaries.

        Raises:
            RuntimeError: If required response fields are missing or invalid.
        """
        daily = payload.get("daily")
        if not isinstance(daily, dict):
            raise RuntimeError(
                "Open-Meteo historical response is missing daily data."
            )

        required_fields = [
            "time",
            "temperature_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_max",
        ]
        missing_fields = [field for field in required_fields if field not in daily]
        if missing_fields:
            fields = ", ".join(missing_fields)
            raise RuntimeError(
                f"Open-Meteo historical response missing fields: {fields}."
            )

        times = daily["time"]
        temperatures = daily["temperature_2m_mean"]
        precipitation_values = daily["precipitation_sum"]
        wind_speeds = daily["wind_speed_10m_max"]

        arrays = [times, temperatures, precipitation_values, wind_speeds]
        if not all(isinstance(array, list) for array in arrays):
            raise RuntimeError(
                "Open-Meteo historical daily fields must be lists."
            )

        expected_length = len(times)
        if any(len(array) != expected_length for array in arrays):
            raise RuntimeError(
                "Open-Meteo historical daily fields have mismatched lengths."
            )

        records: list[dict[str, float | str]] = []
        for index, timestamp in enumerate(times):
            try:
                records.append(
                    {
                        "timestamp": str(timestamp),
                        "temperature": float(temperatures[index]),
                        "humidity": HistoricalWeatherClient.DEFAULT_HUMIDITY,
                        "pressure": HistoricalWeatherClient.DEFAULT_PRESSURE,
                        "wind_speed": float(wind_speeds[index]),
                        "precipitation": float(precipitation_values[index]),
                    }
                )
            except (TypeError, ValueError) as exc:
                raise RuntimeError(
                    "Open-Meteo historical response contains invalid "
                    f"numeric data at index {index}."
                ) from exc

        return records

    @staticmethod
    def _parse_date(field_name: str, value: str) -> datetime:
        """Parse and validate a YYYY-MM-DD date string."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")

        try:
            return datetime.strptime(value, HistoricalWeatherClient.DATE_FORMAT)
        except ValueError as exc:
            raise ValueError(
                f"{field_name} must use YYYY-MM-DD format."
            ) from exc

    @staticmethod
    def _validate_numeric(field_name: str, value: float) -> None:
        """Validate that a value is numeric and not boolean."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be a numeric value.")


if __name__ == "__main__":
    client = HistoricalWeatherClient()

    latitude = 12.9716
    longitude = 77.5946
    start_date = "2025-01-01"
    end_date = "2025-03-31"

    records = client.get_historical_weather(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
    )

    print(f"Records fetched: {len(records)}")
    if records:
        print(records[0])
