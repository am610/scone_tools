#!/usr/bin/env python3
"""
Example script for analyzing SCONE population statistics

This script demonstrates how to load and analyze extracted CSV data
from SCONE TFRecords to understand population characteristics.

Usage:
    python analyze_population.py summary.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys

def load_data(csv_path):
    """Load the extracted SCONE data"""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path, sep=' ')
    print(f"Loaded {len(df)} events")
    return df

def basic_statistics(df):
    """Print basic statistics"""
    print("\n" + "="*60)
    print("BASIC STATISTICS")
    print("="*60)

    print(f"\nTotal events: {len(df)}")
    print(f"SNIa: {np.sum(df['label'] == 1)} ({100*np.sum(df['label'] == 1)/len(df):.1f}%)")
    print(f"Non-Ia: {np.sum(df['label'] == 0)} ({100*np.sum(df['label'] == 0)/len(df):.1f}%)")

    print(f"\nRedshift range: {df['redshift'].min():.3f} - {df['redshift'].max():.3f}")
    print(f"Mean redshift: {df['redshift'].mean():.3f}")
    print(f"Median redshift: {df['redshift'].median():.3f}")

    print(f"\nMean SNR: {df['snr_mean'].mean():.2f}")
    print(f"Mean coverage: {df['coverage_fraction'].mean():.2%}")

def compare_classes(df):
    """Compare SNIa vs Non-Ia characteristics"""
    print("\n" + "="*60)
    print("CLASS COMPARISON")
    print("="*60)

    ia = df[df['label'] == 1]
    non_ia = df[df['label'] == 0]

    metrics = [
        ('rise_time_days', 'Rise Time (days)'),
        ('decline_time_days', 'Decline Time (days)'),
        ('duration_days', 'Duration (days)'),
        ('color_ratio', 'Blue/Red Ratio'),
        ('snr_mean', 'Mean SNR')
    ]

    print(f"\n{'Metric':<25} {'SNIa':>12} {'Non-Ia':>12} {'Difference':>12}")
    print("-" * 60)

    for metric, label in metrics:
        ia_mean = ia[metric].mean()
        non_ia_mean = non_ia[metric].mean()
        diff = ia_mean - non_ia_mean
        print(f"{label:<25} {ia_mean:>12.2f} {non_ia_mean:>12.2f} {diff:>12.2f}")

def find_interesting_events(df, output_file='interesting_snids.txt'):
    """Identify interesting events for further investigation"""
    print("\n" + "="*60)
    print("INTERESTING EVENTS")
    print("="*60)

    interesting = []

    # High redshift events
    high_z = df[df['redshift'] > df['redshift'].quantile(0.95)]
    print(f"\nHigh redshift (>95th percentile): {len(high_z)} events")
    interesting.extend(high_z['snid'].tolist())

    # Low SNR events
    low_snr = df[df['snr_mean'] < df['snr_mean'].quantile(0.05)]
    print(f"Low SNR (<5th percentile): {len(low_snr)} events")
    interesting.extend(low_snr['snid'].tolist())

    # Fast transients
    fast = df[df['duration_days'] < df['duration_days'].quantile(0.1)]
    print(f"Fast transients (<10th percentile duration): {len(fast)} events")
    interesting.extend(fast['snid'].tolist())

    # Poor coverage
    poor_coverage = df[df['coverage_fraction'] < 0.3]
    print(f"Poor coverage (<30%): {len(poor_coverage)} events")
    interesting.extend(poor_coverage['snid'].tolist())

    # Remove duplicates
    interesting = list(set(interesting))

    # Save to file
    with open(output_file, 'w') as f:
        f.write(','.join(map(str, interesting[:100])))  # First 100

    print(f"\nTotal unique interesting events: {len(interesting)}")
    print(f"First 100 saved to: {output_file}")
    print(f"Example SNIDs: {interesting[:5]}")

def create_plots(df, output_dir='.'):
    """Create diagnostic plots"""
    print("\n" + "="*60)
    print("CREATING PLOTS")
    print("="*60)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('SCONE Population Analysis', fontsize=16, fontweight='bold')

    # 1. Redshift distribution
    ax = axes[0, 0]
    for label, name, color in [(1, 'SNIa', 'blue'), (0, 'Non-Ia', 'orange')]:
        data = df[df['label'] == label]['redshift']
        ax.hist(data, bins=30, alpha=0.6, label=name, color=color)
    ax.set_xlabel('Redshift')
    ax.set_ylabel('Count')
    ax.set_title('Redshift Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. SNR distribution
    ax = axes[0, 1]
    for label, name, color in [(1, 'SNIa', 'blue'), (0, 'Non-Ia', 'orange')]:
        data = df[df['label'] == label]['snr_mean']
        ax.hist(data, bins=30, alpha=0.6, label=name, color=color, range=(0, 50))
    ax.set_xlabel('Mean SNR')
    ax.set_ylabel('Count')
    ax.set_title('Signal-to-Noise Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. Rise time comparison
    ax = axes[0, 2]
    data_ia = df[df['label'] == 1]['rise_time_days'].dropna()
    data_non_ia = df[df['label'] == 0]['rise_time_days'].dropna()
    ax.hist([data_ia, data_non_ia], bins=30, alpha=0.6,
            label=['SNIa', 'Non-Ia'], color=['blue', 'orange'])
    ax.set_xlabel('Rise Time (days)')
    ax.set_ylabel('Count')
    ax.set_title('Rise Time Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Decline time comparison
    ax = axes[1, 0]
    data_ia = df[df['label'] == 1]['decline_time_days'].dropna()
    data_non_ia = df[df['label'] == 0]['decline_time_days'].dropna()
    ax.hist([data_ia, data_non_ia], bins=30, alpha=0.6,
            label=['SNIa', 'Non-Ia'], color=['blue', 'orange'])
    ax.set_xlabel('Decline Time (days)')
    ax.set_ylabel('Count')
    ax.set_title('Decline Time Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 5. Color ratio vs redshift
    ax = axes[1, 1]
    for label, name, color in [(1, 'SNIa', 'blue'), (0, 'Non-Ia', 'orange')]:
        data = df[df['label'] == label]
        ax.scatter(data['redshift'], data['color_ratio'],
                  alpha=0.3, s=1, label=name, color=color)
    ax.set_xlabel('Redshift')
    ax.set_ylabel('Blue/Red Ratio')
    ax.set_title('Color Evolution with Redshift')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 6. Coverage statistics
    ax = axes[1, 2]
    coverage_data = [
        df[df['label'] == 1]['coverage_fraction'],
        df[df['label'] == 0]['coverage_fraction']
    ]
    ax.boxplot(coverage_data, labels=['SNIa', 'Non-Ia'])
    ax.set_ylabel('Coverage Fraction')
    ax.set_title('Data Coverage by Class')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_file = f"{output_dir}/population_analysis.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved plot to: {output_file}")

    plt.close()

def main():
    parser = argparse.ArgumentParser(
        description='Analyze SCONE population from extracted CSV data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_population.py summary.csv
  python analyze_population.py all_events_combined.csv --output-dir analysis_results
        """
    )

    parser.add_argument('csv_file', help='Path to extracted CSV file')
    parser.add_argument('--output-dir', default='.',
                       help='Directory for output files (default: current directory)')
    parser.add_argument('--no-plots', action='store_true',
                       help='Skip creating plots')

    args = parser.parse_args()

    # Load data
    try:
        df = load_data(args.csv_file)
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        return 1

    # Run analyses
    basic_statistics(df)
    compare_classes(df)
    find_interesting_events(df, f"{args.output_dir}/interesting_snids.txt")

    if not args.no_plots:
        create_plots(df, args.output_dir)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Review the interesting SNIDs in interesting_snids.txt")
    print("2. Visualize specific events using visualize_tfrecords.py")
    print("3. Check the population_analysis.png plot")

    return 0

if __name__ == '__main__':
    sys.exit(main())
