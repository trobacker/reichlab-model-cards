"""
Extract and structure model metrics for model card generation.
"""

import pandas as pd
from pathlib import Path

try:
    from .html_parser import parse_wis_report
except ImportError:
    from html_parser import parse_wis_report


def extract_model_metrics(model_name, reports_dir=None, html_path=None):
    """
    Extract metrics for a specific model from evaluation reports.

    Parameters
    ----------
    model_name : str
        Name of the model (e.g., "UMass-flusion")
    reports_dir : str or Path, optional
        Directory containing HTML reports
    html_path : str or Path, optional
        Path to specific HTML report

    Returns
    -------
    dict
        Dictionary with model metrics suitable for model card generation
    """

    if html_path is None:
        if reports_dir is None:
            reports_dir = Path('temp-repos/FluSight-forecast-hub/reports')
        else:
            reports_dir = Path(reports_dir)

        # Find the WIS hospitalization report
        wis_reports = list(reports_dir.glob("*Hospitalizations*WIS*.html"))
        if len(wis_reports) == 0:
            raise FileNotFoundError(f"No WIS hospitalization reports found in {reports_dir}")

        html_path = wis_reports[0]  # Use most recent

    # Parse the report
    df = parse_wis_report(html_path)

    # Find the model
    if model_name not in df.index:
        raise ValueError(f"Model '{model_name}' not found in report. Available models: {df.index.tolist()[:10]}...")

    model_data = df.loc[model_name]
    total_models = len(df)

    # Calculate rankings for different metrics
    # (Lower WIS is better, higher coverage is better)
    df['wis_rank'] = df['absolute_wis'].rank(method='min').astype(int)
    df['mae_rank'] = df['mae'].rank(method='min').astype(int)
    df['coverage_50_rank'] = df['coverage_50pct'].rank(method='min', ascending=False).astype(int)
    df['coverage_95_rank'] = df['coverage_95pct'].rank(method='min', ascending=False).astype(int)

    # Extract model's rankings
    rankings = {
        'WIS': df.loc[model_name, 'wis_rank'],
        'MAE': df.loc[model_name, 'mae_rank'],
        '50% Coverage': df.loc[model_name, 'coverage_50_rank'],
        '95% Coverage': df.loc[model_name, 'coverage_95_rank']
    }

    # Structure for model card
    metrics_data = {
        'model_name': model_name,
        'overall_rank': int(model_data['rank']),
        'total_models': total_models,
        'metrics': {
            'WIS': {
                'value': f"{model_data['absolute_wis']:.2f}",
                'rank': rankings['WIS'],
                'total_models': total_models
            },
            'MAE': {
                'value': f"{model_data['mae']:.2f}",
                'rank': rankings['MAE'],
                'total_models': total_models
            },
            '50% Coverage': {
                'value': f"{model_data['coverage_50pct']:.1f}%",
                'rank': rankings['50% Coverage'],
                'total_models': total_models
            },
            '95% Coverage': {
                'value': f"{model_data['coverage_95pct']:.1f}%",
                'rank': rankings['95% Coverage'],
                'total_models': total_models
            }
        },
        'rankings_for_spider': {
            'WIS': {'rank': rankings['WIS'], 'total_models': total_models},
            'MAE': {'rank': rankings['MAE'], 'total_models': total_models},
            '50% Coverage': {'rank': rankings['50% Coverage'], 'total_models': total_models},
            '95% Coverage': {'rank': rankings['95% Coverage'], 'total_models': total_models}
        }
    }

    return metrics_data


def get_model_rankings(html_path=None):
    """
    Get rankings for all models.

    Returns
    -------
    pd.DataFrame
        DataFrame with rankings across multiple metrics
    """

    if html_path is None:
        reports_dir = Path('temp-repos/FluSight-forecast-hub/reports')
        wis_reports = list(reports_dir.glob("*Hospitalizations*WIS*.html"))
        if len(wis_reports) == 0:
            raise FileNotFoundError(f"No WIS reports found")
        html_path = wis_reports[0]

    df = parse_wis_report(html_path)

    # Calculate rankings
    df['wis_rank'] = df['absolute_wis'].rank(method='min').astype(int)
    df['mae_rank'] = df['mae'].rank(method='min').astype(int)
    df['coverage_50_rank'] = df['coverage_50pct'].rank(method='min', ascending=False).astype(int)
    df['coverage_95_rank'] = df['coverage_95pct'].rank(method='min', ascending=False).astype(int)

    return df


if __name__ == '__main__':
    # Test extraction for UMass-flusion
    print("Extracting metrics for UMass-flusion...")

    metrics = extract_model_metrics('UMass-flusion')

    print("\n" + "=" * 80)
    print("Extracted Metrics:")
    print(f"  Model: {metrics['model_name']}")
    print(f"  Overall Rank: {metrics['overall_rank']} / {metrics['total_models']}")
    print("\nDetailed Metrics:")
    for metric_name, metric_info in metrics['metrics'].items():
        print(f"  {metric_name:20s} Value: {metric_info['value']:10s} Rank: {metric_info['rank']:2d} / {metric_info['total_models']}")

    print("\nRankings for Spider Plot:")
    for metric_name, ranking in metrics['rankings_for_spider'].items():
        print(f"  {metric_name:20s} Rank: {ranking['rank']:2d} / {ranking['total_models']}")

    print("\n✓ Metrics extraction successful!")
