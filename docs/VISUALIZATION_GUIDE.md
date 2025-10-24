# SCONE TFRecord Visualization - Quick Start Guide

## Location
All tools are now in: `~/soft/scone_tools/`

You can call them from any directory!

---

## Your Data

Each tfrecord file contains: **~47,000 events**
Total events across 40 files: **~1.9 million events**
Each plot: **~220 KB**

**⚠️ Plotting ALL events would create 395 GB of plots and take ~520 hours!**

---

## Recommended Workflows

### 1️⃣ Quick Sample (Best for exploration)

Sample a few events from each file:

```bash
cd /path/to/your/heatmaps/directory
~/soft/scone_tools/plot_samples.sh 10 my_sample_plots
```

This creates:
- 10 plots per tfrecord file
- 400 total plots (40 files × 10)
- ~86 MB total
- Takes ~7 minutes

**Adjust the sample size:**
```bash
~/soft/scone_tools/plot_samples.sh 5 quick_look    # 5 per file
~/soft/scone_tools/plot_samples.sh 20 detailed     # 20 per file
```

---

### 2️⃣ Statistical Summaries (Best for overview)

Create one summary plot per tfrecord file:

```bash
cd /path/to/your/heatmaps/directory
~/soft/scone_tools/plot_statistics.sh 1000 stats_plots
```

This creates:
- 1 statistics plot per tfrecord file
- 40 total plots
- ~16 MB total
- Takes ~80 minutes
- Each plot shows: mean flux, std dev, class distribution, redshifts, mean light curves, mean spectra

**Adjust statistics sample size:**
```bash
~/soft/scone_tools/plot_statistics.sh 500 quick_stats   # Faster, less accurate
~/soft/scone_tools/plot_statistics.sh 2000 detailed_stats  # Slower, more accurate
```

---

### 3️⃣ Specific Events (Best for investigation)

Plot specific SNIDs you're interested in:

```bash
cd /path/to/your/heatmaps/directory

# Single file, specific SNIDs
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --sample_ids 1009,1521,2209,5678

# Find events across multiple files
for f in heatmaps/heatmaps_*.tfrecord; do
    ~/soft/scone_tools/visualize_tfrecords.py \
        --tfrecord "$f" \
        --sample_ids 1009,1521 \
        --output_dir snid_search
done
```

**Use case:** After running SCONE predictions, check `predictions.csv` for:
- Low confidence predictions (near 0.5)
- Misclassifications
- High-redshift events
- Then plot those specific SNIDs

---

### 4️⃣ Single File in Detail

If you want to plot many events from one specific file:

```bash
cd /path/to/your/heatmaps/directory

# Plot first 100 events from one file
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --num_samples 100 \
    --output_dir file_0000_detail
```

**Note:** One file has 47k events. Even 1000 plots = 220 MB and takes ~17 minutes.

---

## Understanding File Names

### Plot Naming Convention

```
sample_0000_snid_1009.png
   │     │      │    │
   │     │      │    └─> SNID (Supernova ID from your data)
   │     │      └──────> Keyword identifier
   │     └─────────────> Sample index (order in tfrecord)
   └───────────────────> Prefix
```

- **Sample index**: Order the event appears in the tfrecord file (0, 1, 2, ...)
- **SNID**: Actual supernova identifier from your simulation/observations

### Example:
- `sample_0000_snid_1009.png` = First event in file, happens to be SNID 1009
- `sample_0001_snid_1521.png` = Second event in file, happens to be SNID 1521

The SNID is what matters for tracking specific supernovae!

---

## Common Use Cases

### Compare Ia vs CC populations

```bash
# In Ia directory
cd .../SCONE_PREDICT_BIASCOR_LSST_BIASCOR_Ia_DEBUG
~/soft/scone_tools/plot_statistics.sh 1000 ../comparison_ia

# In CC directory
cd ../SCONE_PREDICT_BIASCOR_LSST_BIASCOR_CC_COPY
~/soft/scone_tools/plot_statistics.sh 1000 ../comparison_cc

# Compare the statistics_*.png files
```

### Quality Assurance

```bash
# Quick visual check of each file
~/soft/scone_tools/plot_samples.sh 5 qa_plots
# Review plots for: gaps, artifacts, unusual patterns
```

### Find interesting events

```bash
# First, run statistics to understand distribution
~/soft/scone_tools/plot_statistics.sh 500 stats

# Then plot a few samples to see variety
~/soft/scone_tools/plot_samples.sh 10 samples

# If you find interesting SNIDs, plot them specifically
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0005.tfrecord \
    --sample_ids 1234,5678,9012
```

---

## Advanced Direct Usage

### Main Python script options:

```bash
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord PATH              # Required: path to .tfrecord file
    --num_samples N              # How many individual plots (default: 5)
    --sample_ids ID1,ID2         # Plot specific SNIDs (comma-separated)
    --statistics                 # Create statistical summary
    --stat_samples N             # Events for statistics (default: 100)
    --output_dir DIR             # Where to save plots (default: ./tfrecord_plots)
```

### Examples:

```bash
# Just statistics, no individual plots
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --statistics \
    --stat_samples 1000 \
    --num_samples 0

# Both statistics and samples
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --statistics \
    --stat_samples 1000 \
    --num_samples 20

# Large sample for detailed review (will take time!)
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --num_samples 500
```

---

## Viewing Plots

### Transfer to Local Machine

From your local computer:

```bash
scp -r perlmutter:/path/to/plots ./local_plots/
```

### Or use NERSC's Jupyter

If available, navigate to your plots directory in JupyterLab and view images there.

---

## What Each Plot Shows

### Individual Event Plots (5 panels):
1. **Flux Heatmap**: Wavelength vs Time, main visualization
2. **Error Heatmap**: Uncertainties across the spectrum
3. **Light Curve**: Total flux evolution over time
4. **Peak Spectrum**: Average spectrum near maximum (-10 to +20 days)
5. **SNR Map**: Signal-to-noise ratio (quality indicator)

### Statistics Plots (6 panels):
1. **Mean Flux**: Average heatmap across many samples
2. **Std Dev**: Variability in the data
3. **Class Distribution**: Bar chart of SNIa vs Non-Ia
4. **Redshift Distribution**: Histogram of redshifts
5. **Mean Light Curves by Class**: Compare SNIa vs Non-Ia evolution
6. **Mean Spectra by Class**: Compare spectral features

---

## Tips

✅ **Start small**: Use statistics or small samples first
✅ **Be selective**: Plot specific interesting events, not everything
✅ **Plan ahead**: Estimate time/size before large runs
✅ **Use parallel jobs**: If needed, split across slurm jobs

❌ **Don't plot all 1.9M events!** You'll never review them all
❌ **Don't run on login nodes** for large batches

---

## File Sizes Reference

| Number of Plots | Disk Space | Time Estimate |
|----------------|------------|---------------|
| 10 plots | 2.2 MB | 10 seconds |
| 100 plots | 22 MB | 2 minutes |
| 1,000 plots | 220 MB | 17 minutes |
| 10,000 plots | 2.2 GB | 3 hours |
| 47,000 plots (one file) | 10 GB | 13 hours |
| 1.9M plots (all files) | 395 GB | 520 hours ⚠️ |

---

## Getting Help

```bash
# View README
cat ~/soft/scone_tools/README.md

# View script help
~/soft/scone_tools/visualize_tfrecords.py --help

# This guide
cat ~/soft/scone_tools/USAGE_GUIDE.md
```

---

## Quick Command Reference

```bash
# Sample approach (recommended first step)
~/soft/scone_tools/plot_samples.sh 10 my_plots

# Statistics approach (good overview)
~/soft/scone_tools/plot_statistics.sh 1000 stats

# Specific SNIDs
~/soft/scone_tools/visualize_tfrecords.py \
    --tfrecord heatmaps/heatmaps_0000.tfrecord \
    --sample_ids 1009,1521,2209
```

Happy visualizing! 🔭
