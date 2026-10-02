"""Rule-based recommendation engine for weather guidance."""

from __future__ import annotations


class RecommendationEngine:
    """Generate hydration, clothing, and activity recommendations."""

    VALID_DEHYDRATION_RISKS = {"High", "Moderate", "Low"}
    VALID_ACTIVITY_RISKS = {"Unsafe", "Caution", "Safe"}

    @staticmethod
    def get_hydration_recommendation(dehydration_risk: str) -> str:
        """
        Return a hydration recommendation for a dehydration risk level.

        Args:
            dehydration_risk: Dehydration risk level: High, Moderate, or Low.

        Returns:
            Hydration recommendation text.

        Raises:
            TypeError: If dehydration_risk is not a string.
            ValueError: If dehydration_risk is not supported.
        """
        RecommendationEngine._validate_dehydration_risk(dehydration_risk)

        recommendations = {
            "High": (
                "Drink at least 3-4 liters of water and avoid prolonged sun "
                "exposure."
            ),
            "Moderate": "Drink 2-3 liters of water throughout the day.",
            "Low": "Maintain normal hydration levels.",
        }
        return recommendations[dehydration_risk]

    @staticmethod
    def get_clothing_recommendation(temperature: float) -> str:
        """
        Return a clothing recommendation for the current temperature.

        Args:
            temperature: Air temperature in degrees Celsius.

        Returns:
            Clothing recommendation text.

        Raises:
            TypeError: If temperature is not numeric.
            ValueError: If temperature is outside a realistic accepted range.
        """
        RecommendationEngine._validate_temperature(temperature)

        if temperature >= 35:
            return "Wear light-colored breathable clothing."
        if temperature >= 25:
            return "Light casual clothing is recommended."
        return "Consider carrying a light jacket."

    @staticmethod
    def get_activity_recommendation(outdoor_activity_risk: str) -> str:
        """
        Return an activity recommendation for an outdoor activity risk level.

        Args:
            outdoor_activity_risk: Outdoor risk level: Unsafe, Caution, or Safe.

        Returns:
            Activity recommendation text.

        Raises:
            TypeError: If outdoor_activity_risk is not a string.
            ValueError: If outdoor_activity_risk is not supported.
        """
        RecommendationEngine._validate_activity_risk(outdoor_activity_risk)

        recommendations = {
            "Unsafe": "Avoid outdoor activities.",
            "Caution": "Limit outdoor activities and take precautions.",
            "Safe": "Outdoor activities are safe.",
        }
        return recommendations[outdoor_activity_risk]

    @staticmethod
    def generate_recommendations(
        temperature: float,
        dehydration_risk: str,
        outdoor_activity_risk: str,
    ) -> dict[str, str]:
        """
        Generate all supported weather recommendations.

        Args:
            temperature: Air temperature in degrees Celsius.
            dehydration_risk: Dehydration risk level.
            outdoor_activity_risk: Outdoor activity risk level.

        Returns:
            Dictionary containing hydration, clothing, and activity
            recommendations.
        """
        return {
            "hydration_recommendation": (
                RecommendationEngine.get_hydration_recommendation(
                    dehydration_risk=dehydration_risk,
                )
            ),
            "clothing_recommendation": (
                RecommendationEngine.get_clothing_recommendation(
                    temperature=temperature,
                )
            ),
            "activity_recommendation": (
                RecommendationEngine.get_activity_recommendation(
                    outdoor_activity_risk=outdoor_activity_risk,
                )
            ),
        }

    @staticmethod
    def _validate_dehydration_risk(dehydration_risk: str) -> None:
        """Validate dehydration risk label."""
        RecommendationEngine._validate_string(
            field_name="dehydration_risk",
            value=dehydration_risk,
        )

        if dehydration_risk not in RecommendationEngine.VALID_DEHYDRATION_RISKS:
            valid_values = ", ".join(
                sorted(RecommendationEngine.VALID_DEHYDRATION_RISKS)
            )
            raise ValueError(
                f"dehydration_risk must be one of: {valid_values}."
            )

    @staticmethod
    def _validate_activity_risk(outdoor_activity_risk: str) -> None:
        """Validate outdoor activity risk label."""
        RecommendationEngine._validate_string(
            field_name="outdoor_activity_risk",
            value=outdoor_activity_risk,
        )

        if outdoor_activity_risk not in RecommendationEngine.VALID_ACTIVITY_RISKS:
            valid_values = ", ".join(
                sorted(RecommendationEngine.VALID_ACTIVITY_RISKS)
            )
            raise ValueError(
                f"outdoor_activity_risk must be one of: {valid_values}."
            )

    @staticmethod
    def _validate_temperature(temperature: float) -> None:
        """Validate temperature input."""
        if isinstance(temperature, bool) or not isinstance(
            temperature,
            (int, float),
        ):
            raise TypeError("temperature must be a numeric value.")

        if not -80 <= temperature <= 60:
            raise ValueError("temperature must be between -80 and 60 Celsius.")

    @staticmethod
    def _validate_string(field_name: str, value: str) -> None:
        """Validate that a value is a non-empty string."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        if not value.strip():
            raise ValueError(f"{field_name} must not be empty.")


if __name__ == "__main__":
    engine = RecommendationEngine()

    temperature = 36
    dehydration_risk = "High"
    outdoor_activity_risk = "Caution"

    hydration_recommendation = engine.get_hydration_recommendation(
        dehydration_risk=dehydration_risk,
    )
    clothing_recommendation = engine.get_clothing_recommendation(
        temperature=temperature,
    )
    activity_recommendation = engine.get_activity_recommendation(
        outdoor_activity_risk=outdoor_activity_risk,
    )
    recommendation_dictionary = engine.generate_recommendations(
        temperature=temperature,
        dehydration_risk=dehydration_risk,
        outdoor_activity_risk=outdoor_activity_risk,
    )

    print(f"hydration recommendation: {hydration_recommendation}")
    print(f"clothing recommendation: {clothing_recommendation}")
    print(f"activity recommendation: {activity_recommendation}")
    print(f"recommendation dictionary: {recommendation_dictionary}")
