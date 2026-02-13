"""
Explore HTML report structure to understand data format.
"""

from bs4 import BeautifulSoup
import json
import re

def explore_html_report(html_path):
    """Explore the structure of an HTML evaluation report."""

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')

    print(f"Exploring: {html_path}\n")
    print("=" * 80)

    # Find all script tags
    scripts = soup.find_all('script')
    print(f"\nFound {len(scripts)} script tags")

    json_scripts = []
    for i, script in enumerate(scripts):
        if script.string and 'application/json' in str(script):
            json_scripts.append(i)
            print(f"  Script {i}: Contains JSON data")

    # Look for plotly data
    plotly_pattern = re.compile(r'Plotly\.newPlot|plotly_data', re.IGNORECASE)
    plotly_scripts = []
    for i, script in enumerate(scripts):
        if script.string and plotly_pattern.search(script.string):
            plotly_scripts.append(i)
            print(f"  Script {i}: Contains Plotly data")

    # Try to extract JSON from script tags with type="application/json"
    json_data_tags = soup.find_all('script', {'type': 'application/json'})
    print(f"\nFound {len(json_data_tags)} <script type='application/json'> tags")

    for i, tag in enumerate(json_data_tags[:3]):  # Show first 3
        try:
            data = json.loads(tag.string)
            print(f"\n  JSON Tag {i} structure:")
            print(f"    Type: {type(data)}")
            if isinstance(data, dict):
                print(f"    Keys: {list(data.keys())[:10]}")
                # Look for plotly/chart data
                if 'x' in data:
                    print(f"      Has 'x' key (likely chart data)")
                if 'data' in data:
                    print(f"      Has 'data' key")
                    if isinstance(data['data'], list) and len(data['data']) > 0:
                        print(f"      First data item keys: {list(data['data'][0].keys())[:10]}")
            elif isinstance(data, list):
                print(f"    Length: {len(data)}")
                if len(data) > 0:
                    print(f"    First item type: {type(data[0])}")
                    if isinstance(data[0], dict):
                        print(f"    First item keys: {list(data[0].keys())[:10]}")
        except json.JSONDecodeError:
            print(f"  JSON Tag {i}: Failed to parse")

    # Look for tables
    tables = soup.find_all('table')
    print(f"\nFound {len(tables)} table elements")

    # Look for specific patterns that might indicate WIS scores
    wis_pattern = re.compile(r'WIS|wis|weighted.*interval.*score', re.IGNORECASE)
    text_with_wis = soup.find_all(string=wis_pattern)
    print(f"\nFound {len(text_with_wis)} text elements mentioning WIS")

    return soup, json_data_tags


if __name__ == '__main__':
    html_path = 'temp-repos/FluSight-forecast-hub/reports/Flu_Hospitalizations_Forecasts_WIS_11 February 2026.html'
    soup, json_tags = explore_html_report(html_path)

    if len(json_tags) > 0:
        print("\n" + "=" * 80)
        print("\nAttempting to extract first JSON data structure...")
        try:
            data = json.loads(json_tags[0].string)
            print(json.dumps(data, indent=2)[:2000])  # First 2000 chars
        except:
            print("Could not parse first JSON tag")
