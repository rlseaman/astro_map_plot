# New Features: Poles and Grid Coordinate Systems

## 1. Coordinate System Poles

Display the north and south poles of celestial coordinate systems.

### Usage

```bash
# Show ecliptic poles (darkorange X markers)
mapplot --catalog --ecliptic --poles ecliptic

# Show galactic poles (cyan squares)
mapplot --catalog --galactic-plane --poles galactic

# Show equatorial poles (lime triangles)
mapplot --catalog --celestial-equator --poles equatorial

# Show all poles at once
mapplot --catalog --poles all

# Combine multiple
mapplot --catalog --poles ecliptic galactic
```

### Pole Locations

**Equatorial Poles (Celestial Poles):**
- North Celestial Pole (NCP): RA=0°, Dec=+90°
- South Celestial Pole (SCP): RA=0°, Dec=-90°
- Marker: Green triangle (^)
- Near Polaris for NCP

**Ecliptic Poles:**
- North Ecliptic Pole (NEP): Ecliptic lon=0°, lat=+90°
- South Ecliptic Pole (SEP): Ecliptic lon=0°, lat=-90°
- Marker: Red X
- In equatorial: NEP at RA≈270°, Dec≈+66.6°

**Galactic Poles:**
- North Galactic Pole (NGP): Galactic l=0°, b=+90°
- South Galactic Pole (SGP): Galactic l=0°, b=-90°
- Marker: Blue square
- In equatorial: NGP at RA≈192.9°, Dec≈+27.1°

### Coordinate Transformations

Poles are automatically transformed to match your plot coordinate system:

```bash
# Plot in equatorial, show ecliptic poles (transformed)
mapplot --catalog --plot-coord equatorial --poles ecliptic -p mollweide -g

# Plot in galactic, show all poles (all transformed)
mapplot --catalog --plot-coord galactic --poles all -p hammer -g
```

## 2. Grid Coordinate System

Display gridlines in a different coordinate system than the plot coordinates.

### Usage

```bash
# Data and plot in equatorial, but grid in galactic coordinates
mapplot --catalog --plot-coord equatorial --grid-coord galactic -g

# Data in galactic, plot in equatorial, grid in ecliptic
mapplot --input-coord galactic --plot-coord equatorial --grid-coord ecliptic -g

# Show where galactic grid lines appear in equatorial view
mapplot --catalog --grid-coord galactic --grid-spacing 30 30 -g
```

### Why This Is Useful

1. **Visualize coordinate system relationships:**
   - See how galactic coordinates overlay on equatorial views
   - Understand coordinate transformations visually

2. **Multi-wavelength astronomy:**
   - Plot in one system, grid in another for reference
   - Useful for comparing surveys in different systems

3. **Educational:**
   - Show students how different coordinate systems relate
   - Demonstrate coordinate transformations

### Examples

**Example 1: Galactic grid on equatorial plot**
```bash
mapplot --catalog --ecliptic --galactic-plane \
  --plot-coord equatorial --grid-coord galactic -g \
  --grid-spacing 30 30 -p mollweide \
  --title "Equatorial View with Galactic Grid"
```

**Example 2: All three systems visualized**
```bash
mapplot --catalog \
  --ecliptic --galactic-plane --celestial-equator \
  --poles all \
  --plot-coord equatorial --grid-coord galactic -g \
  -p hammer --legend \
  --title "Multi-Coordinate System View"
```

**Example 3: Ecliptic grid on galactic plot**
```bash
mapplot --catalog \
  --plot-coord galactic --grid-coord ecliptic -g \
  --grid-spacing 30 30 -p aitoff \
  --title "Galactic View with Ecliptic Grid"
```

## 3. Celestial Equator

The celestial equator is now available as an overlay (like ecliptic and galactic plane).

### Usage

```bash
# Show celestial equator
mapplot --catalog --celestial-equator -p mollweide -g

# With equatorial poles
mapplot --catalog --celestial-equator --poles equatorial

# All three reference planes
mapplot --catalog --ecliptic --galactic-plane --celestial-equator \
  -p hammer -g --legend
```

The celestial equator is plotted in lime to match the equatorial poles.

## Complete Example

Here's a comprehensive example showing all new features:

```bash
mapplot --catalog --max-mag 5.0 \
  --ecliptic --galactic-plane --celestial-equator \
  --poles all \
  --plot-coord equatorial --grid-coord galactic \
  -g --grid-spacing 30 15 \
  -p mollweide \
  --bgcolor black --grid-color white --grid-alpha 0.3 \
  --legend \
  --title "Complete Celestial Coordinate Reference" \
  -o complete_sky_reference.png
```

This creates a map showing:
- BSC5 stars (mag ≤ 5.0)
- Ecliptic plane (darkorange line)
- Galactic plane (cyan line)
- Celestial equator (green line)
- All coordinate system poles (colored markers)
- Galactic coordinate grid (30° × 15°)
- All in equatorial plotting coordinates

## Quick Reference

### Pole Options
```
--poles equatorial    # Green triangles
--poles ecliptic      # Red X markers
--poles galactic      # Blue squares
--poles all           # Show all poles
--poles ecliptic galactic  # Multiple systems
```

### Grid Options
```
--grid-coord equatorial    # Grid in RA/Dec
--grid-coord ecliptic      # Grid in ecliptic lon/lat
--grid-coord galactic      # Grid in galactic l/b
```

### Reference Planes
```
--ecliptic            # Ecliptic plane (red)
--galactic-plane      # Galactic plane (blue)
--celestial-equator   # Celestial equator (green)
```

## Color Coding

- **Red:** Ecliptic system (ecliptic plane, ecliptic poles)
- **Blue:** Galactic system (galactic plane, galactic poles)
- **Green:** Equatorial system (celestial equator, celestial poles)

This consistent color coding helps distinguish between coordinate systems on complex plots.

## Notes

1. Poles are always plotted with size 150 and black edges for visibility
2. Grid coordinates can be independent of both input and plot coordinates
3. All transformations are done using astropy for accuracy
4. Discontinuities in transformed coordinates are handled automatically
