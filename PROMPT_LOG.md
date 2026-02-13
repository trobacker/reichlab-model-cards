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

*This log will be updated as the project progresses.*
