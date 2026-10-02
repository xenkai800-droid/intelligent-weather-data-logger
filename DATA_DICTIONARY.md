# Data Dictionary

## Weather Data Fields

| Field Name    | Data Type | Unit    | Description                  |
| ------------- | --------- | ------- | ---------------------------- |
| timestamp     | DATETIME  | UTC     | Date and time of observation |
| latitude      | FLOAT     | Degrees | Geographic latitude          |
| longitude     | FLOAT     | Degrees | Geographic longitude         |
| temperature   | FLOAT     | °C      | Air temperature              |
| humidity      | FLOAT     | %       | Relative humidity            |
| pressure      | FLOAT     | hPa     | Atmospheric pressure         |
| wind_speed    | FLOAT     | km/h    | Wind speed                   |
| precipitation | FLOAT     | mm      | Rainfall / precipitation     |

---

## Comfort Analysis Fields

| Field Name       | Data Type | Description              |
| ---------------- | --------- | ------------------------ |
| comfort_score    | FLOAT     | Calculated comfort score |
| comfort_category | TEXT      | Comfort classification   |

### Allowed Comfort Categories

* Very Comfortable
* Comfortable
* Moderate
* Uncomfortable
* Very Uncomfortable

---

## Anomaly Detection Fields

| Field Name    | Data Type | Description                                |
| ------------- | --------- | ------------------------------------------ |
| anomaly_score | FLOAT     | Degree of deviation from normal conditions |
| anomaly_flag  | BOOLEAN   | Indicates anomaly detection result         |

### Allowed Values

* TRUE
* FALSE

---

## Environmental Risk Fields

| Field Name            | Data Type | Description                 |
| --------------------- | --------- | --------------------------- |
| heat_stress_risk      | TEXT      | Heat stress risk level      |
| dehydration_risk      | TEXT      | Dehydration risk level      |
| outdoor_activity_risk | TEXT      | Outdoor activity risk level |

### Allowed Risk Levels

* Low
* Moderate
* High
* Severe

---

## Recommendation Fields

| Field Name               | Data Type | Description             |
| ------------------------ | --------- | ----------------------- |
| hydration_recommendation | TEXT      | Hydration advice        |
| clothing_recommendation  | TEXT      | Clothing advice         |
| activity_recommendation  | TEXT      | Outdoor activity advice |

---

## Machine Learning Fields

| Field Name                 | Data Type | Description                 |
| -------------------------- | --------- | --------------------------- |
| predicted_comfort_category | TEXT      | ML predicted comfort class  |
| prediction_confidence      | FLOAT     | Prediction confidence score |

---

## Primary ML Features

* temperature
* humidity
* pressure
* wind_speed
* precipitation

## Target Variable

comfort_category

## Location Information

| Field Name | Data Type | Description |
|------------|------------|-------------|
| city_name | TEXT | User selected city name |
| latitude | FLOAT | Geographic latitude |
| longitude | FLOAT | Geographic longitude |