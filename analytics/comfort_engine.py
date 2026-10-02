"""Rule-based weather comfort scoring engine."""

from __future__ import annotations


class ComfortEngine:
    """Calculate and classify human comfort from weather conditions."""

    MIN_SCORE = 0.0
    MAX_SCORE = 100.0

    @staticmethod
    def calculate_comfort_score(
        temperature: float,
        humidity: float,
        wind_speed: float,
    ) -> float:
        """
        Calculate a rule-based comfort score from weather measurements.

        The score starts at 100 and applies proportional penalties when
        temperature, humidity, or wind speed falls outside ideal ranges.

        Args:
            temperature: Air temperature in degrees Celsius.
            humidity: Relative humidity percentage.
            wind_speed: Wind speed in kilometers per hour.

        Returns:
            A rounded comfort score clamped between 0 and 100.

        Raises:
            ValueError: If any input is outside a realistic accepted range.
            TypeError: If any input is not numeric.
        """
        ComfortEngine._validate_weather_inputs(
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
        )

        score = 100.0

        score -= ComfortEngine._range_penalty(
            value=temperature,
            minimum=20.0,
            maximum=26.0,
            penalty_per_unit=3.0,
        )
        score -= ComfortEngine._range_penalty(
            value=humidity,
            minimum=30.0,
            maximum=60.0,
            penalty_per_unit=0.6,
        )
        score -= ComfortEngine._range_penalty(
            value=wind_speed,
            minimum=0.0,
            maximum=15.0,
            penalty_per_unit=1.2,
        )

        clamped_score = max(
            ComfortEngine.MIN_SCORE,
            min(ComfortEngine.MAX_SCORE, score),
        )
        return round(clamped_score, 2)

    @staticmethod
    def classify_comfort(score: float) -> str:
        """
        Classify a comfort score into a human-readable category.

        Args:
            score: Comfort score from 0 to 100.

        Returns:
            Comfort category name.

        Raises:
            ValueError: If score is outside 0 to 100.
            TypeError: If score is not numeric.
        """
        ComfortEngine._validate_score(score)

        if score >= 90:
            return "Excellent"
        if score >= 75:
            return "Good"
        if score >= 60:
            return "Moderate"
        if score >= 40:
            return "Poor"
        return "Extreme"

    @staticmethod
    def analyze_weather(
        temperature: float,
        humidity: float,
        wind_speed: float,
    ) -> dict[str, float | str]:
        """
        Calculate comfort score and category for weather conditions.

        Args:
            temperature: Air temperature in degrees Celsius.
            humidity: Relative humidity percentage.
            wind_speed: Wind speed in kilometers per hour.

        Returns:
            Dictionary containing comfort_score and comfort_category.
        """
        comfort_score = ComfortEngine.calculate_comfort_score(
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
        )
        comfort_category = ComfortEngine.classify_comfort(comfort_score)

        return {
            "comfort_score": comfort_score,
            "comfort_category": comfort_category,
        }

    @staticmethod
    def _range_penalty(
        value: float,
        minimum: float,
        maximum: float,
        penalty_per_unit: float,
    ) -> float:
        """Calculate a proportional penalty outside an ideal range."""
        if value < minimum:
            return (minimum - value) * penalty_per_unit
        if value > maximum:
            return (value - maximum) * penalty_per_unit
        return 0.0

    @staticmethod
    def _validate_weather_inputs(
        temperature: float,
        humidity: float,
        wind_speed: float,
    ) -> None:
        """Validate weather inputs before scoring."""
        ComfortEngine._validate_numeric("temperature", temperature)
        ComfortEngine._validate_numeric("humidity", humidity)
        ComfortEngine._validate_numeric("wind_speed", wind_speed)

        if not -80 <= temperature <= 60:
            raise ValueError("temperature must be between -80 and 60 Celsius.")
        if not 0 <= humidity <= 100:
            raise ValueError("humidity must be between 0 and 100 percent.")
        if not 0 <= wind_speed <= 300:
            raise ValueError("wind_speed must be between 0 and 300 km/h.")

    @staticmethod
    def _validate_score(score: float) -> None:
        """Validate comfort score before classification."""
        ComfortEngine._validate_numeric("score", score)

        if not ComfortEngine.MIN_SCORE <= score <= ComfortEngine.MAX_SCORE:
            raise ValueError("score must be between 0 and 100.")

    @staticmethod
    def _validate_numeric(field_name: str, value: float) -> None:
        """Validate that a value is numeric and not boolean."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be a numeric value.")


if __name__ == "__main__":
    engine = ComfortEngine()

    temperature = 25
    humidity = 50
    wind_speed = 10

    comfort_score = engine.calculate_comfort_score(
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
    )
    comfort_category = engine.classify_comfort(comfort_score)
    analysis = engine.analyze_weather(
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
    )

    print(f"comfort score: {comfort_score}")
    print(f"comfort category: {comfort_category}")
    print(f"analysis dictionary: {analysis}")
