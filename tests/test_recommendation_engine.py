"""Unit tests for the RecommendationEngine."""

from __future__ import annotations

import pytest

from analytics.recommendation_engine import RecommendationEngine


class TestHydrationRecommendations:
    """Tests for hydration recommendations."""

    def test_high_risk_recommendation(self) -> None:
        result = RecommendationEngine.get_hydration_recommendation(
            dehydration_risk="High",
        )

        assert "3-4 liters" in result

    def test_moderate_risk_recommendation(self) -> None:
        result = RecommendationEngine.get_hydration_recommendation(
            dehydration_risk="Moderate",
        )

        assert result == "Drink 2-3 liters of water throughout the day."

    def test_low_risk_recommendation(self) -> None:
        result = RecommendationEngine.get_hydration_recommendation(
            dehydration_risk="Low",
        )

        assert result == "Maintain normal hydration levels."


class TestClothingRecommendations:
    """Tests for clothing recommendations."""

    def test_hot_weather_clothing(self) -> None:
        result = RecommendationEngine.get_clothing_recommendation(
            temperature=35,
        )

        assert result == "Wear light-colored breathable clothing."

    def test_warm_weather_clothing(self) -> None:
        result = RecommendationEngine.get_clothing_recommendation(
            temperature=25,
        )

        assert result == "Light casual clothing is recommended."

    def test_cool_weather_clothing(self) -> None:
        result = RecommendationEngine.get_clothing_recommendation(
            temperature=15,
        )

        assert result == "Consider carrying a light jacket."


class TestActivityRecommendations:
    """Tests for activity recommendations."""

    def test_unsafe_activity_recommendation(self) -> None:
        result = RecommendationEngine.get_activity_recommendation(
            outdoor_activity_risk="Unsafe",
        )

        assert result == "Avoid outdoor activities."

    def test_caution_activity_recommendation(self) -> None:
        result = RecommendationEngine.get_activity_recommendation(
            outdoor_activity_risk="Caution",
        )

        assert (
            result
            == "Limit outdoor activities and take precautions."
        )

    def test_safe_activity_recommendation(self) -> None:
        result = RecommendationEngine.get_activity_recommendation(
            outdoor_activity_risk="Safe",
        )

        assert result == "Outdoor activities are safe."


class TestRecommendationGeneration:
    """Tests for generate_recommendations()."""

    def test_generate_contains_expected_keys(self) -> None:
        result = RecommendationEngine.generate_recommendations(
            temperature=36,
            dehydration_risk="High",
            outdoor_activity_risk="Caution",
        )

        assert "hydration_recommendation" in result
        assert "clothing_recommendation" in result
        assert "activity_recommendation" in result

    def test_generate_expected_values(self) -> None:
        result = RecommendationEngine.generate_recommendations(
            temperature=36,
            dehydration_risk="High",
            outdoor_activity_risk="Caution",
        )

        assert (
            result["hydration_recommendation"]
            == (
                "Drink at least 3-4 liters of water and avoid "
                "prolonged sun exposure."
            )
        )

        assert (
            result["clothing_recommendation"]
            == "Wear light-colored breathable clothing."
        )

        assert (
            result["activity_recommendation"]
            == "Limit outdoor activities and take precautions."
        )


class TestValidation:
    """Tests for validation logic."""

    def test_invalid_dehydration_risk_type(self) -> None:
        with pytest.raises(TypeError):
            RecommendationEngine.get_hydration_recommendation(
                dehydration_risk=123,
            )

    def test_invalid_dehydration_risk_value(self) -> None:
        with pytest.raises(ValueError):
            RecommendationEngine.get_hydration_recommendation(
                dehydration_risk="Extreme",
            )

    def test_empty_dehydration_risk(self) -> None:
        with pytest.raises(ValueError):
            RecommendationEngine.get_hydration_recommendation(
                dehydration_risk="",
            )

    def test_invalid_activity_risk_type(self) -> None:
        with pytest.raises(TypeError):
            RecommendationEngine.get_activity_recommendation(
                outdoor_activity_risk=123,
            )

    def test_invalid_activity_risk_value(self) -> None:
        with pytest.raises(ValueError):
            RecommendationEngine.get_activity_recommendation(
                outdoor_activity_risk="Dangerous",
            )

    def test_empty_activity_risk(self) -> None:
        with pytest.raises(ValueError):
            RecommendationEngine.get_activity_recommendation(
                outdoor_activity_risk="",
            )

    def test_invalid_temperature_type(self) -> None:
        with pytest.raises(TypeError):
            RecommendationEngine.get_clothing_recommendation(
                temperature="hot",
            )

    def test_boolean_temperature_not_allowed(self) -> None:
        with pytest.raises(TypeError):
            RecommendationEngine.get_clothing_recommendation(
                temperature=True,
            )

    def test_temperature_above_range(self) -> None:
        with pytest.raises(ValueError):
            RecommendationEngine.get_clothing_recommendation(
                temperature=100,
            )

    def test_temperature_below_range(self) -> None:
        with pytest.raises(ValueError):
            RecommendationEngine.get_clothing_recommendation(
                temperature=-100,
            )