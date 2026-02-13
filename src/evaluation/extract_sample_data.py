"""
Extract a sample of data from HTML report to understand structure.
"""

from bs4 import BeautifulSoup
import json
import pandas as pd

def extract_first_table_data(html_path):
    """Extract the first data table from HTML report."""

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')
    json_data_tags = soup.find_all('script', {'type': 'application/json'})

    if len(json_data_tags) == 0:
        print("No JSON data found")
        return None

    # Parse first JSON tag
    data = json.loads(json_data_tags[0].string)

    print("Top-level keys:", list(data.keys()))
    print("\n'x' keys:", list(data['x'].keys()))

    # The 'data' field should contain the table data
    table_data = data['x']['data']

    print(f"\nTable data type: {type(table_data)}")
    if isinstance(table_data, list):
        print(f"Number of rows: {len(table_data)}")
        if len(table_data) > 0:
            print(f"Columns per row: {len(table_data[0])}")
            print(f"\nFirst 3 rows:")
            for i, row in enumerate(table_data[:3]):
                print(f"  Row {i}: {row}")

    # Try to find column names
    if 'container' in data['x']:
        print(f"\n'container' field: {data['x']['container'][:500]}")

    if 'options' in data['x']:
        print(f"\n'options' keys: {list(data['x']['options'].keys())}")
        if 'columnDefs' in data['x']['options']:
            print(f"Column definitions: {data['x']['options']['columnDefs'][:3]}")

    # Convert to DataFrame if possible
    if isinstance(table_data, list) and len(table_data) > 0:
        print("\n" + "="*80)
        print("Attempting to create DataFrame...")

        # Extract column names from HTML container if possible
        if 'container' in data['x']:
            container_html = data['x']['container']
            container_soup = BeautifulSoup(container_html, 'lxml')
            headers = container_soup.find_all('th')
            column_names = [h.get_text().strip() for h in headers]
            print(f"Column names from HTML: {column_names}")

            if len(column_names) == len(table_data[0]):
                df = pd.DataFrame(table_data, columns=column_names)
                print(f"\nDataFrame shape: {df.shape}")
                print(f"\nDataFrame head:")
                print(df.head(10))
                print(f"\nDataFrame columns: {df.columns.tolist()}")

                # Save to CSV for inspection
                output_path = 'temp_wis_data.csv'
                df.to_csv(output_path, index=False)
                print(f"\n✓ Saved to {output_path}")

                return df

    return None


if __name__ == '__main__':
    html_path = 'temp-repos/FluSight-forecast-hub/reports/Flu_Hospitalizations_Forecasts_WIS_11 February 2026.html'
    df = extract_first_table_data(html_path)
