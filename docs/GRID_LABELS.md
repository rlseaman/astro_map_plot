# Grid Labels and Cardinal Directions

## Overview

New options to add axis labels and cardinal direction markers to your maps for better orientation and readability.

## Features

### --grid-labels -p plate-carree
Shows coordinate values along the edges of the map.

**What it does:**
- Displays longitude/RA values along the bottom edge (meridians)
- Displays latitude/Dec values along the left edge (parallels)
- Automatically formats labels based on coordinate system
- Works with both terrestrial and celestial maps
- **Celestial coordinates are left-handed:** E on left, W on right (astronomical convention)

**Coordinate Convention:**
- **Terrestrial (Earth) maps:** Right-handed system (E on right, W on left)
- **Celestial (Sky) maps:** Left-handed system (E on left, W on right)
  - This matches astronomical convention for observers in the Northern Hemisphere facing south
  - The map orientation matches what you see when looking up at the sky

**Usage:**
```bash
# Sky map with labeled grid
mapplot --catalog -g --grid-labels -p plate-carree

# Earth map with labeled grid
mapplot --earth cities.txt -g --grid-labels -p mercator

# Custom grid spacing with labels
mapplot --catalog -g --grid-labels -p plate-carree --grid-spacing 15 15
```

**Note:** Grid labels work best with certain projections:
- **Supported:** plate-carree, mercator
- **Not supported:** mollweide, hammer, aitoff, robinson, orthographic, etc.
- **Why:** Cartopy's gridline labeling system requires specific projection types
- **Workaround:** Use `-p plate-carree` or `-p mercator` for labeled grids

### --cardinal
Shows cardinal direction markers (N, S, E, W) on the map.

**What it does:**
- Places directional markers at appropriate positions
- White circles with black letters for visibility
- Position depends on map mode:
  - **Earth mode:** N=North, S=South, E=East, W=West
  - **Sky mode:** N=higher latitude, S=lower latitude, E/W=longitude direction
  - **Solar-relative:** N/S=ecliptic latitude, E/W=elongation direction

**Usage:**
```bash
# Earth map with cardinal directions
mapplot --earth cities.txt -g --cardinal -p robinson

# Sky map with cardinal directions
mapplot --catalog -g --cardinal -p mollweide

# Both labels and cardinals
mapplot --catalog -g --grid-labels -p plate-carree --cardinal
```

## Examples

### Example 1: Labeled Earth Map

```bash
mapplot --earth example_cities.txt \
  -g --grid-labels -p plate-carree --cardinal \
  -p mercator \
  --coastlines --countries \
  --title "World Cities with Grid"
```

Creates a world map with:
- Grid lines every 30°
- Coordinate labels on axes
- N, S, E, W markers
- Coastlines and countries

### Example 2: Labeled Sky Map

```bash
mapplot --catalog --max-mag 4.0 \
  -g --grid-labels -p plate-carree --cardinal \
  -p plate-carree \
  --ecliptic \
  --title "Bright Stars with Coordinates"
```

Creates a star map with:
- Bright stars (mag ≤ 4)
- RA/Dec grid with labels
- Cardinal directions
- Ecliptic plane

### Example 3: Solar-Relative with Orientation

```bash
mapplot --solar-relative example_solar_relative.txt \
  -g --cardinal --grid-spacing 30 15 \
  -p hammer \
  --ecliptic \
  --title "Asteroid Track with Orientation"
```

Shows:
- Solar-relative coordinates
- Ecliptic latitude grid
- Cardinal markers (N/S for latitude, E/W for elongation)
- Ecliptic as horizontal line

### Example 4: Custom Grid with Labels

```bash
mapplot --earth --observatories \
  --obs-codes 675 703 G96 \
  -g --grid-labels -p plate-carree --cardinal \
  --grid-spacing 5 5 \
  --extent -115 -105 30 37 \
  -p mercator \
  --title "Arizona Observatories"
```

Regional map with:
- Fine 5° grid
- Labeled axes
- Cardinal directions
- Observatory locations

## Combining Features

Grid labels and cardinal directions work well with all other features:

```bash
# With multiple datasets
mapplot --earth file1.txt file2.txt \
  -c red -c blue \
  -g --grid-labels -p plate-carree --cardinal \
  --legend --labels "Dataset 1" "Dataset 2"

# With overlays
mapplot --catalog --ecliptic --galactic-plane \
  -g --grid-labels -p plate-carree --cardinal \
  --bgcolor black --grid-color white

# With custom styling
mapplot --earth cities.txt \
  -g --grid-labels -p plate-carree --cardinal \
  --grid-color darkgray --grid-alpha 0.3 \
  --bgcolor lightblue
```

## Cardinal Direction Positioning

### Earth Mode (--earth) - Right-Handed
- **N** - Top center (90° latitude)
- **S** - Bottom center (-90° latitude)  
- **E** - Right edge (increasing longitude to right)
- **W** - Left edge (decreasing longitude to left)

### Sky Mode (default) - Left-Handed (Astronomical Convention)
- **N** - Top (positive declination/latitude)
- **S** - Bottom (negative declination/latitude)
- **E** - LEFT (increasing RA/longitude to left)
- **W** - RIGHT (decreasing RA/longitude to right)

**Why left-handed for celestial coordinates?**

When you stand in the Northern Hemisphere and face south (looking at the sky), east is to your left and west is to your right. Celestial maps use this convention so that the map orientation matches what you see when looking up. This is the standard in astronomy.

**Comparison:**
```
Terrestrial (looking DOWN at Earth):     Celestial (looking UP at sky):
        N                                          N
        |                                          |
    W---+---E                                  E---+---W
        |                                          |
        S                                          S
  (right-handed)                             (left-handed)
```

### Solar-Relative Mode
- **N** - Top (positive ecliptic latitude)
- **S** - Bottom (negative ecliptic latitude)
- **E** - Trailing (positive elongation from center)
- **W** - Leading (negative elongation from center)

## Tips

1. **Projection matters:** Grid labels are clearest on cylindrical projections (plate-carree, mercator)

2. **Label overlap:** If labels overlap with data, try:
   - Larger figure size: `--figsize 16 10`
   - Different projection
   - Wider grid spacing

3. **Visibility:** Cardinal markers have white backgrounds for visibility on any map color

4. **Custom positioning:** Cardinals are placed near edges but not at exact coordinates to avoid overlap with grid labels

5. **Publication quality:** For papers/presentations, use:
   ```bash
   mapplot --catalog -g --grid-labels -p plate-carree \
     --figsize 12 8 --dpi 300 \
     -o figure.pdf
   ```

## Technical Details

### Grid Labels
- Generated by cartopy's gridlines system
- Automatically formatted based on coordinate system
- Top and right labels disabled by default (cleaner look)
- Font size: 10pt
- Can be customized via matplotlib rcParams if needed

### Cardinal Markers
- Plotted as text annotations
- Circular white background (80% opacity)
- Bold font, size 14
- Positioned at ±178° longitude, ±88° latitude
- Z-order ensures visibility above most map features

## Limitations

1. **Grid labels** may not display on all projections (e.g., orthographic)
2. **Cardinal markers** use fixed positions that work best with global/hemisphere views
3. For very zoomed regional maps (`--extent`), cardinal markers may be outside view
4. Labels can overlap with data points - adjust placement or size as needed

## See Also

- README.md - Main documentation
- QUICKREF.md - Quick reference for all options
- Grid options: --grid-spacing, --grid-color, --grid-alpha, --grid-style

## Examples in Other Docs

See these files for more examples:
- demo_sky.sh - Automated sky map examples
- test.sh - Terrestrial map tests
- QUICKREF.md - Quick command examples
