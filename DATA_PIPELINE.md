# Data Pipeline

There are separate dashboard and persistence workflows; fetching a dashboard value does not imply a database write.

## Current weather in the dashboard

1. The user selects one of six fixed Indian cities.
2. `WeatherClient` requests current temperature, relative humidity, mean sea-level pressure, wind speed, and precipitation from Open-Meteo.
3. It validates coordinate ranges, required response fields, and converts measurements to numeric values.
4. Streamlit displays the values, runs comfort/risk/recommendation rules, and predicts a comfort category with the saved model.
5. The response is not inserted into SQLite; anomaly analysis is not run in this path.

## Historical import

1. `scripts/import_historical_data.py` requests daily mean temperature, precipitation sum, and maximum wind speed for six hard-coded cities from 2024-01-01 through 2025-12-31.
2. The client validates coordinates, date syntax/order, required response fields, and aligned daily arrays.
3. It converts each daily value to a normalized record. Humidity (50%) and pressure (1013 hPa) are fixed defaults because they are not requested from the archive endpoint.
4. The importer creates or reuses a location and skips observations already stored for that location and timestamp.
5. Run `scripts/populate_training_data.py` separately to calculate derived fields.

## Scheduled current collection

`python -m scheduler.weather_scheduler` uses the configured default city and coordinates. It collects once immediately, inserts a non-duplicate observation, runs enrichment, then repeats at `scheduler.interval_minutes`. The process runs independently of Streamlit and remains active until stopped. The scheduler does not check the `scheduler.enabled` setting.

## Enrichment

The enrichment command selects stored observations whose `comfort_score` is NULL. It calculates comfort score/category, risk labels, recommendation text, and temperature deviation from the fixed 28°C reference. The anomaly flag is set when the absolute difference is strictly greater than 10°C. These derived values are written back to the observation row.

The dashboard's historical charts read temperature, comfort score, comfort category, and heat-stress risk from SQLite. A fresh database has no chart observations until data is imported or collected and enriched.
