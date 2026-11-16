
💧 WellWatch AI
Desert Water Source Monitoring & Early-Warning System
Hackathon track: W-001 — Early Warnings for Desert Water Sources
Event: Breaking Bytes — The 24-Hour Underground Hackathon
Team: Ikshu, Bharath, Shradha
Prototype status: Demonstration prototype using simulated well-monitoring data

Table of Contents
1. Project Overview
2. The Problem
3. Our Proposed Solution
4. Project Objectives
5. Key Features
6. How the System Works
7. System Architecture
8. Technology Stack
9. Project Structure
10. Dataset Description
11. Data Generation
12. Data Inspection and Cleaning
13. Exploratory Data Analysis and Visualisation
14. Prediction Model
15. Model Evaluation
16. Prediction Uncertainty
17. Early-Warning and Risk Classification
18. Sensor Health Monitoring
19. Simulated Sensor Failure Demonstration
20. Dashboard Experience
21. Map Visualisation
22. Offline-Ready Alert Exports
23. Installation and Setup
24. Running the Complete Project
25. Running the Dashboard
26. How to Use the Dashboard
27. Example Demonstration Scenario
28. Responsible Use and Important Limitations
29. Testing and Reproducibility
30. Challenges Addressed
31. Potential Real-World Deployment
32. Future Improvements
33. Impact and Use Cases
34. Team Contributions
35. Hackathon Demo Guide
36. Frequently Asked Questions
37. Troubleshooting
38. Acknowledgements
39. License
40. Disclaimer
1. Project Overview
WellWatch AI is a prototype early-warning platform designed around a critical challenge in desert environments: monitoring limited water sources and identifying potentially concerning changes before they become emergencies.

The project brings together a data-processing pipeline, time-trend forecasting, rule-based risk classification, sensor-health checks, and an interactive web dashboard.

The prototype monitors three demonstration wells. It displays recent readings, historical trends, predicted water-depth values, risk categories, model evaluation metrics, sensor status, and recommended actions.

The goal is to demonstrate how a practical monitoring workflow could help users notice changing conditions earlier and decide when a well should receive additional inspection.
What makes the prototype useful?
- It turns tabular readings into visual trends that are easier to interpret.
- It produces short-horizon water-depth forecasts.
- It separates water-risk indicators from sensor-health warnings.
- It demonstrates how stale sensor data can be flagged.
- It presents recommended next steps in a simple dashboard.
- It provides downloadable alert information for use when connectivity is limited.
Important prototype note
The current project uses simulated well-monitoring data. It is a working technical demonstration, not a deployed groundwater-monitoring service. The sample wells and map coordinates are fictional. The predictions and warning thresholds have not been validated for real wells.
2. The Problem
Desert communities, farms, and remote facilities can depend on a small number of groundwater sources. These sources may be difficult to inspect frequently, especially when monitoring locations are spread over large areas.

A water source can change gradually. If readings are collected infrequently or are difficult to interpret, a concerning trend may not be noticed until the impact is already significant.

Some of the practical challenges include:
- Sparse monitoring measurements.
- Inconsistent or missing sensor readings.
- Communication gaps in remote areas.
- Environmental conditions that change over time.
- Difficulty interpreting multiple readings together.
- The risk of treating old sensor data as if it were current.
- The need to communicate warnings in a clear and actionable way.
A useful early-warning prototype should not only show a current reading. It should also show the direction of change, provide an estimate of what may happen next, explain uncertainty, and identify when the underlying data may be unreliable.
3. Our Proposed Solution
WellWatch AI demonstrates a simple monitoring workflow:
1. Generate or receive well-monitoring records.
2. Inspect the dataset for quality issues.
3. clean and transform the records.
4. Visualise historical water-depth and salinity trends.
5. Train and evaluate a forecasting model.
6. Estimate future water depth at selected forecast horizons.
7. Classify the recent trend into a demonstration risk category.
8. Check whether the sensor readings appear current.
9. Display the results in an interactive dashboard.
10. Present recommended actions and exportable alert information.
The system is designed to make the output understandable to a user who may not have a machine-learning background.
4. Project Objectives
The project has the following objectives:
- Demonstrate a complete data-to-dashboard pipeline.
- Monitor multiple example water sources.
- Forecast future water-depth trends.
- Show historical model errors rather than presenting predictions as certain.
- Categorise wells into Low, Watch, and High demonstration risk levels.
- Detect a simulated stale-sensor condition.
- Explain why sensor reliability matters to prediction interpretation.
- Display information through a browser-based dashboard.
- Demonstrate alert exports that could support communication in low-connectivity settings.
- Establish a foundation for future integration with real sensor and public environmental datasets.
5. Key Features
5.1 Multi-well overview
The dashboard provides an overview of three demonstration wells:
- Well_A
- Well_B
- Well_C
Each well has a current risk label, latest water-depth reading, and 21-day forecast.
5.2 Historical trend analysis
Interactive charts show historical water depth and salinity readings over time. These help users compare the behaviour of each well.
5.3 Short-horizon forecasting
The model generates estimated water-depth values for:
- 7 days ahead
- 14 days ahead
- 21 days ahead
5.4 Risk classification
A separate warning engine examines recent water-depth and salinity trends and assigns a demonstration category:
- LOW: The recent trend does not cross the prototype warning thresholds.
- WATCH: At least one monitored trend crosses a moderate prototype threshold.
- HIGH: Both configured high-risk trend conditions are met.
5.5 Sensor-health warning
The prototype checks whether a sensor's latest reading is sufficiently recent. A stale reading is flagged so that users do not assume the data is current.
5.6 Prediction error information
The dashboard displays validation metrics such as MAE and RMSE, together with a historical absolute-error measure used to illustrate forecast uncertainty.
5.7 Map view
A map displays the three fictional demonstration well locations and their risk categories.
5.8 Offline-ready exports
The prototype can prepare alert information in downloadable text or CSV form. These files can be transferred when a communication channel is available.

The current version does not send SMS messages or operate a live alert-delivery service.
6. How the System Works
The project is organised as a pipeline. Each stage creates or prepares an output used by a later stage.
Simulated well readings
        |
        v
Data inspection
        |
        v
Data cleaning and feature preparation
        |
        +----------------------+
        |                      |
        v                      v
Trend visualisation      Forecast model
                               |
                               v
                       Future depth estimates
                               |
                               v
                       Early-warning engine
                               |
                               v
                       Risk and action output

Sensor-health checks ------------------+
                                        |
                                        v
                              Streamlit dashboard
                                        |
                     +------------------+------------------+
                     |                  |                  |
                     v                  v                  v
                Well overview       Trend charts       Alert exports
The dashboard reads the processed CSV files created by the pipeline. This keeps data preparation and presentation as separate responsibilities.
7. System Architecture
Data layer
The data layer contains the well readings and processed outputs. In this prototype, the original records are generated locally by Python.
Processing layer
Pandas is used to load, inspect, sort, clean, group, and transform records. The cleaning stage also creates a day-number feature and a rolling water-depth average.
Modelling layer
Scikit-learn provides the Linear Regression model. Each well is modelled separately using its historical water-depth readings against the day-number feature.
Warning layer
The alert engine calculates recent trend slopes and applies explicit demonstration thresholds to produce risk labels and recommended actions.
Reliability layer
The sensor-health component checks whether readings are stale. Its output is displayed separately from the model's risk label.
Presentation layer
Streamlit provides the browser-based interface. Plotly is used for interactive charts, while Pandas supplies the dashboard tables.
8. Technology Stack
Technology	Purpose
Python	Main programming language
Pandas	Data loading, cleaning, transformation, and analysis
NumPy	Numerical operations
Matplotlib	Static trend visualisation
Scikit-learn	Linear Regression and model evaluation
Streamlit	Interactive web dashboard
Plotly	Interactive charts
CSV	Simple data exchange between pipeline stages
GitHub	Source-code hosting and project documentation


The project is designed to run locally on a standard computer with Python installed.
9. Project Structure
The main project folder should look similar to this:
WellWatch-AI/
├── app.py
├── generate_data.py
├── inspect_data.py
├── clean_data.py
├── visualize_data.py
├── forecast_model.py
├── alert_engine.py
├── sensor_health.py
├── requirements.txt
├── README.md
├── .gitignore
├── cleaned_data.csv
├── forecast_predictions.csv
├── well_alerts.csv
└── sensor_health.csv
Some generated files may only appear after running the relevant scripts. The exact filenames should match the filenames referenced by the local version of app.py.

Do not include the Python virtual-environment folder (.venv) in the GitHub repository.
10. Dataset Description
The demonstration dataset contains 90 days of records for three wells, resulting in 270 rows.

The dataset contains these columns:
Column	Description
date	Date associated with the reading
well_id	Identifier for the monitored demonstration well
water_depth	Water-level depth measured from a reference point, in metres in the simulation
salinity	Simulated salinity indicator
temperature	Simulated temperature reading
rainfall	Simulated rainfall feature
pumping	Simulated pumping feature


The values are generated for demonstration. The rainfall and pumping columns do not currently have validated physical units or a calibrated relationship to a real location.
Demonstration well patterns
The generator uses different underlying depth trends so that the dashboard can demonstrate different warning categories:
- Well_A has a moderate increasing depth trend.
- Well_B has a stronger increasing depth trend.
- Well_C has a relatively gradual depth trend.
The generated patterns are not observations about actual groundwater sources.
Direction of water depth
In this prototype, water depth is measured downward from a fixed reference. An increasing depth value therefore represents the water surface being farther below that reference. This is different from a measurement where a larger value means more water stored.
11. Data Generation
The generate_data.py script creates the synthetic well dataset.

The generator uses a fixed random seed so that the demonstration can be reproduced. It creates a date sequence and generates readings for each of the three wells.

The synthetic dataset is useful for testing the software pipeline because it provides:
- Multiple well identifiers.
- A time dimension.
- Different trend patterns.
- Several environmental-style variables.
- Enough rows to demonstrate a chronological train/test split.
Run:
python generate_data.py
The script should create well_data.csv.

Do not describe this generated dataset as real sensor data. If real data is added later, document its source, date range, units, missing-data handling, and usage conditions.
12. Data Inspection and Cleaning
Inspection
The inspect_data.py script checks the generated dataset. Typical checks include:
- Displaying the first records.
- Checking the number of rows and columns.
- Inspecting data types.
- Counting missing values.
- Checking duplicate records.
- Reviewing summary statistics.
- Comparing average values by well.
Run:
python inspect_data.py
Cleaning
The clean_data.py script prepares the data for analysis. The current workflow:
1. Loads the original CSV.
2. Converts the date column to a datetime type.
3. Sorts records by well and date.
4. Removes duplicate date/well records.
5. Handles numeric missing values using per-well median values.
6. Creates a sequential day_number feature.
7. Calculates a rolling seven-day water-depth average.
8. Saves the cleaned dataset.
Run:
python clean_data.py
The output is cleaned_data.csv.
Why clean data?
A model can produce misleading output if records are incorrectly ordered, duplicated, missing, or represented using inconsistent data types. Basic checks help make the processing pipeline more reliable.

The current cleaning strategy is suitable for this small synthetic demonstration. A real deployment would need more careful rules for long outages, sensor calibration, impossible readings, unit mismatches, and missing periods.
13. Exploratory Data Analysis and Visualisation
The visualize_data.py script creates static charts from the cleaned dataset.

The charts help compare:
- Water-depth trends over time.
- Salinity trends over time.
- Average water depth across the demonstration wells.
Run:
python visualize_data.py
The script saves wellwatch_trends.png.

Visualisation is important because a single reading does not reveal whether a well is stable, gradually changing, or showing a sudden unusual movement.

The plotted patterns reflect the simulated input and should not be interpreted as field findings.
14. Prediction Model
The current forecasting component uses Linear Regression from Scikit-learn.
Model input and target
For each well, the model uses:
- Input feature (X): day_number
- Target (y): water_depth
The model learns a straight-line relationship between time and water depth.

Conceptually:
Predicted water depth = intercept + (slope × day number)
Separate model per well
Each well is modelled independently. This avoids combining the three demonstration trends into one shared line.
Chronological split
The first 70 days are used for training and the final 20 days are used for testing.

A chronological split is more appropriate for this time-ordered demonstration than randomly mixing earlier and later observations.
Forecast horizons
After evaluation, the model is refitted using all 90 days of available demonstration history. It then estimates water depth at day 97, day 104, and day 111, corresponding to 7, 14, and 21 days after the final observation.

Run:
python forecast_model.py
The output is forecast_predictions.csv.
Important model scope
The current forecasting model uses only day_number as its input feature. It does not use salinity, temperature, rainfall, pumping, satellite imagery, or external climate data as model predictors.

Those other columns are part of the monitoring dataset, and salinity is used separately by the warning engine. They should not be described as inputs to the current Linear Regression forecast.
15. Model Evaluation
The model is evaluated using two common regression metrics.
Mean Absolute Error (MAE)
MAE is the average absolute difference between the observed values and predicted values.

A lower MAE indicates smaller average absolute prediction errors on the evaluation data.
Root Mean Squared Error (RMSE)
RMSE is the square root of the average squared prediction error. It penalises larger errors more strongly than MAE.
Why report both?
Reporting more than one metric gives a clearer view of model performance. MAE is easy to interpret as an average absolute error, while RMSE gives additional weight to larger misses.

The metrics displayed by this prototype describe performance on its chronological holdout portion of the simulated dataset. They are not a guarantee of real-world forecasting performance.
Example validation values from the demonstration run
Well	MAE (m)	RMSE (m)
Well_A	0.061	0.074
Well_B	0.065	0.082
Well_C	0.060	0.078


These are example outputs from the current generated dataset and may change if the data-generation logic changes.
16. Prediction Uncertainty
A forecast is an estimate, not a certainty. WellWatch AI therefore displays an error-based range alongside the forecast.

The current implementation calculates the 90th percentile of the absolute errors observed on the chronological validation set. It uses this value as a simple historical error band around the forecast.

For example, if the predicted depth is 16.63 m and the displayed error amount is 0.11 m, the illustrative range is formed by subtracting and adding that amount.
Important statistical qualification
This is an empirical historical error band. It is not a statistically calibrated 90% prediction interval, and it should not be described as a guarantee that the true value has a 90% probability of falling inside the displayed range.

A production-grade uncertainty method would require stronger statistical validation, suitable time-series backtesting, and calibration using representative real-world data.
17. Early-Warning and Risk Classification
The alert_engine.py script analyses recent trends for each well.

It uses the latest 30 days of readings to estimate trend slopes for:
- Water depth.
- Salinity.
The script then applies the prototype rules below.
Demonstration thresholds
if depth_rate >= 0.03 and salinity_rate >= 3:
    risk = "HIGH"
elif depth_rate >= 0.015 or salinity_rate >= 1.5:
    risk = "WATCH"
else:
    risk = "LOW"
These values are configurable demonstration thresholds. They are not official groundwater safety limits or validated thresholds for a particular aquifer.
Interpretation
HIGH

Both the water-depth trend and salinity trend exceed the configured high-risk thresholds. The dashboard recommends prompt inspection, verification of readings, review of pumping conditions, and preparation of alternative water arrangements where appropriate.

WATCH

At least one recent trend crosses a moderate threshold. The dashboard recommends increased monitoring and inspection.

LOW

The current trends do not cross the prototype warning thresholds. The dashboard recommends routine monitoring.
Recommended actions
The warning engine connects its categories to simple suggested actions. These are prompts for human review, not automatic operational instructions.

Run:
python alert_engine.py
The output is well_alerts.csv.
18. Sensor Health Monitoring
A prediction is only as useful as the data supporting it. A sensor that stops transmitting can leave the dashboard showing old values.

The sensor-health component checks the recency of readings and produces a status for each demonstration well.

Typical statuses include:
- OK: A recent reading is available.
- WARNING / STALE: A reading has not arrived within the configured time threshold.
Run:
python sensor_health.py
The output is sensor_health.csv.
Why keep sensor health separate?
A stale sensor does not automatically mean the water source is in danger. It means the monitoring data may be incomplete or outdated.

Keeping sensor status separate from the water-risk category helps prevent users from confusing a communication problem with a confirmed groundwater problem.
19. Simulated Sensor Failure Demonstration
The project includes a demonstration of a sensor that stops sending readings.

The test can simulate a stale reading for Well_B. The dashboard then displays a sensor warning and advises the user to treat the associated prediction with extra caution until the sensor is checked.

If included in the local project, run:
python test_sensor_failure.py
The exact output depends on the implementation and the current test configuration.
What this demonstrates
- The system can represent a stale-data condition.
- The dashboard can communicate that condition clearly.
- Users are reminded not to treat old measurements as current.
- Sensor reliability is shown as a separate dimension from water-risk classification.
What it does not demonstrate
The simulated failure is not a test of a physical sensor, radio network, satellite connection, or deployed IoT device. In the current implementation, the simulated sensor failure does not automatically retrain the forecast model or recalculate the water-risk classification.
20. Dashboard Experience
The dashboard is implemented using Streamlit and is opened in a web browser.

The main interface includes:
- Project title and prototype disclaimer.
- Overview cards for all monitored wells.
- Risk categories and current depth readings.
- 21-day forecast values.
- Sensor-health status.
- A well selector for detailed analysis.
- Historical water-depth chart.
- Historical salinity chart.
- Future forecast table.
- Recommended actions.
- MAE and RMSE metrics.
- Historical error-band information.
- A demonstration map.
- Offline-ready alert export content.
The interface is intended to make the most important information visible without requiring the user to inspect raw CSV files.
Dashboard design principles
A future polished version should continue to follow these principles:
1. Put the most important status information near the top.
2. Use consistent colours for risk categories.
3. Avoid relying on colour alone; always include text labels.
4. Distinguish observed readings from predicted values.
5. Show the date and age of the latest reading.
6. Make uncertainty visible near the forecast.
7. Explain stale sensor warnings clearly.
8. Keep charts readable on smaller screens.
9. Use plain-language recommended actions.
10. Keep the simulated-data disclaimer visible.
21. Map Visualisation
The dashboard includes a map view showing three demonstration wells.

The prototype coordinates are fictional:
- Well_A: 24.80, 55.30
- Well_B: 24.85, 55.40
- Well_C: 24.75, 55.45
The map uses the risk category to distinguish the markers.

These are not actual groundwater monitoring coordinates. They are included only to demonstrate how a geographic overview could appear in the dashboard.

A real deployment would require verified coordinates and appropriate access controls for sensitive infrastructure locations.
22. Offline-Ready Alert Exports
Remote environments may have intermittent connectivity. The current dashboard therefore provides alert information that can be exported as text or CSV.

These files can be saved locally and shared through an available channel when connectivity is restored.
Current functionality
- Prepare human-readable alert text.
- Provide structured CSV information.
- Show recommended actions.
- Keep the information available for later sharing.
Not currently implemented
- Automatic SMS transmission.
- WhatsApp delivery.
- Push notifications.
- Satellite messaging.
- A live cloud notification service.
These could be future extensions, subject to network availability, user consent, and appropriate operational safeguards.
23. Installation and Setup
Prerequisites
Install:
- Python 3.10 or a compatible newer version.
- Visual Studio Code or another Python editor.
- GitHub account, if you want to host the project online.
Open the project folder
Open the WellWatch_AI folder in your editor.
Create a virtual environment
On Windows PowerShell:
python -m venv .venv
Activate it:
.\.venv\Scripts\Activate.ps1
If PowerShell blocks activation, follow your organisation's or system administrator's approved execution-policy guidance. You can also use Command Prompt activation:
.venv\Scripts\activate.bat
Install dependencies
python -m pip install -r requirements.txt
If a requirements file is not present, install the packages directly:
python -m pip install pandas numpy matplotlib scikit-learn streamlit plotly
Confirm the environment
python -c "import pandas, numpy, sklearn, streamlit, plotly; print('Dependencies are ready')"
Use the same activated environment for all scripts and for Streamlit.
24. Running the Complete Project
Run the scripts in the following order from the project directory:
python generate_data.py
python inspect_data.py
python clean_data.py
python visualize_data.py
python forecast_model.py
python alert_engine.py
python sensor_health.py
If you want to run the sensor-failure demonstration, use the test script if it is included and configured:
python test_sensor_failure.py
The pipeline creates or updates the CSV and image files required by the dashboard.
Why order matters
The forecast model needs the cleaned dataset. The alert engine needs both the cleaned data and forecast output. The dashboard needs the processed files to exist before it starts.

If you change the generated data, rerun the downstream processing scripts so that all outputs correspond to the same dataset.
25. Running the Dashboard
From the project directory, with the virtual environment activated:
streamlit run app.py
Streamlit normally opens the application in your default browser.

If it does not open automatically, use the local URL printed in the terminal. The default is commonly:
http://localhost:8501
To stop the local dashboard, return to the terminal and press Ctrl + C.
26. How to Use the Dashboard
1. Open the dashboard in your browser.
2. Read the prototype/simulated-data notice.
3. Review the three well overview cards.
4. Compare the risk labels and current depth values.
5. Select a well from the detailed-analysis selector.
6. Review its historical water-depth chart.
7. Review its salinity chart.
8. Inspect the forecast table for the 7-, 14-, and 21-day estimates.
9. Review the model error metrics and illustrative error range.
10. Read the recommended action.
11. Inspect sensor-health status.
12. Enable the simulated stale-sensor scenario, if available.
13. Observe the warning and its explanation.
14. Review the demonstration map and export options.
Do not interpret a prototype risk label as an official water-quality or groundwater-safety determination.
27. Example Demonstration Scenario
A useful demonstration is to compare the three wells.

In one generated run, the dashboard showed:
Well	Example risk	Current depth	21-day forecast
Well_A	WATCH	16.39 m	16.63 m
Well_B	HIGH	22.06 m	22.99 m
Well_C	LOW	12.33 m	12.52 m


These are example values from the generated demonstration dataset. They can change if the generator or date range changes.
Suggested walkthrough
- Start with the all-well overview.
- Select Well_B to show the stronger simulated trend.
- Explain that a greater depth means the water surface is farther below the reference point.
- Show the 7-, 14-, and 21-day estimates.
- Explain the historical validation errors.
- Enable the stale-sensor demonstration.
- Point out that sensor status and water-risk status are separate.
- Finish by showing the recommended action and export feature.
28. Responsible Use and Important Limitations
Transparency is essential for an early-warning system. The current prototype has important limitations.
Simulated data
The well readings are generated by code. They are not measurements from real wells.
No live satellite integration
Although satellite and public environmental datasets are relevant to the problem, the current prototype does not ingest live satellite imagery or live satellite-derived groundwater measurements.
Simple forecasting model
The forecast is based on a Linear Regression model using day number as its only feature. It does not capture complex groundwater dynamics, seasonal behaviour, aquifer properties, pumping schedules, or spatial relationships.
Demonstration thresholds
The risk thresholds are prototype values. They are not validated groundwater safety thresholds.
Illustrative uncertainty range
The displayed error band is based on a percentile of historical validation errors. It is not a calibrated prediction interval.
Fictional map coordinates
The map markers are demonstration locations, not actual well locations.
Simulated sensor failure
The stale-sensor feature demonstrates a software warning state. It does not test physical hardware or a real communication network.
No automatic emergency response
The system does not automatically control pumps, close valves, contact emergency services, or make operational decisions.
Human review
Any real-world deployment would require validation by groundwater specialists, local authorities, and the organisations responsible for the water infrastructure.
29. Testing and Reproducibility
The project can be tested by running the data pipeline from the beginning.
Reproducibility
The generator uses a fixed random seed so the same code and environment can reproduce the demonstration dataset.
Basic checks
After generation and cleaning, inspect:
- Whether the expected CSV files exist.
- Whether the date column is correctly parsed.
- Whether duplicate date/well records remain.
- Whether missing values are handled.
- Whether all three well identifiers are present.
- Whether the forecast file contains all expected horizons.
- Whether the alert file contains a category for each well.
- Whether the dashboard opens without missing-file errors.
Sensor-health test
Run the normal sensor-health script and then the simulated failure test. Compare the status output and confirm that the dashboard communicates the stale condition.
Fresh-environment test
For a stronger reproducibility check:
1. Clone or download the repository into a new folder.
2. Create a new virtual environment.
3. Install requirements.txt.
4. Run the scripts in order.
5. Launch the dashboard.
6. Confirm that the outputs are recreated successfully.
30. Challenges Addressed
Challenge	Prototype response
Hard-to-interpret historical readings	Trend charts and summary cards
Need to look ahead	7-, 14-, and 21-day estimates
Need to prioritise attention	Low, Watch, and High categories
Unreliable readings	Stale-sensor warning
Prediction uncertainty	Validation metrics and illustrative error band
Limited connectivity	Downloadable text and CSV alert information
Multiple water sources	Multi-well overview and selector
Need for a quick overview	Browser-based dashboard


The prototype demonstrates these software responses using simulated inputs. It does not yet prove performance in a real desert deployment.
31. Potential Real-World Deployment
A real deployment would require a carefully designed data and validation process.
Sensor integration
Potential inputs could include:
- Water-level sensors.
- Electrical conductivity or salinity sensors.
- Temperature sensors.
- Pump operation measurements.
- Local weather stations.
Public environmental data
Depending on the location and research question, the team could investigate suitable public sources such as:
- Sentinel-2 imagery for land-surface and vegetation context.
- Landsat imagery for long-term land-surface observations.
- NASA GRACE and GRACE-FO products for large-scale terrestrial water-storage context.
- CHIRPS precipitation data.
- ERA5 climate reanalysis.
These datasets have different spatial and temporal resolutions. They are not interchangeable with direct well-level measurements. Their suitability must be assessed for the intended region and prediction target.
Communication
A deployed system could queue alerts locally and transmit them when a network becomes available. Any SMS or messaging integration would need to be implemented and tested separately.
Validation
Before operational use, the model should be tested against independently collected field observations and compared with appropriate baseline methods.
32. Future Improvements
32.1 Real sensor data
Connect physical water-level, conductivity, and temperature sensors through a documented data-ingestion interface.
32.2 Public satellite and climate data
Add relevant satellite and climate-derived features after checking their spatial scale, update frequency, and suitability for the target wells.
32.3 Stronger forecasting
Compare Linear Regression with suitable alternatives such as:
- Persistence baseline.
- Moving-average baseline.
- Random Forest regression.
- Gradient-boosted trees.
- Time-series models appropriate to the data volume and sampling frequency.
Model selection should be based on time-aware validation, not model complexity alone.
32.4 Better uncertainty calibration
Use rolling-origin backtesting and methods designed to produce calibrated prediction intervals. Evaluate coverage and interval width on held-out periods.
32.5 Location-specific thresholds
Work with local groundwater experts to define thresholds based on aquifer characteristics, well construction, measurement conventions, and intended use.
32.6 Better sensor diagnostics
Add checks for:
- Flatlined readings.
- Sudden physically implausible jumps.
- Missing intervals.
- Out-of-range values.
- Sensor drift.
- Conflicting measurements.
32.7 Offline-first mobile experience
Develop a lightweight mobile interface that caches recent readings and queued alerts for later synchronisation.
32.8 Notification integrations
Explore SMS, email, or messaging notifications with delivery confirmation, retry logic, user preferences, and clear escalation policies.
32.9 Multi-location deployment
Support configurable well metadata, verified coordinates, units, local time zones, and role-based access.
32.10 Model monitoring
Track forecast errors over time and flag changes in data distributions or model performance.
33. Impact and Use Cases
If developed and validated with real data, a system like WellWatch AI could support:
- Rural water-resource monitoring teams.
- Agricultural water management.
- Remote facilities that depend on groundwater.
- Field technicians prioritising inspection visits.
- Organisations coordinating water-source maintenance.
- Research teams studying changes in monitored wells.
The potential value is earlier visibility into changing conditions and clearer communication about which locations may need attention.

The current hackathon prototype demonstrates a workflow and interface. It does not establish measured real-world water savings, avoided failures, or field accuracy.
34. Team Contributions
Ikshu
- Data generation and preprocessing.
- Dataset inspection and cleaning.
- Dashboard development and integration.
- Visualisation and presentation workflow.
Bharat
- Forecasting model implementation.
- Risk classification logic.
- Sensor-health and failure-test support.
- Model testing and validation workflow.
Both team members contributed to understanding the end-to-end project and preparing the demonstration.
35. Hackathon Demo Guide
A concise demonstration can follow this order:
1. Introduce the desert water-monitoring problem.
2. Explain the simulated-data status clearly.
3. Show the all-well overview.
4. Compare the risk categories.
5. Select Well_B and show its historical trends.
6. Explain the forecast horizons.
7. Show MAE, RMSE, and the illustrative error band.
8. Enable the stale-sensor simulation.
9. Explain why stale readings require caution.
10. Show the map and its fictional-coordinate disclaimer.
11. Show the alert export.
12. End with the next steps: real sensor data, relevant public datasets, stronger validation, and local threshold calibration.
Keep the demonstration focused on what works today. Clearly distinguish implemented features from future plans.
36. Frequently Asked Questions
Is WellWatch AI using real groundwater data?
No. The current hackathon prototype uses simulated well-monitoring records.
Does the model use satellite imagery?
No. Satellite integration is a possible future improvement, not a current feature.
What does the model predict?
It estimates future water depth for each demonstration well at 7, 14, and 21 days ahead.
What does an increasing water-depth value mean?
In this simulation, depth is measured downward from a fixed reference. A higher depth value means the water surface is farther below that reference.
Does the model use salinity to forecast depth?
No. The current Linear Regression forecast uses day number as its only input. Salinity is analysed separately by the warning engine.
What do MAE and RMSE mean?
They measure prediction errors on the chronological test portion of the dataset. Lower values indicate smaller errors on that evaluation data.
Is the displayed 90th-percentile error band a guaranteed 90% confidence interval?
No. It is an illustrative band based on historical validation errors and is not statistically calibrated as a prediction interval.
Does the system send SMS alerts?
No. The current version provides downloadable text and CSV alert information. It does not send live SMS messages.
Are the map coordinates real?
No. The coordinates are fictional demonstration locations.
Does a stale sensor automatically mean the well is high risk?
No. A stale sensor means the latest data may be outdated. Sensor health and water-risk classification are shown separately.
Can this prototype be used to make real water-supply decisions?
Not in its current form. It requires real data, expert review, local calibration, and extensive validation before operational use.
37. Troubleshooting
ModuleNotFoundError
The active Python environment may not contain the required package.

Activate the project environment and run:
python -m pip install -r requirements.txt
Streamlit cannot find a CSV file
Make sure you are running the command from the project directory and that the data-generation and processing scripts have completed successfully.
Dashboard shows old values
Rerun the relevant pipeline scripts after changing the generator or source data. Refresh the browser page.
VS Code uses the wrong Python interpreter
Select the interpreter inside the project's .venv folder. You can also run scripts directly from a terminal where the virtual environment is activated.
PowerShell does not activate the virtual environment
Use the Command Prompt activation command:
.venv\Scripts\activate.bat
Port 8501 is already in use
Stop the other Streamlit process or launch on another port:
streamlit run app.py --server.port 8502
Charts or outputs do not update
Check that the scripts are writing to the expected project directory and that the dashboard is reading the same filenames.
38. Acknowledgements
This project was developed as a hackathon prototype for the Breaking Bytes — The 24-Hour Underground Hackathon, under track W-001: Early Warnings for Desert Water Sources.

The project explores how data processing, simple forecasting, sensor-health awareness, and accessible visualisation can be combined into an early-warning workflow.
39. License
Add a license before distributing the project for reuse. If you choose the MIT License, include the standard MIT license text in a file named LICENSE and confirm that this choice is suitable for your team and event rules.

Until a license is added, do not assume that others have permission to reuse, modify, or redistribute the code.
40. Disclaimer
WellWatch AI is an experimental hackathon prototype. It uses simulated data, fictional map coordinates, demonstration risk thresholds, and a simple forecasting model.

It is not a certified groundwater-monitoring system, water-quality assessment tool, emergency-warning service, or substitute for professional hydrogeological advice.

Predictions and risk labels must not be used as the sole basis for water-supply, public-health, infrastructure, or emergency decisions. Any real-world use requires verified measurements, local calibration, independent validation, expert oversight, and appropriate operational safeguards.
Built by Team WellWatch AI — Ikshu, Bharath, Shradha
Breaking Bytes | Track W-001
