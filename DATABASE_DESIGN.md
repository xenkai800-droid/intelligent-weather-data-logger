# Database Design

## Database Technology

SQLite

Reason:
Lightweight, free, portable, and ideal for student Data Science projects.

---

# Table 1: locations

Purpose:
Store location information used for weather retrieval.

Fields:

* location_id (Primary Key)
* city_name
* latitude
* longitude

---

# Table 2: weather_observations

Purpose:
Store weather measurements and analytical outputs.

Fields:

* observation_id (Primary Key)
* location_id (Foreign Key)
* timestamp
* data_source

Weather Fields:

* temperature
* humidity
* pressure
* wind_speed
* precipitation

Comfort Analysis:

* comfort_score
* comfort_category

Anomaly Detection:

* anomaly_score
* anomaly_flag

Environmental Risks:

* heat_stress_risk
* dehydration_risk
* outdoor_activity_risk

Recommendations:

* hydration_recommendation
* clothing_recommendation
* activity_recommendation

---

# Table 3: ml_predictions

Purpose:
Store machine learning prediction history.

Fields:

* prediction_id (Primary Key)
* observation_id (Foreign Key)
* prediction_timestamp
* predicted_comfort_category
* prediction_confidence

---

# Relationships

locations
|
| 1 : many
|
weather_observations
|
| 1 : many
|
ml_predictions
