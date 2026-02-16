# mapplot Quick Reference

## Installation
```bash
pip3 install matplotlib cartopy numpy astropy
chmod +x install.sh && ./install.sh
```

## Important Changes
- **Sky mode is now DEFAULT** - No --sky flag needed
- **Earth maps need --earth** - Use `--earth` for terrestrial maps
- **Grid default is 30°** - Use `--grid-spacing 15 15` for finer grid

## Exit Tips
- **Interactive mode**: Close the plot window to exit cleanly
- **No window**: Use `-o FILE` to save without displaying
- **Ctrl-C**: Will exit but may show error message (closing window is cleaner)

## Sky Maps (Default Mode)

### Basic Commands
```bash
# BSC5 star catalog (no --sky needed!)
mapplot --catalog -p mollweide -g

# With magnitude limit
mapplot --catalog --max-mag 4.5 -p hammer -g

# Black background (astronomy style)
mapplot --catalog -g --bgcolor black --grid-color white

# With overlays
mapplot --catalog --ecliptic --galactic-plane -p aitoff -g

# Milky Way density
mapplot --catalog --milky-way -p robinson -g

# Text labels from file (3rd column)
mapplot --labels-from-file objects.txt -p hammer -g

# Show coordinate system poles (NEW!)
mapplot --catalog --ecliptic --poles ecliptic
mapplot --catalog --poles all  # All poles

# Grid in different coordinates (NEW!)
mapplot --catalog --grid-coord galactic -g

# Solar-relative coordinates (NEW!)
mapplot --solar-relative asteroid.txt -p mollweide -g
mapplot --solar-relative --solar-center 90 comet.txt -g

# Grid labels and cardinal directions (NEW!)
mapplot --catalog -g --grid-labels -p plate-carree --cardinal -p plate-carree
mapplot --earth cities.txt -g --grid-labels -p plate-carree --cardinal
```

### Magnitude Cutoffs
```bash
--max-mag 2.0    # Brightest stars (navigation)
--max-mag 4.5    # Urban sky limit
--max-mag 6.0    # Default
--max-mag 6.5    # Dark sky / full BSC5
```

### Coordinate Systems
```bash
# Galactic coordinates
mapplot --catalog --plot-coord galactic -p hammer -g

# Ecliptic coordinates
mapplot --catalog --plot-coord ecliptic -p aitoff -g

# Transform: input galactic, plot equatorial
mapplot --input-coord galactic --plot-coord equatorial data.txt
```

### Solar System Objects
```bash
# Plot on ecliptic plane
mapplot --ecliptic --plot-coord ecliptic \
  asteroids.txt -p eckert4 -g -c orange
```

## Earth Maps (Now Require --earth)

```bash
# Basic
mapplot --earth cities.txt

# With projection and grid  
mapplot --earth -p mollweide -g cities.txt

# Multiple files
mapplot --earth -c red -c blue file1.txt file2.txt

# Variable sizes
mapplot --earth -s 50 cities_pop.txt

# All observatories from MPC (NEW!)
mapplot --earth --observatories -p robinson -g

# Specific observatories (NEW!)
mapplot --earth --obs-codes 675 704 G96 -p mercator -g
```

## Key Options

```
--earth               Earth/terrestrial mode (sky is default)
--catalog             Show BSC5 stars
--max-mag MAG         Maximum magnitude (default: 6.0)
--ecliptic            Show ecliptic plane
--galactic-plane      Show galactic plane
--celestial-equator   Show celestial equator (NEW!)
--milky-way           Show Milky Way density
--poles SYSTEMS       Show poles (equatorial/ecliptic/galactic/all) (NEW!)
--observatories       Show all MPC observatories (terrestrial) (NEW!)
--obs-codes CODES     Show specific observatories (NEW!)
--input-coord SYS     Input: equatorial/ecliptic/galactic
--plot-coord SYS      Plot: equatorial/ecliptic/galactic
--grid-coord SYS      Grid: equatorial/ecliptic/galactic (NEW!)
--solar-relative      Solar-relative coords (input: MJD RA Dec) (NEW!)
--solar-center DEG    Center at solar elongation (default: 180) (NEW!)
--labels-from-file    Use 3rd column as text labels
--ignore-extra        Ignore columns beyond first two
-p PROJ               Projection
-g                    Gridlines (30° default)
--grid-spacing X Y    Custom grid spacing
--grid-labels -p plate-carree         Show axis labels on gridlines (NEW!)
--cardinal            Show cardinal directions (N, S, E, W) (NEW!)
--bgcolor COLOR       Background color
--facecolor COLOR     Axes color
--grid-color COLOR    Grid color
--grid-alpha ALPHA    Grid transparency
-c COLOR              Marker color
-s SIZE               Marker size
-m MARKER             Marker shape
-o FILE               Output file
--figsize W H         Figure size
--dpi DPI             Resolution
--title TEXT          Title
--legend              Show legend
```

**New in this version:**
- `--solar-relative` - Plot objects relative to Sun (asteroids, comets)
- `--solar-center` - Customize solar elongation centering
- `--poles` - Show coordinate system poles
- `--grid-coord` - Grid in different coordinate system  
- `--celestial-equator` - Show celestial equator
- `--observatories` - Plot MPC observatories
- `--observatories` - Plot MPC observatories
- `--obs-codes` - Plot specific observatory codes

## Projections

**Best for sky:** mollweide, hammer, aitoff, robinson, eckert4
**Best for Earth:** robinson, mollweide, mercator, plate-carree

## Data Format

### Sky Data
```
# RA Dec (equatorial, degrees)
83.63 -5.39         # M42 Orion Nebula

# l b (galactic, degrees)  
0.0 0.0             # Galactic center

# lon lat (ecliptic, degrees)
45.0 10.5
```

### Earth Data
```
# longitude latitude
-74.0060 40.7128    # New York
```

## Examples

### Complete Sky Map
```bash
mapplot --sky --catalog --ecliptic --galactic-plane --milky-way \
  -p mollweide -g --grid-spacing 15 15 \
  --bgcolor black --grid-color white --legend \
  -o allsky.png
```

### Publication Figure
```bash
mapplot --sky --catalog --max-mag 5.0 --ecliptic --galactic-plane \
  -p robinson -g --figsize 16 10 --dpi 300 \
  --title "Celestial Sphere (BSC5)" --legend \
  -o publication.png
```

### Solar System
```bash
mapplot --sky --catalog --ecliptic \
  planets.txt -p eckert4 -g \
  -m star -c red -s 200 --legend
```

## BSC5 Information

**Bright Star Catalogue, 5th Edition**
- Source: http://tdc-www.harvard.edu/catalogs/bsc5.html
- 9,110 stars visible to naked eye
- Magnitudes: -1.5 to ~6.5
- Complete: RA, Dec, magnitude, spectral type

**Data file:** `bsc5_data.txt`
- Must be in same directory as mapplot
- Or in `~/.local/share/mapplot/`
- Format: HR_num Name RA_hrs Dec_deg V_mag SpectralType

## Quick Tips

- Sky mode: always use `--sky`
- Default grid: 15° for sky, 30° for Earth
- Star sizes scale with magnitude (brighter = larger)
- Black background: `--bgcolor black --grid-color white`
- Interactive: omit `-o` to zoom/pan
- High-res: `--dpi 300 --figsize 16 10`
