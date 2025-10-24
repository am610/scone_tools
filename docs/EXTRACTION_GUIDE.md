# TFRecord Data Extraction to CSV - Complete Guide

## Overview

- **One row per SNID** with 40+ summary columns

---

## Quick Start

### Extract Summary Statistics (Recommended First Step)

```bash
cd /path/to/your/heatmaps/directory

# Single file
~/soft/scone_tools/extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output info_0000.csv

# All files at once
~/soft/scone_tools/extract_all_tfrecords.sh extracted_data
```

---

## What Gets Extracted

### Summary CSV (40 columns per SNID)

**Basic Metadata:**
- `snid` - Supernova ID
- `label` - Classification (0=Non-Ia, 1=SNIa)
- `label_name` - Human-readable label
- `redshift`, `redshift_err` - Redshift and uncertainty

**Flux Statistics:**
- `total_flux` - Sum of all flux
- `max_flux` - Peak flux value
- `mean_flux`, `median_flux`, `std_flux` - Distribution statistics

**Peak Information:**
- `peak_flux_wavelength` - Wavelength of maximum flux (Angstroms)
- `peak_flux_mjd` - Time of maximum flux (days from peak)
- `peak_flux_wavelength_idx`, `peak_flux_mjd_idx` - Grid indices

**Light Curve Properties:**
- `lc_max` - Maximum of wavelength-integrated light curve
- `lc_mean` - Mean light curve value
- `lc_peak_mjd` - Time of peak brightness
- `flux_before_peak`, `flux_after_peak` - Flux distribution
- `rise_time_days` - Time from half-max to peak
- `decline_time_days` - Time from peak to half-max
- `duration_days` - Total duration above half-max

**Spectrum Properties (averaged -10 to +20 days):**
- `spectrum_max` - Peak spectral flux
- `spectrum_mean` - Mean spectral flux
- `spectrum_peak_wavelength` - Wavelength of peak (Angstroms)

**Color Information:**
- `blue_flux` - Flux in 3000-5000 Å range
- `red_flux` - Flux in 6000-10000 Å range
- `color_ratio` - Blue/red flux ratio

**Signal-to-Noise:**
- `snr_mean`, `snr_median` - Average SNR
- `snr_max` - Maximum SNR
- `snr_peak` - SNR at flux peak

**Data Coverage:**
- `num_nonzero_bins` - Number of filled heatmap bins
- `coverage_fraction` - Fraction of heatmap with data
- `num_epochs_with_data` - Time bins with observations
- `temporal_coverage_fraction` - Fraction of time covered
- `num_wavelengths_with_data` - Wavelength bins with data
- `spectral_coverage_fraction` - Fraction of spectrum covered

### Optional: Full Light Curves CSV

Add `--full_lightcurves` flag to get:
- `snid` - Supernova ID
- `mjd_000` to `mjd_179` - Time values (days from peak)
- `flux_000` to `flux_179` - Flux at each epoch
- `flux_err_000` to `flux_err_179` - Uncertainties

**Total: 541 columns (1 + 180×3)**

### Optional: Full Spectra CSV

Add `--full_spectra` flag to get:
- `snid` - Supernova ID
- `wavelength_00` to `wavelength_31` - Wavelengths (Angstroms)
- `flux_00` to `flux_31` - Flux at each wavelength
- `flux_err_00` to `flux_err_31` - Uncertainties

**Total: 97 columns (1 + 32×3)**

---

## Usage Examples

### 1. Extract from Single File

```bash
# Summary only
~/soft/scone_tools/extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output info.csv

# With light curves
~/soft/scone_tools/extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output info.csv \
    --full_lightcurves

# With spectra
~/soft/scone_tools/extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output info.csv \
    --full_spectra

# Everything
~/soft/scone_tools/extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output info.csv \
    --full_lightcurves \
    --full_spectra
```

### 2. Extract from All Files

```bash
cd /path/to/heatmaps/directory

# Summary only (recommended)
~/soft/scone_tools/extract_all_tfrecords.sh extracted_data

# With light curves
~/soft/scone_tools/extract_all_tfrecords.sh extracted_data --full_lightcurves

# With spectra
~/soft/scone_tools/extract_all_tfrecords.sh extracted_data --full_spectra

# Everything
~/soft/scone_tools/extract_all_tfrecords.sh extracted_data --full_lightcurves --full_spectra
```

This creates one CSV per tfrecord file, then optionally combines them.

### 3. Test on Small Sample

```bash
# Test on first 100 events
~/soft/scone_tools/extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output test.csv \
    --limit 100
```

---

## Size and Time Estimates

| Mode | Total Size | Time | Per File |
|------|-----------|------|----------|
| **Summary only** | 1.0 GB | ~13 hours | 26 MB, ~20 min |
| **+ Light curves** | 19.4 GB | ~16 hours | 485 MB, ~24 min |
| **+ Spectra** | 4.4 GB | ~16 hours | 110 MB, ~24 min |
| **Everything** | 22.8 GB | ~19 hours | 570 MB, ~28 min |

**Comparison:**
- Plots: 395 GB, ~520 hours
- CSVs: 1-23 GB, ~13-19 hours
- **17-28x more efficient!**

---

## Analyzing the Extracted Data

### Using Pandas

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load summary data
df = pd.read_csv('info.csv')

# Basic exploration
print(df.describe())
print(df.groupby('label_name').mean())

# Plot redshift distribution
df['redshift'].hist(bins=50)
plt.xlabel('Redshift')
plt.ylabel('Count')
plt.title('Redshift Distribution')
plt.show()

# Find interesting events
high_z = df[df['redshift'] > 1.0]
low_snr = df[df['snr_mean'] < 3.0]
fast_risers = df[df['rise_time_days'] < 10]

# Compare Ia vs Non-Ia
ia = df[df['label'] == 1]
non_ia = df[df['label'] == 0]

print(f"SNIa mean rise time: {ia['rise_time_days'].mean():.1f} days")
print(f"Non-Ia mean rise time: {non_ia['rise_time_days'].mean():.1f} days")

# Load light curves for specific SNID
lc_df = pd.read_csv('info_lightcurves.csv')
snid_1009 = lc_df[lc_df['snid'] == 1009]
# Extract flux columns
flux_cols = [c for c in snid_1009.columns if c.startswith('flux_')]
mjd_cols = [c for c in snid_1009.columns if c.startswith('mjd_')]
fluxes = snid_1009[flux_cols].values[0]
mjds = snid_1009[mjd_cols].values[0]
plt.plot(mjds, fluxes)
plt.show()
```

### Using R

```r
library(tidyverse)

# Load data
df <- read_csv("info.csv")

# Explore
summary(df)
df %>% group_by(label_name) %>% summarize(across(where(is.numeric), mean))

# Plot
ggplot(df, aes(x=redshift, fill=label_name)) +
  geom_histogram(bins=50, alpha=0.6, position="identity") +
  labs(title="Redshift Distribution by Type")

# Compare populations
df %>%
  group_by(label_name) %>%
  summarize(
    mean_rise = mean(rise_time_days, na.rm=TRUE),
    mean_decline = mean(decline_time_days, na.rm=TRUE),
    mean_snr = mean(snr_mean, na.rm=TRUE)
  )
```

### Using Excel

1. Open CSV in Excel/LibreOffice
2. Use pivot tables to summarize by class
3. Create charts from the columns
4. Filter for interesting events
5. Export selected SNIDs for visualization

---

## Recommended Workflows

### Workflow 1: Initial Exploration

```bash
# Extract summary for all files (~13 hours, 1 GB)
~/soft/scone_tools/extract_all_tfrecords.sh extracted_summary

# Analyze in Python/R to find interesting events
# (See analysis examples above)

# Then plot only interesting SNIDs
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0005.tfrecord \
    --sample_ids 1234,5678,9012
```

### Workflow 2: Complete Data Export

```bash
# Extract everything for detailed analysis
~/soft/scone_tools/extract_all_tfrecords.sh complete_export --full_lightcurves --full_spectra

# Analyze, filter, and export subsets for further study
```

### Workflow 3: Compare Ia vs CC

```bash
# In Ia directory
cd /path/to/Ia/heatmaps/
~/soft/scone_tools/extract_all_tfrecords.sh ../extracted_ia

# In CC directory
cd /path/to/CC/heatmaps/
~/soft/scone_tools/extract_all_tfrecords.sh ../extracted_cc

# Load both in pandas and compare
```

### Workflow 4: Quality Assurance

```bash
# Extract summaries
~/soft/scone_tools/extract_all_tfrecords.sh qa_data

# Check for:
# - Low SNR events (snr_mean < 3)
# - Poor coverage (coverage_fraction < 0.3)
# - Unusual light curve shapes (very short/long durations)
# - Outlier redshifts

# Plot suspicious events for visual inspection
```

---

## Output Files

After running `extract_all_tfrecords.sh extracted_data`:

```
extracted_data/
├── heatmaps_0000.csv              # Summary for file 0
├── heatmaps_0001.csv              # Summary for file 1
├── ...
├── heatmaps_0039.csv              # Summary for file 39
└── all_events_combined.csv        # Combined summary (optional)
```

With `--full_lightcurves`:
```
extracted_data/
├── heatmaps_0000.csv
├── heatmaps_0000_lightcurves.csv  # Light curves for file 0
├── ...
```

With `--full_spectra`:
```
extracted_data/
├── heatmaps_0000.csv
├── heatmaps_0000_spectra.csv      # Spectra for file 0
├── ...
```

---

## Tips and Best Practices

✅ **Start with summary only** - Contains rich information, only 1 GB
✅ **Extract to fast filesystem** - Use /pscratch for best I/O performance
✅ **Use combined CSV** - Easier to analyze than 40 separate files
✅ **Filter before plotting** - Identify interesting SNIDs in CSV, then plot them
✅ **Submit as job** - For large extractions, use slurm batch job

❌ **Don't extract on login nodes** - Use compute nodes for large jobs
❌ **Don't load all light curves at once** - 19 GB can fill memory

---

## Slurm Job Example

For large extractions, submit as a batch job:

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -c 10
#SBATCH -t 24:00:00
#SBATCH -J extract_tfrecords
#SBATCH -o extract_%j.out

cd /pscratch/sd/.../heatmaps/
~/soft/scone_tools/extract_all_tfrecords.sh extracted_data --full_lightcurves --full_spectra
```

---

## Help and Documentation

```bash
# Script help
~/soft/scone_tools/extract_tfrecord_info.py --help

# View this guide
cat ~/soft/scone_tools/EXTRACTION_GUIDE.md

# Test on small sample
~/soft/scone_tools/extract_tfrecord_info.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --output test.csv \
    --limit 100
```

---

## Troubleshooting

**Slow extraction:** Normal - processing 1.9M events takes time. Submit as batch job.

**Out of memory:** Don't use `--limit` too high when testing. Process full files in batch mode.

**CSV too large for Excel:** Use Python/R or split into chunks. Excel has 1M row limit.

**Missing columns:** Check TFRecord format matches SCONE expectations (32×180×2 shape).

---

## Summary

CSV extraction is the **best way to explore your TFRecord data**:

1. Fast and efficient (17-28x better than plotting)
2. Rich information (40+ columns per event)
3. Easy to analyze with standard tools
4. Can still plot interesting events later

**Recommended approach:**
1. Extract summaries for all files (~13 hours, 1 GB)
2. Analyze in pandas/R to understand your data
3. Identify interesting events
4. Plot only those specific SNIDs

Happy analyzing! 📊
