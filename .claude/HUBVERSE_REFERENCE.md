# Hubverse Framework Reference

## Overview

The Hubverse is a standardized framework for collaborative infectious disease forecasting, enabling teams worldwide to contribute predictions that are validated, combined, and evaluated systematically.

## Core Philosophy

**"Collaborate, Share, Inform"**
- **Collaborate:** with modelers around the world
- **Share:** insights in real time
- **Inform:** critical decisions with robust and validated model outputs

## Framework Components

### 1. Data Standards

Configuration-based system defining:
- Tabular model submission formats
- Task specifications (targets, horizons, locations)
- Output types (quantiles, samples, probabilities)
- Metadata requirements

### 2. Software Ecosystem (R-based)

| Package | Purpose |
|---------|---------|
| hubAdmin | Hub setup and management |
| hubValidations | Submission validation |
| hubData | Data retrieval and access |
| hubEnsembles | Model combination |
| hubEvals | Performance evaluation |
| hubViz | Visualization |

### 3. Hub Configuration Files

#### tasks.json
Defines prediction tasks:
- Round IDs (reference dates)
- Task IDs (horizons, locations, targets)
- Output types and quantile levels
- Required vs optional submissions

Example structure:
```json
{
  "round_id": "reference_date",
  "model_tasks": [{
    "task_ids": {
      "reference_date": ["2025-11-22", "2025-11-29", ...],
      "target": ["wk inc flu hosp"],
      "horizon": [-1, 0, 1, 2, 3],
      "location": ["US", "01", "02", ...]
    },
    "output_type": {
      "quantile": {
        "output_type_id": [0.01, 0.025, 0.05, ...]
      }
    }
  }]
}
```

#### model-metadata-schema.json
Defines required metadata fields:
- Team information
- Model description
- Methods and data inputs
- License and funding
- Model type (ensemble, mechanistic, etc.)

#### validations.yml
Specifies validation rules:
- File format checks
- Schema validation
- Value range checks
- Quantile crossing checks

### 4. Standard Directory Structure

```
hub-name/
├── hub-config/              # Configuration files
│   ├── tasks.json
│   ├── model-metadata-schema.json
│   ├── validations.yml
│   └── admin.json
├── model-metadata/          # Team/model documentation
│   ├── Team1-Model1.yml
│   ├── Team2-Model2.yml
│   └── ...
├── model-output/            # Forecast submissions
│   ├── Team1-Model1/
│   │   ├── 2025-11-22-Team1-Model1.parquet
│   │   └── ...
│   └── ...
├── target-data/             # Ground truth data
│   ├── target-hospital-admissions.csv
│   └── ...
└── auxiliary-data/          # Supporting files
    ├── locations.csv
    └── ...
```

## Submission Workflow

1. **Team prepares forecast**
   - Follows hub-specific task definitions
   - Formats output according to schema
   - Names file: `YYYY-MM-DD-TeamAbbr-ModelAbbr.{csv,parquet}`

2. **Automated validation**
   - File format and naming checks
   - Schema validation (required columns, types)
   - Value validation (ranges, quantile crossing)
   - Metadata completeness

3. **Storage and access**
   - Accepted submissions stored in model-output/
   - Mirrored to S3 for public access
   - Versioned through git

4. **Ensemble creation**
   - Combine validated forecasts
   - Apply weights (equal, performance-based, etc.)
   - Generate ensemble predictions

5. **Evaluation**
   - Compare to ground truth data
   - Calculate performance metrics
   - Generate reports and visualizations

## Model Metadata Schema

Required fields in model metadata files:

```yaml
team_name: "Full Team Name"
team_abbr: "ABBR"
model_name: "Descriptive Model Name"
model_abbr: "abbr"
model_version: "1.0"
model_contributors:
  - name: "Contributor Name"
    affiliation: "Institution"
    email: "email@example.com"
license: "CC-BY-4.0"
designated_model: true/false
methods: "Brief description"
data_inputs: "Data sources used"
methods_long: "Detailed methodology"
ensemble_of_models: true/false
ensemble_of_hub_models: true/false
```

## Output Format Standards

### Quantile Predictions

| Column | Type | Description |
|--------|------|-------------|
| reference_date | date | Forecast submission Saturday |
| target | string | Prediction target name |
| horizon | integer | Weeks ahead (-1, 0, 1, 2, 3) |
| target_end_date | date | Saturday of forecast week |
| location | string | FIPS code or "US" |
| output_type | string | "quantile" |
| output_type_id | float | Quantile level (0.01-0.99) |
| value | numeric | Predicted value |

### Sample Trajectories

Same columns as quantile, but:
- `output_type`: "sample"
- `output_type_id`: Sample ID (1-100)
- Samples must be temporally connected across horizons

### Categorical Predictions

Same columns as quantile, but:
- `output_type`: "pmf"
- `output_type_id`: Category name (e.g., "large increase")
- `value`: Probability (sum to 1 within task)

## Cloud Data Access

Hubs mirror data to AWS S3 for efficient access without git:

**S3 Bucket Pattern:** `{org}-{hubname}-hub`
Example: `cdcepi-flusight-forecast-hub`

**Access Methods:**
- R: `hubData::connect_hub(s3_bucket(bucket_name))`
- Python: `pyarrow.dataset.dataset(bucket_path, filesystem=s3)`
- CLI: `aws s3 cp s3://bucket/path . --recursive --no-sign-request`

## Evaluation Metrics (Common)

- **Weighted Interval Score (WIS):** Primary scoring metric
- **Coverage:** Percentage of observations within prediction intervals
- **Calibration:** Agreement between predicted and empirical probabilities
- **Sharpness:** Concentration of predictive distributions
- **Bias:** Systematic over/under-prediction

## Hub Governance

Hubs typically specify:
- Submission deadlines (e.g., Wednesdays 11PM ET)
- Data freezes (what data is available when)
- Model independence requirements
- Embargo periods for results
- Publication and data use policies

## Best Practices

1. **Start simple:** Submit basic forecasts early to test pipeline
2. **Document thoroughly:** Complete metadata helps users understand model
3. **Version clearly:** Track model changes in metadata
4. **Validate locally:** Use hubValidations before submitting
5. **Handle anomalies:** Document how model deals with data quality issues
6. **Communicate uncertainty:** Provide full predictive distributions

## Resources

- Hubverse Documentation: https://hubdocs.readthedocs.io/
- GitHub: https://github.com/hubverse-org
- Schema Specifications: https://github.com/hubverse-org/schemas
