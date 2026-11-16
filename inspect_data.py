
import pandas as pd

# Load our generated dataset
df = pd.read_csv("well_data.csv")

# 1. Display the first 5 rows
print("\n--- FIRST 5 ROWS ---")
print(df.head())

# 2. Check the number of rows and columns
print("\n--- DATASET SIZE ---")
print(df.shape)

# 3. Check column names and data types
print("\n--- DATA INFORMATION ---")
df.info()

# 4. Check for missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 5. Check for duplicate rows
print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

# 6. Calculate average readings for each well
print("\n--- AVERAGE READINGS BY WELL ---")
print(df.groupby("well_id")[
    ["water_depth", "salinity", "temperature", "rainfall", "pumping"]
].mean().round(2))

# 7. Display basic statistics
print("\n--- DATASET STATISTICS ---")
print(df.describe().round(2))
