
import pandas as pd

df = pd.read_csv("well_data.csv")
df["date"] = pd.to_datetime(df["date"])

latest_date = df["date"].max()

# Simulate Well_B losing its latest 3 days of readings
outage_start = latest_date - pd.Timedelta(days=2)

df = df[
    ~(
        (df["well_id"] == "Well_B") &
        (df["date"] >= outage_start)
    )
]

# Check the simulated sensor failure
for well in df["well_id"].unique():

    well_data = df[df["well_id"] == well].sort_values("date")

    last_date = well_data["date"].max()
    days_missing = (latest_date - last_date).days

    if days_missing > 2:
        status = "STALE"
        print(f"WARNING: {well} - {status}")
        print(f"No reading received for {days_missing} days")

    else:
        status = "OK"
        print(f"{well} - {status}")

print("\nSensor failure simulation completed.")
