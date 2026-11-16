
import pandas as pd
from sklearn.linear_model import LinearRegression

print("====================================")
print("       WELLWATCH AI")
print("      EARLY WARNING ENGINE")
print("====================================")

# Load our datasets
df = pd.read_csv("cleaned_data.csv")
forecasts = pd.read_csv("forecast_predictions.csv")

df["date"] = pd.to_datetime(df["date"])

alerts = []

# Analyse each well
for well in df["well_id"].unique():

    well_data = df[df["well_id"] == well].copy()
    well_data = well_data.sort_values("date")

    # Use the latest 30 days
    recent = well_data.tail(30)

    # Calculate water depth trend
    X = recent[["day_number"]]
    depth_model = LinearRegression()
    depth_model.fit(X, recent["water_depth"])

    depth_rate = depth_model.coef_[0]

    # Calculate salinity trend
    salinity_model = LinearRegression()
    salinity_model.fit(X, recent["salinity"])

    salinity_rate = salinity_model.coef_[0]

    # Get latest measurements
    latest = well_data.iloc[-1]

    current_depth = latest["water_depth"]
    current_salinity = latest["salinity"]

    # Get 21-day forecast
    future = forecasts[
        (forecasts["well_id"] == well) &
        (forecasts["forecast_days"] == 21)
    ]

    predicted_depth = future.iloc[0]["predicted_water_depth"]

    error_band = future.iloc[0][
        "error_band_90th_percentile"
    ]

    # Prototype monitoring rules
    if depth_rate >= 0.03 and salinity_rate >= 3:
        risk = "HIGH"
        action = (
            "Inspect the well, verify sensor readings, "
            "and assess pumping conditions. Prepare "
            "alternative water arrangements."
        )

    elif depth_rate >= 0.015 or salinity_rate >= 1.5:
        risk = "WATCH"
        action = (
            "Increase monitoring frequency and inspect "
            "the well and pumping activity."
        )

    else:
        risk = "LOW"
        action = (
            "Continue routine monitoring and record "
            "daily measurements."
        )

    # Save alert
    alerts.append({
        "well_id": well,
        "risk_level": risk,
        "current_depth": round(current_depth, 2),
        "predicted_depth_21_days": round(predicted_depth, 2),
        "depth_change_per_day": round(depth_rate, 4),
        "salinity_change_per_day": round(salinity_rate, 3),
        "validation_error_band": round(error_band, 3),
        "recommended_action": action
    })

# Display results
alert_df = pd.DataFrame(alerts)

print("\nWELL RISK REPORT")

for _, row in alert_df.iterrows():

    print("\n------------------------------------")
    print("WELL:", row["well_id"])
    print("RISK:", row["risk_level"])

    print("Current depth:",
          row["current_depth"], "metres")

    print("Predicted depth in 21 days:",
          row["predicted_depth_21_days"], "metres")

    print("Depth change per day:",
          row["depth_change_per_day"], "metres")

    print("Salinity change per day:",
          row["salinity_change_per_day"])

    print("90th percentile validation error:",
          row["validation_error_band"], "metres")

    print("RECOMMENDED ACTION:")
    print(row["recommended_action"])

# Save report
alert_df.to_csv("well_alerts.csv", index=False)

print("\n====================================")
print("EARLY WARNING ANALYSIS COMPLETED")
print("Saved as well_alerts.csv")
print("====================================")
