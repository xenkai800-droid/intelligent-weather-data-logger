"""Rule-based anomaly detection utilities for weather observations."""

from __future__ import annotations


class AnomalyEngine:
    """Detect simple anomalies by comparing current values to averages."""

    @staticmethod
    def calculate_anomaly_score(
        current_value: float,
        historical_average: float,
    ) -> float:
        """
        Calculate the absolute difference from a historical average.

        Args:
            current_value: Current observed value.
            historical_average: Historical average value for comparison.

        Returns:
            Rounded anomaly score.

        Raises:
            TypeError: If either input is not numeric.
        """
        AnomalyEngine._validate_numeric("current_value", current_value)
        AnomalyEngine._validate_numeric(
            "historical_average",
            historical_average,
        )

        return round(abs(current_value - historical_average), 2)

    @staticmethod
    def detect_anomaly(
        current_value: float,
        historical_average: float,
        threshold: float = 10.0,
    ) -> bool:
        """
        Detect whether a value is anomalous based on a threshold.

        Args:
            current_value: Current observed value.
            historical_average: Historical average value for comparison.
            threshold: Minimum score required to flag an anomaly.

        Returns:
            True if anomaly score is greater than threshold, otherwise False.

        Raises:
            TypeError: If any input is not numeric.
            ValueError: If threshold is negative.
        """
        AnomalyEngine._validate_threshold(threshold)

        anomaly_score = AnomalyEngine.calculate_anomaly_score(
            current_value=current_value,
            historical_average=historical_average,
        )
        return anomaly_score > threshold

    @staticmethod
    def analyze_temperature_anomaly(
        current_temperature: float,
        historical_average_temperature: float,
    ) -> dict[str, float | bool]:
        """
        Analyze temperature anomaly score and flag.

        Args:
            current_temperature: Current air temperature in degrees Celsius.
            historical_average_temperature: Historical average temperature in
                degrees Celsius.

        Returns:
            Dictionary containing anomaly_score and anomaly_flag.
        """
        anomaly_score = AnomalyEngine.calculate_anomaly_score(
            current_value=current_temperature,
            historical_average=historical_average_temperature,
        )
        anomaly_flag = AnomalyEngine.detect_anomaly(
            current_value=current_temperature,
            historical_average=historical_average_temperature,
        )

        return {
            "anomaly_score": anomaly_score,
            "anomaly_flag": anomaly_flag,
        }

    @staticmethod
    def _validate_threshold(threshold: float) -> None:
        """Validate anomaly threshold."""
        AnomalyEngine._validate_numeric("threshold", threshold)
        if threshold < 0:
            raise ValueError("threshold must be greater than or equal to 0.")

    @staticmethod
    def _validate_numeric(field_name: str, value: float) -> None:
        """Validate that a value is numeric and not boolean."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be a numeric value.")


if __name__ == "__main__":
    engine = AnomalyEngine()

    current_temperature = 40
    historical_average_temperature = 28

    anomaly_score = engine.calculate_anomaly_score(
        current_value=current_temperature,
        historical_average=historical_average_temperature,
    )
    anomaly_flag = engine.detect_anomaly(
        current_value=current_temperature,
        historical_average=historical_average_temperature,
    )
    analysis = engine.analyze_temperature_anomaly(
        current_temperature=current_temperature,
        historical_average_temperature=historical_average_temperature,
    )

    print(f"anomaly score: {anomaly_score}")
    print(f"anomaly flag: {anomaly_flag}")
    print(f"analysis dictionary: {analysis}")
