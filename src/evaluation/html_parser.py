"""
Parse HTML evaluation reports to extract model performance metrics.
"""

from bs4 import BeautifulSoup
import json
import pandas as pd
from pathlib import Path


def parse_wis_report(html_path, evaluation_period='last_4'):
    """
    Parse WIS evaluation report HTML to extract model metrics.

    Parameters
    ----------
    html_path : str or Path
        Path to the HTML report file
    evaluation_period : str, optional
        Which evaluation period to extract:
        - 'last_2': Last 2 Forecasts (most recent, but least stable)
        - 'last_4': Last 4 Forecasts (balanced)
        - 'last_8': Last 8 Forecasts (longer-term performance)
        - 'season': Full Season (recommended, complete season evaluation)
        Default: 'last_4'

    Returns
    -------
    tuple
        (DataFrame with metrics, evaluation_period_description)
    """

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')
    json_data_tags = soup.find_all('script', {'type': 'application/json'})

    if len(json_data_tags) == 0:
        raise ValueError(f"No JSON data found in {html_path}")

    # Map evaluation period to table index
    table_map = {
        'last_2': 0,   # Last 2 Forecasts (EW4-EW5)
        'last_4': 2,   # Last 4 Forecasts (EW2-EW5)
        'last_8': 4,   # Last 8 Forecasts (EW51-EW5)
        'season': 9    # Full Season (EW47-EW5)
    }

    if evaluation_period not in table_map:
        raise ValueError(f"Invalid evaluation_period: {evaluation_period}. "
                        f"Must be one of: {list(table_map.keys())}")

    table_idx = table_map[evaluation_period]

    if table_idx >= len(json_data_tags):
        raise ValueError(f"Table for {evaluation_period} not found in report")

    # Parse the selected JSON tag
    data = json.loads(json_data_tags[table_idx].string)

    # Find the section header for this table
    current = json_data_tags[table_idx]
    period_description = "Unknown Period"
    for _ in range(20):
        current = current.find_previous('h2')
        if current:
            period_description = current.get_text().strip()
            break

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

    # Create DataFrame (including relative_wis for spider plots)
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

    return df, period_description


def parse_all_evaluation_periods(html_path):
    """
    Parse all evaluation periods from a WIS report.

    Parameters
    ----------
    html_path : str or Path
        Path to the HTML report file

    Returns
    -------
    dict
        Dictionary mapping evaluation period to (DataFrame, description)
    """

    results = {}

    for period in ['last_2', 'last_4', 'last_8']:
        try:
            df, description = parse_wis_report(html_path, evaluation_period=period)
            results[period] = {
                'dataframe': df,
                'description': description,
                'total_models': len(df)
            }
            print(f"✓ Parsed {description}: {len(df)} models")
        except Exception as e:
            print(f"✗ Failed to parse {period}: {e}")

    return results


if __name__ == '__main__':
    # Test the parser
    html_path = 'temp-repos/FluSight-forecast-hub/reports/Flu_Hospitalizations_Forecasts_WIS_11 February 2026.html'

    print("Testing different evaluation periods...")
    print("=" * 80)

    for period in ['last_2', 'last_4', 'last_8']:
        print(f"\n{period.upper()}:")
        df, description = parse_wis_report(html_path, evaluation_period=period)
        print(f"  Period: {description}")
        print(f"  Models: {len(df)}")

        # Find UMass-flusion
        if 'UMass-flusion' in df.index:
            umass = df.loc['UMass-flusion']
            print(f"  UMass-flusion: Rank {umass['rank']}/{len(df)}, WIS: {umass['absolute_wis']}")

    print("\n" + "=" * 80)
    print("✓ Testing complete")
