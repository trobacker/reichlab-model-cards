# Model Cards Concept

## Inspiration: Sports Analytics

Model Cards for infectious disease forecasting draw inspiration from sports analytics "stat sheets" that provide:
- At-a-glance performance summaries
- Historical trends and patterns
- Contextual information for interpretation
- Comparisons across players/teams
- Strengths and weaknesses analysis

## Objectives

Create human-interpretable summaries of forecasting models that enable:

1. **Quick Assessment:** Understand model performance without deep technical knowledge
2. **Informed Decision-Making:** Choose which models to trust in different contexts
3. **Transparency:** Make model behavior and limitations explicit
4. **Comparability:** Easy comparison across models and ensembles
5. **Accountability:** Track performance over time and across scenarios

## Target Audiences

- **Public Health Officials:** Need reliable forecasts for resource allocation
- **Researchers:** Evaluating model architectures and methods
- **Model Developers:** Understanding their model's behavior and areas for improvement
- **Ensemble Designers:** Selecting and weighting component models
- **General Public:** Understanding forecast uncertainty and reliability

## Proposed Model Card Components

### 1. Model Identity

- Team and model names
- Version history and updates
- Contributors and contact info
- Last updated date

### 2. Model Description

**What is it?**
- Model type (statistical, ML, mechanistic, ensemble)
- Brief methodology summary
- Data sources used
- Key innovations or features

**How does it work?**
- Modeling approach (e.g., time series, spatial correlation)
- Feature engineering
- Uncertainty quantification method
- Ensemble composition (if applicable)

### 3. Performance Summary

**Overall Performance Metrics**
- WIS (Weighted Interval Score) - primary metric
- Coverage at different probability levels
- Calibration scores
- Relative performance vs baseline

**Performance by Context**
- By forecast horizon (0-3 weeks ahead)
- By location type (national vs state-level)
- By season phase (early, peak, late)
- By epidemic intensity (low, moderate, high incidence)

**Temporal Trends**
- Performance over recent weeks
- Seasonal patterns
- Improvement/degradation trends

### 4. Strengths and Limitations

**Strengths**
- Scenarios where model excels
- Unique capabilities
- Robust features

**Limitations**
- Known failure modes
- Data dependency issues
- Scenarios of poor performance
- Assumptions and their validity

### 5. Visual Performance Indicators

**Suggested Visualizations**
- Time series of forecasts vs observations
- WIS over time (by horizon)
- Coverage plots (prediction interval performance)
- Forecast fan charts with uncertainty
- Heatmaps of location-specific performance
- Comparison to ensemble and baseline

### 6. Operational History

**Model Evolution**
- Version changelog
- Methodological updates
- Responses to data anomalies
- Lessons learned

**Reliability Notes**
- Weeks with issues (data quality, model failures)
- Interventions taken (dropped locations, special handling)
- Stability assessment

### 7. Usage Guidance

**When to Use This Model**
- Recommended contexts
- Confidence levels in different scenarios

**When to Be Cautious**
- Situations requiring extra scrutiny
- Alternative models to consider

**Interpretation Tips**
- How to read the uncertainty
- Factors affecting forecast reliability

## Implementation Strategy

### Phase 1: Prototype for UMass-flusion

1. **Data Collection**
   - Extract UMass-flusion forecasts from FluSight hub
   - Gather evaluation data (target-data)
   - Compile model metadata across versions

2. **Metric Calculation**
   - Compute WIS by horizon, location, time
   - Calculate coverage and calibration
   - Generate comparison metrics

3. **Visualization Development**
   - Create standard plotting functions
   - Design card layout and structure
   - Develop interactive elements (if web-based)

4. **Content Generation**
   - Auto-generate performance summaries
   - Extract methodology from metadata
   - Identify anomalies and notes

5. **Card Assembly**
   - Combine components into unified card
   - Export to HTML/PDF/Markdown
   - Test with stakeholders

### Phase 2: Expand to Multiple Models

1. **Standardize pipeline** for any FluSight model
2. **Comparative cards** showing multiple models
3. **Ensemble component cards** showing contribution
4. **Historical archives** of past cards

### Phase 3: Real-time Integration

1. **Automated updates** with each forecast round
2. **Dashboard integration** with FluSight
3. **API access** for programmatic retrieval
4. **Alerting system** for performance changes

## Technical Requirements

### Data Access
- FluSight model-output data (via S3 or hubData)
- Target data for evaluation
- Model metadata files
- Historical forecast archives

### Computation
- Scoring functions (WIS, coverage, calibration)
- Statistical summaries
- Visualization generation
- Markdown/HTML rendering

### Storage
- Card archives (versioned)
- Performance metrics database
- Visualization cache

### Tools and Libraries
- **R:** hubData, hubEvals, ggplot2, rmarkdown
- **Python:** pandas, plotly, matplotlib, jinja2
- **Storage:** Git for versioning, S3 for serving

## Example Card Outline

```markdown
# Model Card: UMass-flusion

**Version:** 1.1 | **Last Updated:** 2025-12-20 | **Team:** UMass-Amherst

---

## Quick Stats (Last 4 Weeks)

| Metric | 0-week | 1-week | 2-week | 3-week |
|--------|--------|--------|--------|--------|
| WIS    | 45.2   | 67.3   | 89.1   | 112.4  |
| 50% Coverage | 52% | 49% | 51% | 48% |
| Rank (vs 20 models) | 3rd | 5th | 4th | 6th |

⭐ **Overall Rating:** Top 5 performer across all horizons

---

## Model Overview

**Type:** Ensemble (Statistical + Machine Learning)

**Methodology:** Quantile average of three components:
1. AR(6) pooled model (NHSN)
2. GBQR spatial model (3 data sources, state-level)
3. GBQR model (3 data sources, national)

**Data Sources:** NHSN, FluSurv-NET, ILINet

---

## Performance Highlights

### Strengths ✅
- Excellent short-term forecasts (0-1 week)
- Strong spatial correlation modeling
- Robust to data anomalies

### Areas for Improvement ⚠️
- Longer-horizon uncertainty may be underestimated
- Performance varies by location size
- Sensitive to reporting delays in small states

---

## Recent Performance

[Time series plot: forecasts vs actuals]
[WIS trend over last 8 weeks]
[Coverage by horizon]

---

## Model Evolution

**v1.1 (2025-12-20):** Added spatial GBQR component
**v1.0 (2024-11-23):** Equal-weighted AR(6) + GBQR ensemble

Notable interventions:
- 2024-12-07: Dropped PR due to data quality
- 2025-01-02: GBQR-only for post-Christmas week

---

## Usage Guidance

✅ **Use with confidence:**
- National-level forecasts
- Short-term (0-2 week) predictions
- Locations with consistent reporting

⚠️ **Use with caution:**
- Small states with reporting variability
- Post-holiday periods
- Locations with recent anomalies

---

## Technical Details

[Link to full metadata]
[Link to code repository]
[Link to forecast downloads]
```

## Success Metrics for Model Cards

1. **Adoption:** Number of views/downloads
2. **Comprehension:** User surveys on interpretability
3. **Action:** Cards leading to model selection changes
4. **Accuracy:** Card insights matching deeper analysis
5. **Timeliness:** Time from forecast to card generation

## Open Questions

1. **Granularity:** Single card per model or multiple views (by location, horizon, etc.)?
2. **Update Frequency:** After every forecast round or weekly summaries?
3. **Comparison Baseline:** Fixed baseline model or dynamic ensemble?
4. **Interactivity:** Static documents or interactive dashboards?
5. **Customization:** One-size-fits-all or audience-specific cards?
6. **Historical Depth:** How many weeks of history to show?
7. **Aggregation:** Separate state cards or aggregated metrics only?

## Next Steps

1. Review FluSight evaluation code to understand existing metrics
2. Identify key performance indicators from dashboard
3. Draft initial card template/schema
4. Implement prototype for single model (UMass-flusion)
5. Gather feedback from stakeholders
6. Iterate and expand

## Related Concepts

- **Model Documentation:** Technical specifications for reproducibility
- **Model Evaluation:** Detailed performance analysis and diagnostics
- **Model Comparison:** Head-to-head performance across multiple models
- **Forecast Communication:** Public-facing summaries and visualizations
- **Model Selection:** Decision support for ensemble composition

## References

- ML Model Cards: https://arxiv.org/abs/1810.03993
- Forecast evaluation: https://forecasters.org/resources/
- Sports analytics: Various stat tracking systems (Baseball Reference, etc.)
