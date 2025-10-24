#!/bin/bash
# Quick start example for SCONE tools
# This script demonstrates a typical workflow

set -e  # Exit on error

echo "=================================================="
echo "SCONE Tools - Quick Start Example"
echo "=================================================="

# Check if we're in a directory with heatmaps
if [ ! -d "heatmaps" ]; then
    echo ""
    echo "ERROR: No 'heatmaps' directory found!"
    echo "Please run this script from a directory containing:"
    echo "  heatmaps/heatmaps_0000.tfrecord"
    echo "  heatmaps/heatmaps_0001.tfrecord"
    echo "  etc."
    exit 1
fi

echo ""
echo "Step 1: Extract summary statistics from first TFRecord file"
echo "-----------------------------------------------------------"
python3 extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output quick_start_summary.csv \
    --limit 1000

echo ""
echo "Step 2: Analyze the extracted data"
echo "-----------------------------------"
python3 examples/analyze_population.py quick_start_summary.csv --output-dir quick_start_results

echo ""
echo "Step 3: Visualize a few sample events"
echo "--------------------------------------"
python3 visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --num_samples 5 \
    --output_dir quick_start_plots

echo ""
echo "Step 4: Create a statistical summary"
echo "-------------------------------------"
python3 visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --statistics \
    --stat_samples 500 \
    --output_dir quick_start_plots

echo ""
echo "=================================================="
echo "QUICK START COMPLETE!"
echo "=================================================="
echo ""
echo "Generated files:"
echo "  - quick_start_summary.csv              (Extracted data)"
echo "  - quick_start_results/population_analysis.png"
echo "  - quick_start_results/interesting_snids.txt"
echo "  - quick_start_plots/sample_*.png       (Individual events)"
echo "  - quick_start_plots/statistics.png     (Population summary)"
echo ""
echo "Next steps:"
echo "  1. Review the plots in quick_start_plots/"
echo "  2. Check interesting_snids.txt for noteworthy events"
echo "  3. Run full extraction with: ./extract_all_tfrecords.sh"
echo "  4. Explore the CSV data in Python/R"
echo ""
