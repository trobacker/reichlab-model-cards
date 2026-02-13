# Plan: Incorporating Real Evaluation Metrics

## Current State

We have a prototype model card system with placeholder metrics. Need to integrate actual evaluation data from the FluSight hub.

## Data Sources Identified

### Available in FluSight Hub

1. **HTML Reports** (`reports/` directory)
   - `Flu_Hospitalizations_Forecasts_WIS_11 February 2026.html` - Contains WIS scores
   - `FluSight_Categorical_eval2026-02-12.html` - Contains categorical eval metrics
   - These are R Markdown/interactive reports with embedded JSON data (19 JSON instances per file)
   - **Pros:** Contains pre-computed WIS scores and rankings
   - **Cons:** Requires HTML/JSON parsing

2. **Weekly Summaries** (`weekly-summaries/YYYY-MM-DD/`)
   - Forecast data by model: `YYYY-MM-DD_flu_forecasts_data.csv`
   - Target/truth data: `YYYY-MM-DD_flu_target_hospital_admissions_data.csv`
   - **Pros:** Clean CSV format, easy to parse
   - **Cons:** No pre-computed evaluation metrics

3. **Model Outputs** (`model-output/` directory)
   - Individual model forecast files
   - **Pros:** Direct access to all forecasts
   - **Cons:** Need to compute metrics ourselves

4. **Target Data** (`target-data/` directory)
   - Ground truth: `target-hospital-admissions.csv`
   - **Pros:** Official evaluation data
   - **Cons:** Need to align with forecasts and compute metrics

## Recommended Approach

### **Option 1: Parse HTML Reports (CHOSEN)**

**Rationale:** The HTML reports already contain computed WIS scores and rankings. This is what the dashboard uses.

**Steps:**
1. Extract JSON data from HTML reports
2. Parse plotly/interactive chart data containing WIS scores
3. Extract model rankings and performance metrics
4. Structure data for model card generation

**Advantages:**
- Pre-computed metrics (same as dashboard)
- Rankings already calculated
- No need to implement WIS calculation
- Matches official dashboard values

**Challenges:**
- HTML parsing can be brittle
- Need to understand JSON structure

### Option 2: Compute Metrics Ourselves

**Steps:**
1. Load forecast data from weekly summaries or model-output
2. Load target/truth data
3. Implement WIS calculation in Python
4. Calculate coverage metrics
5. Rank models across metrics

**Advantages:**
- Full control over metrics
- Can compute additional metrics (MAE, CRPS, etc.)
- More flexible for future enhancements

**Challenges:**
- Need to implement proper WIS calculation
- Must match hubverse standards
- More complex implementation
- May not match dashboard exactly

### Option 3: Use R via rpy2

**Steps:**
1. Install R and hubEvals package
2. Use rpy2 to call R from Python
3. Compute metrics using official hubverse tools

**Advantages:**
- Uses official evaluation code
- Guaranteed to match standards
- Access to all hubverse evaluation functions

**Challenges:**
- Additional dependency (R)
- More complex setup for users
- Cross-language integration complexity

## Implementation Plan (Option 1)

### Phase 1: HTML Parsing Proof of Concept

1. **Extract JSON from HTML report**
   ```python
   from bs4 import BeautifulSoup
   import json
   import re

   # Parse HTML, find script tags with JSON data
   # Extract plotly data containing WIS scores
   ```

2. **Identify data structure**
   - Find WIS scores by model
   - Find rankings
   - Identify time periods/horizons

3. **Create extraction function**
   ```python
   def extract_wis_scores(html_path):
       # Returns: dict with model names, WIS by horizon, rankings
       pass
   ```

### Phase 2: Data Structuring

1. **Create data classes/schemas**
   ```python
   @dataclass
   class ModelMetrics:
       model_name: str
       wis_0week: float
       wis_1week: float
       wis_2week: float
       wis_3week: float
       coverage_50pct: float
       coverage_95pct: float
       overall_rank: int
       total_models: int
       rankings_by_metric: dict
   ```

2. **Aggregate metrics**
   - Combine across horizons
   - Calculate average ranks
   - Identify best/worst metrics

### Phase 3: Integration with Model Card Generator

1. **Update `generate_card.py`**
   - Add `--real-data` flag
   - Load evaluation metrics
   - Combine with model metadata

2. **Update card generation**
   - Replace placeholder metrics with real data
   - Generate spider plot with real rankings
   - Populate strengths/limitations based on actual performance

### Phase 4: Automate for Multiple Models/Dates

1. **Create batch generation script**
   ```python
   # Generate cards for all models in a specific week
   python src/generate_cards_batch.py --date 2025-01-18

   # Generate card for specific model
   python src/generate_card.py --model UMass-flusion --date 2025-01-18 --real-data
   ```

## File Structure

```
src/
├── evaluation/
│   ├── __init__.py
│   ├── html_parser.py          # Parse HTML reports
│   ├── metrics_extractor.py    # Extract and structure metrics
│   └── data_models.py           # Data classes for metrics
├── generate_card.py             # Main CLI (updated)
├── model_card_generator.py      # HTML generator (existing)
└── spider_plot.py               # Spider plots (existing)
```

## Next Steps

1. ✅ Create this plan document
2. Implement HTML parsing proof of concept
3. Test with one model (UMass-flusion) for one date (2025-01-18)
4. Generate real model card
5. Validate metrics match dashboard
6. Extend to multiple models
7. Add error handling and edge cases

## Alternative: Scraping Dashboard Directly

If HTML parsing proves too complex, we could:
1. Use Selenium/Playwright to load dashboard
2. Extract displayed metrics from rendered page
3. More robust to HTML structure changes
4. But adds browser automation dependency

## Future Enhancements

- Cache extracted metrics to avoid re-parsing
- Support multiple evaluation periods
- Add historical performance tracking
- Compute additional metrics beyond WIS
- Create comparative cards across models
