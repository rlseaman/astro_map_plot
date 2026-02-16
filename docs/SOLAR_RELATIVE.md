# Solar-Relative Coordinate Mode

## Overview

Solar-relative mode plots objects in ecliptic coordinates relative to the Sun's position at the time of observation. This is especially useful for:

- **Asteroid and comet tracking** - See position relative to opposition
- **Solar system dynamics** - Understand orbital geometry
- **Observability planning** - Opposition (180°) is optimal viewing
- **Solar elongation studies** - Track angular distance from Sun

## Concept

Instead of absolute ecliptic longitude, solar-relative mode shows **solar elongation** - the angular distance from the Sun measured along the ecliptic.

**Key Points:**
- Input includes **time** (MJD) for each observation
- Sun's position is calculated for each time
- Object's elongation from Sun is computed
- Plot can be centered on any elongation (default: opposition at 180°)

## Input File Format

When using `--solar-relative`, the input file format changes:

```
# Column 1: MJD (Modified Julian Date)
# Column 2: RA or coord1 (degrees)
# Column 3: Dec or coord2 (degrees)
# Column 4: [optional] size
# Column 5: [optional] color value

60000.0  180.0  10.0
60010.0  185.5  12.3
60020.0  191.2  14.8
```

**Note:** You can still use `--input-coord` to specify if columns 2-3 are equatorial, ecliptic, or galactic coordinates.

## Basic Usage

```bash
# Default: center on opposition (180° from Sun)
mapplot --solar-relative asteroid.txt -p mollweide -g

# Show ecliptic plane for reference
mapplot --solar-relative --ecliptic asteroid.txt -p hammer -g

# With catalog stars
mapplot --solar-relative --catalog asteroid.txt -p aitoff -g
```

## Solar Center Option

Use `--solar-center` to center the plot on different solar elongations:

```bash
# Opposition (180°) - default
mapplot --solar-relative asteroid.txt -g

# Conjunction (0°) - object near Sun
mapplot --solar-relative --solar-center 0 asteroid.txt -g

# Quadrature (90°) - object at right angle to Sun
mapplot --solar-relative --solar-center 90 asteroid.txt -g

# Eastern quadrature (270° or -90°)
mapplot --solar-relative --solar-center 270 asteroid.txt -g
```

### Solar Elongation Reference

| Elongation | Name | Description | Observability |
|-----------|------|-------------|---------------|
| 0° | Conjunction | Object near Sun | Not visible |
| 90° | Western Quadrature | 90° west of Sun | Morning sky |
| 180° | Opposition | Opposite Sun | Best viewing (all night) |
| 270° | Eastern Quadrature | 90° east of Sun | Evening sky |

## Coordinate System

Solar-relative mode:
1. Converts input coordinates to ecliptic
2. Calculates Sun's ecliptic longitude at each MJD
3. Computes relative longitude: `elongation = object_lon - sun_lon`
4. Centers plot: `plot_lon = elongation - solar_center + 180`
5. Keeps ecliptic latitude unchanged

**Axes:**
- **Horizontal**: Solar-relative ecliptic longitude
- **Vertical**: Ecliptic latitude (unchanged)

## Examples

### Example 1: Asteroid Opposition Track

Track an asteroid approaching opposition:

```bash
# Data file: asteroid_track.txt
# 60000.0  45.0   5.0
# 60005.0  50.2   5.5
# 60010.0  55.8   6.1
# ... (continues)

mapplot --solar-relative asteroid_track.txt \
  --ecliptic \
  -p hammer -g \
  --title "Asteroid Track Approaching Opposition"
```

Center of plot (longitude 0) represents opposition - best viewing.

### Example 2: Comet Perihelion Passage

Show a comet passing through perihelion (closest to Sun):

```bash
mapplot --solar-relative --solar-center 0 comet.txt \
  -p mollweide -g \
  --title "Comet Perihelion Passage"
```

Center (longitude 0) represents conjunction with Sun.

### Example 3: Multi-Object Comparison

Compare positions of multiple asteroids:

```bash
mapplot --solar-relative \
  asteroid1.txt asteroid2.txt asteroid3.txt \
  -c red -c blue -c green \
  --labels "Asteroid A" "Asteroid B" "Asteroid C" \
  --legend -p robinson -g
```

### Example 4: With Background Stars

Show object against star field:

```bash
mapplot --solar-relative --catalog --max-mag 5.0 \
  neo_track.txt \
  -c orange -s 100 \
  -p aitoff -g \
  --bgcolor black --grid-color white \
  --title "NEO Against Star Background"
```

### Example 5: Different Input Coordinates

Input can be in any coordinate system:

```bash
# Ecliptic input
mapplot --solar-relative --input-coord ecliptic \
  obj_ecliptic.txt -g

# Galactic input
mapplot --solar-relative --input-coord galactic \
  obj_galactic.txt -g
```

## Time Format: Modified Julian Date (MJD)

MJD = JD - 2400000.5

**Quick conversions:**
- MJD 0 = November 17, 1858
- MJD 60000 ≈ February 24, 2023
- MJD 60500 ≈ July 8, 2024

**From calendar date:**
```python
from astropy.time import Time
t = Time('2024-01-15')
print(t.mjd)  # 60325.0
```

**Current MJD:**
```python
from astropy.time import Time
print(Time.now().mjd)
```

## Understanding the Plot

### Opposition-Centered (Default)

When centered on opposition (`--solar-center 180`):
- **Longitude 0°**: Object at opposition (180° from Sun)
- **Longitude +90°**: Object 90° east of opposition
- **Longitude -90°**: Object 90° west of opposition
- **Edge of map**: Object near conjunction with Sun

### Conjunction-Centered

When centered on conjunction (`--solar-center 0`):
- **Longitude 0°**: Object at conjunction (0° from Sun)
- **Longitude +90°**: Object 90° ahead of Sun
- **Longitude -90°**: Object 90° behind Sun
- **Edge of map**: Object at opposition

### Grid Lines

Grid lines show constant solar elongations and ecliptic latitudes:
- **Vertical lines**: Constant elongation from center
- **Horizontal lines**: Constant ecliptic latitude

## Combining with Other Features

### With Ecliptic Plane

```bash
mapplot --solar-relative --ecliptic \
  --poles ecliptic \
  object.txt -p mollweide -g
```

Shows the ecliptic plane and poles for reference.

### With Star Catalog

```bash
mapplot --solar-relative --catalog --max-mag 4.0 \
  asteroid.txt -p hammer -g \
  --bgcolor black --grid-color white
```

Shows bright stars for reference (stars don't move in solar-relative frame).

### With Custom Grid

```bash
mapplot --solar-relative \
  --grid-spacing 15 10 \
  object.txt -p aitoff -g
```

Finer grid: 15° in longitude, 10° in latitude.

## Compatible and Incompatible Options

### ✅ Compatible Options

**These work with --solar-relative:**
- `--catalog` - Show BSC5 stars (they appear at fixed positions since stars don't move relative to ecliptic)
- `--ecliptic` - Shows as a horizontal line at latitude=0
- `--input-coord` - Specify input coordinate system (equatorial/ecliptic/galactic)
- `--labels-from-file` - Text labels from fourth column (after MJD, RA, Dec)
- `--ignore-extra` - Ignore columns beyond first three
- All projection options (`-p`)
- All gridline options (`-g`, `--grid-spacing`, etc.)
- All styling options (colors, sizes, markers, etc.)
- All output options (`-o`, `--figsize`, `--dpi`, etc.)

### ❌ Incompatible Options

**These are REJECTED with error messages:**
- `--earth` - Solar-relative is celestial only
- `--galactic-plane` - Wrong coordinate system (would show as sinusoid)
- `--celestial-equator` - Wrong coordinate system (would show as sinusoid)
- `--milky-way` - Galactic coordinates don't align with solar-relative frame
- `--poles` - Coordinate poles are not meaningful in solar-relative frame
- `--grid-coord` - Solar-relative uses its own fixed coordinate system
- `--plot-coord` - Solar-relative uses its own fixed coordinate system

**Why these are incompatible:**

Solar-relative coordinates create a special ecliptic-based frame where:
- Longitude = solar elongation (angular distance from Sun)
- Latitude = ecliptic latitude

Other celestial reference frames (galactic, equatorial) don't have constant orientations in this frame, so they would appear as complex curves rather than meaningful reference lines.

## Limitations

1. **Input coordinates must be sky coordinates** (equatorial, ecliptic, or galactic)
2. **Not compatible with --earth mode** (solar-relative is celestial only)
3. **Not compatible with most celestial overlays** (see incompatible options above)
4. **Requires astropy** for Sun position calculation
5. **All input must have MJD** as first column
6. **Must provide input files** (--catalog alone is not sufficient)

## Technical Details

### Sun Position Calculation

Uses `astropy.coordinates.get_sun()` to compute the Sun's ICRS position at each MJD, then transforms to ecliptic coordinates.

### Coordinate Transformation Pipeline

1. Read MJD, RA, Dec from file
2. Convert input coords → ecliptic (if needed)
3. Calculate Sun's ecliptic longitude at each MJD
4. Compute: `elongation = object_lon - sun_lon`
5. Wrap to ±180°
6. Center: `plot_lon = elongation - solar_center`
7. Plot with ecliptic latitude unchanged

### Wrapping Behavior

Longitudes are wrapped to ±180° for standard map projections:
- +180° to -180° boundary is at anti-center point
- For opposition centering, this is conjunction
- For conjunction centering, this is opposition

## Troubleshooting

**"Error: --solar-relative requires MJD as first column"**
- Ensure your file has MJD in column 1
- Check that file isn't empty
- Verify numeric format (no text in MJD column)

**Objects appear in wrong location:**
- Check MJD values (MJD 60000 ≈ 2023)
- Verify coordinate system with `--input-coord`
- Ensure RA/Dec are in degrees (not hours for RA)

**Plot looks strange:**
- Try different `--solar-center` values
- Check your projection with `-p`
- Verify time range in your data

**Sun position seems wrong:**
- Verify MJD calculation
- Check that times are reasonable (MJD 50000-70000 for modern dates)

## Examples with Real Data

### Minor Planet Center Format Conversion

If you have MPC-format observations:

```python
# Convert MPC observations to solar-relative format
# MPC format: YYMMDD.ddd HH MM SS.s +DD MM SS.s
# Output: MJD RA Dec

from astropy.time import Time
from astropy.coordinates import Angle

# Example conversion
date_str = "20240115.5"  # MPC format
ra_str = "10 30 45.2"     # HH MM SS
dec_str = "+25 15 30.5"   # DD MM SS

# Convert to MJD
t = Time(date_str, format='yday', scale='utc')
mjd = t.mjd

# Convert RA/Dec to degrees
ra = Angle(ra_str, unit='hourangle').degree
dec = Angle(dec_str, unit='deg').degree

print(f"{mjd} {ra} {dec}")
```

### JPL Horizons Data

JPL Horizons can output in observer format. Convert to:
```
MJD  RA(deg)  Dec(deg)
```

## See Also

- **example_solar_relative.txt** - Sample data file
- **README.md** - Main documentation
- **NEW_FEATURES.md** - Poles and grid documentation
- **QUICKREF.md** - Quick reference

## Reference

**MJD Resources:**
- https://aa.usno.navy.mil/data/JulianDate
- Astropy Time: https://docs.astropy.org/en/stable/time/

**Solar System Ephemerides:**
- JPL Horizons: https://ssd.jpl.nasa.gov/horizons/
- Minor Planet Center: https://www.minorplanetcenter.net/

**Understanding Solar Elongation:**
- Opposition: https://en.wikipedia.org/wiki/Opposition_(astronomy)
- Conjunction: https://en.wikipedia.org/wiki/Conjunction_(astronomy)
