# Model Cards for Infectious Disease Forecasting

A prototype system for generating human-interpretable "Model Cards" for infectious disease forecasting models, specifically focusing on the FluSight forecast hub.

## Project Structure

```
reichlab-model-cards/
├── src/                          # Development code
│   ├── spider_plot.py           # Spider/radar plot generation
│   ├── model_card_generator.py  # HTML model card generation
│   └── generate_card.py         # Main entry point script
├── cards/                        # Generated model cards (HTML)
├── .claude/                      # Context documentation
│   ├── HUBVERSE_REFERENCE.md    # Hubverse framework reference
│   └── MODEL_CARDS_CONCEPT.md   # Model cards concept document
├── CONTEXT.md                    # Project context and repository relationships
├── PROMPT_LOG.md                 # Session prompts and findings log
├── requirements.txt              # Python dependencies
└── README.md                     # Main project README
```

## Setup

### Prerequisites
- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/reichlab/reichlab-model-cards.git
   cd reichlab-model-cards
   ```

2. **Set up virtual environment with uv (recommended):**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

   Or with standard pip:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

### Generate Sample Model Card

Generate a prototype model card with mock data:

```bash
python src/generate_card.py --sample
```

This will create:
- `cards/umass-flusion-spider.png` - Spider plot showing model rankings
- `cards/UMass-flusion-2025-01-18.html` - Complete HTML model card

Open the HTML file in your browser to view the model card.

### Generate Model Card for Specific Date (Future)

```bash
python src/generate_card.py --model UMass-flusion --date 2025-01-18
```

Note: Real data processing is not yet implemented. Use `--sample` for demo.

## Model Card Components

The generated model cards include:

1. **Quick Stats** - Overview metrics and model ranking
2. **Model Overview** - Methodology and data sources
3. **Performance Rankings** - Spider plot comparing metrics across models
4. **Key Metrics** - Detailed performance metrics table
5. **Strengths** - Where the model performs well
6. **Limitations** - Known weaknesses and failure modes
7. **Usage Guidance** - When to trust vs use caution
8. **Recent Evolution** - Model changes and updates

## Spider Plot

The spider/radar plot visualizes model rankings across multiple evaluation metrics:
- Each "spoke" represents a different metric (e.g., WIS 0-week, WIS 1-week, etc.)
- Values shown as percentiles: 100% = Rank 1st, 0% = Last place
- Better performance appears as a larger shape on the plot
- Allows quick visual comparison of model strengths across different metrics

## Development

### Key Scripts

- **`spider_plot.py`** - Generates radar charts for model performance
  - `generate_spider_plot()` - Main function for custom data
  - `generate_sample_spider_plot()` - Demo with mock data

- **`model_card_generator.py`** - Creates HTML model cards
  - `generate_model_card_html()` - Main function with data dict
  - `generate_sample_umass_flusion_card()` - Demo card

- **`generate_card.py`** - Command-line interface
  - Coordinates spider plot and card generation
  - Handles arguments and output paths

### Adding New Models

To create a card for a new model:

1. Prepare model data dictionary with required fields (see `generate_sample_umass_flusion_card()` for structure)
2. Prepare metrics data for spider plot (metric names and rankings)
3. Call `generate_spider_plot()` and `generate_model_card_html()`

### Customizing Card Design

The HTML template in `model_card_generator.py` uses embedded CSS. Key sections:
- `.header` - Top banner with model name and metadata
- `.card` - Individual component sections
- `.metrics-table` - Performance metrics table
- Designed for 1-page printing (letter size)
- Easy to export to PDF via browser print

## Future Enhancements

### Planned Features
1. **Real data integration** - Connect to FluSight hub evaluation data
2. **Weekly automation** - Generate cards automatically for each forecast submission
3. **Multiple model comparison** - Side-by-side model card views
4. **Interactive dashboards** - Web-based exploration of cards
5. **PDF export** - Direct PDF generation (currently via browser print)
6. **Historical archives** - Track model performance over time
7. **Ensemble component analysis** - Show contribution of ensemble components

### Evaluation Metrics to Add
- Mean absolute error (MAE)
- Continuous ranked probability score (CRPS)
- Log score
- Prediction interval width
- Bias measures

## Data Sources

### FluSight Forecast Hub
- Repository: https://github.com/cdcepi/FluSight-forecast-hub
- Dashboard: https://reichlab.io/flusight-dashboard/
- S3 Bucket: `cdcepi-flusight-forecast-hub`

### Hubverse Framework
- Documentation: https://hubdocs.readthedocs.io/
- GitHub: https://github.com/hubverse-org

### Reich Lab Forecast Sandbox
- Repository: https://github.com/reichlab/forecast-sandbox-2025-2026
- Experimental model implementations and variants

## References

- **ML Model Cards**: Mitchell et al. (2019) - https://arxiv.org/abs/1810.03993
- **Hubverse**: https://hubverse.io/
- **FluSight Challenge**: CDC Influenza Division forecasting collaboration

## Contributing

This is a prototype project. Feedback and suggestions are welcome!

## License

See LICENSE file for details.

## Contact

- Project Lead: Thomas Robacker (trobacker@umass.edu)
- Reich Lab: https://reichlab.io/
