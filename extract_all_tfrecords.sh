#!/bin/bash
# Extract information from all TFRecord files
# Usage: ./extract_all_tfrecords.sh [output_dir] [--full_lightcurves] [--full_spectra]

OUTPUT_DIR=${1:-"./tfrecord_extracted"}
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check for optional flags
EXTRA_FLAGS=""
for arg in "$@"; do
    if [ "$arg" = "--full_lightcurves" ] || [ "$arg" = "--full_spectra" ]; then
        EXTRA_FLAGS="$EXTRA_FLAGS $arg"
    fi
done

echo "=========================================="
echo "Extracting data from all TFRecord files"
echo "Output directory: ${OUTPUT_DIR}"
echo "Extra flags: ${EXTRA_FLAGS}"
echo "=========================================="

mkdir -p "${OUTPUT_DIR}"

count=0
total_events=0

for tfrecord in heatmaps/heatmaps_*.tfrecord; do
    if [ -f "$tfrecord" ]; then
        filename=$(basename "$tfrecord" .tfrecord)
        output_csv="${OUTPUT_DIR}/${filename}.csv"

        echo ""
        echo "[$(date +%H:%M:%S)] Processing ${filename}..."

        python3 "${SCRIPT_DIR}/extract_tfrecord_info.py" \
            --tfrecord "$tfrecord" \
            --output "$output_csv" \
            $EXTRA_FLAGS

        # Count events in this file
        if [ -f "$output_csv" ]; then
            events=$(wc -l < "$output_csv")
            events=$((events - 1))  # Subtract header
            total_events=$((total_events + events))
            echo "  ✓ Extracted ${events} events"
        fi

        count=$((count + 1))
    fi
done

echo ""
echo "=========================================="
echo "Done! Processed ${count} TFRecord files"
echo "Total events extracted: ${total_events}"
echo "CSV files saved to: ${OUTPUT_DIR}/"
echo "=========================================="

# Optionally combine all CSVs into one master file
echo ""
read -p "Combine all CSVs into one master file? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Combining CSV files..."
    master_csv="${OUTPUT_DIR}/all_events_combined.csv"

    # Use first file to get header
    first_file=$(ls ${OUTPUT_DIR}/heatmaps_*.csv | head -1)
    head -1 "$first_file" > "$master_csv"

    # Append all data (skip headers)
    for csv in ${OUTPUT_DIR}/heatmaps_*.csv; do
        tail -n +2 "$csv" >> "$master_csv"
    done

    combined_events=$(wc -l < "$master_csv")
    combined_events=$((combined_events - 1))
    echo "✓ Combined file created: $master_csv"
    echo "  Total events: ${combined_events}"
fi

echo ""
echo "All done!"
