"""Train and persist a comfort category classification model."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from logs.logger import get_logger

logger = get_logger(__name__)


class ComfortModelTrainer:
    """Train a Random Forest model for weather comfort classification."""

    FEATURE_COLUMNS = ["temperature", "humidity", "wind_speed"]
    TARGET_COLUMN = "comfort_category"

    def __init__(self, db_path: str, model_path: str) -> None:
        """
        Initialize the model trainer.

        Args:
            db_path: Path to the SQLite database file.
            model_path: Path where the trained model should be saved.
        """
        self.db_path = Path(db_path)
        self.model_path = Path(model_path)
        self.encoder_path = Path(
            str(self.model_path).replace(".joblib", "_encoder.joblib")
        )

    def load_data(self) -> pd.DataFrame:
        """
        Load labeled weather observations from SQLite.
        """
        query = """
            SELECT
                temperature,
                humidity,
                wind_speed,
                comfort_category
            FROM weather_observations
            WHERE comfort_category IS NOT NULL;
        """

        try:
            with sqlite3.connect(self.db_path) as connection:
                data = pd.read_sql_query(query, connection)

            logger.info(
                "Loaded %s labeled observations for training.",
                len(data),
            )

            return data

        except (sqlite3.Error, pd.errors.DatabaseError) as exc:
            logger.error(
                "Failed to load training data: %s",
                exc,
            )
            raise RuntimeError("Failed to load training data.") from exc

    def train_model(self) -> None:
        """
        Train and save the comfort classification model and label encoder.
        """
        data = self.load_data()

        self._validate_training_data(data)
        self._print_training_summary(data)

        features = data[self.FEATURE_COLUMNS]
        target = data[self.TARGET_COLUMN]

        label_encoder = LabelEncoder()
        encoded_target = label_encoder.fit_transform(target)

        try:
            logger.info("Starting model training.")

            (
                x_train,
                x_test,
                y_train,
                y_test,
            ) = train_test_split(
                features,
                encoded_target,
                test_size=0.2,
                random_state=42,
                stratify=encoded_target,
            )

            logger.info(
                "Training samples=%s Testing samples=%s",
                len(x_train),
                len(x_test),
            )

            model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
            )

            model.fit(x_train, y_train)

            logger.info("Model training completed successfully.")

            predictions = model.predict(x_test)

            report = classification_report(
                y_test,
                predictions,
            )

            print(report)

            self.model_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.encoder_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            joblib.dump(
                model,
                self.model_path,
            )

            joblib.dump(
                label_encoder,
                self.encoder_path,
            )

            logger.info(
                "Model saved to %s",
                self.model_path,
            )

            logger.info(
                "Encoder saved to %s",
                self.encoder_path,
            )

        except ValueError:
            raise

        except Exception as exc:
            logger.error(
                "Model training failed: %s",
                exc,
            )

            raise RuntimeError(
                "Failed to train comfort model."
            ) from exc

    def _validate_training_data(
        self,
        data: pd.DataFrame,
    ) -> None:
        """
        Validate labeled data before model training.
        """
        missing_columns = [
            column
            for column in [*self.FEATURE_COLUMNS, self.TARGET_COLUMN]
            if column not in data.columns
        ]

        if missing_columns:
            columns = ", ".join(missing_columns)

            raise ValueError(
                f"Training data missing columns: {columns}."
            )

        if data.empty:
            raise ValueError(
                "No labeled observations found. Add rows with "
                "comfort_category before training."
            )

        if len(data) < 20:
            raise ValueError(
                "At least 20 labeled observations are required for training."
            )

        self._validate_class_distribution(data)

        if data[self.FEATURE_COLUMNS].isnull().any().any():
            raise ValueError(
                "Training features must not contain NULL values."
            )

    def _validate_class_distribution(
        self,
        data: pd.DataFrame,
    ) -> None:
        """
        Validate that comfort categories are suitable for ML training.
        """
        class_distribution = data[self.TARGET_COLUMN].value_counts()

        detected_classes = len(class_distribution)

        if detected_classes < 2:
            raise ValueError(
                "At least 2 distinct comfort categories are required "
                f"for training. Detected {detected_classes} class."
            )

        underrepresented_classes = {
            str(class_name): int(sample_count)
            for class_name, sample_count in class_distribution.items()
            if sample_count < 10
        }

        if underrepresented_classes:
            raise ValueError(
                "Insufficient training samples for classes:\n"
                f"{underrepresented_classes}\n\n"
                "Each class must contain at least 10 observations."
            )

    def _print_training_summary(
        self,
        data: pd.DataFrame,
    ) -> None:
        """
        Print a concise summary of the training dataset.
        """
        class_distribution = data[self.TARGET_COLUMN].value_counts()

        print("## Training Dataset Summary")
        print(f"Total Samples: {len(data)}")
        print()

        print("Class Distribution:")

        for class_name, sample_count in class_distribution.items():
            print(f"{class_name}: {sample_count}")

        print()


if __name__ == "__main__":
    trainer = ComfortModelTrainer(
        db_path="data/weather.db",
        model_path="ml/comfort_model.joblib",
    )

    trainer.train_model()