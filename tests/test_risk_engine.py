"""Unit tests for the RiskEngine."""

from __future__ import annotations

import pytest

from analytics.risk_engine import RiskEngine


class TestHeatStressRisk:
    """Tests for heat stress risk assessment."""

    def test_high_risk_by_temperature(self) -> None:
        assert (
            RiskEngine.assess_heat_stress_risk(
                temperature=35,
                humidity=50,
            )
            == "High"
        )

    def test_high_risk_by_temperature_and_humidity(self) -> None:
        assert (
            RiskEngine.assess_heat_stress_risk(
                temperature=32,
                humidity=70,
            )
            == "High"
        )

    def test_moderate_risk_by_temperature(self) -> None:
        assert (
            RiskEngine.assess_heat_stress_risk(
                temperature=30,
                humidity=50,
            )
            == "Moderate"
        )

    def test_moderate_risk_by_humidity(self) -> None:
        assert (
            RiskEngine.assess_heat_stress_risk(
                temperature=25,
                humidity=65,
            )
            == "Moderate"
        )

    def test_low_risk(self) -> None:
        assert (
            RiskEngine.assess_heat_stress_risk(
                temperature=25,
                humidity=50,
            )
            == "Low"
        )


class TestDehydrationRisk:
    """Tests for dehydration risk assessment."""

    def test_high_risk(self) -> None:
        assert (
            RiskEngine.assess_dehydration_risk(
                temperature=35,
                humidity=50,
            )
            == "High"
        )

    def test_moderate_risk(self) -> None:
        assert (
            RiskEngine.assess_dehydration_risk(
                temperature=30,
                humidity=50,
            )
            == "Moderate"
        )

    def test_low_risk(self) -> None:
        assert (
            RiskEngine.assess_dehydration_risk(
                temperature=25,
                humidity=50,
            )
            == "Low"
        )


class TestOutdoorActivityRisk:
    """Tests for outdoor activity risk assessment."""

    def test_unsafe_by_temperature(self) -> None:
        assert (
            RiskEngine.assess_outdoor_activity_risk(
                temperature=41,
                precipitation=0,
                wind_speed=10,
            )
            == "Unsafe"
        )

    def test_unsafe_by_precipitation(self) -> None:
        assert (
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=21,
                wind_speed=10,
            )
            == "Unsafe"
        )

    def test_unsafe_by_wind(self) -> None:
        assert (
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=0,
                wind_speed=41,
            )
            == "Unsafe"
        )

    def test_caution_by_temperature(self) -> None:
        assert (
            RiskEngine.assess_outdoor_activity_risk(
                temperature=33,
                precipitation=0,
                wind_speed=10,
            )
            == "Caution"
        )

    def test_caution_by_precipitation(self) -> None:
        assert (
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=6,
                wind_speed=10,
            )
            == "Caution"
        )

    def test_caution_by_wind(self) -> None:
        assert (
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=0,
                wind_speed=26,
            )
            == "Caution"
        )

    def test_safe_conditions(self) -> None:
        assert (
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=0,
                wind_speed=10,
            )
            == "Safe"
        )


class TestRiskAnalysis:
    """Tests for analyze_risks()."""

    def test_analysis_contains_expected_keys(self) -> None:
        result = RiskEngine.analyze_risks(
            temperature=36,
            humidity=75,
            precipitation=0,
            wind_speed=10,
        )

        assert "heat_stress_risk" in result
        assert "dehydration_risk" in result
        assert "outdoor_activity_risk" in result

    def test_analysis_values(self) -> None:
        result = RiskEngine.analyze_risks(
            temperature=36,
            humidity=75,
            precipitation=0,
            wind_speed=10,
        )

        assert result["heat_stress_risk"] == "High"
        assert result["dehydration_risk"] == "High"
        assert result["outdoor_activity_risk"] == "Caution"


class TestValidation:
    """Tests for validation logic."""

    def test_invalid_temperature_type(self) -> None:
        with pytest.raises(TypeError):
            RiskEngine.assess_heat_stress_risk(
                temperature="hot",
                humidity=50,
            )

    def test_invalid_humidity_type(self) -> None:
        with pytest.raises(TypeError):
            RiskEngine.assess_heat_stress_risk(
                temperature=25,
                humidity="high",
            )

    def test_invalid_precipitation_type(self) -> None:
        with pytest.raises(TypeError):
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation="rain",
                wind_speed=10,
            )

    def test_invalid_wind_type(self) -> None:
        with pytest.raises(TypeError):
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=0,
                wind_speed="fast",
            )

    def test_boolean_not_allowed(self) -> None:
        with pytest.raises(TypeError):
            RiskEngine.assess_heat_stress_risk(
                temperature=True,
                humidity=50,
            )

    def test_temperature_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            RiskEngine.assess_heat_stress_risk(
                temperature=100,
                humidity=50,
            )

    def test_humidity_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            RiskEngine.assess_heat_stress_risk(
                temperature=25,
                humidity=150,
            )

    def test_precipitation_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=1000,
                wind_speed=10,
            )

    def test_wind_speed_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            RiskEngine.assess_outdoor_activity_risk(
                temperature=25,
                precipitation=0,
                wind_speed=500,
            )
