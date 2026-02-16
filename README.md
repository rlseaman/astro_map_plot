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

## Quick Start

```bash
# Install dependencies
pip install matplotlib cartopy numpy astropy pyyaml

# For MP4 animation output
brew install ffmpeg    # macOS
# or: sudo apt-get install ffmpeg   # Debian/Ubuntu

# Basic star map
./src/mapplot --catalog -p mollweide -g

# Earth map with cities
./src/mapplot --earth data/example_cities.txt -p robinson --coastlines -g

# Animate asteroid observations
./src/mapplot --animate data/example_solar_relative.txt --ecliptic -o sandbox/test.mp4
```

## Repository Structure

```
astro_map_plot/
  src/              Main source code
    mapplot           Primary executable (Python 3)
    download_bsc5.py  Script to download full BSC5 catalog
    install.sh        System-wide installation script
    mapplotrc.example YAML configuration template
  docs/             Documentation
    QUICKREF.md       Command reference with examples
    ANIMATION.md      Core animation guide
    ANIMATION_ADVANCED.md  Advanced animation techniques
    COLORS_AND_CONFIG.md   Color palettes and YAML configuration
    SOLAR_RELATIVE.md      Solar-relative coordinate system
    OBSERVATORIES.md       MPC observatory database usage
    OBSERVATORY_ANIMATION.md  Animating observatory operational dates
    GRID_LABELS.md         Grid labels and cardinal directions
    NEW_FEATURES.md        Coordinate poles, independent grids
    VERSION_2.0_RELEASE_NOTES.md  v2.0 release notes
    CHANGELOG.md           Consolidated development history
  data/             Input data files
    bsc5_data.txt     Bright Star Catalog v5 (5,704 stars)
    mpc_observatories.txt  MPC observatory codes and positions
    example_*.txt     Example datasets (cities, Messier objects, etc.)
    mjd_ra_dec_*.txt  Asteroid ephemeris data with MJD timestamps
    ra_dec_*.txt      Asteroid ephemeris data (RA/Dec only)
    neos_*.txt        NEO survey data binned by magnitude
    ast_*.txt         Asteroid type classification data
  scripts/          Shell scripts
    demo_sky.sh       Generate demonstration sky maps
    test.sh           Basic functionality tests
    test_animation.sh Animation feature tests
  sandbox/          Output files (plots, videos)
  OLD/              Historical development versions (not tracked)
```

## Usage Examples

```bash
# Star map with reference lines
./src/mapplot --catalog --ecliptic --galactic-plane --celestial-equator \
  -p hammer -g --cardinal

# Solar-relative asteroid plot
./src/mapplot --solar-relative data/mjd_ra_dec_near_22.txt --ecliptic -g

# Observatory locations
./src/mapplot --earth --observatories -p mercator --coastlines

# Multi-object animation with trails
./src/mapplot --animate data/mjd_ra_dec_near_22.txt data/mjd_ra_dec_far_22.txt \
  --legend --labels "Near-Earth" "Distant" \
  --palette tableau10 \
  --trail-days 60 --trail-fade \
  --show-time --time-format year \
  --end-pause 5.0 \
  -o sandbox/survey.mp4

# Publication-quality figure
./src/mapplot --catalog --max-magnitude 5.0 \
  --ecliptic --galactic-plane --milky-way \
  -p robinson -g --grid-spacing 15 15 \
  --bgcolor black --grid-color lightgray --grid-alpha 0.25 \
  --figsize 16 10 --dpi 300 \
  -o sandbox/publication.png
```

## Configuration

Copy `src/mapplotrc.example` to `~/.mapplotrc` and edit to set default
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

**Required:** Python 3.7+, matplotlib, cartopy, numpy, astropy

**Optional:** pyyaml (configuration files), ffmpeg (MP4 output),
pillow (GIF output)

## Documentation

See `docs/QUICKREF.md` for a command reference card with copy-paste examples.
Feature-specific guides are in the `docs/` directory. The full development
history is in `docs/CHANGELOG.md`.

## License

See repository for license information.
