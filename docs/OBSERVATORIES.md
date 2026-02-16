# Observatory Plotting Feature

Plot astronomical observatory locations from the Minor Planet Center (MPC) database.

## Data Source

Observatory codes from: https://www.minorplanetcenter.net/iau/lists/ObsCodesF.html

The MPC maintains a comprehensive database of observatory locations worldwide, including:
- Professional observatories
- Amateur observatories
- Satellite observatories
- Spacecraft
- Roving observers

## Usage

### Plot All Observatories

```bash
# Show all observatories on a world map
mapplot --earth --observatories -p robinson -g

# With coastlines and countries
mapplot --earth --observatories --countries -p mollweide -g

# Zoom to a region
mapplot --earth --observatories --extent -130,-60,20,50 -p mercator
```

### Plot Specific Observatories

```bash
# Show specific observatory codes
mapplot --earth --obs-codes 675 704 G96 -p robinson -g

# Major observatories
mapplot --earth --obs-codes 675 704 568 645 691 -p mollweide -g \
  --title "Major Observatories"

# European observatories
mapplot --earth --obs-codes 004 012 089 950 -p lambert-conformal -g
```

### Common Observatory Codes

**Major Professional Observatories:**
- **675** - Palomar Mountain (California, USA)
- **704** - Apache Point (New Mexico, USA)
- **568** - Mauna Kea (Hawaii, USA)
- **645** - Cerro Tololo (Chile)
- **691** - Steward Observatory (Arizona, USA)
- **809** - Catalina Sky Survey (Arizona, USA)
- **G96** - Mt. Lemmon Survey (Arizona, USA)
- **950** - La Silla (Chile)
- **V37** - Haleakala (Hawaii, USA)
- **J04** - Mauna Kea UH88 (Hawaii, USA)

**Historic/Famous Observatories:**
- **000** - Greenwich (England)
- **004** - Haute-Provence (France)
- **012** - Lowell Observatory (Arizona, USA)
- **089** - Lick Observatory (California, USA)

**Space Observatories:**
- **245** - Spitzer Space Telescope
- **250** - Hubble Space Telescope
- **C51** - WISE
- **C57** - TESS

## Data Format

The MPC observatory file uses a special format:
```
Code Longitude rho*cos(phi) rho*sin(phi) Name
```

Where:
- **Code**: 3-character observatory code
- **Longitude**: East longitude in degrees (0-360°)
- **rho*cos(phi)**: Cosine component (rho = Earth radii)
- **rho*sin(phi)**: Sine component
- **phi**: Geocentric latitude

### Coordinate Conversion

The tool automatically converts from cos/sin to latitude:

```python
# Given rho*cos(phi) and rho*sin(phi)
latitude = arctan2(rho*sin(phi), rho*cos(phi))

# Convert longitude to standard range
if longitude > 180:
    longitude = longitude - 360
```

## Examples

### Example 1: World Observatory Map

```bash
mapplot --earth --observatories -p robinson -g \
  --title "MPC Observatory Network" \
  -o world_observatories.png
```

### Example 2: North American Observatories

```bash
mapplot --earth --observatories \
  --extent -130,-60,20,50 \
  -p mercator -g \
  --title "North American Observatories"
```

### Example 3: Specific Observatory List

```bash
mapplot --earth --obs-codes 675 704 568 645 691 809 G96 \
  -p robinson -g --countries \
  --title "Major Survey Telescopes"
```

### Example 4: Amateur Observatory Network

```bash
# List your local observatory codes
mapplot --earth --obs-codes H01 J47 K92 L01 \
  --extent -10,10,35,55 \
  -p lambert-conformal -g \
  --title "European Amateur Network"
```

### Example 5: Compare with Cities

```bash
# Plot observatories along with cities
mapplot --earth cities.txt --obs-codes 675 704 568 -p robinson -g \
  -c blue -m circle --legend \
  --labels "Cities" "Observatories"
```

## Features

### Automatic Download
The tool automatically downloads the latest observatory data from MPC when needed.

### Local Cache
You can save the observatory file locally and use it:

```bash
# Download once
curl -o observatories.txt \
  https://www.minorplanetcenter.net/iau/lists/ObsCodesF.html

# Use local file
mapplot --earth --observatories --obs-file observatories.txt -p robinson -g
```

### Smart Labeling
- **≤ 50 observatories**: Shows codes as labels
- **> 50 observatories**: Shows only markers (to avoid clutter)

### Visual Style
- **Marker**: Red triangle (^) pointing up
- **Edge**: Dark red border
- **Size**: 50 points
- **Transparency**: 80%
- **Layer**: On top (zorder=5)

## Finding Observatory Codes

### Search the MPC Website
1. Visit: https://minorplanetcenter.net/iau/lists/ObsCodes.html
2. Search for your observatory name
3. Note the 3-character code

### Common Patterns
- **Numeric codes (000-999)**: Traditional ground observatories
- **Letter codes (A00-Z99)**: Modern observatories
- **Space codes**: Various formats for spacecraft

### By Country/Region

**United States:**
- 675 (Palomar), 704 (Apache Point), 691 (Steward), 689 (Lick)
- 309 (Kitt Peak), 568 (Mauna Kea), 695 (Mt. Hopkins)

**Chile:**
- 304 (Cerro Tololo), 807 (Cerro Paranal), 809 (La Silla)

**Hawaii:**
- 568 (Mauna Kea), 608 (Haleakala), 266 (Mauna Loa)

**Australia:**
- 413 (Siding Spring), 260 (Perth), 246 (Charters Towers)

**Europe:**
- 000 (Greenwich), 004 (Haute-Provence), 089 (Heidelberg)
- 950 (Calar Alto), 021 (Torun), 030 (Caussols)

## Advanced Usage

### High-Resolution Regional Map

```bash
mapplot --earth --observatories \
  --extent -125,-100,30,45 \
  -p mercator -g --grid-spacing 5 5 \
  --countries --figsize 16 12 --dpi 300 \
  --title "Southwestern US Observatories" \
  -o southwest_obs_hires.png
```

### Combination Plot

```bash
# Show observatories with custom data
mapplot --earth --observatories \
  my_observation_sites.txt \
  -p robinson -g \
  -c red -c blue \
  --legend \
  --labels "MPC Observatories" "My Sites"
```

### Publication Figure

```bash
mapplot --earth --obs-codes 675 704 568 645 691 \
  -p robinson -g --countries \
  --figsize 12 8 --dpi 300 \
  --title "Major Asteroid Survey Facilities" \
  --bgcolor white --facecolor white \
  -o publication_observatories.png
```

## Notes

- Observatory data is downloaded from MPC on first use
- Conversion from geocentric to geodetic latitude is automatic
- Some codes may be for spacecraft or satellites (not ground-based)
- The MPC database contains 2000+ observatory codes
- Labels are only shown for ≤50 observatories to maintain readability

## Troubleshooting

**"Could not download MPC observatories"**
- Check internet connection
- Try using `--obs-file` with a local copy
- Download manually from the MPC website

**"No observatories found with codes: ..."**
- Check that codes are exactly 3 characters
- Codes are case-insensitive
- Verify codes exist in the MPC database

**Too many labels overlapping:**
- Use `--obs-codes` to show specific observatories
- Zoom to a smaller region with `--extent`
- Labels are automatically hidden if > 50 observatories

## References

- MPC Observatory Codes: https://minorplanetcenter.net/iau/lists/ObsCodes.html
- MPC Data Format: https://minorplanetcenter.net/iau/lists/ObsCodesF.html
- About Observatory Codes: https://minorplanetcenter.net/iau/info/ObsDetails.html
