"""Application configuration loader for the weather analytics system."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class Settings:
    """Load, validate, cache, and expose application configuration values."""

    DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.yaml")
    REQUIRED_SCHEMA = {
        "database": ("path",),
        "api": ("open_meteo_timeout",),
        "weather": (
            "default_city",
            "default_latitude",
            "default_longitude",
        ),
        "historical_data": ("start_date", "end_date"),
        "ml": ("model_path", "encoder_path"),
        "scheduler": ("enabled", "interval_minutes"),
        "logging": ("level", "file"),
    }

    def __init__(self, config_path: Path | str | None = None) -> None:
        """
        Initialize settings with an optional YAML configuration path.

        Args:
            config_path: Optional path to a YAML configuration file. Defaults
                to config/config.yaml.
        """
        self.config_path = Path(config_path or self.DEFAULT_CONFIG_PATH)
        self._config: dict[str, Any] | None = None

    def load(self) -> dict[str, Any]:
        """
        Load and validate configuration from disk once.

        Returns:
            Cached configuration dictionary.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the YAML content or required structure is invalid.
            RuntimeError: If the configuration file cannot be read.
        """
        if self._config is not None:
            return self._config

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with self.config_path.open("r", encoding="utf-8") as config_file:
                loaded_config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            raise ValueError(
                f"Invalid YAML configuration: {self.config_path}"
            ) from exc
        except OSError as exc:
            raise RuntimeError(
                f"Unable to read configuration file: {self.config_path}"
            ) from exc

        if not isinstance(loaded_config, dict):
            raise ValueError("Configuration root must be a mapping.")

        self._validate_config(loaded_config)
        self._config = loaded_config
        return self._config

    def get_database_path(self) -> Path:
        """
        Return the configured SQLite database path.

        Returns:
            Database path as a Path object.
        """
        return self._get_path("database", "path")

    def get_model_path(self) -> Path:
        """
        Return the configured model artifact path.

        Returns:
            Model path as a Path object.
        """
        return self._get_path("ml", "model_path")

    def get_encoder_path(self) -> Path:
        """
        Return the configured label encoder artifact path.

        Returns:
            Encoder path as a Path object.
        """
        return self._get_path("ml", "encoder_path")

    def get_default_city(self) -> str:
        """
        Return the configured default city name.

        Returns:
            Default city name.
        """
        return self._get_str("weather", "default_city")

    def get_default_latitude(self) -> float:
        """
        Return the configured default latitude.

        Returns:
            Default latitude.
        """
        return self._get_float("weather", "default_latitude")

    def get_default_longitude(self) -> float:
        """
        Return the configured default longitude.

        Returns:
            Default longitude.
        """
        return self._get_float("weather", "default_longitude")

    def get_scheduler_interval(self) -> int:
        """
        Return the configured scheduler interval in minutes.

        Returns:
            Scheduler interval.
        """
        return self._get_int("scheduler", "interval_minutes")

    def get_scheduler_enabled(self) -> bool:
        """
        Return whether scheduled collection is enabled.

        Returns:
            Scheduler enabled flag.
        """
        return self._get_bool("scheduler", "enabled")

    def get_log_file(self) -> Path:
        """
        Return the configured application log file path.

        Returns:
            Log file path as a Path object.
        """
        return self._get_path("logging", "file")

    def get_log_level(self) -> str:
        """
        Return the configured logging level.

        Returns:
            Logging level string.
        """
        return self._get_str("logging", "level")

    def _validate_config(self, config: dict[str, Any]) -> None:
        """
        Validate required configuration sections and keys.

        Args:
            config: Loaded configuration dictionary.

        Raises:
            ValueError: If any required section or key is missing.
        """
        for section, required_keys in self.REQUIRED_SCHEMA.items():
            if section not in config:
                raise ValueError(
                    f"Missing required configuration section: {section}"
                )

            if not isinstance(config[section], dict):
                raise ValueError(
                    f"Configuration section '{section}' must be a mapping."
                )

            for key in required_keys:
                if key not in config[section]:
                    raise ValueError(
                        "Missing required configuration key: "
                        f"{section}.{key}"
                    )

        self._validate_paths(config)

    def _validate_paths(self, config: dict[str, Any]) -> None:
        """
        Validate configured file path values.

        Args:
            config: Loaded configuration dictionary.

        Raises:
            ValueError: If any configured path is empty or invalid.
        """
        path_fields = (
            ("database", "path"),
            ("ml", "model_path"),
            ("ml", "encoder_path"),
            ("logging", "file"),
        )

        for section, key in path_fields:
            path_value = config[section][key]
            if not isinstance(path_value, str) or not path_value.strip():
                raise ValueError(
                    f"Configuration value {section}.{key} must be a path "
                    "string."
                )

    def _get_path(self, section: str, key: str) -> Path:
        """
        Return a configuration value as a Path.

        Args:
            section: Configuration section name.
            key: Configuration key name.

        Returns:
            Path value.
        """
        value = self._get_str(section, key)
        return Path(value)

    def _get_str(self, section: str, key: str) -> str:
        """
        Return a configuration value as a non-empty string.

        Args:
            section: Configuration section name.
            key: Configuration key name.

        Returns:
            String value.

        Raises:
            ValueError: If the value is missing, empty, or not a string.
        """
        value = self._get_raw_value(section, key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Configuration value {section}.{key} must be a non-empty "
                "string."
            )
        return value

    def _get_float(self, section: str, key: str) -> float:
        """
        Return a configuration value as a float.

        Args:
            section: Configuration section name.
            key: Configuration key name.

        Returns:
            Float value.

        Raises:
            ValueError: If the value is not numeric.
        """
        value = self._get_raw_value(section, key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"Configuration value {section}.{key} must be numeric."
            )
        return float(value)

    def _get_int(self, section: str, key: str) -> int:
        """
        Return a configuration value as an integer.

        Args:
            section: Configuration section name.
            key: Configuration key name.

        Returns:
            Integer value.

        Raises:
            ValueError: If the value is not an integer.
        """
        value = self._get_raw_value(section, key)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                f"Configuration value {section}.{key} must be an integer."
            )
        return value

    def _get_bool(self, section: str, key: str) -> bool:
        """
        Return a configuration value as a boolean.

        Args:
            section: Configuration section name.
            key: Configuration key name.

        Returns:
            Boolean value.

        Raises:
            ValueError: If the value is not a boolean.
        """
        value = self._get_raw_value(section, key)
        if not isinstance(value, bool):
            raise ValueError(
                f"Configuration value {section}.{key} must be a boolean."
            )
        return value

    def _get_raw_value(self, section: str, key: str) -> Any:
        """
        Return a raw configuration value after lazy loading.

        Args:
            section: Configuration section name.
            key: Configuration key name.

        Returns:
            Raw configuration value.

        Raises:
            ValueError: If the section or key is missing.
        """
        config = self.load()

        try:
            return config[section][key]
        except KeyError as exc:
            raise ValueError(
                f"Missing configuration value: {section}.{key}"
            ) from exc


if __name__ == "__main__":
    settings = Settings()
    settings.load()

    print(f"Database: {settings.get_database_path()}")
    print(f"Model: {settings.get_model_path()}")
    print(f"Encoder: {settings.get_encoder_path()}")
    print(f"Default City: {settings.get_default_city()}")
    print(f"Latitude: {settings.get_default_latitude()}")
    print(f"Longitude: {settings.get_default_longitude()}")
    print(f"Scheduler Enabled: {settings.get_scheduler_enabled()}")
    print(f"Scheduler Interval: {settings.get_scheduler_interval()}")
    print(f"Log File: {settings.get_log_file()}")
    print(f"Log Level: {settings.get_log_level()}")
