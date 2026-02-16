# mapplot - Celestial & Terrestrial Mapping Tool

A command-line Python tool for creating publication-quality maps of celestial
and terrestrial data, with support for animated time-series visualization.

## Features

**Static plotting:**
- Sky maps with Bright Star Catalog (BSC5, 5,704 stars)
- Earth maps with coastlines, countries, and custom data
- 20+ map projections (Mollweide, Hammer, Aitoff, Robinson, Plate Carree, etc.)
- Reference overlays: ecliptic, galactic plane, celestial equator, coordinate poles
- Solar-relative coordinate system for asteroid/comet tracking
- MPC observatory database (2,000+ sites)
- Professional color palettes (Tableau 10, Set2, Vibrant, Muted)
- Multiple coordinate systems (equatorial, ecliptic, galactic) with transformations

**Animation:**
- Time-based motion visualization from MJD-stamped data
- Trail modes (point-based or time-based) with fade effects
- Sun position tracking along the ecliptic
- Observatory appearance/disappearance animation
- Secondary timeline plot with rolling statistics
- Keyframe summary frames
- Output to MP4, GIF, AVI, or WebM

## Installation

```bash
# Install in development mode (recommended for local use)
pip install -e .

# Or install normally
pip install .

# For animation support (MP4 output)
brew install ffmpeg    # macOS
# or: sudo apt-get install ffmpeg   # Debian/Ubuntu
```

## Quick Start

```bash
# Basic star map
mapplot --catalog -p mollweide -g

# Earth map with cities
mapplot --earth data/example_cities.txt -p robinson --coastlines -g

# Animate asteroid observations
mapplot --animate data/example_solar_relative.txt --ecliptic -o sandbox/test.mp4

# Full help
mapplot --help

# Check version
mapplot --version

# Alternative: run as Python module
python -m mapplot --catalog -p mollweide -g
```

## Repository Structure

```
astro_map_plot/
  pyproject.toml        Package metadata and dependencies
  src/mapplot/          Python package
    __init__.py           Version string
    __main__.py           python -m mapplot support
    cli.py                Argument parser
    config.py             Configuration and color palettes
    constants.py          Projections, markers
    coordinates.py        Coordinate transforms, sun position, MJD utilities
    geometry.py           Ecliptic, galactic plane, equator paths, poles
    catalog.py            BSC5 star catalog loading
    observatories.py      MPC observatory database
    data_io.py            Data file reading
    plotting.py           Static map plotting
    animation.py          Animation engine
    core.py               Main orchestration and entry point
  data/                 Input data files
    bsc5_data.txt         Bright Star Catalog v5 (5,704 stars)
    mpc_observatories.txt MPC observatory codes and positions
    example_*.txt         Example datasets
  docs/                 Documentation
  scripts/              Shell scripts (demo, test)
  sandbox/              Output files (plots, videos)
  tests/                Unit tests
```

## Usage Examples

```bash
# Star map with reference lines
mapplot --catalog --ecliptic --galactic-plane --celestial-equator \
  -p hammer -g --cardinal

# Solar-relative asteroid plot
mapplot --solar-relative data/mjd_ra_dec_near_22.txt --ecliptic -g

# Observatory locations
mapplot --earth --observatories -p mercator --coastlines

# Multi-object animation with trails
mapplot --animate data/mjd_ra_dec_near_22.txt data/mjd_ra_dec_far_22.txt \
  --legend --labels "Near-Earth" "Distant" \
  --palette tableau10 \
  --trail-days 60 --trail-fade \
  --show-time --time-format year \
  --end-pause 5.0 \
  -o sandbox/survey.mp4

# Publication-quality figure
mapplot --catalog --max-magnitude 5.0 \
  --ecliptic --galactic-plane --milky-way \
  -p robinson -g --grid-spacing 15 15 \
  --bgcolor black --grid-color lightgray --grid-alpha 0.25 \
  --figsize 16 10 --dpi 300 \
  -o sandbox/publication.png
```

## Configuration

Copy `src/mapplot/mapplotrc.example` to `~/.mapplotrc` and edit to set default
preferences for projection, colors, grid spacing, and other options.

```yaml
display:
  projection: hammer
  figsize: [14, 9]
  dpi: 150
colors:
  data_palette: tableau10
grid:
  spacing: [15, 15]
  color: gray
  alpha: 0.3
```

## Dependencies

**Required:** Python 3.10+, matplotlib, cartopy, numpy, astropy

**Optional:** pyyaml (configuration files), ffmpeg (MP4 output),
pillow (GIF output)

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
scripts/test.sh
scripts/test_animation.sh
scripts/demo_sky.sh
```

## Documentation

See `docs/QUICKREF.md` for a command reference card with copy-paste examples.
Feature-specific guides are in the `docs/` directory. The full development
history is in `docs/CHANGELOG.md`.

## License

See repository for license information.
