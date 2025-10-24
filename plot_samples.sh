#!/bin/bash
# Quick script to plot sample events from tfrecord files
# Usage: ./plot_samples.sh [num_samples_per_file] [output_dir]

NUM_SAMPLES=${1:-10}  # Default 10 samples per file
OUTPUT_DIR=${2:-"./sample_plots"}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=========================================="
echo "Plotting ${NUM_SAMPLES} samples per tfrecord file"
echo "Output: ${OUTPUT_DIR}"
echo "=========================================="

mkdir -p "${OUTPUT_DIR}"

count=0
for tfrecord in heatmaps/heatmaps_*.tfrecord; do
    if [ -f "$tfrecord" ]; then
        filename=$(basename "$tfrecord" .tfrecord)
        echo ""
        echo "Processing ${filename}..."

        python3 "${SCRIPT_DIR}/visualize_tfrecords.py" \
            --tfrecord "$tfrecord" \
            --num_samples "${NUM_SAMPLES}" \
            --output_dir "${OUTPUT_DIR}/${filename}"

        count=$((count + 1))
    fi
done

echo ""
echo "=========================================="
echo "Done! Processed ${count} tfrecord files"
echo "Plots saved to: ${OUTPUT_DIR}/"
echo "=========================================="
