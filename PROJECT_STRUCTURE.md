# Project Structure

weather_project/
│
├── main.py
│
├── app/
│   └── dashboard.py
│
├── api/
│   └── weather_client.py
│
├── database/
│   ├── database_manager.py
│   └── schema.py
│
├── processing/
│   ├── data_cleaner.py
│   └── feature_engineering.py
│
├── analytics/
│   ├── comfort_engine.py
│   ├── anomaly_engine.py
│   ├── risk_engine.py
│   └── recommendation_engine.py
│
├── ml/
│   ├── train_model.py
│   ├── predictor.py
│   └── model_loader.py
│
├── visualizations/
│   └── charts.py
│
├── config/
│   └── settings.py
│
├── data/
│   ├── weather.db
│   ├── raw/
│   └── processed/
│
├── logs/
│
├── tests/
│
└── docs/
│
├── PROJECT_SCOPE.md
├── REQUIREMENTS.md
├── SYSTEM_FLOW.md
├── DATA_DICTIONARY.md
├── DATABASE_DESIGN.md
├── ARCHITECTURE_DECISIONS.md
└── PROJECT_STRUCTURE.md

---

Module Responsibilities

main.py

Purpose:
Application entry point.

Responsibilities:

* Initialize application
* Coordinate modules
* Launch dashboard

---

app/dashboard.py

Purpose:
User Interface Layer

Responsibilities:

* Streamlit UI
* Display metrics
* Display charts
* Display ML predictions
* Display recommendations

---

api/weather_client.py

Purpose:
Weather API Integration

Responsibilities:

* Connect to Open-Meteo
* Send requests
* Parse responses
* Handle API errors

---

database/database_manager.py

Purpose:
Database Operations

Responsibilities:

* Insert records
* Retrieve records
* Update records
* Database queries

---

database/schema.py

Purpose:
Database Schema Management

Responsibilities:

* Create tables
* Verify schema

---

processing/data_cleaner.py

Purpose:
Data Cleaning

Responsibilities:

* Missing values
* Validation
* Formatting

---

processing/feature_engineering.py

Purpose:
Feature Generation

Responsibilities:

* Create ML features
* Prepare training data

---

analytics/comfort_engine.py

Purpose:
Comfort Analysis

Responsibilities:

* Calculate comfort score
* Assign comfort category

---

analytics/anomaly_engine.py

Purpose:
Anomaly Detection

Responsibilities:

* Detect abnormal weather
* Historical comparisons

---

analytics/risk_engine.py

Purpose:
Environmental Risk Assessment

Responsibilities:

* Heat stress analysis
* Dehydration analysis
* Outdoor activity risk analysis

---

analytics/recommendation_engine.py

Purpose:
Recommendation Generation

Responsibilities:

* Hydration advice
* Clothing advice
* Activity advice

---

ml/train_model.py

Purpose:
Model Training

Responsibilities:

* Train Random Forest
* Save model

---

ml/predictor.py

Purpose:
Prediction Engine

Responsibilities:

* Generate predictions
* Return confidence scores

---

ml/model_loader.py

Purpose:
Model Management

Responsibilities:

* Load saved models
* Validate model availability

---

visualizations/charts.py

Purpose:
Visualization Layer

Responsibilities:

* Plotly charts
* Trend graphs
* Analytics visualizations

---

config/settings.py

Purpose:
Configuration Management

Responsibilities:

* API settings
* Database paths
* Default locations
* Application constants

---

logs/

Purpose:
Store application logs

---

tests/

Purpose:
Store unit tests and integration tests
