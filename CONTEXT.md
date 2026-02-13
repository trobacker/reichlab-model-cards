# Project Context: Model Cards for Infectious Disease Forecasting

## Project Overview

This repository is dedicated to prototyping "Model Cards" for infectious disease modeling and forecasting. The concept draws parallels to sports analytics stat reporting, aiming to create human-interpretable summaries and evaluations of forecasting models.

## Key Repositories and Their Relationships

### 1. Hubverse Framework (https://hubverse.io/)

**Purpose:** Standardized infrastructure for collaborative modeling hubs

**Key Components:**
- **Data Standards:** Flexible, structured configuration files defining tabular model submission formats
- **Software Tools:** R-based packages (hubAdmin, hubValidations, hubData, hubEnsembles, hubEvals, hubViz)
- **Validation:** Automated submission validation against hub-specific rules
- **Ensemble Creation:** Aggregation of multiple model forecasts
- **Visualization:** Interactive dashboards for forecast communication

**Real-World Use:** CDC, European Centre for Disease Prevention and Control, California Dept of Public Health

### 2. FluSight-forecast-hub (https://github.com/cdcepi/FluSight-forecast-hub)

**Purpose:** CDC's collaborative forecasting exercise for 2025-2026 influenza season

**Structure:**
```
FluSight-forecast-hub/
├── hub-config/           # Hub configuration (tasks, validation, schema)
├── model-metadata/       # Model documentation files (.yml)
├── model-output/         # Forecast submissions (parquet/csv)
├── target-data/          # Ground truth data for evaluation
├── auxiliary-data/       # Supporting data (locations, populations)
├── ensemble-weights/     # Weights for ensemble models
├── reports/              # Evaluation reports
└── weekly-summaries/     # Weekly forecast summaries
```

**Prediction Targets:**
1. **Primary:** Weekly lab-confirmed influenza hospitalizations (quantile forecasts)
2. Weekly proportion of ED visits due to influenza
3. Rate-trend categories (increase/decrease classifications)
4. Seasonal targets: peak week and peak incidence

**Data Sources:**
- NHSN Weekly Hospital Respiratory Dataset (primary evaluation data)
- FluSurv-NET (historical flu hospitalizations)
- ILINet (outpatient influenza-like illness)
- NSSP (emergency department visit data)

**Forecast Format:**
- Reference dates: Saturdays (end of epiweek)
- Horizons: -1, 0, 1, 2, 3 weeks ahead
- Locations: US national, all 50 states, DC, Puerto Rico
- Output types: quantile predictions, samples, categorical probabilities

**Evaluation Dashboard:** https://reichlab.io/flusight-dashboard/
- Displays latest forecasts and model performance
- Provides interactive visualizations
- Shows model comparisons and evaluation metrics

### 3. forecast-sandbox-2025-2026 (https://github.com/reichlab/forecast-sandbox-2025-2026)

**Purpose:** Reich Lab testbed for experimental forecasts before/during 2025-2026 season

**Structure:**
```
forecast-sandbox-2025-2026/
├── hub-config/           # Hub configuration
├── model-metadata/       # Experimental model documentation
├── model-output/         # Experimental forecasts
├── src/                  # Model implementation code
│   ├── flusion_fourier/
│   ├── flusion_spatial/
│   ├── flusion_spatial2/
│   ├── flusion_spatial2_prod/
│   ├── flusion3/
│   ├── flusion3_weighted/
│   └── flu_flusion/
├── target-data/          # Ground truth data
└── auxiliary-data/       # Supporting data
```

**Key Features:**
- Models are instances from [idmodels](https://github.com/reichlab/idmodels)
- Implementation from [operational-models](https://github.com/reichlab/operational-models)
- Data pipelines from [iddata](https://github.com/reichlab/iddata)
- Many UMass-flusion variants for experimentation

## Focus: UMass-flusion Models

### Model Overview

**Team:** UMass-Amherst
**Model Name:** Ensemble of time series models
**Current Version:** 1.1 (as of 2025-12-20)

### Model Architecture (2025/26 Season)

Quantile average ensemble of three components:

1. **AR(6) Pooled Model**
   - Shared AR coefficients across all locations
   - Per-location variance parameters
   - Fit to NHSN data only

2. **GBQR 3-Source Spatial2 Model** (State-level)
   - Gradient Boosted Quantile Regression
   - Incorporates spatial correlation
   - Uses NHSN, FluSurv-NET, and ILINet data

3. **GBQR 3-Source Model** (US National)
   - Gradient Boosted Quantile Regression
   - No spatial component
   - Uses NHSN, FluSurv-NET, and ILINet data

### Data Inputs

- **NHSN:** Weekly incident flu hospitalizations
- **FluSurv-NET:** Flu hospitalization surveillance network
- **ILINet:** Outpatient influenza-like illness data

### Evolution Across Seasons

**2023/24 Season:**
- Linear pool of two sub-ensembles
- Components: AR(8), gradient boosting with bootstrap, gradient boosting with quantile regression
- Multiple adjustments for data anomalies (AK suspect data, Christmas effects)

**2024/25 Season:**
- Quantile average of GBQR and AR(6)
- Equally weighted components
- Handling of data quality issues (OH anomalies, PR dropped)
- Special handling for Christmas week (GBQR only)

**2025/26 Season:**
- Added spatial correlation component
- Separate national vs state-level models
- Three-component ensemble

## Model Cards Objective

Create human-interpretable "report cards" for forecasting models that:

1. **Summarize Model Performance**
   - Accuracy metrics across different horizons
   - Performance by location and time period
   - Comparison to baseline and other models

2. **Explain Model Behavior**
   - Which data sources are used
   - How the model makes predictions
   - Known limitations and failure modes

3. **Provide Transparency**
   - Model changes over time
   - Data quality considerations
   - Uncertainty quantification

4. **Enable Decision-Making**
   - When to trust the model
   - Which models work best in which contexts
   - Ensemble contribution and weights

## Next Steps for Model Cards Development

1. Identify key metrics and visualizations from FluSight dashboard
2. Define model card structure and components
3. Prototype cards for UMass-flusion variants
4. Design evaluation framework for card effectiveness
5. Iterate based on user feedback

## Data Access

Both FluSight and forecast-sandbox repos mirror data to AWS S3:
- Bucket: `cdcepi-flusight-forecast-hub`
- Access via: hubData (R), pyarrow (Python), AWS CLI
- Real-time access without git cloning

## References

- Hubverse Documentation: https://hubdocs.readthedocs.io/
- FluSight Dashboard: https://reichlab.io/flusight-dashboard/
- Reich Lab GitHub: https://github.com/reichlab
