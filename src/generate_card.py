#!/usr/bin/env python3
"""
Main script to generate model cards.

Usage:
    python generate_card.py --model UMass-flusion --date 2025-01-18
    python generate_card.py --sample  # Generate sample card with mock data
"""

import argparse
from pathlib import Path
from spider_plot import generate_spider_plot, generate_sample_spider_plot
from model_card_generator import generate_model_card_html, generate_sample_umass_flusion_card


def main():
    parser = argparse.ArgumentParser(description='Generate model cards for forecasting models')
    parser.add_argument('--model', type=str, help='Model name (e.g., UMass-flusion)')
    parser.add_argument('--date', type=str, help='Reference date (YYYY-MM-DD)')
    parser.add_argument('--sample', action='store_true', help='Generate sample card with mock data')
    parser.add_argument('--output-dir', type=str, default='cards', help='Output directory for cards')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    if args.sample:
        print("Generating sample model card with mock data...")
        card_path = generate_sample_umass_flusion_card()
        print(f"\n✓ Sample model card generated successfully!")
        print(f"  Location: {card_path}")
        print(f"\nOpen the file in your browser to view it.")
    else:
        if not args.model or not args.date:
            print("Error: --model and --date are required (or use --sample for demo)")
            return

        print(f"Generating model card for {args.model} (date: {args.date})...")
        print("Note: This requires evaluation data. Use --sample for demo with mock data.")

        # TODO: Implement real data loading and processing
        # For now, just show a message
        print("\nReal data processing not yet implemented.")
        print("Please use --sample to generate a demo card.")


if __name__ == '__main__':
    main()
