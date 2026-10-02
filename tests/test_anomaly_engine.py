"""Unit tests for the AnomalyEngine."""

from __future__ import annotations

import pytest

from analytics.anomaly_engine import AnomalyEngine


class TestAnomalyScore:
    """Tests for anomaly score calculation."""

    def test_positive_difference(self) -> None:
        score = AnomalyEngine.calculate_anomaly_score(
            current_value=40,
            historical_average=28,
        )

        assert score == 12.0

    def test_negative_difference(self) -> None:
        score = AnomalyEngine.calculate_anomaly_score(
            current_value=20,
            historical_average=28,
        )

        assert score == 8.0

    def test_identical_values(self) -> None:
        score = AnomalyEngine.calculate_anomaly_score(
            current_value=25,
            historical_average=25,
        )

        assert score == 0.0

    def test_rounding(self) -> None:
        score = AnomalyEngine.calculate_anomaly_score(
            current_value=25.555,
            historical_average=20.111,
        )

        assert score == 5.44


class TestAnomalyDetection:
    """Tests for anomaly detection."""

    def test_detects_anomaly_above_threshold(self) -> None:
        result = AnomalyEngine.detect_anomaly(
            current_value=40,
            historical_average=28,
        )

        assert result is True

    def test_no_anomaly_below_threshold(self) -> None:
        result = AnomalyEngine.detect_anomaly(
            current_value=35,
            historical_average=28,
        )

        assert result is False

    def test_equal_to_threshold_is_not_anomaly(self) -> None:
        result = AnomalyEngine.detect_anomaly(
            current_value=38,
            historical_average=28,
            threshold=10,
        )

        assert result is False

    def test_custom_threshold(self) -> None:
        result = AnomalyEngine.detect_anomaly(
            current_value=38,
            historical_average=28,
            threshold=5,
        )

        assert result is True


class TestTemperatureAnalysis:
    """Tests for analyze_temperature_anomaly()."""

    def test_analysis_contains_expected_keys(self) -> None:
        result = AnomalyEngine.analyze_temperature_anomaly(
            current_temperature=40,
            historical_average_temperature=28,
        )

        assert "anomaly_score" in result
        assert "anomaly_flag" in result

    def test_analysis_values(self) -> None:
        result = AnomalyEngine.analyze_temperature_anomaly(
            current_temperature=40,
            historical_average_temperature=28,
        )

        assert result["anomaly_score"] == 12.0
        assert result["anomaly_flag"] is True

    def test_analysis_no_anomaly(self) -> None:
        result = AnomalyEngine.analyze_temperature_anomaly(
            current_temperature=30,
            historical_average_temperature=28,
        )

        assert result["anomaly_score"] == 2.0
        assert result["anomaly_flag"] is False


class TestValidation:
    """Tests for validation logic."""

    def test_invalid_current_value_type(self) -> None:
        with pytest.raises(TypeError):
            AnomalyEngine.calculate_anomaly_score(
                current_value="40",
                historical_average=28,
            )

    def test_invalid_historical_average_type(self) -> None:
        with pytest.raises(TypeError):
            AnomalyEngine.calculate_anomaly_score(
                current_value=40,
                historical_average="28",
            )

    def test_boolean_current_value_not_allowed(self) -> None:
        with pytest.raises(TypeError):
            AnomalyEngine.calculate_anomaly_score(
                current_value=True,
                historical_average=28,
            )

    def test_boolean_historical_average_not_allowed(self) -> None:
        with pytest.raises(TypeError):
            AnomalyEngine.calculate_anomaly_score(
                current_value=40,
                historical_average=False,
            )

    def test_invalid_threshold_type(self) -> None:
        with pytest.raises(TypeError):
            AnomalyEngine.detect_anomaly(
                current_value=40,
                historical_average=28,
                threshold="10",
            )

    def test_boolean_threshold_not_allowed(self) -> None:
        with pytest.raises(TypeError):
            AnomalyEngine.detect_anomaly(
                current_value=40,
                historical_average=28,
                threshold=True,
            )

    def test_negative_threshold(self) -> None:
        with pytest.raises(ValueError):
            AnomalyEngine.detect_anomaly(
                current_value=40,
                historical_average=28,
                threshold=-1,
            )