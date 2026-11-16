import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# WELLWATCH AI - DESERT WATER SOURCE EARLY-WARNING DASHBOARD
# Redesigned UI. Uses the existing project CSV files.
# ============================================================

st.set_page_config(
    page_title="WellWatch AI | Water Intelligence",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------- THEME -------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #081522; color: #e8f1f7; }
    [data-testid="stHeader"] { background: rgba(8,21,34,0); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d2233 0%, #091825 100%);
        border-right: 1px solid rgba(93, 210, 210, .16);
    }
    [data-testid="stSidebar"] * { color: #e8f1f7; }
    .block-container { padding-top: 1.6rem; padding-bottom: 2.5rem; max-width: 1500px; }
    h1, h2, h3 { color: #f2f8fb !important; letter-spacing: -.03em; }
    p, label, .stMarkdown { color: #c5d5df; }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #112b3d, #0d2232);
        border: 1px solid rgba(91, 210, 210, .18);
        padding: 17px 18px;
        border-radius: 16px;
    }
    [data-testid="stMetricLabel"] { color: #9db6c5 !important; }
    [data-testid="stMetricValue"] { color: #f2fbff !important; }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(91, 210, 210, .15);
        border-radius: 12px;
        overflow: hidden;
    }
    .hero {
        padding: 26px 30px;
        border-radius: 20px;
        background: linear-gradient(115deg, #103449 0%, #0c2639 55%, #123c43 100%);
        border: 1px solid rgba(95, 226, 216, .25);
        margin-bottom: 18px;
    }
    .hero-kicker { color: #68e0d2; font-size: 12px; font-weight: 800; letter-spacing: .16em; }
    .hero-title { color: #f4fbff; font-size: 34px; font-weight: 800; margin: 5px 0 3px; }
    .hero-sub { color: #b6cbd7; font-size: 15px; }
    .section-tag {
        color: #68e0d2; font-size: 11px; font-weight: 800;
        letter-spacing: .14em; text-transform: uppercase;
    }
    .status-pill {
        display: inline-block; padding: 5px 10px; border-radius: 30px;
        font-size: 11px; font-weight: 800; letter-spacing: .06em;
    }
    .small-muted { color: #8fa8b8; font-size: 12px; }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 10px; border: 1px solid rgba(93,210,210,.35);
        background: #12384a; color: #eafcff; font-weight: 700;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        border-color: #69e2d6; color: white; background: #17495a;
    }
    [data-baseweb="tab"] { color: #c5d5df; }
    hr { border-color: rgba(132, 177, 197, .16); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------- DATA -------------------------------
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    required = {
        "cleaned_data.csv": "cleaned historical well readings",
        "forecast_predictions.csv": "model forecast output",
        "well_alerts.csv": "well risk and recommended actions",
    }
    missing = [name for name in required if not (BASE_DIR / name).exists()]
    if missing:
        raise FileNotFoundError(
            "Missing project data file(s): " + ", ".join(missing)
            + ". Run the project data-generation, cleaning, forecasting, "
              "and alert scripts first."
        )

    data = pd.read_csv(BASE_DIR / "cleaned_data.csv")
    forecasts = pd.read_csv(BASE_DIR / "forecast_predictions.csv")
    alerts = pd.read_csv(BASE_DIR / "well_alerts.csv")

    sensor_path = BASE_DIR / "sensor_health.csv"
    if sensor_path.exists():
        sensor_health = pd.read_csv(sensor_path)
    else:
        sensor_health = pd.DataFrame(columns=[
            "well_id", "sensor_status", "last_reading_date",
            "days_since_reading", "missing_days_last_7", "reason"
        ])

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    if "forecast_date" in forecasts.columns:
        forecasts["forecast_date"] = pd.to_datetime(
            forecasts["forecast_date"], errors="coerce"
        )
    return data, forecasts, alerts, sensor_health


try:
    df, forecasts, alerts, sensor_health = load_data()
except Exception as error:
    st.error(f"Unable to load WellWatch AI data: {error}")
    st.info(
        "Check that app.py and the CSV files are in the same project folder. "
        "Then run your existing Python pipeline scripts."
    )
    st.stop()

# Normalize text fields to avoid case-related mismatches.
for frame, column in [
    (alerts, "well_id"), (df, "well_id"),
    (forecasts, "well_id"), (sensor_health, "well_id")
]:
    if column in frame.columns:
        frame[column] = frame[column].astype(str)

if alerts.empty or df.empty or forecasts.empty:
    st.error("One or more required CSV files contain no records.")
    st.stop()

# ------------------------------- HELPERS -------------------------------
def risk_color(level):
    level = str(level).upper()
    return {"HIGH": "#ff647c", "WATCH": "#ffbd59", "LOW": "#5bd6ad"}.get(
        level, "#9db6c5"
    )

def show_risk(level):
    level = str(level).upper()
    if level == "HIGH":
        st.error("🔴 HIGH RISK")
    elif level == "WATCH":
        st.warning("🟠 WATCH")
    else:
        st.success("🟢 LOW RISK")

def get_sensor_row(well_id, sensor_frame):
    if sensor_frame.empty or "well_id" not in sensor_frame.columns:
        return None
    match = sensor_frame[sensor_frame["well_id"] == well_id]
    return None if match.empty else match.iloc[0]

# ------------------------------- SIDEBAR -------------------------------
with st.sidebar:
    st.markdown("## 💧 WELLWATCH AI")
    st.caption("WATER INTELLIGENCE PLATFORM")
    st.divider()
    page = st.radio(
        "NAVIGATION",
        ["Overview", "Well analysis", "Sensor health", "Alerts & reports", "About"],
        label_visibility="visible",
    )
    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.success("Dashboard loaded")
    st.caption(f"{df['well_id'].nunique()} monitored demo wells")
    if st.button("↻ Refresh dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.caption("Prototype • Simulated monitoring data")

# ------------------------------- HEADER -------------------------------
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">DESERT WATER SOURCE EARLY-WARNING SYSTEM</div>
      <div class="hero-title">Water intelligence, at a glance.</div>
      <div class="hero-sub">Monitor well conditions, explore experimental forecasts,
      and review sensor reliability from one dashboard.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.warning(
    "DEMO MODE — This prototype uses simulated well-monitoring data. "
    "Predictions and risk thresholds are experimental, not verified "
    "real-world failure warnings."
)

well_ids = sorted(df["well_id"].dropna().unique().tolist())
selected_well = None
if page == "Well analysis":
    selected_well = st.selectbox("Choose a water source", well_ids)

# ------------------------------- OVERVIEW -------------------------------
if page == "Overview":
    st.markdown('<div class="section-tag">LIVE DEMONSTRATION SNAPSHOT</div>', unsafe_allow_html=True)
    st.header("Water source monitoring")

    cards = st.columns(min(3, max(1, len(alerts))))
    for idx, (_, alert) in enumerate(alerts.iterrows()):
        with cards[idx % len(cards)]:
            level = str(alert.get("risk_level", "UNKNOWN")).upper()
            show_risk(level)
            st.subheader(str(alert["well_id"]))
            st.metric("Current water depth", f"{float(alert['current_depth']):.2f} m")
            st.metric(
                "21-day predicted depth",
                f"{float(alert['predicted_depth_21_days']):.2f} m"
            )

    st.divider()
    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("Water depth trends")
        trend = df.sort_values("date")
        fig = px.line(
            trend, x="date", y="water_depth", color="well_id",
            markers=False, template="plotly_dark",
            labels={"date": "Date", "water_depth": "Water depth (m)", "well_id": "Well"},
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend_title_text="", margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Risk distribution")
        risk_counts = alerts["risk_level"].astype(str).str.upper().value_counts().reset_index()
        risk_counts.columns = ["Risk level", "Wells"]
        fig_risk = px.pie(
            risk_counts, names="Risk level", values="Wells", hole=0.62,
            template="plotly_dark", color="Risk level",
            color_discrete_map={"HIGH": "#ff647c", "WATCH": "#ffbd59", "LOW": "#5bd6ad"},
        )
        fig_risk.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=5, r=5, t=10, b=5), legend_title_text="",
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    st.subheader("At-a-glance well register")
    display_cols = [
        c for c in ["well_id", "risk_level", "current_depth",
                    "predicted_depth_21_days", "recommended_action"]
        if c in alerts.columns
    ]
    st.dataframe(alerts[display_cols], use_container_width=True, hide_index=True)

# ------------------------------- WELL ANALYSIS -------------------------------
elif page == "Well analysis":
    st.markdown('<div class="section-tag">INDIVIDUAL SOURCE PROFILE</div>', unsafe_allow_html=True)
    st.header(f"{selected_well} · Well analysis")

    well_data = df[df["well_id"] == selected_well].sort_values("date")
    well_alert_rows = alerts[alerts["well_id"] == selected_well]
    well_forecast = forecasts[forecasts["well_id"] == selected_well].copy()

    if well_data.empty or well_alert_rows.empty or well_forecast.empty:
        st.error("Data for this well is incomplete. Check the CSV files.")
        st.stop()

    well_alert = well_alert_rows.iloc[0]
    latest = well_data.iloc[-1]
    sensor = get_sensor_row(selected_well, sensor_health)

    show_risk(well_alert.get("risk_level", "UNKNOWN"))
    m1, m2, m3 = st.columns(3)
    m1.metric("Current water depth", f"{float(latest['water_depth']):.2f} m")
    if "salinity" in latest:
        m2.metric("Salinity", f"{float(latest['salinity']):.2f}")
    if "temperature" in latest:
        m3.metric("Temperature", f"{float(latest['temperature']):.1f} °C")

    st.divider()
    tab1, tab2, tab3 = st.tabs(["Historical trends", "Future predictions", "Recommended action"])
    with tab1:
        st.subheader("Water depth history")
        depth_fig = px.line(
            well_data, x="date", y="water_depth", markers=True,
            template="plotly_dark", labels={"date": "Date", "water_depth": "Depth (m)"},
        )
        depth_fig.update_traces(line=dict(color="#55d9cf", width=3))
        depth_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=25, b=10),
        )
        st.plotly_chart(depth_fig, use_container_width=True)

        if "salinity" in well_data.columns:
            st.subheader("Salinity history")
            sal_fig = px.line(
                well_data, x="date", y="salinity", markers=True,
                template="plotly_dark", labels={"date": "Date", "salinity": "Salinity"},
            )
            sal_fig.update_traces(line=dict(color="#f5b85b", width=3))
            sal_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=25, b=10),
            )
            st.plotly_chart(sal_fig, use_container_width=True)

    with tab2:
        st.subheader("Future water depth predictions")
        sort_col = "forecast_days" if "forecast_days" in well_forecast.columns else None
        if sort_col:
            well_forecast = well_forecast.sort_values(sort_col)
        forecast_cols = [
            c for c in ["forecast_days", "forecast_date", "predicted_water_depth"]
            if c in well_forecast.columns
        ]
        forecast_display = well_forecast[forecast_cols].copy()
        rename_map = {
            "forecast_days": "Forecast horizon (days)",
            "forecast_date": "Forecast date",
            "predicted_water_depth": "Predicted depth (m)",
        }
        forecast_display = forecast_display.rename(columns=rename_map)

        error_value = None
        if "error_band_90th_percentile" in well_forecast.columns:
            error_value = float(well_forecast.iloc[0]["error_band_90th_percentile"])
            if "Predicted depth (m)" in forecast_display.columns:
                forecast_display["Estimated lower range (m)"] = (
                    forecast_display["Predicted depth (m)"] - error_value
                ).clip(lower=0)
                forecast_display["Estimated upper range (m)"] = (
                    forecast_display["Predicted depth (m)"] + error_value
                )
        st.dataframe(
            forecast_display.round(3), use_container_width=True, hide_index=True
        )
        if error_value is not None:
            st.metric("Historical validation error indicator", f"{error_value:.3f} m")
        st.info(
            "The displayed range uses the 90th-percentile absolute error from "
            "historical validation. It is illustrative, not a calibrated "
            "confidence interval or a guaranteed limit."
        )
        if "predicted_water_depth" in well_forecast.columns and "forecast_days" in well_forecast.columns:
            pred_fig = px.line(
                well_forecast, x="forecast_days", y="predicted_water_depth",
                markers=True, template="plotly_dark",
                labels={"forecast_days": "Days ahead", "predicted_water_depth": "Predicted depth (m)"},
            )
            pred_fig.update_traces(line=dict(color="#55d9cf", width=3))
            pred_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(pred_fig, use_container_width=True)

    with tab3:
        st.subheader("Early warning and recommended action")
        show_risk(well_alert.get("risk_level", "UNKNOWN"))
        st.write(well_alert.get("recommended_action", "No recommended action available."))
        if sensor is None:
            st.warning("Sensor health information is unavailable for this well.")
        else:
            sensor_status = str(sensor.get("sensor_status", "UNKNOWN")).upper()
            if sensor_status == "OK":
                st.success("Sensor health check: no issue detected in the demo data.")
            else:
                st.error(f"Sensor status: {sensor_status}. Treat the prediction with extra caution.")
        if all(c in well_forecast.columns for c in ["validation_mae", "validation_rmse"]):
            f1, f2 = st.columns(2)
            f1.metric("Validation MAE", f"{float(well_forecast.iloc[0]['validation_mae']):.3f} m")
            f2.metric("Validation RMSE", f"{float(well_forecast.iloc[0]['validation_rmse']):.3f} m")
        st.caption("Validation metrics describe this simulated historical test split, not guaranteed future accuracy.")

# ------------------------------- SENSOR HEALTH -------------------------------
elif page == "Sensor health":
    st.markdown('<div class="section-tag">DATA QUALITY MONITORING</div>', unsafe_allow_html=True)
    st.header("Sensor health centre")
    st.write("Review whether monitoring sensors are sending recent and consistent readings.")

    simulate_failure = st.toggle("Simulate a stale sensor for Well_B", value=False)
    sensor_display = sensor_health.copy()
    if simulate_failure and not sensor_display.empty and "well_id" in sensor_display.columns:
        if "sensor_status" in sensor_display.columns:
            sensor_display.loc[sensor_display["well_id"] == "Well_B", "sensor_status"] = "STALE"
        if "days_since_reading" in sensor_display.columns:
            sensor_display.loc[sensor_display["well_id"] == "Well_B", "days_since_reading"] = 3
        if "reason" in sensor_display.columns:
            sensor_display.loc[
                sensor_display["well_id"] == "Well_B", "reason"
            ] = "DEMO: No sensor reading received for 3 days"

    if sensor_display.empty:
        st.warning("Sensor health data is unavailable. Run: python sensor_health.py")
    else:
        status_col = "sensor_status" if "sensor_status" in sensor_display.columns else None
        if status_col:
            counts = sensor_display[status_col].astype(str).str.upper().value_counts()
            a, b, c = st.columns(3)
            a.metric("Healthy", int(counts.get("OK", 0)))
            b.metric("Stale", int(counts.get("STALE", 0)))
            c.metric("Missing", int(counts.get("MISSING", 0)))
        st.dataframe(sensor_display, use_container_width=True, hide_index=True)
        for _, sensor_row in sensor_display.iterrows():
            status = str(sensor_row.get("sensor_status", "UNKNOWN")).upper()
            if status == "OK":
                st.success(f"{sensor_row.get('well_id', 'Well')}: sensor healthy")
            elif status in ("STALE", "MISSING", "FLATLINE"):
                st.warning(
                    f"{sensor_row.get('well_id', 'Well')}: {status} — "
                    f"{sensor_row.get('reason', 'Check sensor readings.')}"
                )
            else:
                st.info(f"{sensor_row.get('well_id', 'Well')}: status {status}")
    st.caption("The simulated sensor failure is for demonstration only and does not recalculate model risk.")

# ------------------------------- ALERTS & REPORTS -------------------------------
elif page == "Alerts & reports":
    st.markdown('<div class="section-tag">FIELD-READY OUTPUTS</div>', unsafe_allow_html=True)
    st.header("Alerts and offline-ready reports")
    well_choice = st.selectbox("Select a well for its alert", well_ids)
    alert_rows = alerts[alerts["well_id"] == well_choice]
    if alert_rows.empty:
        st.warning("No alert record found for this well.")
    else:
        alert = alert_rows.iloc[0]
        sensor = get_sensor_row(well_choice, sensor_health)
        sensor_status = "UNKNOWN" if sensor is None else str(sensor.get("sensor_status", "UNKNOWN")).upper()
        reliability = (
            "WARNING: Sensor data may be unreliable. Verify sensor readings."
            if sensor_status != "OK" else "Sensor health check passed."
        )
        current_depth = float(alert.get("current_depth", 0))
        predicted_depth = float(alert.get("predicted_depth_21_days", 0))
        risk_level = str(alert.get("risk_level", "UNKNOWN"))
        action = str(alert.get("recommended_action", "Review the well."))
        offline_message = (
            "WELLWATCH AI ALERT\n"
            f"Water source: {well_choice}\n"
            f"Risk level: {risk_level}\n"
            f"Current water depth: {current_depth:.2f} m\n"
            f"21-day predicted depth: {predicted_depth:.2f} m\n"
            f"Sensor status: {sensor_status}\n"
            f"{reliability}\n"
            f"Recommended action: {action}\n"
            "DEMO DATA - Verify before taking action."
        )
        st.text_area("SMS-ready alert (copy or save)", value=offline_message, height=210)
        st.download_button(
            "Download selected well alert",
            data=offline_message,
            file_name=f"{well_choice}_alert.txt",
            mime="text/plain",
        )

    st.divider()
    st.subheader("All-well report")
    report = alerts.copy()
    if not sensor_health.empty and "well_id" in sensor_health.columns:
        cols = [c for c in ["well_id", "sensor_status", "reason"] if c in sensor_health.columns]
        report = report.merge(sensor_health[cols], on="well_id", how="left")
    st.dataframe(report, use_container_width=True, hide_index=True)
    st.download_button(
        "Download all-well report (CSV)",
        data=report.to_csv(index=False),
        file_name="wellwatch_all_well_report.csv",
        mime="text/csv",
    )
    st.caption("These are downloadable demo alerts, not automatic SMS messages or verified emergency warnings.")

# ------------------------------- ABOUT -------------------------------
elif page == "About":
    st.markdown('<div class="section-tag">PROJECT INFORMATION</div>', unsafe_allow_html=True)
    st.header("About WellWatch AI")
    st.write(
        "WellWatch AI is a prototype dashboard designed to demonstrate how "
        "water-source monitoring data, simple forecasting, risk rules, and "
        "sensor-health checks can be brought together in one interface."
    )
    st.subheader("What this prototype demonstrates")
    st.markdown(
        "- Historical water-depth and salinity visualisation\n"
        "- Per-well experimental water-depth forecasts\n"
        "- Rule-based HIGH / WATCH / LOW risk labels\n"
        "- Sensor-health status and a simulated stale-sensor scenario\n"
        "- Downloadable well alerts and CSV reports"
    )
    st.subheader("Important limitations")
    st.markdown(
        "- The dataset is simulated and is not connected to real sensors.\n"
        "- Forecasts are experimental and use a simplified time-based model.\n"
        "- Risk thresholds are demonstration rules, not locally validated thresholds.\n"
        "- Forecast error ranges are illustrative and are not calibrated confidence intervals.\n"
        "- Sensor-failure simulation does not recalculate the water-risk model.\n"
        "- Downloadable alerts are not automatically transmitted by SMS."
    )
    st.info("Do not use this prototype for real-world water-management or emergency decisions.")

# ------------------------------- FOOTER -------------------------------
st.divider()
st.markdown(
    '<p class="small-muted">WELLWATCH AI · DESERT WATER SOURCE EARLY-WARNING PROTOTYPE · SIMULATED DATA</p>',
    unsafe_allow_html=True,
)
