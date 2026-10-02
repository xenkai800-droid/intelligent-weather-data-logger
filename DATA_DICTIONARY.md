# Data Dictionary

The SQLite schema is defined in `database/schema.py`. Numeric units below are the values requested or normalized by the Open-Meteo clients.

## Locations

| Field | SQLite type | Meaning |
| --- | --- | --- |
| `location_id` | INTEGER | Primary key. |
| `city_name` | TEXT | Configured or imported location name. |
| `latitude`, `longitude` | REAL | Coordinates; unique as a pair. |

## Weather observations

| Field | SQLite type | Meaning |
| --- | --- | --- |
| `observation_id` | INTEGER | Primary key. |
| `location_id` | INTEGER | Optional reference to `locations.location_id`. |
| `timestamp` | TEXT | Timestamp/date returned by the corresponding Open-Meteo endpoint. |
| `data_source` | TEXT | Inserted as `Open-Meteo` by `DatabaseManager`. |
| `temperature` | REAL | °C; current 2 m temperature or historical daily mean. |
| `humidity` | REAL | %; current relative humidity, or fixed 50% for archive rows. |
| `pressure` | REAL | hPa; current mean sea-level pressure, or fixed 1013 hPa for archive rows. |
| `wind_speed` | REAL | km/h; current 10 m speed or historical daily maximum. |
| `precipitation` | REAL | mm; current precipitation or historical daily sum. |
| `comfort_score` | REAL | Rule-based score from 0 to 100, populated by enrichment. |
| `comfort_category` | TEXT | `Excellent`, `Good`, `Moderate`, `Poor`, or `Extreme`, populated by enrichment. |
| `anomaly_score` | REAL | Absolute temperature difference from 28°C in the enrichment workflow. |
| `anomaly_flag` | INTEGER | 1 if the difference is greater than 10°C; otherwise 0. |
| `heat_stress_risk` | TEXT | `Low`, `Moderate`, or `High`. |
| `dehydration_risk` | TEXT | `Low`, `Moderate`, or `High`. |
| `outdoor_activity_risk` | TEXT | `Safe`, `Caution`, or `Unsafe`. |
| `hydration_recommendation` | TEXT | Rule-selected hydration text. |
| `clothing_recommendation` | TEXT | Rule-selected clothing text. |
| `activity_recommendation` | TEXT | Rule-selected activity text. |

Derived fields remain NULL until an observation is enriched. The current dashboard fetch does not create an observation row.

## ML predictions

| Field | SQLite type | Meaning |
| --- | --- | --- |
| `prediction_id` | INTEGER | Primary key. |
| `observation_id` | INTEGER | Optional related observation. |
| `prediction_timestamp` | TEXT | Prediction timestamp, if written by a future/other caller. |
| `predicted_comfort_category` | TEXT | Encoded model output decoded to a category. |
| `prediction_confidence` | REAL | Largest predicted class probability, expressed as a percentage by the predictor. |

The present prediction flow displays results in Streamlit and does not populate this table.
