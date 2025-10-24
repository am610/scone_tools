#!/bin/bash
# Create statistical summary plots from all tfrecord files
# Usage: ./plot_statistics.sh [num_events_to_sample] [output_dir]

NUM_EVENTS=${1:-500}  # Default 500 events for statistics
OUTPUT_DIR=${2:-"./statistics_plots"}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=========================================="
echo "Creating statistics from ${NUM_EVENTS} events per file"
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
            --statistics \
            --stat_samples "${NUM_EVENTS}" \
            --num_samples 0 \
            --output_dir "${OUTPUT_DIR}"

        # Rename the statistics.png to include the file name
        if [ -f "${OUTPUT_DIR}/statistics.png" ]; then
            mv "${OUTPUT_DIR}/statistics.png" "${OUTPUT_DIR}/statistics_${filename}.png"
        fi

        count=$((count + 1))
    fi
done

echo ""
echo "=========================================="
echo "Done! Created statistics from ${count} tfrecord files"
echo "Plots saved to: ${OUTPUT_DIR}/"
echo "=========================================="
