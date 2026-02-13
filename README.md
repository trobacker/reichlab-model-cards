# Model Cards for Infectious Disease Forecasting

Generate human-interpretable "Model Cards" for infectious disease forecasting models, drawing inspiration from sports analytics stat reporting. This project creates concise, one-page summaries that help researchers, public health officials, and modelers quickly understand model performance, strengths, limitations, and appropriate use cases.

## Overview

Model Cards provide:
- **Performance rankings** across multiple evaluation metrics (visualized as spider plots)
- **Quick stats** showing overall model ranking and key metrics
- **Strengths & limitations** identified through evaluation
- **Usage guidance** for when to trust model forecasts
- **Model evolution** tracking changes and interventions over time

Initial focus: [FluSight forecast hub](https://github.com/cdcepi/FluSight-forecast-hub) models, starting with UMass-flusion variants.

## Quick Start

### Prerequisites
- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/reichlab/reichlab-model-cards.git
cd reichlab-model-cards

# Set up virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### Generate Sample Model Card

```bash
# Generate a prototype card with mock data
python src/generate_card.py --sample

# Open the generated card in your browser
open cards/UMass-flusion-2025-01-18.html
```

The model card can be printed to PDF directly from your browser (File → Print → Save as PDF).

## Project Structure

```
├── src/                          # Development code
│   ├── spider_plot.py           # Spider/radar plot generation
│   ├── model_card_generator.py  # HTML model card generator
│   └── generate_card.py         # CLI interface
├── cards/                        # Generated model cards (HTML + images)
├── .claude/                      # Project context documentation
├── CONTEXT.md                    # Repository relationships & data sources
├── PROMPT_LOG.md                 # Development session history
└── PROJECT_README.md             # Detailed documentation
```

## Model Card Components

Each model card includes:
1. **Quick Stats** - Overall ranking and model type
2. **Model Overview** - Methodology and data sources
3. **Performance Rankings** - Spider plot comparing metrics
4. **Key Metrics Table** - Detailed performance breakdown
5. **Strengths & Limitations** - Identified through evaluation
6. **Usage Guidance** - When to use with confidence vs caution
7. **Recent Evolution** - Model changes and updates

## Next Steps

- Integrate real evaluation data from FluSight hub
- Automate weekly card generation
- Add time series forecast visualizations
- Expand to additional models and ensembles

## Documentation

- See [PROJECT_README.md](PROJECT_README.md) for detailed documentation
- See [CONTEXT.md](CONTEXT.md) for background on hubverse and FluSight
- See `.claude/` directory for technical references

## Related Resources

- [FluSight Forecast Hub](https://github.com/cdcepi/FluSight-forecast-hub)
- [FluSight Dashboard](https://reichlab.io/flusight-dashboard/)
- [Hubverse Framework](https://hubverse.io/)
- [Reich Lab](https://reichlab.io/)

## License

See LICENSE file for details.
