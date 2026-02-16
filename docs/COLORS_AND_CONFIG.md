# Colors and Configuration

## Overview

mapplot now supports:
1. **Professional color palettes** for data series (avoiding conflicts with reference lines)
2. **YAML configuration files** for setting defaults
3. **Classic RGB colors** for reference lines (red/green/blue)

## Color System

### Reference Lines (Fixed Colors)

Reference lines use classic, memorable colors:

| Feature | Color | Why |
|---------|-------|-----|
| **Ecliptic** plane & poles | 🔴 Red | Traditional astronomy color |
| **Celestial Equator** & poles | 🟢 Green | Earth's equator projection |
| **Galactic** plane & poles | 🔵 Blue | Milky Way structure |

These colors are **reserved** for reference frames and don't change.

### Data Series (Professional Palettes)

Data from multiple input files uses carefully chosen color palettes that **avoid red, green, and blue** to prevent conflicts with reference lines.

#### Available Palettes

**Tableau 10** (default) - Industry standard, colorblind-friendly:
```
#4E79A7 (steel blue)
#F28E2B (orange) 
#E15759 (coral)
#76B7B2 (teal)
#59A14F (green-teal)
#EDC948 (gold)
#B07AA1 (mauve)
#FF9DA7 (pink)
#9C755F (brown)
#BAB0AC (gray)
```

**Set2** - ColorBrewer, excellent for print:
```
#66C2A5 (mint)
#FC8D62 (orange)
#8DA0CB (lavender)
#E78AC3 (pink)
#A6D854 (lime)
#FFD92F (yellow)
#E5C494 (tan)
#B3B3B3 (gray)
```

**Vibrant** - High contrast, attention-grabbing:
```
#EE7733 (orange)
#0077BB (blue)
#33BBEE (cyan)
#EE3377 (magenta)
#CC3311 (red)
#009988 (teal)
#BBBBBB (gray)
```

**Muted** - Subtle, professional:
```
#CC6677 (rose)
#332288 (indigo)
#DDCC77 (sand)
#117733 (forest)
#88CCEE (sky)
#882255 (wine)
#44AA99 (teal)
#999933 (olive)
#AA4499 (purple)
```

**Default** - Classic (for compatibility):
```
red, blue, green, orange, purple, brown, pink, gray
```

### Choosing a Palette

**Command line:**
```bash
# Use Tableau 10 (default)
mapplot file1.txt file2.txt file3.txt

# Use Set2
mapplot --palette set2 file1.txt file2.txt file3.txt

# Use Vibrant
mapplot --palette vibrant file1.txt file2.txt
```

**In config file:**
```yaml
colors:
  data_palette: tableau10  # or set2, vibrant, muted, default
```

## Configuration Files

### Quick Start

1. Copy the example config:
```bash
cp mapplotrc.example ~/.mapplotrc
```

2. Edit to your preferences:
```bash
nano ~/.mapplotrc
```

3. Use automatically (or specify with `--config`):
```bash
mapplot data.txt  # Uses ~/.mapplotrc
mapplot --config myconfig.yaml data.txt  # Uses specific config
```

### Configuration File Format

mapplot uses **YAML** format for configuration files. YAML is human-readable and supports comments.

**Example ~/.mapplotrc:**
```yaml
# My mapplot defaults

display:
  projection: hammer           # I prefer Hammer projection
  figsize: [14, 9]            # Larger figure
  dpi: 150                    # Higher resolution
  bgcolor: '#F5F5F5'          # Light gray background

grid:
  spacing: [15, 15]           # Finer grid (15° instead of 30°)
  color: '#333333'            # Dark gray grid
  alpha: 0.3                  # More subtle

colors:
  data_palette: set2          # ColorBrewer palette

celestial:
  max_mag: 5.0                # Only brightest stars

paths:
  bsc5_data: ~/astronomy/catalogs/bsc5.txt
```

### Configuration Precedence

Settings are applied in this order (later overrides earlier):

1. **Built-in defaults** (in DEFAULT_CONFIG)
2. **Config file** (~/.mapplotrc or specified with --config)
3. **Command-line arguments** (always win)

Example:
```yaml
# ~/.mapplotrc
display:
  projection: mollweide
  figsize: [12, 8]
```

```bash
# This uses mollweide (from config) with [16, 10] (from command line)
mapplot --figsize 16 10 data.txt

# This uses plate-carree (command line overrides config)
mapplot -p plate-carree data.txt
```

### Available Settings

#### Display Section
```yaml
display:
  projection: plate-carree    # Map projection
  figsize: [12, 8]            # Width, height in inches
  dpi: 100                    # Resolution
  bgcolor: white              # Background color
  facecolor: null             # Axes color (null = transparent)
```

#### Grid Section
```yaml
grid:
  spacing: [30, 30]           # [longitude, latitude] spacing
  color: gray                 # Line color
  alpha: 0.5                  # Transparency (0-1)
  style: '--'                 # Line style (-- - : etc)
```

#### Colors Section
```yaml
colors:
  data_palette: tableau10     # Palette name
  ecliptic: red              # Reference colors (don't change these)
  equator: green
  galactic: blue
```

#### Celestial Section
```yaml
celestial:
  max_mag: 6.0                # Star catalog magnitude limit
```

#### Paths Section
```yaml
paths:
  config: ~/.mapplotrc
  bsc5_data: ~/.local/share/mapplot/bsc5_data.txt
  mpc_observatories: ~/.local/share/mapplot/mpc_observatories.txt
```

### Partial Configuration

You only need to specify settings you want to change:

```yaml
# Minimal config - just change projection and palette
display:
  projection: hammer

colors:
  data_palette: vibrant
```

### Multiple Configurations

You can have different config files for different purposes:

```bash
# Default setup
mapplot data.txt

# Presentation mode
mapplot --config ~/.mapplotrc-presentation data.txt

# Publication mode
mapplot --config ~/.mapplotrc-publication data.txt
```

**Example ~/.mapplotrc-presentation:**
```yaml
display:
  figsize: [16, 9]            # Widescreen
  dpi: 150                    # Sharp on projector
  bgcolor: black              # Dark background

grid:
  color: white                # White grid on black
  alpha: 0.3

colors:
  data_palette: vibrant       # High contrast
```

**Example ~/.mapplotrc-publication:**
```yaml
display:
  figsize: [12, 8]
  dpi: 300                    # Print quality
  bgcolor: white

grid:
  color: '#666666'            # Gray for print
  alpha: 0.4

colors:
  data_palette: set2          # Colorblind-friendly
```

## Examples

### Example 1: Multiple Data Files with Distinct Colors

```bash
# Default Tableau 10 palette
mapplot survey1.txt survey2.txt survey3.txt survey4.txt \
  --legend --labels "Survey A" "Survey B" "Survey C" "Survey D"
```

Each survey gets a distinct color from Tableau 10 palette:
- Survey A: Steel blue (#4E79A7)
- Survey B: Orange (#F28E2B)
- Survey C: Coral (#E15759)
- Survey D: Teal (#76B7B2)

Reference lines (if shown) remain red/green/blue and don't conflict.

### Example 2: Reference Lines with Data

```bash
mapplot --catalog --ecliptic --galactic-plane --celestial-equator \
  asteroid.txt comet.txt \
  --palette set2 \
  --legend --labels "Asteroids" "Comets" \
  -p plate-carree -g
```

Result:
- Stars: Yellow (catalog default)
- Ecliptic: Red line (reference)
- Galactic plane: Blue line (reference)
- Celestial equator: Green line (reference)
- Asteroids: Mint (#66C2A5) from Set2
- Comets: Orange (#FC8D62) from Set2

No color conflicts - everything is clearly distinguishable!

### Example 3: Using Config for Consistent Style

**~/.mapplotrc:**
```yaml
display:
  projection: hammer
  figsize: [14, 9]
  dpi: 150
  bgcolor: '#1a1a1a'          # Dark gray

grid:
  color: '#444444'
  alpha: 0.5

colors:
  data_palette: vibrant       # Bright colors on dark background
```

```bash
# All these use your config automatically
mapplot asteroids.txt
mapplot --catalog observations.txt
mapplot --solar-relative comet_track.txt
```

Every plot will have consistent dark theme with vibrant colors!

## Tips

1. **Start simple** - Copy mapplotrc.example and change just what you need

2. **Test your config:**
   ```bash
   mapplot --config test.yaml data.txt
   ```

3. **Override when needed** - Command line always wins:
   ```bash
   # Uses config projection except today
   mapplot -p mercator data.txt
   ```

4. **Colorblind-friendly** - Tableau 10 and Set2 are designed for accessibility

5. **Print vs screen** - Set2 is great for print, Vibrant for presentations

6. **Comments** - YAML supports comments (#), use them!
   ```yaml
   # This is for my asteroid survey project
   display:
     projection: hammer  # I prefer equal-area
   ```

7. **Color names** - You can use:
   - Names: `red`, `blue`, `forestgreen`
   - Hex: `#FF0000`, `#4E79A7`
   - RGB: Not directly in YAML, but in command line

## Requirements

Configuration file support requires PyYAML:
```bash
pip install pyyaml
```

If PyYAML is not installed, mapplot will use built-in defaults and ignore config files (with a warning).

## Migration from Old Version

If you used custom colors before:

**Old way:**
```bash
mapplot file1.txt file2.txt -c red -c blue
```

**New way (same result):**
```bash
mapplot file1.txt file2.txt -c red -c blue  # Still works!
```

**Or use palette:**
```bash
mapplot file1.txt file2.txt --palette default  # Uses old default colors
```

## See Also

- mapplotrc.example - Full example configuration file
- README.md - Main documentation
- QUICKREF.md - Quick command reference
- Color palette sources:
  - Tableau: https://www.tableau.com/about/blog/2016/7/colors-upgrade-tableau-10-56782
  - ColorBrewer: https://colorbrewer2.org/
