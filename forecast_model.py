
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("====================================")
print("       WELLWATCH AI")
print("     WATER DEPTH PREDICTION")
print("====================================")

# Load cleaned dataset
df = pd.read_csv("cleaned_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Store future predictions
all_forecasts = []

# Process each well separately
for well in df["well_id"].unique():

    print("\n------------------------------------")
    print("Analysing:", well)

    # Select one well
    well_data = df[df["well_id"] == well].copy()
    well_data = well_data.sort_values("day_number")

    # Input and target
    X = well_data[["day_number"]]
    y = well_data["water_depth"]

    # Split chronologically:
    # First 70 days for training
    # Last 20 days for testing
    X_train = X.iloc[:70]
    X_test = X.iloc[70:]

    y_train = y.iloc[:70]
    y_test = y.iloc[70:]

    # Train initial model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict the last 20 historical days
    test_predictions = model.predict(X_test)

    # Evaluate model performance
    mae = mean_absolute_error(y_test, test_predictions)
    rmse = np.sqrt(mean_squared_error(y_test, test_predictions))

    # Estimate a provisional error range
    absolute_errors = np.abs(y_test.values - test_predictions)
    error_band = np.quantile(absolute_errors, 0.90)

    print("Validation MAE:", round(mae, 3), "metres")
    print("Validation RMSE:", round(rmse, 3), "metres")
    print("90th percentile validation error:",
          round(error_band, 3), "metres")

    # Retrain using all 90 days
    final_model = LinearRegression()
    final_model.fit(X, y)

    # Forecast 7, 14 and 21 days after the last reading
    last_day = int(well_data["day_number"].max())
    last_date = well_data["date"].max()

    future_days = [last_day + 7, last_day + 14, last_day + 21]

    future_predictions = final_model.predict(
        pd.DataFrame({"day_number": future_days})
    )

    for days, predicted_depth in zip(
        [7, 14, 21], future_predictions
    ):

        future_date = last_date + pd.Timedelta(days=days)

        all_forecasts.append({
            "well_id": well,
            "forecast_days": days,
            "forecast_date": future_date,
            "predicted_water_depth": round(predicted_depth, 2),
            "validation_mae": round(mae, 3),
            "validation_rmse": round(rmse, 3),
            "error_band_90th_percentile": round(error_band, 3)
        })

        print(
            days, "days ahead:",
            round(predicted_depth, 2), "metres"
        )

# Convert forecasts into a DataFrame
forecast_df = pd.DataFrame(all_forecasts)

# Save predictions
forecast_df.to_csv("forecast_predictions.csv", index=False)

print("\n====================================")
print("PREDICTION COMPLETED!")
print("====================================")

print("\nAll future predictions:")
print(forecast_df.to_string(index=False))

print("\nSaved as forecast_predictions.csv")
