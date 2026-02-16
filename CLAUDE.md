# CLAUDE.md - Project Guide for AI Assistants

## Project Overview

**mapplot** is a command-line Python tool for plotting geographic and celestial
data on various map projections. It supports both static plots and animated
time-series visualizations. The primary use case is astronomical: plotting
asteroid/NEO observations, observatory locations, and celestial reference
features on all-sky maps.

## Repository Structure

- `src/mapplot` - Single-file Python 3 executable (~2,766 lines). This is the
  entire application. No package structure; runs directly with `#!/usr/bin/env python3`.
- `src/install.sh` - Installs mapplot to `~/.local/bin/` and data to
  `~/.local/share/mapplot/`.
- `src/mapplotrc.example` - YAML configuration file template.
- `src/download_bsc5.py` - Downloads the full Bright Star Catalog.
- `data/` - Input data files (star catalogs, observatory codes, example datasets,
  asteroid ephemerides, NEO survey data).
- `docs/` - Feature documentation and changelog.
- `scripts/` - Demo and test shell scripts. These use relative paths from the
  project root via `$ROOT_DIR`.
- `sandbox/` - Output directory for generated plots and videos. Contents are
  gitignored.
- `OLD/` - Historical development versions (37 directories). Gitignored.
  Preserved for reference but not part of the active codebase.

## Key Technical Details

- **Single-file architecture**: All functionality is in `src/mapplot`. There are
  no separate modules or packages.
- **Dependencies**: matplotlib, cartopy, numpy, astropy (required); pyyaml,
  ffmpeg, pillow (optional).
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

## Development History

This codebase was consolidated from 37 development directories spanning
Dec 30, 2025 through Jan 3, 2026. The progression was:
1. v3-v17: Core features (projections, BSC5, observatories, solar-relative, grids)
2. v2.0: Major rewrite adding animation, professional colors, YAML config
3. Feature branches: Sun animation, timeline plots, galactic center, polish
4. `mapplot_summary/mapplot` is the canonical latest version

See `docs/CHANGELOG.md` for the full consolidated development history.

## Common Tasks

### Running mapplot
```bash
./src/mapplot --catalog -p mollweide -g              # Basic sky map
./src/mapplot --earth data/example_cities.txt -p robinson --coastlines  # Earth
./src/mapplot --animate data/mjd_ra_dec_near_22.txt -o sandbox/out.mp4  # Animation
./src/mapplot -h                                      # Full help
```

### Running tests
```bash
scripts/test.sh              # Basic functionality
scripts/test_animation.sh    # Animation features
scripts/demo_sky.sh          # Generate demo sky maps
```

### Adding features
All code changes go in `src/mapplot`. The file is organized as:
- Imports and constants at top
- Utility functions (coordinate transforms, MJD conversion, Sun position, etc.)
- Data loading functions
- Plotting functions
- Animation functions
- Argument parser and main() at bottom

## Conventions

- No emojis in code or documentation files.
- Shell scripts use `$ROOT_DIR` / `$SCRIPT_DIR` for portable path references.
- Output files go in `sandbox/` and are gitignored.
- Data files are plain text, space-separated, with `#` comments.
