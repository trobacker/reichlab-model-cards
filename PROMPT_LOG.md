# Prompt Log

This document tracks all major prompts and interactions for the reichlab-model-cards project.

---

## Session 1: 2026-02-12

### Initial Project Setup and Context Gathering

**Prompt:**
```
Welcome to this repo! I'm planning to use this repo to protoype "Model Cards" for infectious disease modeling and forecasts - drawing parallels to similar ideas with sports analytics (stats reporting).

To help facilitate this project, there's several repos we'll need to understand together for a big picture (multiple contexts). I'd like for you to review a few repos to understand them and be aware of their context for this project:

https://hubverse.io/: This is the framework for hosting "modeling hubs" related to several infectious diseases.
https://github.com/cdcepi/FluSight-forecast-hub: This is the flusight hub that'd I'd like to experiment with at first. Can you review this hub in detail and consider it's relation with the hubverse?
https://github.com/reichlab/forecast-sandbox-2025-2026: This repo is kind of auxiliary but it's where we've done a lot of model experimentation to submit for flusight. In particular, I work primarily with the UMass-flusion variants of models. I'm thinking we can use flusight and perhaps some of the sandbox to facilitate experiments.

Take your time reviewing how these hubs relate, what it takes to construct evaluation dashboards (can you find these for the flusight hub please?? - I believe this is it: https://reichlab.io/flusight-dashboard/).

We're going to review this in preparation for constructing "Model Cards" for models and ensembles for human interpretability prototypes.

Can you please keep a log of my prompts in this repo and formulate any claude.md files you might need for context management?
```

**Summary:**
- Reviewed hubverse.io framework and its components
- Cloned and explored FluSight-forecast-hub repository structure
- Cloned and explored forecast-sandbox-2025-2026 repository
- Analyzed FluSight evaluation dashboard at https://reichlab.io/flusight-dashboard/
- Examined UMass-flusion model metadata in both repos
- Created PROMPT_LOG.md (this file) and context documentation

**Key Findings:**
- Hubverse provides standardized infrastructure for collaborative modeling
- FluSight hub follows hubverse standards with weekly flu hospitalization forecasts
- UMass-flusion is an ensemble model combining AR(6), GBQR, and spatial models
- Dashboard evaluates model performance with various metrics
- Model metadata files (.yml) provide structured documentation of models

---

## Session 2: 2026-02-13

### Prototype Model Card Generation

**Prompt:**
```
This is a wonderful start.

Let's try creating an HTML/web-based cards, where the model cards are no longer than a typical 1 page in length. I'd like to keep in mind that we may work toward a PDF output as well.

Let's also start with a single model card for UMass-flusion for the recent season. I imagine that we could issue a model card for a particular forecast submission date (updated weekly eventually). As an in-between step, I'd like to see if we can incorporate a "spider plot" that plots all the evaluation metrics where each "spoke" on the web displays the rank of the particular model on the model card relative to all the other models that made forecasts for the season. Let's generate these separately if needed and then insert them into the model card(s).

I'd like to keep a directory (maybe ./src ?) that keeps relevant development code and then another directory that can store the cards. Let's try producing a protype model card then!

We'll experiment with several features after our prototype.
```

**Actions Taken:**
1. Set up project directory structure (`src/` for code, `cards/` for outputs)
2. Created `spider_plot.py` - Generates radar/spider plots showing model rankings across metrics
3. Created `model_card_generator.py` - HTML model card generator with embedded CSS
4. Created `generate_card.py` - Main CLI script to coordinate card generation
5. Set up Python virtual environment using uv
6. Generated prototype model card for UMass-flusion with mock data
7. Created comprehensive PROJECT_README.md with usage instructions
8. Updated .gitignore to exclude temp-repos and venv

**Generated Files:**
- `cards/UMass-flusion-2025-01-18.html` - Prototype HTML model card (1-page design)
- `cards/umass-flusion-spider.png` - Spider plot showing performance rankings
- `src/spider_plot.py` - Spider plot generation code
- `src/model_card_generator.py` - Model card HTML generator
- `src/generate_card.py` - CLI interface
- `requirements.txt` - Python dependencies
- `PROJECT_README.md` - Project documentation

**Key Features Implemented:**
- 1-page HTML design with print-friendly CSS
- Spider/radar plot with percentile rankings (100% = 1st place, 0% = last)
- Embedded base64 images (no external file dependencies)
- Comprehensive card sections: overview, metrics, strengths, limitations, usage guidance
- Mock data structure that can be easily replaced with real evaluation data

**Technical Stack:**
- Python 3.13 with uv virtual environment
- matplotlib for spider plot generation
- numpy and pandas for data handling
- Pure HTML/CSS for card rendering (no JavaScript dependencies)

**Next Steps:**
- Integrate real evaluation data from FluSight hub
- Test PDF export via browser print
- Experiment with additional visualizations
- Iterate on card design based on feedback

---

## Session 3: 2026-02-13 (continued)

### Real Evaluation Metrics Integration

**Prompt:**
```
Excellent! I've merged the changes..! Now, I'd like to actually incorporate the actual evaluation metrics. I know the flusight hub has evaluation reports. Can you plan how to incorporate the actual evaluation metrics to be used for our prototype model card(s)?

First, let's find the most recent evaluations and then extract the relevant eval metrics and model rankings for UMass-flusion. As a next step, let's look at how to make an accompanying spider plot with the real metrics. Then, let's also continue to update the model card generator to use real data from the evaluations.

Let's do all of this on a new branch.
```

**Actions Taken:**
1. Created `real-evaluation-metrics` branch
2. Located evaluation reports in `temp-repos/FluSight-forecast-hub/reports/`
3. Created `src/evaluation/` module with HTML parser and metrics extractor
4. Implemented BeautifulSoup-based parser for FluSight HTML reports
5. Generated first model card with real metrics for UMass-flusion
6. Discovered reports contain embedded JSON in `<script type="application/json">` tags
7. Successfully extracted WIS, MAE, and coverage metrics with rankings

**Generated Files:**
- `src/evaluation/__init__.py` - Evaluation module
- `src/evaluation/html_parser.py` - Parse FluSight HTML reports
- `src/evaluation/metrics_extractor.py` - Extract model-specific metrics
- `src/evaluation/README.md` - Module documentation
- `.claude/EVALUATION_METRICS_PLAN.md` - Implementation plan
- `src/generate_real_card.py` - Real data card generation script

**Initial Results:**
- UMass-flusion rank: 27/51 (using "Last 2 Forecasts" evaluation period)
- WIS: 53.66 (Rank 25)
- 95% Coverage: 80.1% (Rank 38)

---

### Evaluation Period Clarification and Full Season Rankings

**Prompt:**
```
Then, I'd like to understand better how we got this Overall Rank of 27/51 for UMass-flusion. Can we perhaps improve on the model card for what seasons we are doing the ranking? I like the idea of having a ranking for the 'current season' and then perhaps having ranks over past seasons. To me, it seems like this ranking as is might be over all evaluations? Can you clarify that?
```

**Investigation Results:**
Discovered that FluSight HTML reports contain **multiple evaluation periods**:
- Last 2 Forecasts (EW4-EW5): Rank 27/51 - most recent, least stable
- Last 4 Forecasts (EW2-EW5): Rank 17/52 - more balanced
- Last 8 Forecasts (EW51-EW5): Rank 4/56 - longer-term
- **Season (EW47-EW5): Rank 4/56** - full 2025-2026 season ⭐

**Actions Taken:**
1. Updated `html_parser.py` to support configurable evaluation periods
2. Changed default from 'last_2' to 'last_4' for more representative rankings
3. Added evaluation period description to model card display

---

### Season Clarity and Enhanced Metrics

**Prompt:**
```
This is a good step towards improvement. Let's visit another aspect before commiting changes. On the top of the card it shows "Season: 2024-2025" and then "Updated: 226-02-11". This is a bit confusing because are we including evaluations from the past season and up to this current season too? Is the overall ranking for just the current season (2025-2026)? Can you ensure the overall rank is for the "current season"? Also, can we add the all the other eval metrics to the spider plot (e.g. rWIS, rMAE, ...)?
```

**Actions Taken:**
1. **Added 'season' evaluation period** covering full EW47-EW5 (2025-2026 season)
2. **Changed default from 'last_4' to 'season'** for complete season rankings
3. **Fixed season year** from "2024-2025" to "2025-2026"
4. **Expanded spider plot** from 4 to 5 metrics:
   - WIS (Absolute Weighted Interval Score)
   - **Relative WIS (NEW!)** - Shows excellent performance (rank 3/56)
   - MAE (Mean Absolute Error)
   - 50% Coverage
   - 95% Coverage
5. **Enhanced model card display** with evaluation period in Quick Stats section

**Final Results - UMass-flusion Full Season (2025-2026):**
- **Overall Rank: 4 / 56** (top 7%) 🎯
- WIS: 124.52 (Rank 11/56)
- **Relative WIS: 0.639 (Rank 3/56)** - excellent!
- MAE: 181.26 (Rank 10/56)
- 50% Coverage: 30.0% (Rank 36/56)
- 95% Coverage: 72.6% (Rank 27/56)

**Files Modified:**
- `src/evaluation/html_parser.py` - Added 'season' period mapping
- `src/evaluation/metrics_extractor.py` - Added Relative WIS extraction
- `src/generate_real_card.py` - Changed defaults and added rWIS to spider
- `src/model_card_generator.py` - Added evaluation period display
- Regenerated model card with full season data

**PR Created:**
- [PR #2: Integrate real evaluation metrics with full season rankings](https://github.com/trobacker/reichlab-model-cards/pull/2)
- Comprehensive PR description with before/after comparisons
- Testing instructions and future enhancement ideas

---

*This log will be updated as the project progresses.*
