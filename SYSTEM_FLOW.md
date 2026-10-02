# System Flow

## Dashboard startup

1. Streamlit executes `app/dashboard.py`.
2. The dashboard creates the configured-by-code local SQLite schema if needed.
3. It renders a city selector, a current-weather button, historical charts, and database summary.
4. The historical charts and summary query existing local observations. Empty tables produce empty chart results and zero counts.

## On-demand current weather

```text
City selection
  → Open-Meteo current endpoint
  → field validation and numeric normalization
  → metrics in Streamlit
  → comfort / risk / recommendation rules
  → saved Random Forest + label encoder prediction
```

This request path does not persist current weather, run anomaly detection, or save the model prediction.

## Historical persistence and analysis

```text
Open-Meteo archive endpoint
  → historical importer (six fixed cities and date range)
  → duplicate timestamp check
  → SQLite observation rows
  → separately run enrichment command
  → historical chart queries in dashboard
```

The archive client requests daily mean temperature, precipitation sum, and maximum wind speed. The normalized records use default values for humidity and pressure. Enrichment calculates the derived database fields using the analytics engines; its anomaly reference is fixed at 28°C.

## Scheduled persistence

```text
manual scheduler process start
  → collect once at configured default location
  → insert if location/timestamp is not present
  → enrich unprocessed observations
  → wait and repeat at configured interval
```

The scheduler is a standalone blocking loop. Streamlit does not start or manage it. It uses the configured default city, coordinates, and interval; the `enabled` setting is not consulted.

## Model training and inference

Enriched stored comfort categories are read by `ml/train_model.py`. The trainer encodes the category labels, performs a stratified train/test split, fits the Random Forest, prints a classification report, and saves the model and encoder. During the dashboard current-weather flow, the predictor loads those artifacts, predicts a category, and reports the largest class probability as confidence.
