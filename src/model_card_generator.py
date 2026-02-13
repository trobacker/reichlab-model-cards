"""
Generate HTML model cards for forecasting models.
"""

from datetime import datetime
from pathlib import Path
import base64


def encode_image_base64(image_path):
    """Encode an image file to base64 for embedding in HTML."""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def generate_model_card_html(model_data, spider_plot_path, output_path):
    """
    Generate an HTML model card.

    Parameters
    ----------
    model_data : dict
        Dictionary containing model information and metrics
    spider_plot_path : str
        Path to the spider plot image
    output_path : str
        Path to save the HTML file

    Returns
    -------
    str
        Path to the generated HTML file
    """

    # Encode spider plot as base64 for embedding
    spider_plot_b64 = encode_image_base64(spider_plot_path)

    # Extract data
    model_name = model_data.get('model_name', 'Unknown Model')
    team_name = model_data.get('team_name', 'Unknown Team')
    version = model_data.get('version', '1.0')
    season = model_data.get('season', '2024-2025')
    reference_date = model_data.get('reference_date', 'N/A')
    last_updated = model_data.get('last_updated', datetime.now().strftime('%Y-%m-%d'))

    # Model overview
    model_type = model_data.get('model_type', 'Unknown')
    methodology = model_data.get('methodology', 'No description available.')
    data_sources = model_data.get('data_sources', ['Unknown'])

    # Performance metrics
    metrics = model_data.get('metrics', {})
    overall_rank = model_data.get('overall_rank', 'N/A')
    total_models = model_data.get('total_models', 'N/A')

    # Strengths and limitations
    strengths = model_data.get('strengths', [])
    limitations = model_data.get('limitations', [])

    # Usage guidance
    use_with_confidence = model_data.get('use_with_confidence', [])
    use_with_caution = model_data.get('use_with_caution', [])

    # Model evolution
    recent_changes = model_data.get('recent_changes', [])

    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model Card: {model_name}</title>
    <style>
        @page {{
            size: letter;
            margin: 0.5in;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.4;
            color: #333;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
            background: white;
            font-size: 11pt;
        }}

        .header {{
            background: linear-gradient(135deg, #2E86AB 0%, #1E5A7A 100%);
            color: white;
            padding: 0.75rem 1rem;
            border-radius: 8px 8px 0 0;
            margin: -0.5in -0.5in 0.75rem -0.5in;
        }}

        .header h1 {{
            margin: 0;
            font-size: 20pt;
            font-weight: 600;
        }}

        .header .meta {{
            font-size: 9pt;
            margin-top: 0.25rem;
            opacity: 0.95;
        }}

        .badge {{
            display: inline-block;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: 600;
            margin-right: 0.3rem;
            background: rgba(255,255,255,0.2);
        }}

        .content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        .card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 0.6rem;
            page-break-inside: avoid;
        }}

        .card h2 {{
            margin: 0 0 0.4rem 0;
            font-size: 12pt;
            color: #2E86AB;
            border-bottom: 2px solid #2E86AB;
            padding-bottom: 0.2rem;
        }}

        .card h3 {{
            margin: 0.4rem 0 0.2rem 0;
            font-size: 10pt;
            color: #495057;
        }}

        .metrics-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9pt;
            margin-top: 0.3rem;
        }}

        .metrics-table th {{
            background: #e9ecef;
            padding: 0.3rem 0.4rem;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #2E86AB;
        }}

        .metrics-table td {{
            padding: 0.25rem 0.4rem;
            border-bottom: 1px solid #dee2e6;
        }}

        .metrics-table tr:last-child td {{
            border-bottom: none;
        }}

        .quick-stat {{
            display: inline-block;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 0.3rem 0.5rem;
            margin: 0.2rem 0.2rem 0.2rem 0;
            font-size: 9pt;
        }}

        .quick-stat .label {{
            color: #6c757d;
            font-size: 8pt;
            display: block;
        }}

        .quick-stat .value {{
            color: #2E86AB;
            font-weight: 600;
            font-size: 11pt;
        }}

        .spider-plot {{
            text-align: center;
            margin: 0.5rem 0;
        }}

        .spider-plot img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
        }}

        ul {{
            margin: 0.3rem 0;
            padding-left: 1.2rem;
        }}

        li {{
            margin-bottom: 0.2rem;
            font-size: 9.5pt;
        }}

        .icon {{
            margin-right: 0.2rem;
        }}

        .strength {{
            color: #28a745;
        }}

        .limitation {{
            color: #dc3545;
        }}

        .confidence {{
            color: #28a745;
        }}

        .caution {{
            color: #ffc107;
        }}

        .footer {{
            margin-top: 0.75rem;
            padding-top: 0.5rem;
            border-top: 1px solid #dee2e6;
            font-size: 8pt;
            color: #6c757d;
            text-align: center;
        }}

        .methodology {{
            font-size: 9.5pt;
            line-height: 1.4;
            margin: 0.3rem 0;
        }}

        .data-sources {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.3rem;
            margin-top: 0.3rem;
        }}

        .data-source-tag {{
            background: #2E86AB;
            color: white;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: 600;
        }}

        .change-item {{
            font-size: 9pt;
            margin-bottom: 0.3rem;
            padding-left: 0.5rem;
            border-left: 3px solid #2E86AB;
        }}

        .change-date {{
            font-weight: 600;
            color: #2E86AB;
        }}

        @media print {{
            body {{
                margin: 0;
                padding: 0.5in;
            }}
            .header {{
                margin: -0.5in -0.5in 0.75rem -0.5in;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{model_name}</h1>
        <div class="meta">
            <span class="badge">Version {version}</span>
            <span class="badge">{team_name}</span>
            <span class="badge">Season: {season}</span>
            <span class="badge">Updated: {last_updated}</span>
        </div>
    </div>

    <div class="content">
        <div class="card full-width">
            <h2>📊 Quick Stats</h2>
            <div>
                <div class="quick-stat">
                    <span class="label">Overall Rank</span>
                    <span class="value">{overall_rank} / {total_models}</span>
                </div>
                <div class="quick-stat">
                    <span class="label">Model Type</span>
                    <span class="value">{model_type}</span>
                </div>
                <div class="quick-stat">
                    <span class="label">Reference Date</span>
                    <span class="value">{reference_date}</span>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🎯 Model Overview</h2>
            <div class="methodology">
                <strong>Methodology:</strong> {methodology}
            </div>
            <div style="margin-top: 0.4rem;">
                <strong style="font-size: 9.5pt;">Data Sources:</strong>
                <div class="data-sources">
                    {''.join([f'<span class="data-source-tag">{source}</span>' for source in data_sources])}
                </div>
            </div>
        </div>

        <div class="card">
            <h2>📈 Performance Rankings</h2>
            <div class="spider-plot">
                <img src="data:image/png;base64,{spider_plot_b64}" alt="Performance Spider Plot" style="max-height: 3.5in;">
            </div>
        </div>

        <div class="card">
            <h2>📊 Key Metrics</h2>
            <table class="metrics-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                        <th>Rank</th>
                    </tr>
                </thead>
                <tbody>
"""

    # Add metrics rows
    for metric_name, metric_info in metrics.items():
        value = metric_info.get('value', 'N/A')
        rank = metric_info.get('rank', 'N/A')
        total = metric_info.get('total_models', total_models)
        html_content += f"""                    <tr>
                        <td>{metric_name}</td>
                        <td>{value}</td>
                        <td>{rank} / {total}</td>
                    </tr>
"""

    html_content += """                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>✅ Strengths</h2>
            <ul>
"""

    for strength in strengths:
        html_content += f'                <li><span class="icon strength">✓</span>{strength}</li>\n'

    html_content += """            </ul>
        </div>

        <div class="card">
            <h2>⚠️ Limitations</h2>
            <ul>
"""

    for limitation in limitations:
        html_content += f'                <li><span class="icon limitation">!</span>{limitation}</li>\n'

    html_content += """            </ul>
        </div>

        <div class="card full-width">
            <h2>💡 Usage Guidance</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <div>
                    <h3 class="confidence">✓ Use with Confidence</h3>
                    <ul style="margin-top: 0.2rem;">
"""

    for item in use_with_confidence:
        html_content += f'                        <li>{item}</li>\n'

    html_content += """                    </ul>
                </div>
                <div>
                    <h3 class="caution">⚠ Use with Caution</h3>
                    <ul style="margin-top: 0.2rem;">
"""

    for item in use_with_caution:
        html_content += f'                        <li>{item}</li>\n'

    html_content += """                    </ul>
                </div>
            </div>
        </div>

        <div class="card full-width">
            <h2>🔄 Recent Model Evolution</h2>
"""

    for change in recent_changes:
        date = change.get('date', 'N/A')
        description = change.get('description', '')
        html_content += f'            <div class="change-item"><span class="change-date">{date}:</span> {description}</div>\n'

    html_content += """        </div>
    </div>

    <div class="footer">
        Generated on {generation_date} | FluSight Forecast Hub |
        <a href="https://github.com/cdcepi/FluSight-forecast-hub" style="color: #2E86AB;">GitHub Repository</a>
    </div>
</body>
</html>
""".format(generation_date=datetime.now().strftime('%Y-%m-%d %H:%M'))

    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Model card generated: {output_path}")
    return output_path


def generate_sample_umass_flusion_card():
    """Generate a sample model card for UMass-flusion with mock data."""

    model_data = {
        'model_name': 'UMass-flusion',
        'team_name': 'UMass-Amherst',
        'version': '1.1',
        'season': '2024-2025',
        'reference_date': '2025-01-18',
        'last_updated': '2025-01-18',
        'model_type': 'Ensemble (Statistical + ML)',
        'methodology': 'Quantile average ensemble of three components: (1) AR(6) pooled model with shared coefficients across locations, (2) GBQR 3-source spatial model incorporating spatial correlation for state-level forecasts, (3) GBQR 3-source model for US national forecasts.',
        'data_sources': ['NHSN', 'FluSurv-NET', 'ILINet'],
        'overall_rank': '4',
        'total_models': '20',
        'metrics': {
            'WIS 0-week': {'value': '45.2', 'rank': 3, 'total_models': 20},
            'WIS 1-week': {'value': '67.3', 'rank': 5, 'total_models': 20},
            'WIS 2-week': {'value': '89.1', 'rank': 4, 'total_models': 20},
            'WIS 3-week': {'value': '112.4', 'rank': 6, 'total_models': 20},
            '50% Coverage (avg)': {'value': '50%', 'rank': 8, 'total_models': 20},
            '95% Coverage (avg)': {'value': '93%', 'rank': 4, 'total_models': 20},
        },
        'strengths': [
            'Excellent short-term forecasting performance (0-1 week ahead)',
            'Strong spatial correlation modeling captures geographic patterns',
            'Robust handling of data anomalies through ensemble averaging',
            'Well-calibrated uncertainty quantification',
            'Consistently ranks in top 5 across multiple metrics'
        ],
        'limitations': [
            'Longer-horizon (3+ week) forecasts show increased uncertainty',
            'Performance varies with location population size',
            'Sensitive to reporting delays in small states',
            'May underestimate uncertainty during rapid epidemic growth',
            'Post-holiday periods can show temporary performance degradation'
        ],
        'use_with_confidence': [
            'National-level forecasts',
            'Short-term (0-2 week) predictions',
            'Locations with consistent data reporting',
            'Mid-season stable epidemic periods'
        ],
        'use_with_caution': [
            'Small states with high reporting variability',
            'Weeks immediately following major holidays',
            'Locations with recent data anomalies',
            'Early season when signal is weak'
        ],
        'recent_changes': [
            {
                'date': '2025-01-18',
                'description': 'All components active for this week\'s submission'
            },
            {
                'date': '2025-01-02',
                'description': 'GBQR-only submission for post-Christmas week to avoid AR(6) underperformance during seasonal effects'
            },
            {
                'date': '2024-12-20',
                'description': 'Version 1.1 released: Added GBQR spatial2 component for improved state-level forecasts'
            },
            {
                'date': '2024-12-07',
                'description': 'Dropped Puerto Rico forecasts due to data quality concerns'
            }
        ]
    }

    # First generate the spider plot
    from spider_plot import generate_sample_spider_plot
    spider_plot_path = generate_sample_spider_plot()

    # Then generate the model card
    output_path = 'cards/UMass-flusion-2025-01-18.html'
    generate_model_card_html(model_data, spider_plot_path, output_path)

    return output_path


if __name__ == '__main__':
    generate_sample_umass_flusion_card()
