# SCONE Tools

**Tools for analyzing and visualizing SCONE (Supernova Classification with Optimal Nearby Examples) TFRecord outputs**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/tensorflow-2.x-orange.svg)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This toolkit provides utilities to extract, analyze, and visualize supernova data from SCONE TFRecord heatmap files. Whether you're performing quality assurance, exploring classification results, or conducting detailed analysis, these tools make it easy to work with SCONE outputs.

## Features

- **📊 Data Extraction**: Convert TFRecord heatmaps to CSV with rich summary statistics
- **📈 Visualization**: Create comprehensive plots showing flux evolution, spectra, and light curves
- **🔍 Analysis**: Extract 40+ statistical features per supernova for downstream analysis
- **⚡ Performance**: Process millions of events efficiently
- **🎯 Flexible**: Sample randomly, plot specific events, or create statistical summaries

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/scone_tools.git
cd scone_tools
pip install -r requirements.txt
```

### Basic Usage

```bash
# Extract data from TFRecords to CSV
python extract_tfrecord_info.py --tfrecord heatmaps/heatmaps_0000.tfrecord --output summary.csv

# Visualize specific supernovae
python visualize_tfrecords.py --tfrecord heatmaps/heatmaps_0000.tfrecord --sample_ids 1009,1521,2034

# Create statistical summary plots
python visualize_tfrecords.py --tfrecord heatmaps/heatmaps_0000.tfrecord --statistics --stat_samples 1000
```

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

### 1. Quality Assurance

```bash
# Extract data and check for anomalies
./extract_all_tfrecords.sh qa_data
# Analyze CSV for low SNR, poor coverage, etc.
```

### 2. Classification Analysis

```python
import pandas as pd

# Load extracted data
df = pd.read_csv('summary.csv')

# Find misclassified events
interesting = df[df['snr_mean'] < 3.0]['snid'].tolist()

# Visualize them
# python visualize_tfrecords.py --tfrecord ... --sample_ids 1234,5678
```

### 3. Population Studies

```bash
# Compare SNIa vs Non-Ia distributions
./plot_statistics.sh 2000 population_stats
```

### 4. Individual Event Investigation

```bash
# Deep dive into specific supernovae
python visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0005.tfrecord \
    --sample_ids 12345,23456 \
    --output_dir investigation_plots
```

## Data Extraction Features

Each TFRecord event can be extracted with:

### Summary Statistics (40 columns)
- Basic metadata: SNID, label, redshift
- Flux statistics: total, max, mean, median, std
- Peak information: location, wavelength, time
- Light curve properties: rise/decline times, duration
- Spectral features: peak wavelength, color ratios
- Quality metrics: SNR, coverage statistics

### Optional Exports
- **Full Light Curves**: 180 time bins with flux and errors
- **Peak Spectra**: 32 wavelength bins with flux and errors

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

## SCONE Data Format

SCONE TFRecords contain 2D heatmaps with:
- **Shape**: (32 wavelengths, 180 time bins, 2 channels)
- **Wavelength range**: 3000-10100 Angstroms
- **Time range**: -50 to +130 days relative to peak
- **Channels**: [0] = flux, [1] = flux error
- **Metadata**: SNID, label (0=Non-Ia, 1=SNIa), redshift, redshift_error

See [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md) for full specifications.

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

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Citation

If you use these tools in your research, please cite the SCONE paper:

```bibtex
@article{scone2024,
  title={SCONE: Supernova Classification with Optimal Nearby Examples},
  author={Your Name et al.},
  journal={Journal Name},
  year={2024}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: See the `docs/` directory
- **Issues**: Please report bugs via GitHub Issues
- **Examples**: Check the `examples/` directory for usage patterns

## Acknowledgments

Developed for analyzing SCONE outputs on NERSC Perlmutter. Thanks to the DESC collaboration and LSST community.

---

**Happy analyzing!** 📊🔭
