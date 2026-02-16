# CLAUDE.md - Project Guide for AI Assistants

## Project Overview

**mapplot** is a command-line Python tool for plotting geographic and celestial
data on various map projections. It supports both static plots and animated
time-series visualizations. The primary use case is astronomical: plotting
asteroid/NEO observations, observatory locations, and celestial reference
features on all-sky maps.

## Repository Structure

- `src/mapplot/` - Python package (installed via `pip install -e .`)
  - `__init__.py` - Version string
  - `__main__.py` - `python -m mapplot` support
  - `cli.py` - Argument parser (`parse_args`)
  - `config.py` - `DEFAULT_CONFIG`, `COLOR_PALETTES`, `load_config`, `get_data_colors`
  - `constants.py` - `TERRESTRIAL_PROJECTIONS`, `MARKERS`
  - `coordinates.py` - Coordinate transforms, sun position, MJD utilities, solar-relative
  - `geometry.py` - Ecliptic, galactic plane, celestial equator paths, poles, Milky Way
  - `catalog.py` - BSC5 star catalog loading (`get_bright_stars`)
  - `observatories.py` - MPC download/parse/load, observatory dates
  - `data_io.py` - `read_data`, `prepare_animation_data`
  - `plotting.py` - `plot_sky_map`, `plot_terrestrial_map`, `plot_cardinal_directions`, `plot_custom_gridlines`
  - `animation.py` - `create_animation` (animation engine)
  - `core.py` - `run_mapplot` (main orchestration), `main()` entry point
  - `mapplotrc.example` - YAML configuration file template
  - `download_bsc5.py` - Info about downloading the full BSC5 catalog
- `pyproject.toml` - Package metadata, dependencies, entry point
- `data/` - Input data files (star catalogs, observatory codes, example datasets,
  asteroid ephemerides, NEO survey data).
- `docs/` - Feature documentation and changelog.
- `scripts/` - Demo and test shell scripts.
- `sandbox/` - Output directory for generated plots and videos. Contents are
  gitignored.
- `tests/` - Unit tests (pytest).

## Key Technical Details

- **Package architecture**: Proper Python package under `src/mapplot/` with
  `pyproject.toml`. Entry point: `mapplot = "mapplot.core:main"`.
- **Dependencies**: matplotlib, cartopy, numpy, astropy (required); pyyaml,
  pillow (optional).
- **Coordinate systems**: Equatorial (RA/Dec), ecliptic, galactic, with
  transformations via astropy. Celestial coordinates use left-handed convention
  (RA increases right-to-left).
- **Data format**: Space-separated text files. Columns vary by mode:
  - Basic: `lon lat [value] [size] [label]`
  - Animation/solar-relative: `MJD RA Dec [value] [size] [label]`
- **Color conventions**: Red = ecliptic, green = celestial equator, blue =
  galactic plane. Data series use configurable palettes (Tableau 10 default).
- **Animation**: Uses matplotlib's animation framework. Output via ffmpeg
  (MP4, H.264 CRF 23) or pillow (GIF). Performance-critical paths use binary
  search and batched scatter plots.

## Common Tasks

### Running mapplot
```bash
mapplot --catalog -p mollweide -g              # Basic sky map
mapplot --earth data/example_cities.txt -p robinson --coastlines  # Earth
mapplot --animate data/mjd_ra_dec_near_22.txt -o sandbox/out.mp4  # Animation
mapplot --version                              # Version
mapplot -h                                      # Full help
python -m mapplot --catalog -p mollweide -g    # Alternative invocation
```

### Running tests
```bash
python -m pytest tests/          # Unit tests
scripts/test.sh                  # Basic functionality
scripts/test_animation.sh        # Animation features
scripts/demo_sky.sh              # Generate demo sky maps
```

### Installation
```bash
pip install -e .                 # Development install
pip install .                    # Normal install
```

### Adding features
Code is organized into modules under `src/mapplot/`:
- Coordinate/math changes -> `coordinates.py` or `geometry.py`
- Data loading changes -> `data_io.py`
- CLI argument changes -> `cli.py`
- Config/color changes -> `config.py`
- Static plot changes -> `plotting.py`
- Animation changes -> `animation.py`
- Orchestration/validation -> `core.py`

## Conventions

- No emojis in code or documentation files.
- Shell scripts use `python -m mapplot` for invocation.
- Output files go in `sandbox/` and are gitignored.
- Data files are plain text, space-separated, with `#` comments.
