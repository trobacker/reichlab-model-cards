"""
Parse HTML evaluation reports to extract model performance metrics.
"""

from bs4 import BeautifulSoup
import json
import pandas as pd
from pathlib import Path


def parse_wis_report(html_path):
    """
    Parse WIS evaluation report HTML to extract model metrics.

    Parameters
    ----------
    html_path : str or Path
        Path to the HTML report file

    Returns
    -------
    pd.DataFrame
        DataFrame with model names as index and metrics as columns
    """

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')
    json_data_tags = soup.find_all('script', {'type': 'application/json'})

    if len(json_data_tags) == 0:
        raise ValueError(f"No JSON data found in {html_path}")

    # Parse first JSON tag (contains main summary table)
    data = json.loads(json_data_tags[0].string)

    # Extract column names from HTML container
    container_html = data['x']['container']
    container_soup = BeautifulSoup(container_html, 'lxml')
    headers = container_soup.find_all('th')
    column_names = [h.get_text().strip() for h in headers]

    # Extract table data
    # Data is transposed: each column is a model, rows are metrics
    rows = data['x']['data']

    # Row mapping:
    # Row 0: Rank
    # Row 1: Model names
    # Row 2: Absolute WIS
    # Row 3: Relative WIS
    # Row 4: Log Relative WIS
    # Row 5: MAE
    # Row 6: 50% Coverage (%)
    # Row 7: 95% Coverage (%)
    # Row 8: Number of Forecasts Submitted
    # Row 9: % Forecasts Submitted
    # Row 10: Number of Locations Submitted
    # Row 11: % Locations Submitted

    ranks = rows[0]
    model_names = rows[1]
    absolute_wis = rows[2]
    relative_wis = rows[3]
    log_relative_wis = rows[4]
    mae = rows[5]
    coverage_50 = rows[6]
    coverage_95 = rows[7]
    n_forecasts = rows[8]
    pct_forecasts = rows[9]
    n_locations = rows[10]
    pct_locations = rows[11]

    # Create DataFrame
    df = pd.DataFrame({
        'model': model_names,
        'rank': ranks,
        'absolute_wis': absolute_wis,
        'relative_wis': relative_wis,
        'log_relative_wis': log_relative_wis,
        'mae': mae,
        'coverage_50pct': coverage_50,
        'coverage_95pct': coverage_95,
        'n_forecasts': n_forecasts,
        'pct_forecasts': pct_forecasts,
        'n_locations': n_locations,
        'pct_locations': pct_locations
    })

    # Set model as index
    df = df.set_index('model')

    # Convert rank to int
    df['rank'] = df['rank'].astype(int)

    return df


def parse_all_wis_horizons(reports_dir):
    """
    Parse WIS reports for different horizons if available.

    Parameters
    ----------
    reports_dir : str or Path
        Directory containing HTML reports

    Returns
    -------
    dict
        Dictionary mapping horizon to DataFrame
    """

    reports_dir = Path(reports_dir)

    # Look for WIS reports
    wis_reports = list(reports_dir.glob("*WIS*.html"))

    results = {}

    for report_path in wis_reports:
        try:
            df = parse_wis_report(report_path)
            # Try to infer horizon from filename
            # For now, use "overall" as key
            results['overall'] = df
            print(f"✓ Parsed {report_path.name}")
        except Exception as e:
            print(f"✗ Failed to parse {report_path.name}: {e}")

    return results


if __name__ == '__main__':
    # Test the parser
    html_path = 'temp-repos/FluSight-forecast-hub/reports/Flu_Hospitalizations_Forecasts_WIS_11 February 2026.html'

    print("Parsing WIS report...")
    df = parse_wis_report(html_path)

    print(f"\n✓ Successfully parsed {len(df)} models")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nDataFrame shape: {df.shape}")

    print("\n" + "=" * 80)
    print("Top 10 models by rank:")
    print(df.sort_values('rank').head(10)[['rank', 'absolute_wis', 'coverage_50pct', 'coverage_95pct']])

    print("\n" + "=" * 80)
    print("UMass models:")
    umass_models = df[df.index.str.contains('UMass', case=False)]
    print(umass_models[['rank', 'absolute_wis', 'coverage_50pct', 'coverage_95pct']])

    # Save to CSV
    output_path = 'extracted_wis_metrics.csv'
    df.to_csv(output_path)
    print(f"\n✓ Saved all metrics to {output_path}")
