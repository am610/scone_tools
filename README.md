# SCONE Tools

**Tools for analyzing and visualizing SCONE (Supernova Classification with Optimal Nearby Examples) TFRecord outputs**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/tensorflow-2.x-orange.svg)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This toolkit provides utilities to extract, analyze, and visualize supernova data from SCONE TFRecord heatmap files. Whether exploring classification results, or examining SN candidates, these can make it easy to work with SCONE outputs.
We can either make plots from the heatmap files, or extract csv files from the information in the TFrecord files.

## Features

- **📊 Data Extraction**: Convert TFRecord heatmaps to CSV with summary statistics
- **📈 Visualization**: Create comprehensive plots showing light curves etc.
- **⚡ Performance**: Can process millions of events (but I dont recommend ! )
- **🎯 Flexible**: Sample randomly, plot specific events, or create statistical summaries

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/scone_tools.git
cd scone_tools
pip install -r requirements.txt
```
If you are on perlmutter and if scone runs in your environment without problem then you need not do anything else. 

### Basic Usage

```bash
# Extract data from TFRecords to CSV
python extract_tfrecord_info.py --tfrecord heatmaps/heatmaps_0000.tfrecord --output summary.csv

# Visualize specific supernovae by snids
python visualize_tfrecords.py --tfrecord heatmaps/heatmaps_0000.tfrecord --sample_ids 1009,1521,2034

# Create statistical summary plots of 1000 events
python visualize_tfrecords.py --tfrecord heatmaps/heatmaps_0000.tfrecord --statistics --stat_samples 1000
```
<img width="2041" height="1401" alt="sample_0001_snid_309" src="https://github.com/user-attachments/assets/5294a7a1-8749-4567-82e2-ca2baf5962cd" />



## What's Included

### Core Scripts

| Tool | Purpose |
|------|---------|
| `extract_tfrecord_info.py` | Extract TFRecord data to CSV format |
| `visualize_tfrecords.py` | Create heatmap visualizations |
| `extract_all_tfrecords.sh` | Batch process multiple TFRecord files |
| `plot_samples.sh` | Sample and plot events from all files |
| `plot_statistics.sh` | Create statistical summaries for all files |

### Documentation

| Document | Contents |
|----------|----------|
| `docs/EXTRACTION_GUIDE.md` | Detailed guide for data extraction |
| `docs/VISUALIZATION_GUIDE.md` | How to create and interpret plots |
| `docs/DATA_FORMAT.md` | TFRecord structure and output specifications |

## Use Cases

### Individual Event Investigation

```bash
# Deep dive into specific supernovae
python visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0005.tfrecord \
    --sample_ids 12345,23456 \
    --output_dir investigation_plots
```

## Data Extraction Features

Each TFRecord event can be extracted with:

### Summary Statistics 
- Basic metadata: SNID, label, redshift
- Flux statistics: total, max, mean, median, std
- Peak information: location, wavelength, time
- Light curve properties: rise/decline times, duration
- Spectral features: peak wavelength, color ratios
- Quality metrics: SNR, coverage statistics etc.

### Optional Exports
- **Full Light Curves**:
- **Peak Spectra**: 
See [docs/EXTRACTION_GUIDE.md](docs/EXTRACTION_GUIDE.md) for details.

## Visualization Capabilities

### Individual Event Plots (5 panels)
1. **Flux Heatmap**: Wavelength vs Time showing spectral evolution
2. **Error Heatmap**: Uncertainty distribution
3. **Light Curve**: Integrated flux over time
4. **Peak Spectrum**: Time-averaged spectrum near maximum
5. **SNR Map**: Signal-to-noise quality indicator

### Statistical Summary Plots (6 panels)
1. **Mean Flux**: Average heatmap across samples
2. **Std Deviation**: Variability in the population
3. **Class Distribution**: SNIa vs Non-Ia counts
4. **Redshift Distribution**: Histogram of redshifts
5. **Mean Light Curves by Class**: Compare evolution
6. **Mean Spectra by Class**: Compare spectral features

See [docs/VISUALIZATION_GUIDE.md](docs/VISUALIZATION_GUIDE.md) for details.

## Examples

### Example 1: Quick Exploration

```bash
# Sample 10 events from each TFRecord file
./plot_samples.sh 10 sample_plots

# Create statistical summaries
./plot_statistics.sh 1000 stats
```

### Example 2: Full Data Extraction

```bash
# Extract complete dataset with light curves
./extract_all_tfrecords.sh complete_data --full_lightcurves

# Analyze in Python
python examples/analyze_population.py complete_data/all_events_combined.csv
```

### Example 3: Investigate Specific Events

```bash
# Find interesting events from SCONE predictions
python examples/find_interesting_events.py predictions.csv

# Visualize them
python visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --sample_ids $(cat interesting_snids.txt)
```

## Performance

| Operation | Output Size | Time | Notes |
|-----------|------------|------|-------|
| Extract summaries (40 files) | ~1 GB | ~13 hrs | Most efficient for analysis |
| Extract + light curves | ~19 GB | ~16 hrs | Full time series data |
| Sample plots (10/file) | ~86 MB | ~7 min | Good for QA |
| Statistics (1000/file) | ~16 MB | ~80 min | Population overview |

## Requirements

- Python 3.7+
- TensorFlow 2.x
- NumPy
- Pandas
- Matplotlib

See [requirements.txt](requirements.txt) for complete dependencies.


More examples are kept in Perlmutter: 
`$PIPPIN_OUTPUT/LSST_ANALYSIS-2/Other/3_CLAS_BACKUP/SCONE_PREDICT_BIASCOR_LSST_BIASCOR_Ia_DEBUG/`


Developed for analyzing SCONE outputs on NERSC Perlmutter. 
