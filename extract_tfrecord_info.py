#!/usr/bin/env python3
"""
Extract information from SCONE TFRecord files to CSV

This script reads TFRecord files and extracts metadata and summary statistics
for each supernova event, saving to CSV files. Much faster than creating plots!

Usage:
    python extract_tfrecord_info.py --tfrecord heatmaps_0000.tfrecord --output info.csv
    python extract_tfrecord_info.py --tfrecord heatmaps_0000.tfrecord --output info.csv --full_lightcurves
    python extract_tfrecord_info.py --tfrecord heatmaps_0000.tfrecord --output info.csv --full_spectra
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import argparse
import os
import sys
from pathlib import Path

# Configuration from SCONE
NUM_WAVELENGTH_BINS = 32
NUM_MJD_BINS = 180
INPUT_SHAPE = (NUM_WAVELENGTH_BINS, NUM_MJD_BINS, 2)

# Physical parameters
WAVELENGTH_MIN = 3000  # Angstroms
WAVELENGTH_MAX = 10100
MJD_RANGE_START = -50  # days relative to peak
MJD_RANGE_END = 130

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
    image = tf.reshape(tf.io.decode_raw(example['image_raw'], tf.float64), INPUT_SHAPE)

    return {
        'id': int(example['id'].numpy()),
        'label': int(example['label'].numpy()),
        'z': float(example['z'].numpy()),
        'z_err': float(example['z_err'].numpy()),
        'flux': image[:, :, 0].numpy(),  # (wavelength, mjd)
        'flux_err': image[:, :, 1].numpy()
    }

def get_wavelength_array():
    """Get wavelength bin centers in Angstroms"""
    return np.linspace(WAVELENGTH_MIN, WAVELENGTH_MAX, NUM_WAVELENGTH_BINS)

def get_mjd_array():
    """Get MJD bin centers in days relative to peak"""
    return np.linspace(MJD_RANGE_START, MJD_RANGE_END, NUM_MJD_BINS)

def extract_summary_statistics(data):
    """Extract summary statistics from a single event"""

    flux = data['flux']
    flux_err = data['flux_err']

    # Basic metadata
    info = {
        'snid': data['id'],
        'label': data['label'],
        'label_name': 'SNIa' if data['label'] == 1 else 'Non-Ia',
        'redshift': data['z'],
        'redshift_err': data['z_err'],
    }

    # Overall flux statistics
    info['total_flux'] = np.sum(flux)
    info['max_flux'] = np.max(flux)
    info['mean_flux'] = np.mean(flux)
    info['median_flux'] = np.median(flux)
    info['std_flux'] = np.std(flux)

    # Peak statistics
    peak_flux_idx = np.unravel_index(np.argmax(flux), flux.shape)
    info['peak_flux_wavelength_idx'] = peak_flux_idx[0]
    info['peak_flux_mjd_idx'] = peak_flux_idx[1]

    wavelengths = get_wavelength_array()
    mjds = get_mjd_array()
    info['peak_flux_wavelength'] = wavelengths[peak_flux_idx[0]]
    info['peak_flux_mjd'] = mjds[peak_flux_idx[1]]

    # Light curve statistics (flux summed over all wavelengths)
    light_curve = np.sum(flux, axis=0)
    info['lc_max'] = np.max(light_curve)
    info['lc_mean'] = np.mean(light_curve)
    info['lc_peak_mjd_idx'] = np.argmax(light_curve)
    info['lc_peak_mjd'] = mjds[np.argmax(light_curve)]

    # Pre-peak vs post-peak flux
    peak_idx = np.argmax(light_curve)
    info['flux_before_peak'] = np.sum(light_curve[:peak_idx]) if peak_idx > 0 else 0
    info['flux_after_peak'] = np.sum(light_curve[peak_idx:]) if peak_idx < len(light_curve) else 0

    # Rise and decline time (rough estimates based on half-max)
    half_max = info['lc_max'] / 2.0
    above_half = light_curve > half_max
    if np.any(above_half):
        first_half_idx = np.where(above_half)[0][0]
        last_half_idx = np.where(above_half)[0][-1]
        info['rise_time_days'] = mjds[peak_idx] - mjds[first_half_idx]
        info['decline_time_days'] = mjds[last_half_idx] - mjds[peak_idx]
        info['duration_days'] = mjds[last_half_idx] - mjds[first_half_idx]
    else:
        info['rise_time_days'] = np.nan
        info['decline_time_days'] = np.nan
        info['duration_days'] = np.nan

    # Spectrum statistics (time-averaged near peak: -10 to +20 days)
    mjd_array = get_mjd_array()
    peak_start_idx = np.argmin(np.abs(mjd_array - (-10)))
    peak_end_idx = np.argmin(np.abs(mjd_array - 20))

    peak_spectrum = np.mean(flux[:, peak_start_idx:peak_end_idx], axis=1)
    info['spectrum_max'] = np.max(peak_spectrum)
    info['spectrum_mean'] = np.mean(peak_spectrum)
    info['spectrum_peak_wavelength_idx'] = np.argmax(peak_spectrum)
    info['spectrum_peak_wavelength'] = wavelengths[np.argmax(peak_spectrum)]

    # Color information (approximate using wavelength ranges)
    # Blue: 3000-5000 Å, Red: 6000-10000 Å
    blue_idx = (wavelengths >= 3000) & (wavelengths <= 5000)
    red_idx = (wavelengths >= 6000) & (wavelengths <= 10000)

    if np.any(blue_idx) and np.any(red_idx):
        blue_flux = np.sum(light_curve * np.sum(flux[blue_idx, :], axis=0))
        red_flux = np.sum(light_curve * np.sum(flux[red_idx, :], axis=0))
        info['blue_flux'] = blue_flux
        info['red_flux'] = red_flux
        info['color_ratio'] = blue_flux / red_flux if red_flux > 0 else np.nan
    else:
        info['blue_flux'] = np.nan
        info['red_flux'] = np.nan
        info['color_ratio'] = np.nan

    # Signal-to-noise statistics
    snr = np.where(flux_err > 0, flux / flux_err, 0)
    info['snr_mean'] = np.mean(snr[snr > 0]) if np.any(snr > 0) else 0
    info['snr_median'] = np.median(snr[snr > 0]) if np.any(snr > 0) else 0
    info['snr_max'] = np.max(snr)
    info['snr_peak'] = snr[peak_flux_idx[0], peak_flux_idx[1]]

    # Data coverage statistics
    non_zero_flux = flux > 0
    info['num_nonzero_bins'] = np.sum(non_zero_flux)
    info['coverage_fraction'] = np.sum(non_zero_flux) / flux.size

    # Temporal coverage
    has_data_per_time = np.any(flux > 0, axis=0)
    info['num_epochs_with_data'] = np.sum(has_data_per_time)
    info['temporal_coverage_fraction'] = np.sum(has_data_per_time) / len(has_data_per_time)

    # Spectral coverage
    has_data_per_wavelength = np.any(flux > 0, axis=1)
    info['num_wavelengths_with_data'] = np.sum(has_data_per_wavelength)
    info['spectral_coverage_fraction'] = np.sum(has_data_per_wavelength) / len(has_data_per_wavelength)

    return info

def extract_lightcurve(data):
    """Extract full light curve (flux summed over wavelengths)"""
    light_curve = np.sum(data['flux'], axis=0)
    light_curve_err = np.sqrt(np.sum(data['flux_err']**2, axis=0))
    mjds = get_mjd_array()

    lc_dict = {
        'snid': data['id'],
    }

    for i, (mjd, flux, flux_err) in enumerate(zip(mjds, light_curve, light_curve_err)):
        lc_dict[f'mjd_{i:03d}'] = mjd
        lc_dict[f'flux_{i:03d}'] = flux
        lc_dict[f'flux_err_{i:03d}'] = flux_err

    return lc_dict

def extract_spectrum(data):
    """Extract peak spectrum (time-averaged near peak)"""
    mjd_array = get_mjd_array()
    peak_start_idx = np.argmin(np.abs(mjd_array - (-10)))
    peak_end_idx = np.argmin(np.abs(mjd_array - 20))

    spectrum = np.mean(data['flux'][:, peak_start_idx:peak_end_idx], axis=1)
    spectrum_err = np.sqrt(np.mean(data['flux_err'][:, peak_start_idx:peak_end_idx]**2, axis=1))
    wavelengths = get_wavelength_array()

    spec_dict = {
        'snid': data['id'],
    }

    for i, (wave, flux, flux_err) in enumerate(zip(wavelengths, spectrum, spectrum_err)):
        spec_dict[f'wavelength_{i:02d}'] = wave
        spec_dict[f'flux_{i:02d}'] = flux
        spec_dict[f'flux_err_{i:02d}'] = flux_err

    return spec_dict

def process_tfrecord(tfrecord_path, output_csv, full_lightcurves=False, full_spectra=False,
                     limit=None, verbose=True):
    """
    Process a TFRecord file and extract information to CSV

    Parameters:
    -----------
    tfrecord_path : str
        Path to TFRecord file
    output_csv : str
        Output CSV file path
    full_lightcurves : bool
        If True, also save full light curves to separate CSV
    full_spectra : bool
        If True, also save peak spectra to separate CSV
    limit : int or None
        Limit number of events to process (for testing)
    verbose : bool
        Print progress information
    """

    if verbose:
        print(f"Processing: {tfrecord_path}")
        print(f"Output: {output_csv}")

    dataset = tf.data.TFRecordDataset(tfrecord_path)

    if limit:
        dataset = dataset.take(limit)

    # Collect all data
    summary_data = []
    lightcurve_data = [] if full_lightcurves else None
    spectrum_data = [] if full_spectra else None

    count = 0
    for raw_record in dataset:
        data = parse_tfrecord(raw_record)

        # Extract summary statistics
        summary_data.append(extract_summary_statistics(data))

        # Extract full light curve if requested
        if full_lightcurves:
            lightcurve_data.append(extract_lightcurve(data))

        # Extract spectrum if requested
        if full_spectra:
            spectrum_data.append(extract_spectrum(data))

        count += 1
        if verbose and count % 1000 == 0:
            print(f"  Processed {count} events...")

    if verbose:
        print(f"  Total events processed: {count}")

    # Save summary statistics
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv(output_csv, float_format="%.3f",index=False,sep=' ')
    if verbose:
        print(f"  Saved summary to: {output_csv}")
        print(f"  Columns: {len(df_summary.columns)}")
        print(f"  Rows: {len(df_summary)}")

    # Save light curves if requested
    if full_lightcurves and lightcurve_data:
        lc_output = output_csv.replace('.csv', '_lightcurves.csv')
        df_lc = pd.DataFrame(lightcurve_data)
        df_lc.to_csv(lc_output, index=False)
        if verbose:
            print(f"  Saved light curves to: {lc_output}")

    # Save spectra if requested
    if full_spectra and spectrum_data:
        spec_output = output_csv.replace('.csv', '_spectra.csv')
        df_spec = pd.DataFrame(spectrum_data)
        df_spec.to_csv(spec_output, index=False)
        if verbose:
            print(f"  Saved spectra to: {spec_output}")

    return df_summary

def main():
    parser = argparse.ArgumentParser(
        description='Extract information from SCONE TFRecord files to CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic: Extract summary statistics only
  python extract_tfrecord_info.py --tfrecord heatmaps/heatmaps_0000.tfrecord --output info.csv

  # Include full light curves
  python extract_tfrecord_info.py --tfrecord heatmaps/heatmaps_0000.tfrecord --output info.csv --full_lightcurves

  # Include full spectra
  python extract_tfrecord_info.py --tfrecord heatmaps/heatmaps_0000.tfrecord --output info.csv --full_spectra

  # Include everything
  python extract_tfrecord_info.py --tfrecord heatmaps/heatmaps_0000.tfrecord --output info.csv --full_lightcurves --full_spectra

  # Test on first 100 events
  python extract_tfrecord_info.py --tfrecord heatmaps/heatmaps_0000.tfrecord --output test.csv --limit 100

Summary CSV contains per-SNID:
  - Basic metadata (SNID, label, redshift)
  - Flux statistics (total, max, mean, median, std)
  - Peak information (location, value)
  - Light curve properties (rise/decline times, duration)
  - Spectrum properties (peak wavelength)
  - Color information (blue/red flux ratio)
  - SNR statistics
  - Data coverage metrics

Light curves CSV contains:
  - Full time series (180 time bins) for each SNID
  - Flux and error at each epoch

Spectra CSV contains:
  - Peak spectrum (32 wavelength bins) for each SNID
  - Flux and error at each wavelength
        """
    )

    parser.add_argument('--tfrecord', required=True, help='Path to TFRecord file')
    parser.add_argument('--output', required=True, help='Output CSV file path')
    parser.add_argument('--full_lightcurves', action='store_true',
                       help='Also save full light curves to separate CSV')
    parser.add_argument('--full_spectra', action='store_true',
                       help='Also save peak spectra to separate CSV')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of events to process (for testing)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress progress output')

    args = parser.parse_args()

    # Check input file exists
    if not os.path.exists(args.tfrecord):
        print(f"Error: TFRecord file not found: {args.tfrecord}", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process the file
    df = process_tfrecord(
        args.tfrecord,
        args.output,
        full_lightcurves=args.full_lightcurves,
        full_spectra=args.full_spectra,
        limit=args.limit,
        verbose=not args.quiet
    )

    if not args.quiet:
        print("\nDone!")
        print(f"\nQuick summary:")
        print(f"  Total events: {len(df)}")
        print(f"  SNIa: {np.sum(df['label'] == 1)}")
        print(f"  Non-Ia: {np.sum(df['label'] == 0)}")
        print(f"  Redshift range: {df['redshift'].min():.3f} - {df['redshift'].max():.3f}")
        print(f"  Mean SNR: {df['snr_mean'].mean():.2f}")

if __name__ == '__main__':
    main()
