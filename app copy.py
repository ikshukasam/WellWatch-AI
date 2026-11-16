
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

    data["date"] = pd.to_datetime(data["date"])
    forecasts["forecast_date"] = pd.to_datetime(
        forecasts["forecast_date"]
    )

    return data, forecasts, alerts


try:
    df, forecasts, alerts = load_data()
except Exception as error:
    st.error(f"Could not load project data: {error}")
    st.stop()

# -------------------------------
# HEADER
# -------------------------------

st.title("💧 WELLWATCH AI")
st.subheader("Desert Water Source Early-Warning System")

st.info(
    "DEMO MODE: This prototype currently uses simulated "
    "well-monitoring data. Predictions are experimental "
    "and are not verified real-world failure warnings."
)

# -------------------------------
# OVERALL WELL STATUS
# -------------------------------

st.header("Water Source Monitoring")

columns = st.columns(3)

for index, (_, alert) in enumerate(alerts.iterrows()):

    with columns[index]:

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

st.plotly_chart(fig, use_container_width=True)

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

st.plotly_chart(fig2, use_container_width=True)

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

st.dataframe(
    forecast_display,
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# RISK AND ACTION
# -------------------------------

st.divider()
st.header("Early Warning and Recommended Action")

risk = well_alert["risk_level"]

if risk == "HIGH":
    st.error(f"🚨 HIGH PRIORITY: {selected_well}")
elif risk == "WATCH":
    st.warning(f"⚠️ MONITOR CLOSELY: {selected_well}")
else:
    st.success(f"✅ ROUTINE MONITORING: {selected_well}")

st.write("**Recommended action:**")
st.write(well_alert["recommended_action"])

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
