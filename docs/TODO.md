# TODO - Future Work

## Testing

- Add integration tests for plot generation (verify output files are valid PNGs)
- Add tests for config loading (YAML parsing, precedence, missing file)
- Add tests for observatory parsing (fixed-width format edge cases)
- Add tests for geometry functions (ecliptic_path, galactic_plane_path)
- Add tests for animation data preparation (sorting, downsampling)
- Test solar-relative coordinate transform end-to-end against known ephemeris

## Code Quality

- Add type annotations to public API functions
- Replace `print(..., file=sys.stderr)` with Python logging module
- Add `py.typed` marker for PEP 561 compliance
- Consider dataclasses for structured data (observatory records, animation records)

## Features

- Support reading CSV files (comma-separated, not just space-separated)
- Support FITS table input for catalog data
- Add `--quiet` / `--verbose` flags to control stderr output
- Add `--list-projections` and `--list-palettes` convenience flags
- Support custom marker colors per-point from a file column (not just per-file)
- Add `--sun-position MJD` flag to show sun at a specific time on static plots
- Support for proper motion in star catalog (BSC5 has PM data)

## Packaging and Distribution

- Add GitHub Actions CI (run tests on push, test across Python 3.10-3.13)
- Publish to PyPI (`pip install mapplot`)
- Add `mapplot --update-data` to download/refresh BSC5 and MPC observatory files
- Consider bundling data files as package data instead of relying on search paths

## Documentation

- Add docstrings to all public functions (currently minimal)
- Generate API docs (sphinx or mkdocs)
- Add examples directory with Jupyter notebooks
- Update docs/ guides to reference module locations instead of line numbers
