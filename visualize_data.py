
import pandas as pd
import matplotlib.pyplot as plt

print("WELLWATCH AI - DATA VISUALIZATION")

# Load cleaned dataset
df = pd.read_csv("cleaned_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Create three charts
fig, axes = plt.subplots(3, 1, figsize=(12, 14))

# GRAPH 1: Water depth trends
for well in df["well_id"].unique():
    well_data = df[df["well_id"] == well]
    axes[0].plot(
        well_data["date"],
        well_data["water_depth"],
        label=well
    )

axes[0].set_title("Water Depth Trends Across Wells")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Depth (metres)")
axes[0].legend()
axes[0].grid(True)

# GRAPH 2: Salinity trends
for well in df["well_id"].unique():
    well_data = df[df["well_id"] == well]
    axes[1].plot(
        well_data["date"],
        well_data["salinity"],
        label=well
    )

axes[1].set_title("Salinity Trends Across Wells")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Salinity (simulated units)")
axes[1].legend()
axes[1].grid(True)

# GRAPH 3: Average water depth
average_depth = df.groupby("well_id")["water_depth"].mean()

axes[2].bar(average_depth.index, average_depth.values)
axes[2].set_title("Average Water Depth Comparison")
axes[2].set_xlabel("Well")
axes[2].set_ylabel("Average Depth (metres)")
axes[2].grid(axis="y")

plt.tight_layout()

# Save graph
plt.savefig("wellwatch_trends.png", dpi=300)

print("\nGraphs generated successfully!")
print("Saved as wellwatch_trends.png")

plt.show()
