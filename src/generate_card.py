#!/usr/bin/env python3
"""
Main script to generate model cards.

Usage:
    python generate_card.py --sample  # Generate sample card with placeholder data
    python generate_card.py --model UMass-flusion --real-data  # Generate with real metrics
    python generate_card.py --model UMass-flusion --report path/to/report.html  # Custom report
"""

import argparse
from pathlib import Path
from spider_plot import generate_spider_plot, generate_sample_spider_plot
from model_card_generator import generate_model_card_html, generate_sample_umass_flusion_card


def main():
    parser = argparse.ArgumentParser(description='Generate model cards for forecasting models')
    parser.add_argument('--model', type=str, help='Model name (e.g., UMass-flusion)')
    parser.add_argument('--sample', action='store_true', help='Generate sample card with placeholder data')
    parser.add_argument('--real-data', action='store_true', help='Use real evaluation metrics from FluSight')
    parser.add_argument('--report', type=str, help='Path to HTML evaluation report')
    parser.add_argument('--output-dir', type=str, default='cards', help='Output directory for cards')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    if args.sample:
        print("Generating sample model card with placeholder data...")
        card_path = generate_sample_umass_flusion_card()
        print(f"\n✓ Sample model card generated successfully!")
        print(f"  Location: {card_path}")
        print(f"\nOpen the file in your browser to view it.")

    elif args.real_data or args.report:
        if not args.model:
            print("Error: --model is required when using --real-data or --report")
            return

        # Import real data generation function
        try:
            from generate_real_card import generate_real_model_card
        except ImportError:
            print("Error: Unable to import evaluation modules.")
            print("Make sure the evaluation package is properly installed.")
            return

        # Determine report path
        if args.report:
            report_path = args.report
        else:
            # Use default FluSight report location
            report_path = 'temp-repos/FluSight-forecast-hub/reports/Flu_Hospitalizations_Forecasts_WIS_11 February 2026.html'

            if not Path(report_path).exists():
                print(f"Error: Default report not found at {report_path}")
                print("Please specify report path with --report or ensure FluSight hub is cloned")
                return

        print(f"Generating model card for {args.model} with real evaluation metrics...")

        try:
            card_path = generate_real_model_card(
                model_name=args.model,
                html_report_path=report_path,
                output_dir=args.output_dir
            )
        except Exception as e:
            print(f"\nError generating model card: {e}")
            print("Please check that the model name exists in the evaluation report.")
            return

    else:
        print("Error: Please specify either --sample or --model with --real-data")
        print("\nExamples:")
        print("  python generate_card.py --sample")
        print("  python generate_card.py --model UMass-flusion --real-data")
        print("  python generate_card.py --model UMass-flusion --report path/to/report.html")


if __name__ == '__main__':
    main()
