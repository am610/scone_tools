# SCONE TFRecord Data Format

## Overview

SCONE (Supernova Classification with Optimal Nearby Examples) stores supernova observations as TensorFlow TFRecord files containing 2D heatmaps of spectral time series data.

## TFRecord Structure

### Input Shape

Each event is stored as a 3D array:
```
Shape: (NUM_WAVELENGTH_BINS, NUM_MJD_BINS, 2)
Default: (32, 180, 2)
```

- **Dimension 0**: Wavelength bins (32)
- **Dimension 1**: Time bins (180)
- **Dimension 2**: Channels (2)
  - Channel 0: Flux values
  - Channel 1: Flux errors

### Physical Parameters

| Parameter | Value | Units | Description |
|-----------|-------|-------|-------------|
| **Wavelength Min** | 3000 | Angstroms | Minimum wavelength |
| **Wavelength Max** | 10100 | Angstroms | Maximum wavelength |
| **Time Min** | -50 | days | Days before peak |
| **Time Max** | +130 | days | Days after peak |
| **Num Wavelength Bins** | 32 | - | Spectral resolution |
| **Num Time Bins** | 180 | - | Temporal resolution |

### Wavelength Bins

Wavelengths are evenly spaced in the rest frame:

```python
wavelengths = np.linspace(3000, 10100, 32)  # Angstroms
# Bin spacing: ~222 Angstroms
```

Example wavelength values:
```
[3000, 3222, 3444, 3667, 3889, 4111, ..., 9656, 9878, 10100]
```

### Time Bins

Time bins are evenly spaced relative to peak MJD:

```python
mjds = np.linspace(-50, 130, 180)  # days from peak
# Bin spacing: 1 day
```

Example time values:
```
[-50, -49, -48, ..., 0 (peak), ..., 128, 129, 130]
```

## TFRecord Features

Each TFRecord example contains the following features:

| Feature | Type | Description |
|---------|------|-------------|
| `image_raw` | bytes | Serialized float64 array of shape (32, 180, 2) |
| `id` | int64 | Supernova ID (SNID) |
| `label` | int64 | Classification label (0=Non-Ia, 1=SNIa) |
| `z` | float32 | Redshift |
| `z_err` | float32 | Redshift uncertainty |

### Reading TFRecords

```python
import tensorflow as tf
import numpy as np

def parse_tfrecord(raw_record):
    """Parse a single TFRecord example"""
    feature_description = {
        'label': tf.io.FixedLenFeature([], tf.int64),
        'image_raw': tf.io.FixedLenFeature([], tf.string),
        'id': tf.io.FixedLenFeature([], tf.int64),
        'z': tf.io.FixedLenFeature([], tf.float32),
        'z_err': tf.io.FixedLenFeature([], tf.float32),
    }

    example = tf.io.parse_single_example(raw_record, feature_description)
    image = tf.reshape(
        tf.io.decode_raw(example['image_raw'], tf.float64),
        (32, 180, 2)
    )

    return {
        'id': int(example['id'].numpy()),
        'label': int(example['label'].numpy()),
        'z': float(example['z'].numpy()),
        'z_err': float(example['z_err'].numpy()),
        'flux': image[:, :, 0].numpy(),  # (wavelength, mjd)
        'flux_err': image[:, :, 1].numpy()
    }

# Load dataset
dataset = tf.data.TFRecordDataset('heatmaps_0000.tfrecord')
for raw_record in dataset.take(1):
    data = parse_tfrecord(raw_record)
    print(f"SNID: {data['id']}")
    print(f"Label: {data['label']} ({'SNIa' if data['label'] == 1 else 'Non-Ia'})")
    print(f"Redshift: {data['z']:.4f} ± {data['z_err']:.4f}")
    print(f"Flux shape: {data['flux'].shape}")  # (32, 180)
```

## Flux Values

### Units

Flux values are typically in physical units of:
- **erg/s/cm²/Angstrom** (spectroscopic flux density)

Or normalized/scaled for machine learning purposes.

### Interpretation

- **Positive flux**: Detected emission
- **Zero flux**: No observation or masked data
- **Negative flux**: Possible (background subtraction artifacts)

### Error Values

Flux errors represent 1-sigma uncertainties in the same units as flux.

## Heatmap Coordinate System

### Array Indexing

```python
flux[wavelength_idx, time_idx]
```

- `wavelength_idx`: 0 to 31 (blue to red)
- `time_idx`: 0 to 179 (early to late)

### Example Access

```python
# Get flux at specific wavelength and time
wavelength_idx = 15  # ~5500 Angstroms
time_idx = 50        # Day 0 (peak)
flux_value = data['flux'][wavelength_idx, time_idx]

# Get full light curve (all times, one wavelength)
light_curve_5500A = data['flux'][15, :]

# Get full spectrum at peak (all wavelengths, one time)
peak_spectrum = data['flux'][:, 50]

# Get wavelength-integrated light curve
total_light_curve = np.sum(data['flux'], axis=0)
```

## Data Quality Indicators

### Coverage

Not all bins contain observations:

```python
# Check data coverage
has_data = flux > 0
coverage_fraction = np.sum(has_data) / flux.size

# Temporal coverage
has_data_per_time = np.any(flux > 0, axis=0)
temporal_coverage = np.sum(has_data_per_time) / len(has_data_per_time)

# Spectral coverage
has_data_per_wavelength = np.any(flux > 0, axis=1)
spectral_coverage = np.sum(has_data_per_wavelength) / len(has_data_per_wavelength)
```

### Signal-to-Noise

```python
snr = np.where(flux_err > 0, flux / flux_err, 0)
mean_snr = np.mean(snr[snr > 0])
```

## Label Definitions

| Label | Value | Description |
|-------|-------|-------------|
| **Non-Ia** | 0 | Non-Type Ia supernova (core collapse, etc.) |
| **SNIa** | 1 | Type Ia supernova |

For binary classification, label=1 is typically the "positive" class (SNIa).

## File Naming Convention

Typical SCONE output structure:

```
heatmaps/
├── heatmaps_0000.tfrecord  # First shard
├── heatmaps_0001.tfrecord  # Second shard
├── ...
└── heatmaps_0039.tfrecord  # Last shard (example with 40 files)
```

Each file typically contains ~40,000-50,000 events, depending on the dataset size and sharding strategy.

## Coordinate Transformations

### Index to Physical Units

```python
import numpy as np

# Configuration
NUM_WAVELENGTH_BINS = 32
NUM_MJD_BINS = 180
WAVELENGTH_MIN = 3000
WAVELENGTH_MAX = 10100
MJD_RANGE_START = -50
MJD_RANGE_END = 130

# Create coordinate arrays
wavelengths = np.linspace(WAVELENGTH_MIN, WAVELENGTH_MAX, NUM_WAVELENGTH_BINS)
mjds = np.linspace(MJD_RANGE_START, MJD_RANGE_END, NUM_MJD_BINS)

# Convert index to physical value
def idx_to_wavelength(idx):
    return wavelengths[idx]

def idx_to_mjd(idx):
    return mjds[idx]

# Convert physical value to index
def wavelength_to_idx(wave):
    return np.argmin(np.abs(wavelengths - wave))

def mjd_to_idx(mjd):
    return np.argmin(np.abs(mjds - mjd))
```

### Example Usage

```python
# Find flux at 6000 Angstroms, 10 days after peak
wave_idx = wavelength_to_idx(6000)
time_idx = mjd_to_idx(10)
flux_at_6000A_day10 = data['flux'][wave_idx, time_idx]

# Get spectrum near peak (-10 to +20 days)
peak_start = mjd_to_idx(-10)
peak_end = mjd_to_idx(20)
peak_spectrum = np.mean(data['flux'][:, peak_start:peak_end], axis=1)
```

## Typical Data Characteristics

### Type Ia Supernovae (label=1)

- **Light curve**: Sharp rise (~15-20 days), slower decline
- **Peak wavelength**: Blue early, red later
- **Spectral features**: Si II (6150Å), S II lines
- **Duration**: Visible for 100+ days
- **Redshift range**: Typically z < 1.2 for LSST

### Non-Ia Supernovae (label=0)

- **Light curve**: Variable (depends on subtype)
- **Spectral features**: Hydrogen lines (Type II), helium (Type Ib/c)
- **Duration**: Can be shorter or longer than SNIa
- **Diversity**: Much more heterogeneous class

## Memory Requirements

### Per Event

```
Size = 32 × 180 × 2 × 8 bytes (float64) = 92,160 bytes ≈ 90 KB
Plus metadata: ~100 KB per event
```

### Per File

```
~47,000 events × 100 KB ≈ 4.7 GB per file (uncompressed)
TFRecord compression reduces this to ~170 MB to 4 GB depending on data
```

### Full Dataset (40 files)

```
40 files × 47,000 events = 1,880,000 events total
Storage: ~7-160 GB (depending on compression)
```

## Related Tools

This data format is read by:
- `extract_tfrecord_info.py` - Converts to CSV
- `visualize_tfrecords.py` - Creates plots
- SCONE training/prediction scripts

## References

- TensorFlow TFRecord format: https://www.tensorflow.org/tutorials/load_data/tfrecord
- SCONE paper: [Add citation when published]

---

For practical examples of working with this data format, see:
- [EXTRACTION_GUIDE.md](EXTRACTION_GUIDE.md)
- [VISUALIZATION_GUIDE.md](VISUALIZATION_GUIDE.md)
