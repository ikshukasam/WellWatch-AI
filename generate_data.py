
import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Generate 90 days
dates = pd.date_range(start="2026-08-19", periods=90, freq="D")

data = []

# Generate readings for 3 wells
for well in ["Well_A", "Well_B", "Well_C"]:

    for day in range(90):

        # Different starting conditions
        if well == "Well_A":
            base_depth = 15
            decline = 0.015

        elif well == "Well_B":
            base_depth = 18
            decline = 0.045

        else:
            base_depth = 12
            decline = 0.005

        water_depth = (
            base_depth
            + decline * day
            + np.random.normal(0, 0.08)
        )

        salinity = (
            1200
            + decline * 100 * day
            + np.random.normal(0, 15)
        )

        temperature = (
            38
            + np.random.normal(0, 3)
        )

        rainfall = max(
            0,
            np.random.normal(0.3, 0.5)
        )

        pumping = (
            30
            + np.random.normal(0, 4)
        )

        data.append({
            "date": dates[day],
            "well_id": well,
            "water_depth": round(water_depth, 2),
            "salinity": round(salinity, 2),
            "temperature": round(temperature, 2),
            "rainfall": round(rainfall, 2),
            "pumping": round(pumping, 2)
        })

# Convert into a DataFrame
df = pd.DataFrame(data)

# Save dataset
df.to_csv("well_data.csv", index=False)

print("Dataset generated successfully!")
print(df.head(10))
print("\nDataset shape:", df.shape)
