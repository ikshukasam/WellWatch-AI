
print("WELLWATCH AI - CLEANING STARTED")

import pandas as pd
import os

# Check current working directory
print("Working directory:", os.getcwd())

# Load dataset
print("\nLoading dataset...")
df = pd.read_csv("well_data.csv")

print("Original dataset loaded:", df.shape)

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Sort records
df = df.sort_values(by=["well_id", "date"])

# Remove duplicates
df = df.drop_duplicates(subset=["date", "well_id"])

# Fill missing values
numeric_columns = [
    "water_depth",
    "salinity",
    "temperature",
    "rainfall",
    "pumping"
]

for column in numeric_columns:
    df[column] = df.groupby("well_id")[column].transform(
        lambda values: values.fillna(values.median())
    )

# Create day number
df["day_number"] = df.groupby("well_id").cumcount() + 1

# Calculate rolling average
df["water_depth_7day_avg"] = (
    df.groupby("well_id")["water_depth"]
    .transform(lambda values: values.rolling(7, min_periods=1).mean())
)

# Save output using an absolute path
output_path = os.path.join(os.getcwd(), "cleaned_data.csv")

df.to_csv(output_path, index=False)

print("\nCLEANING COMPLETED!")
print("Final dataset shape:", df.shape)
print("Missing values:", df.isnull().sum().sum())
print("Saved file at:", output_path)

print("\nFirst five cleaned records:")
print(df.head())

print("\nWELLWATCH AI - CLEANING FINISHED")
