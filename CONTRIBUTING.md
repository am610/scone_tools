# Contributing to SCONE Tools

Thank you for your interest in contributing to SCONE Tools! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the GitHub Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)
   - Example code/data if applicable

### Contributing Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/scone_tools.git
   cd scone_tools
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Add docstrings to functions
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Test on a small sample
   python extract_tfrecord_info.py --tfrecord test.tfrecord --output test.csv --limit 100
   python visualize_tfrecords.py --tfrecord test.tfrecord --num_samples 2
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub with a clear description.

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular

### Python Style Example

```python
def process_lightcurve(flux_data, time_bins):
    """
    Process light curve data and extract features.

    Parameters:
    -----------
    flux_data : np.ndarray
        Flux values, shape (n_wavelengths, n_times)
    time_bins : np.ndarray
        Time bin centers in days

    Returns:
    --------
    dict
        Dictionary with extracted features
    """
    # Implementation here
    pass
```

## Documentation

When adding new features:

1. Update relevant documentation in `docs/`
2. Add examples to `examples/` if applicable
3. Update the main `README.md` if needed
4. Include docstrings in code

## Testing

While we don't have formal unit tests yet, please:

1. Test your code on small samples first
2. Verify output files are correct
3. Check that plots render properly
4. Test edge cases (empty data, single event, etc.)

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- [ ] Add unit tests (pytest)
- [ ] Improve error handling and validation
- [ ] Add progress bars for long operations
- [ ] Support for additional TFRecord formats
- [ ] Parallel processing for batch operations

### Medium Priority
- [ ] Additional statistical features
- [ ] More visualization options
- [ ] Interactive plots (plotly/bokeh)
- [ ] Support for different wavelength/time ranges
- [ ] Export to other formats (HDF5, FITS)

### Documentation
- [ ] Tutorial notebooks (Jupyter)
- [ ] Video tutorials
- [ ] More usage examples
- [ ] API reference documentation
- [ ] Troubleshooting guide

### Analysis Tools
- [ ] Machine learning utilities
- [ ] Anomaly detection
- [ ] Clustering analysis
- [ ] Cross-matching with catalogs
- [ ] Statistical comparison tools

## Feature Requests

Before implementing a new feature:

1. Open an issue to discuss it
2. Get feedback from maintainers
3. Agree on the approach
4. Then implement and submit PR

This helps avoid duplicate work and ensures the feature fits the project goals.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the problem, not the person
- Help newcomers learn

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues
3. Open a new issue with the "question" label
4. Reach out to the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve SCONE Tools! 🚀
