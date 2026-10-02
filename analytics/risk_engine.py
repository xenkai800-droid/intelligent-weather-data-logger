"""Rule-based environmental risk assessment engine."""

from __future__ import annotations


class RiskEngine:
    """Assess environmental risks from current weather conditions."""

    @staticmethod
    def assess_heat_stress_risk(temperature: float, humidity: float) -> str:
        """
        Assess heat stress risk from temperature and humidity.

        Args:
            temperature: Air temperature in degrees Celsius.
            humidity: Relative humidity percentage.

        Returns:
            Heat stress risk level: High, Moderate, or Low.

        Raises:
            TypeError: If any input is not numeric.
            ValueError: If any input is outside a realistic accepted range.
        """
        RiskEngine._validate_temperature(temperature)
        RiskEngine._validate_humidity(humidity)

        if temperature >= 35 or (temperature >= 32 and humidity >= 70):
            return "High"
        if temperature >= 28 or humidity >= 65:
            return "Moderate"
        return "Low"

    @staticmethod
    def assess_dehydration_risk(temperature: float, humidity: float) -> str:
        """
        Assess dehydration risk from temperature and humidity.

        Args:
            temperature: Air temperature in degrees Celsius.
            humidity: Relative humidity percentage.

        Returns:
            Dehydration risk level: High, Moderate, or Low.

        Raises:
            TypeError: If any input is not numeric.
            ValueError: If any input is outside a realistic accepted range.
        """
        RiskEngine._validate_temperature(temperature)
        RiskEngine._validate_humidity(humidity)

        if temperature >= 35:
            return "High"
        if 28 <= temperature <= 34:
            return "Moderate"
        return "Low"

    @staticmethod
    def assess_outdoor_activity_risk(
        temperature: float,
        precipitation: float,
        wind_speed: float,
    ) -> str:
        """
        Assess outdoor activity risk from weather conditions.

        Args:
            temperature: Air temperature in degrees Celsius.
            precipitation: Precipitation amount in millimeters.
            wind_speed: Wind speed in kilometers per hour.

        Returns:
            Outdoor activity risk level: Unsafe, Caution, or Safe.

        Raises:
            TypeError: If any input is not numeric.
            ValueError: If any input is outside a realistic accepted range.
        """
        RiskEngine._validate_temperature(temperature)
        RiskEngine._validate_precipitation(precipitation)
        RiskEngine._validate_wind_speed(wind_speed)

        if temperature > 40 or precipitation > 20 or wind_speed > 40:
            return "Unsafe"
        if temperature > 32 or precipitation > 5 or wind_speed > 25:
            return "Caution"
        return "Safe"

    @staticmethod
    def analyze_risks(
        temperature: float,
        humidity: float,
        precipitation: float,
        wind_speed: float,
    ) -> dict[str, str]:
        """
        Assess all supported weather-related environmental risks.

        Args:
            temperature: Air temperature in degrees Celsius.
            humidity: Relative humidity percentage.
            precipitation: Precipitation amount in millimeters.
            wind_speed: Wind speed in kilometers per hour.

        Returns:
            Dictionary containing heat stress, dehydration, and outdoor
            activity risk levels.
        """
        return {
            "heat_stress_risk": RiskEngine.assess_heat_stress_risk(
                temperature=temperature,
                humidity=humidity,
            ),
            "dehydration_risk": RiskEngine.assess_dehydration_risk(
                temperature=temperature,
                humidity=humidity,
            ),
            "outdoor_activity_risk": RiskEngine.assess_outdoor_activity_risk(
                temperature=temperature,
                precipitation=precipitation,
                wind_speed=wind_speed,
            ),
        }

    @staticmethod
    def _validate_temperature(temperature: float) -> None:
        """Validate temperature input."""
        RiskEngine._validate_numeric("temperature", temperature)
        if not -80 <= temperature <= 60:
            raise ValueError("temperature must be between -80 and 60 Celsius.")

    @staticmethod
    def _validate_humidity(humidity: float) -> None:
        """Validate humidity input."""
        RiskEngine._validate_numeric("humidity", humidity)
        if not 0 <= humidity <= 100:
            raise ValueError("humidity must be between 0 and 100 percent.")

    @staticmethod
    def _validate_precipitation(precipitation: float) -> None:
        """Validate precipitation input."""
        RiskEngine._validate_numeric("precipitation", precipitation)
        if not 0 <= precipitation <= 500:
            raise ValueError("precipitation must be between 0 and 500 mm.")

    @staticmethod
    def _validate_wind_speed(wind_speed: float) -> None:
        """Validate wind speed input."""
        RiskEngine._validate_numeric("wind_speed", wind_speed)
        if not 0 <= wind_speed <= 300:
            raise ValueError("wind_speed must be between 0 and 300 km/h.")

    @staticmethod
    def _validate_numeric(field_name: str, value: float) -> None:
        """Validate that a value is numeric and not boolean."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be a numeric value.")


if __name__ == "__main__":
    engine = RiskEngine()

    temperature = 36
    humidity = 75
    precipitation = 0
    wind_speed = 10

    heat_stress_risk = engine.assess_heat_stress_risk(
        temperature=temperature,
        humidity=humidity,
    )
    dehydration_risk = engine.assess_dehydration_risk(
        temperature=temperature,
        humidity=humidity,
    )
    outdoor_activity_risk = engine.assess_outdoor_activity_risk(
        temperature=temperature,
        precipitation=precipitation,
        wind_speed=wind_speed,
    )
    analysis = engine.analyze_risks(
        temperature=temperature,
        humidity=humidity,
        precipitation=precipitation,
        wind_speed=wind_speed,
    )

    print(f"heat stress risk: {heat_stress_risk}")
    print(f"dehydration risk: {dehydration_risk}")
    print(f"outdoor activity risk: {outdoor_activity_risk}")
    print(f"analysis dictionary: {analysis}")
