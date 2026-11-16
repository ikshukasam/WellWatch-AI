
import pandas as pd

# Read RAW data, before missing values are filled
df = pd.read_csv("well_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Latest date available in the dataset
latest_date = df["date"].max()

results = []

for well in df["well_id"].unique():

    well_data = df[df["well_id"] == well].sort_values("date")

    # Most recent sensor reading
    last_reading = well_data.iloc[-1]
    last_date = last_reading["date"]

    # Check the last 7 calendar days
    recent_start = latest_date - pd.Timedelta(days=6)

    recent_data = well_data[
        well_data["date"] >= recent_start
    ]

    expected_days = pd.date_range(
        start=recent_start,
        end=latest_date,
        freq="D"
    )

    actual_days = pd.DatetimeIndex(recent_data["date"].dt.normalize())
    missing_days = len(expected_days.difference(actual_days))

    # Check whether the sensor has stopped sending data
    days_since_reading = (latest_date - last_date).days

    # Check whether water depth has remained unchanged
    last_five = well_data["water_depth"].tail(5)
    flatline = len(last_five) == 5 and last_five.nunique() == 1

    # Classify sensor health
    if days_since_reading > 2:
        status = "STALE"
        reason = f"No recent reading for {days_since_reading} days"

    elif missing_days > 0:
        status = "MISSING"
        reason = f"{missing_days} missing day(s) in the last 7 days"

    elif flatline:
        status = "FLATLINE"
        reason = "Water depth has not changed for 5 readings"

    else:
        status = "OK"
        reason = "Sensor readings appear normal"

    results.append({
        "well_id": well,
        "sensor_status": status,
        "last_reading_date": last_date.date(),
        "days_since_reading": days_since_reading,
        "missing_days_last_7": missing_days,
        "reason": reason
    })

# Save results
health_df = pd.DataFrame(results)
health_df.to_csv("sensor_health.csv", index=False)

print("\n========== SENSOR HEALTH REPORT ==========")
print(health_df.to_string(index=False))
print("\nSaved successfully as sensor_health.csv")
