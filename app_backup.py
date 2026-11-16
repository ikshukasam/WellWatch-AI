import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="WellWatch AI",
    page_icon="💧",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------

@st.cache_data
def load_data():

    data = pd.read_csv("cleaned_data.csv")
    forecasts = pd.read_csv("forecast_predictions.csv")
    alerts = pd.read_csv("well_alerts.csv")

    try:
        sensor_health = pd.read_csv("sensor_health.csv")
    except FileNotFoundError:
        sensor_health = pd.DataFrame(columns=[
            "well_id",
            "sensor_status",
            "last_reading_date",
            "days_since_reading",
            "missing_days_last_7",
            "reason"
        ])

    data["date"] = pd.to_datetime(data["date"])
    forecasts["forecast_date"] = pd.to_datetime(
        forecasts["forecast_date"]
    )

    return data, forecasts, alerts, sensor_health


try:
    df, forecasts, alerts, sensor_health = load_data()

except Exception as error:
    st.error(f"Could not load project data: {error}")
    st.stop()


# -------------------------------
# HEADER
# -------------------------------

st.title("💧 WELLWATCH AI")

st.subheader(
    "Desert Water Source Early-Warning System"
)

st.info(
    "DEMO MODE: This prototype currently uses simulated "
    "well-monitoring data. Predictions are experimental "
    "and are not verified real-world failure warnings."
)

if st.button("🔄 Refresh Dashboard Data"):
    st.cache_data.clear()
    st.rerun()


# -------------------------------
# OVERALL WELL STATUS
# -------------------------------

st.header("Water Source Monitoring")

columns = st.columns(3)

for index, (_, alert) in enumerate(alerts.iterrows()):

    with columns[index % 3]:

        if alert["risk_level"] == "HIGH":
            st.error("🔴 HIGH RISK")

        elif alert["risk_level"] == "WATCH":
            st.warning("🟠 WATCH")

        else:
            st.success("🟢 LOW RISK")

        st.subheader(alert["well_id"])

        st.metric(
            "Current water depth",
            f'{alert["current_depth"]:.2f} m'
        )

        st.metric(
            "21-day predicted depth",
            f'{alert["predicted_depth_21_days"]:.2f} m'
        )


# -------------------------------
# INTERACTIVE WELL LOCATION MAP
# -------------------------------

st.divider()

st.header("🗺️ Desert Water Source Map")

st.warning(
    "DEMO MAP: All coordinates below are fictional "
    "demonstration locations and do not represent actual wells."
)

# Fictional demonstration coordinates
well_locations = {
    "Well_A": [24.80, 55.30],
    "Well_B": [24.85, 55.40],
    "Well_C": [24.75, 55.45]
}

map_data = alerts.copy()

map_data["latitude"] = map_data["well_id"].map(
    lambda well: well_locations.get(well, [None, None])[0]
)

map_data["longitude"] = map_data["well_id"].map(
    lambda well: well_locations.get(well, [None, None])[1]
)

# Assign marker colours based on risk
risk_colors = {
    "HIGH": "#FF0000",
    "WATCH": "#FFA500",
    "LOW": "#00AA00"
}

map_data["marker_color"] = map_data["risk_level"].map(
    risk_colors
)

# Display map
st.map(
    map_data,
    latitude="latitude",
    longitude="longitude",
    color="marker_color",
    zoom=9,
    use_container_width=True
)

# Well details below map
st.subheader("Mapped Well Details")

st.dataframe(
    map_data[
        [
            "well_id",
            "risk_level",
            "current_depth",
            "predicted_depth_21_days",
            "latitude",
            "longitude"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Red = High Risk | Orange = Watch | Green = Low Risk. "
    "Map coordinates are simulated for demonstration."
)

# -------------------------------
# SENSOR HEALTH MONITORING
# -------------------------------

st.divider()

st.header("🛠️ Sensor Health Monitoring")

st.write(
    "Checks whether monitoring sensors are sending "
    "recent and consistent readings."
)

# Demo control for judges
simulate_failure = st.checkbox(
    "🧪 Enable simulated sensor failure (Well_B)"
)

# Use a separate copy so original sensor data stays unchanged
sensor_health_display = sensor_health.copy()

if simulate_failure and not sensor_health_display.empty:

    sensor_health_display.loc[
        sensor_health_display["well_id"] == "Well_B",
        "sensor_status"
    ] = "STALE"

    sensor_health_display.loc[
        sensor_health_display["well_id"] == "Well_B",
        "days_since_reading"
    ] = 3

    sensor_health_display.loc[
        sensor_health_display["well_id"] == "Well_B",
        "reason"
    ] = "DEMO: No sensor reading received for 3 days"

if sensor_health.empty:

    st.warning(
        "Sensor health data is unavailable. "
        "Run: python sensor_health.py"
    )

else:

    sensor_columns = st.columns(3)

    for index, (_, sensor) in enumerate(
    sensor_health_display.iterrows()
):

        with sensor_columns[index % 3]:

            status = str(
                sensor["sensor_status"]
            ).upper()

            st.subheader(sensor["well_id"])

            if status == "OK":
                st.success("🟢 SENSOR HEALTHY")

            elif status == "STALE":
                st.error("🔴 SENSOR STALE")

            elif status == "MISSING":
                st.error("🔴 DATA MISSING")

            elif status == "FLATLINE":
                st.warning("🟠 SENSOR FLATLINE")

            else:
                st.warning("⚠️ UNKNOWN SENSOR STATUS")

            st.write(
                f'**Last reading:** '
                f'{sensor["last_reading_date"]}'
            )

            st.write(
                f'**Days since reading:** '
                f'{sensor["days_since_reading"]}'
            )

            st.caption(str(sensor["reason"]))


# -------------------------------
# WELL SELECTION
# -------------------------------

st.divider()

st.header("Individual Well Analysis")

selected_well = st.selectbox(
    "Select a water source",
    sorted(df["well_id"].unique())
)

well_data = df[
    df["well_id"] == selected_well
].sort_values("date")

well_alert = alerts[
    alerts["well_id"] == selected_well
].iloc[0]

well_forecast = forecasts[
    forecasts["well_id"] == selected_well
].sort_values("forecast_days")


# -------------------------------
# SELECTED SENSOR STATUS
# -------------------------------

st.subheader("Selected Well Sensor Status")

selected_sensor = sensor_health_display[
    sensor_health_display["well_id"] == selected_well
]

if selected_sensor.empty:

    st.warning(
        "No sensor health information available for this well."
    )

else:

    sensor = selected_sensor.iloc[0]

    status = str(sensor["sensor_status"]).upper()

    if status == "OK":

        st.success(
            "🟢 Sensor is healthy. Recent readings are available."
        )

    elif status == "STALE":

        st.error(
            "🔴 Sensor is stale. Recent readings have not arrived."
        )

        st.warning(
            "The water-risk prediction should be treated with "
            "extra caution until the sensor is checked."
        )

    elif status == "MISSING":

        st.error(
            "🔴 Missing sensor readings detected."
        )

        st.warning(
            "Verify the sensor connection before relying on "
            "the water-risk prediction."
        )

    elif status == "FLATLINE":

        st.warning(
            "🟠 Sensor flatline detected. The reading has "
            "remained unchanged for several observations."
        )

        st.warning(
            "Check whether the sensor is stuck or malfunctioning."
        )

    else:

        st.warning(
            "Sensor status is unknown. Verify the sensor."
        )


# -------------------------------
# PREDICTION RELIABILITY WARNING
# -------------------------------

st.subheader("Prediction Reliability")

if selected_sensor.empty:

    st.warning(
        "Sensor health data is unavailable. "
        "Prediction reliability cannot be verified."
    )

else:

    sensor_status = str(
        selected_sensor.iloc[0]["sensor_status"]
    ).upper()

    if sensor_status == "OK":

        st.success(
            "Prediction data check: No sensor-health issue detected."
        )

    else:

        st.error(
            "⚠️ SENSOR DATA WARNING: "
            "The prediction may be unreliable."
        )

        st.warning(
            "Recommended action: Inspect the sensor, restore "
            "data transmission, and verify the latest readings "
            "before making water-management decisions."
        )

        st.info(
            f"Current model risk classification: {risk if 'risk' in locals() else well_alert['risk_level']}. "
            "This classification has not been recalculated using "
            "the simulated sensor failure."
        )

# -------------------------------
# OFFLINE-READY WARNING SYSTEM
# -------------------------------

st.divider()
st.header("📡 Offline-Ready Warning System")

st.write(
    "Generate compact alerts that can be downloaded, "
    "stored locally, or shared when connectivity is available."
)

# Find sensor status for selected well
offline_sensor = sensor_health_display[
    sensor_health_display["well_id"] == selected_well
]

if offline_sensor.empty:
    offline_status = "UNKNOWN"
else:
    offline_status = str(
        offline_sensor.iloc[0]["sensor_status"]
    ).upper()

# Prepare warning message
current_depth = well_alert["current_depth"]
predicted_depth = well_alert["predicted_depth_21_days"]
current_risk = well_alert["risk_level"]

if offline_status != "OK":

    reliability_message = (
        "WARNING: Sensor data may be unreliable. "
        "Verify sensor readings."
    )

else:

    reliability_message = (
        "Sensor health check passed."
    )

offline_message = (
    f"WELLWATCH AI ALERT\n"
    f"Water source: {selected_well}\n"
    f"Risk level: {current_risk}\n"
    f"Current water depth: {current_depth:.2f} m\n"
    f"21-day predicted depth: {predicted_depth:.2f} m\n"
    f"Sensor status: {offline_status}\n"
    f"{reliability_message}\n"
    f"Recommended action: "
    f"{well_alert['recommended_action']}\n"
    f"DEMO DATA - Verify before taking action."
)

st.subheader("SMS-Ready Alert")

st.text_area(
    "Save or copy this warning message:",
    value=offline_message,
    height=220
)

st.download_button(
    label="📥 Download Selected Well Alert",
    data=offline_message,
    file_name=f"{selected_well}_alert.txt",
    mime="text/plain"
)

# Prepare a report for all wells
offline_report = alerts.merge(
    sensor_health_display[
        ["well_id", "sensor_status", "reason"]
    ],
    on="well_id",
    how="left"
)

st.subheader("All-Well Offline Report")

st.dataframe(
    offline_report[
        [
            "well_id",
            "risk_level",
            "current_depth",
            "predicted_depth_21_days",
            "sensor_status",
            "reason"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

csv_report = offline_report.to_csv(index=False)

st.download_button(
    label="📥 Download All-Well Report (CSV)",
    data=csv_report,
    file_name="wellwatch_offline_report.csv",
    mime="text/csv"
)

st.caption(
    "Offline-ready exports are generated from the current "
    "demo data. They are not automatic SMS notifications "
    "or verified emergency alerts."
)

# -------------------------------
# CURRENT MEASUREMENTS
# -------------------------------

latest = well_data.iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Water depth",
    f'{latest["water_depth"]:.2f} m'
)

col2.metric(
    "Salinity",
    f'{latest["salinity"]:.2f}'
)

col3.metric(
    "Temperature",
    f'{latest["temperature"]:.1f} °C'
)


# -------------------------------
# WATER DEPTH GRAPH
# -------------------------------

st.subheader("Historical Water Depth")

fig = px.line(
    well_data,
    x="date",
    y="water_depth",
    title=f"{selected_well} - Water Depth History",
    markers=True
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Water depth (metres)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -------------------------------
# SALINITY GRAPH
# -------------------------------

st.subheader("Historical Salinity")

fig2 = px.line(
    well_data,
    x="date",
    y="salinity",
    title=f"{selected_well} - Salinity History",
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# -------------------------------
# FUTURE PREDICTIONS
# -------------------------------

st.divider()

st.header("Future Water Depth Predictions")

forecast_display = well_forecast[
    [
        "forecast_days",
        "forecast_date",
        "predicted_water_depth"
    ]
].copy()

forecast_display.columns = [
    "Forecast Horizon (days)",
    "Forecast Date",
    "Predicted Depth (m)"
]

# -------------------------------
# PREDICTION UNCERTAINTY RANGE
# -------------------------------

historical_error = float(
    well_forecast.iloc[0]["error_band_90th_percentile"]
)

forecast_display["Estimated Lower Range (m)"] = (
    forecast_display["Predicted Depth (m)"] - historical_error
).clip(lower=0)

forecast_display["Estimated Upper Range (m)"] = (
    forecast_display["Predicted Depth (m)"] + historical_error
)

# Round values for easier reading
numeric_columns = [
    "Predicted Depth (m)",
    "Estimated Lower Range (m)",
    "Estimated Upper Range (m)"
]

forecast_display[numeric_columns] = (
    forecast_display[numeric_columns].round(3)
)

st.dataframe(
    forecast_display,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Prediction uncertainty: The estimated lower and upper "
    "ranges are calculated using the 90th-percentile absolute "
    "error from historical validation. They are illustrative "
    "error ranges, not calibrated confidence intervals or "
    "guaranteed limits."
)

st.metric(
    "Historical validation error indicator",
    f"{historical_error:.3f} m"
)


# -------------------------------
# RISK AND ACTION
# -------------------------------

st.divider()

st.header("Early Warning and Recommended Action")

risk = well_alert["risk_level"]

if risk == "HIGH":

    st.error(
        f"🚨 HIGH PRIORITY: {selected_well}"
    )

elif risk == "WATCH":

    st.warning(
        f"⚠️ MONITOR CLOSELY: {selected_well}"
    )

else:

    st.success(
        f"✅ ROUTINE MONITORING: {selected_well}"
    )

st.write("**Recommended action:**")

st.write(
    well_alert["recommended_action"]
)


# -------------------------------
# MODEL PERFORMANCE
# -------------------------------

st.divider()

st.header("Prediction Model Performance")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Validation MAE",
    f'{well_forecast.iloc[0]["validation_mae"]:.3f} m'
)

col2.metric(
    "Validation RMSE",
    f'{well_forecast.iloc[0]["validation_rmse"]:.3f} m'
)

col3.metric(
    "90th percentile validation error",
    f'{well_forecast.iloc[0]["error_band_90th_percentile"]:.3f} m'
)

st.caption(
    "These are historical validation metrics, not "
    "guaranteed future prediction accuracy or a "
    "calibrated confidence interval."
)


# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "WELLWATCH AI | Desert Water Early-Warning Prototype | "
    "Simulated demonstration data"
)