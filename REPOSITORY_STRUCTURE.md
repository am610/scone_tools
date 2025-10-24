# SCONE Tools Repository Structure

```
scone_tools/
├── README.md                      # Main repository README with overview
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution guidelines
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── Core Scripts
│   ├── extract_tfrecord_info.py   # Extract TFRecord data to CSV
│   ├── visualize_tfrecords.py     # Create visualizations
│   ├── extract_all_tfrecords.sh   # Batch extraction script
│   ├── plot_samples.sh             # Sample plotting script
│   └── plot_statistics.sh          # Statistics plotting script
│
├── docs/                           # Documentation
│   ├── EXTRACTION_GUIDE.md        # Detailed extraction guide
│   ├── VISUALIZATION_GUIDE.md     # Visualization guide
│   └── DATA_FORMAT.md             # TFRecord format specification
│
└── examples/                       # Example scripts and workflows
    ├── analyze_population.py      # Population analysis example
    └── quick_start.sh             # Quick start workflow

```

## File Descriptions

### Root Level

- **README.md**: Main entry point with quick start, features, and usage examples
- **LICENSE**: MIT License for open source distribution
- **CONTRIBUTING.md**: Guidelines for contributors
- **requirements.txt**: Python package dependencies
- **.gitignore**: Files and directories to exclude from git

### Core Scripts

All executable scripts in the root directory:

1. **extract_tfrecord_info.py**
   - Extracts TFRecord data to CSV format
   - Produces summary statistics (40 columns)
   - Optional: full light curves and spectra
   - Usage: `python extract_tfrecord_info.py --tfrecord file.tfrecord --output summary.csv`

2. **visualize_tfrecords.py**
   - Creates comprehensive visualization plots
   - Individual event plots (5 panels)
   - Statistical summary plots (6 panels)
   - Usage: `python visualize_tfrecords.py --tfrecord file.tfrecord --num_samples 10`

3. **extract_all_tfrecords.sh**
   - Batch processes all TFRecord files
   - Optionally combines results
   - Usage: `./extract_all_tfrecords.sh output_dir`

4. **plot_samples.sh**
   - Samples events from all files
   - Usage: `./plot_samples.sh 10 output_dir`

5. **plot_statistics.sh**
   - Creates statistics for all files
   - Usage: `./plot_statistics.sh 1000 output_dir`

### Documentation (docs/)

Comprehensive guides for users:

1. **EXTRACTION_GUIDE.md**
   - Complete guide to data extraction
   - CSV column descriptions
   - Analysis workflows
   - Performance estimates

2. **VISUALIZATION_GUIDE.md**
   - How to create and interpret plots
   - Recommended workflows
   - Use case examples
   - Troubleshooting

3. **DATA_FORMAT.md**
   - TFRecord structure specification
   - Physical parameters and units
   - Coordinate systems
   - Code examples for reading data

### Examples (examples/)

Ready-to-use example scripts:

1. **analyze_population.py**
   - Loads and analyzes extracted CSV data
   - Generates statistical comparisons
   - Identifies interesting events
   - Creates diagnostic plots

2. **quick_start.sh**
   - Complete workflow demonstration
   - Runs extraction, analysis, and visualization
   - Good starting point for new users

## Usage Patterns

### For End Users

1. Start with **README.md** for overview
2. Run **examples/quick_start.sh** to test
3. Read relevant guide in **docs/**
4. Use core scripts for your analysis

### For Developers

1. Read **CONTRIBUTING.md** for guidelines
2. Check **docs/DATA_FORMAT.md** for specifications
3. Review core scripts for implementation details
4. Add examples to **examples/** for new features

### For Researchers

1. Use **extract_all_tfrecords.sh** for data extraction
2. Analyze with **examples/analyze_population.py**
3. Visualize specific events with **visualize_tfrecords.py**
4. Cite the repository in your publications

## File Sizes

- Core scripts: ~43 KB total
- Documentation: ~27 KB total
- Examples: ~10 KB total
- **Total repository: ~80 KB** (excluding data)

## Dependencies

See `requirements.txt` for complete list. Main dependencies:
- TensorFlow 2.x
- NumPy
- Pandas
- Matplotlib

## Next Steps

After cloning the repository:

1. Install dependencies: `pip install -r requirements.txt`
2. Navigate to your SCONE output directory
3. Run quick start: `bash examples/quick_start.sh`
4. Explore the generated outputs
5. Read documentation for advanced usage

---

For questions or issues, please visit the GitHub repository.
