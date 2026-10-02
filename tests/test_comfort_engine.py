"""Unit tests for the ComfortEngine."""

from __future__ import annotations

import pytest

from analytics.comfort_engine import ComfortEngine


class TestComfortScore:
    """Tests for comfort score calculation."""

    def test_ideal_conditions_return_100(self) -> None:
        score = ComfortEngine.calculate_comfort_score(
            temperature=25,
            humidity=50,
            wind_speed=10,
        )

        assert score == 100.0

    def test_temperature_penalty_below_range(self) -> None:
        score = ComfortEngine.calculate_comfort_score(
            temperature=18,
            humidity=50,
            wind_speed=10,
        )

        assert score == 94.0

    def test_temperature_penalty_above_range(self) -> None:
        score = ComfortEngine.calculate_comfort_score(
            temperature=30,
            humidity=50,
            wind_speed=10,
        )

        assert score == 88.0

    def test_humidity_penalty_below_range(self) -> None:
        score = ComfortEngine.calculate_comfort_score(
            temperature=25,
            humidity=20,
            wind_speed=10,
        )

        assert score == 94.0

    def test_humidity_penalty_above_range(self) -> None:
        score = ComfortEngine.calculate_comfort_score(
            temperature=25,
            humidity=70,
            wind_speed=10,
        )

        assert score == 94.0

    def test_wind_penalty_above_range(self) -> None:
        score = ComfortEngine.calculate_comfort_score(
            temperature=25,
            humidity=50,
            wind_speed=20,
        )

        assert score == 94.0

    def test_score_clamped_to_zero(self) -> None:
        score = ComfortEngine.calculate_comfort_score(
            temperature=-80,
            humidity=100,
            wind_speed=300,
        )

        assert score == 0.0


class TestComfortClassification:
    """Tests for comfort category classification."""

    def test_excellent_category(self) -> None:
        assert ComfortEngine.classify_comfort(95) == "Excellent"

    def test_good_category(self) -> None:
        assert ComfortEngine.classify_comfort(80) == "Good"

    def test_moderate_category(self) -> None:
        assert ComfortEngine.classify_comfort(65) == "Moderate"

    def test_poor_category(self) -> None:
        assert ComfortEngine.classify_comfort(45) == "Poor"

    def test_extreme_category(self) -> None:
        assert ComfortEngine.classify_comfort(20) == "Extreme"


class TestWeatherAnalysis:
    """Tests for analyze_weather()."""

    def test_analysis_contains_expected_keys(self) -> None:
        result = ComfortEngine.analyze_weather(
            temperature=25,
            humidity=50,
            wind_speed=10,
        )

        assert "comfort_score" in result
        assert "comfort_category" in result

    def test_analysis_values(self) -> None:
        result = ComfortEngine.analyze_weather(
            temperature=25,
            humidity=50,
            wind_speed=10,
        )

        assert result["comfort_score"] == 100.0
        assert result["comfort_category"] == "Excellent"


class TestValidation:
    """Tests for validation logic."""

    def test_invalid_temperature_type(self) -> None:
        with pytest.raises(TypeError):
            ComfortEngine.calculate_comfort_score(
                temperature="hot",
                humidity=50,
                wind_speed=10,
            )

    def test_invalid_humidity_type(self) -> None:
        with pytest.raises(TypeError):
            ComfortEngine.calculate_comfort_score(
                temperature=25,
                humidity="high",
                wind_speed=10,
            )

    def test_invalid_wind_type(self) -> None:
        with pytest.raises(TypeError):
            ComfortEngine.calculate_comfort_score(
                temperature=25,
                humidity=50,
                wind_speed="fast",
            )

    def test_boolean_not_allowed(self) -> None:
        with pytest.raises(TypeError):
            ComfortEngine.calculate_comfort_score(
                temperature=True,
                humidity=50,
                wind_speed=10,
            )

    def test_temperature_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            ComfortEngine.calculate_comfort_score(
                temperature=100,
                humidity=50,
                wind_speed=10,
            )

    def test_humidity_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            ComfortEngine.calculate_comfort_score(
                temperature=25,
                humidity=150,
                wind_speed=10,
            )

    def test_wind_speed_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            ComfortEngine.calculate_comfort_score(
                temperature=25,
                humidity=50,
                wind_speed=500,
            )

    def test_invalid_score_for_classification(self) -> None:
        with pytest.raises(ValueError):
            ComfortEngine.classify_comfort(101)

    def test_invalid_score_type(self) -> None:
        with pytest.raises(TypeError):
            ComfortEngine.classify_comfort("high")