#!/usr/bin/env python3
"""
Generate model card with real evaluation metrics from FluSight hub.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.metrics_extractor import extract_model_metrics
from src.spider_plot import generate_spider_plot
from src.model_card_generator import generate_model_card_html


def generate_real_model_card(model_name, html_report_path, output_dir='cards'):
    """
    Generate a model card with real evaluation metrics.

    Parameters
    ----------
    model_name : str
        Name of the model (e.g., "UMass-flusion")
    html_report_path : str or Path
        Path to the WIS evaluation HTML report
    output_dir : str
        Output directory for generated cards

    Returns
    -------
    str
        Path to the generated model card
    """

    print(f"Generating model card for {model_name} with real metrics...")
    print("=" * 80)

    # Extract real metrics
    print("\n1. Extracting evaluation metrics from HTML report...")
    metrics = extract_model_metrics(model_name, html_path=html_report_path)

    print(f"   ✓ Overall Rank: {metrics['overall_rank']} / {metrics['total_models']}")
    print(f"   ✓ WIS: {metrics['metrics']['WIS']['value']} (Rank {metrics['metrics']['WIS']['rank']})")
    print(f"   ✓ Coverage: {metrics['metrics']['95% Coverage']['value']} (Rank {metrics['metrics']['95% Coverage']['rank']})")

    # Load model metadata
    print("\n2. Loading model metadata...")
    model_metadata = load_model_metadata(model_name)

    # Generate spider plot with real rankings
    print("\n3. Generating spider plot with real rankings...")
    spider_plot_path = Path(output_dir) / f'{model_name.lower().replace("-", "_")}_spider_real.png'

    spider_metrics = {
        'WIS': metrics['rankings_for_spider']['WIS'],
        'MAE': metrics['rankings_for_spider']['MAE'],
        '50%\nCoverage': metrics['rankings_for_spider']['50% Coverage'],
        '95%\nCoverage': metrics['rankings_for_spider']['95% Coverage']
    }

    generate_spider_plot(
        model_name=model_name,
        metrics_data=spider_metrics,
        output_path=str(spider_plot_path),
        total_models=metrics['total_models']
    )
    print(f"   ✓ Spider plot saved to {spider_plot_path}")

    # Prepare model card data
    print("\n4. Preparing model card data...")
    card_data = {
        'model_name': model_name,
        'team_name': model_metadata.get('team_name', 'UMass-Amherst'),
        'version': model_metadata.get('version', '1.1'),
        'season': '2024-2025',
        'reference_date': 'Through 2026-02-11',  # From report date
        'last_updated': '2026-02-11',
        'model_type': model_metadata.get('model_type', 'Ensemble (Statistical + ML)'),
        'methodology': model_metadata.get('methodology', ''),
        'data_sources': model_metadata.get('data_sources', ['NHSN', 'FluSurv-NET', 'ILINet']),
        'overall_rank': str(metrics['overall_rank']),
        'total_models': str(metrics['total_models']),
        'metrics': metrics['metrics'],
        'strengths': derive_strengths(metrics),
        'limitations': derive_limitations(metrics),
        'use_with_confidence': [
            'Overall performance within top 60% of models',
            'Locations with consistent data reporting',
            'Mid-season stable epidemic periods'
        ],
        'use_with_caution': [
            'Coverage metrics show room for improvement',
            'Small states with high reporting variability',
            'Weeks immediately following major holidays'
        ],
        'recent_changes': model_metadata.get('recent_changes', [])
    }

    # Generate model card
    print("\n5. Generating HTML model card...")
    card_filename = f'{model_name}-real-metrics-{card_data["last_updated"]}.html'
    card_output_path = Path(output_dir) / card_filename

    generate_model_card_html(
        model_data=card_data,
        spider_plot_path=str(spider_plot_path),
        output_path=str(card_output_path)
    )

    print(f"   ✓ Model card saved to {card_output_path}")
    print("\n" + "=" * 80)
    print(f"✓ Model card generation complete!")
    print(f"\nOpen the card: open {card_output_path}")

    return str(card_output_path)


def load_model_metadata(model_name):
    """Load model metadata from hub or use defaults."""

    # For UMass-flusion, use known metadata
    if model_name == 'UMass-flusion':
        return {
            'team_name': 'UMass-Amherst',
            'version': '1.1',
            'model_type': 'Ensemble (Statistical + ML)',
            'methodology': 'Quantile average ensemble of three components: (1) AR(6) pooled model with shared coefficients across locations, (2) GBQR 3-source spatial model incorporating spatial correlation for state-level forecasts, (3) GBQR 3-source model for US national forecasts.',
            'data_sources': ['NHSN', 'FluSurv-NET', 'ILINet'],
            'recent_changes': [
                {
                    'date': '2025-01-18',
                    'description': 'All components active for this evaluation period'
                },
                {
                    'date': '2025-01-02',
                    'description': 'GBQR-only submission for post-Christmas week to avoid AR(6) underperformance'
                },
                {
                    'date': '2024-12-20',
                    'description': 'Version 1.1 released: Added GBQR spatial2 component for improved state-level forecasts'
                }
            ]
        }

    # Default metadata for other models
    return {
        'team_name': 'Unknown Team',
        'version': '1.0',
        'model_type': 'Unknown',
        'methodology': 'Model methodology not available.',
        'data_sources': ['Unknown'],
        'recent_changes': []
    }


def derive_strengths(metrics):
    """Derive strengths based on actual performance."""

    strengths = []
    rank = metrics['overall_rank']
    total = metrics['total_models']

    # Overall performance
    if rank <= total * 0.25:
        strengths.append('Excellent overall performance, ranking in top 25% of models')
    elif rank <= total * 0.5:
        strengths.append('Strong overall performance, ranking in top 50% of models')
    else:
        strengths.append(f'Consistent performance across evaluation period (rank {rank}/{total})')

    # WIS performance
    wis_rank = metrics['metrics']['WIS']['rank']
    if wis_rank <= total * 0.3:
        strengths.append('Strong forecast accuracy measured by WIS')

    # Coverage performance
    cov_95_rank = metrics['metrics']['95% Coverage']['rank']
    cov_95_val = float(metrics['metrics']['95% Coverage']['value'].rstrip('%'))

    if cov_95_val >= 90:
        strengths.append('Excellent uncertainty quantification with 95% coverage near target')
    elif cov_95_val >= 80:
        strengths.append('Good uncertainty quantification with 80%+ coverage at 95% level')

    # Add general strengths
    strengths.append('Ensemble approach combines multiple modeling strategies')
    strengths.append('Incorporates spatial correlation for improved geographic patterns')

    return strengths


def derive_limitations(metrics):
    """Derive limitations based on actual performance."""

    limitations = []
    total = metrics['total_models']

    # Coverage issues
    cov_50_rank = metrics['metrics']['50% Coverage']['rank']
    cov_50_val = float(metrics['metrics']['50% Coverage']['value'].rstrip('%'))

    if cov_50_val < 45:
        limitations.append(f'50% prediction intervals show undercoverage ({cov_50_val:.1f}%, target ~50%)')

    # MAE performance
    mae_rank = metrics['metrics']['MAE']['rank']
    if mae_rank > total * 0.6:
        limitations.append('Point forecast accuracy (MAE) has room for improvement')

    # General limitations
    limitations.append('Performance varies with location population size')
    limitations.append('Sensitive to reporting delays in small states')
    limitations.append('May underestimate uncertainty during rapid epidemic changes')

    return limitations


if __name__ == '__main__':
    # Generate card for UMass-flusion
    model_name = 'UMass-flusion'
    html_report_path = 'temp-repos/FluSight-forecast-hub/reports/Flu_Hospitalizations_Forecasts_WIS_11 February 2026.html'

    output_path = generate_real_model_card(
        model_name=model_name,
        html_report_path=html_report_path,
        output_dir='cards'
    )
