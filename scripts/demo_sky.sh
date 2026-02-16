#!/bin/bash
# Demonstration of sky mapping capabilities
# Run from the astro_map_plot root directory

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
MAPPLOT="$ROOT_DIR/src/mapplot"
DATA_DIR="$ROOT_DIR/data"
OUTPUT_DIR="$ROOT_DIR/sandbox"

# Ensure mapplot is executable
chmod +x "$MAPPLOT"

echo "Sky Mapping Demonstration"
echo "========================="
echo ""

echo "1. Basic sky map with bright star catalog..."
"$MAPPLOT" --sky --catalog -p mollweide -g \
  --grid-spacing 15 15 \
  --bgcolor black --grid-color white --grid-alpha 0.3 \
  -o "$OUTPUT_DIR/demo_sky_basic.png" \
  --title "Bright Star Catalog (Magnitude < 6.0)"

echo "Created: $OUTPUT_DIR/demo_sky_basic.png"
echo ""

echo "2. Sky map with ecliptic and galactic plane..."
"$MAPPLOT" --sky --catalog --ecliptic --galactic-plane \
  -p hammer -g --grid-spacing 15 15 \
  --bgcolor black --grid-color cyan --grid-alpha 0.3 \
  --legend \
  -o "$OUTPUT_DIR/demo_sky_overlays.png" \
  --title "Celestial Sphere with Ecliptic and Galactic Plane"

echo "Created: $OUTPUT_DIR/demo_sky_overlays.png"
echo ""

echo "3. Sky map with Milky Way density..."
"$MAPPLOT" --sky --catalog --galactic-plane --milky-way \
  -p mollweide -g --grid-spacing 30 15 \
  --bgcolor black --grid-color white --grid-alpha 0.2 \
  --legend \
  -o "$OUTPUT_DIR/demo_milky_way.png" \
  --title "Milky Way Structure"

echo "Created: $OUTPUT_DIR/demo_milky_way.png"
echo ""

echo "4. Galactic coordinate system view..."
"$MAPPLOT" --sky --catalog --ecliptic \
  --plot-coord galactic \
  -p aitoff -g --grid-spacing 30 15 \
  --bgcolor navy --grid-color yellow --grid-alpha 0.4 \
  --legend \
  -o "$OUTPUT_DIR/demo_galactic_coords.png" \
  --title "Galactic Coordinates with Ecliptic"

echo "Created: $OUTPUT_DIR/demo_galactic_coords.png"
echo ""

echo "5. Ecliptic coordinate system view..."
"$MAPPLOT" --sky --catalog --galactic-plane \
  --plot-coord ecliptic \
  -p hammer -g --grid-spacing 30 15 \
  --bgcolor midnightblue --grid-color gold --grid-alpha 0.4 \
  --legend \
  -o "$OUTPUT_DIR/demo_ecliptic_coords.png" \
  --title "Ecliptic Coordinates with Galactic Plane"

echo "Created: $OUTPUT_DIR/demo_ecliptic_coords.png"
echo ""

echo "6. Custom objects (Messier catalog) in equatorial coordinates..."
"$MAPPLOT" --sky --catalog --ecliptic --galactic-plane \
  -p mollweide -g --grid-spacing 15 15 \
  --bgcolor black --grid-color white --grid-alpha 0.2 \
  -m diamond -c cyan -s 100 \
  --legend --labels "Stars" "Ecliptic" "Galactic Plane" "Messier Objects" \
  -o "$OUTPUT_DIR/demo_messier.png" \
  --title "Messier Objects and Bright Stars" \
  "$DATA_DIR/example_messier.txt"

echo "Created: $OUTPUT_DIR/demo_messier.png"
echo ""

echo "7. High-resolution publication figure..."
"$MAPPLOT" --sky --catalog --max-magnitude 5.0 \
  --ecliptic --galactic-plane --milky-way \
  -p robinson -g --grid-spacing 15 15 \
  --bgcolor black --grid-color lightgray --grid-alpha 0.25 \
  --figsize 16 10 --dpi 300 \
  --legend \
  -o "$OUTPUT_DIR/demo_publication.png" \
  --title "All-Sky Map with Celestial Features"

echo "Created: $OUTPUT_DIR/demo_publication.png (high resolution)"
echo ""

echo "8. Different projections comparison..."
for proj in mollweide hammer aitoff robinson eckert4; do
  "$MAPPLOT" --sky --catalog --ecliptic --galactic-plane \
    -p $proj -g --grid-spacing 30 15 \
    --bgcolor black --grid-color white --grid-alpha 0.3 \
    -o "$OUTPUT_DIR/demo_proj_${proj}.png" \
    --title "Projection: ${proj}"
  echo "  Created: $OUTPUT_DIR/demo_proj_${proj}.png"
done

echo ""
echo "9. Coordinate transformation example..."
# Create a temporary sample file in galactic coordinates
TMPFILE=$(mktemp)
cat > "$TMPFILE" << EOF
# Galactic coordinates (l, b)
0 0      # Galactic center direction
180 0    # Anti-center
90 0
270 0
45 45
135 -30
EOF

"$MAPPLOT" --sky --catalog \
  --input-coord galactic --plot-coord equatorial \
  -p mollweide -g --grid-spacing 15 15 \
  --bgcolor black --grid-color white --grid-alpha 0.3 \
  -m square -c red -s 200 \
  --legend --labels "Stars" "Galactic Points" \
  -o "$OUTPUT_DIR/demo_coord_transform.png" \
  --title "Galactic Coordinates Transformed to Equatorial" \
  "$TMPFILE"

echo "Created: $OUTPUT_DIR/demo_coord_transform.png"
rm "$TMPFILE"

echo ""
echo "10. Terrestrial map for comparison..."
"$MAPPLOT" -p robinson -g --grid-spacing 30 15 \
  --coastlines --countries \
  --grid-color blue --grid-alpha 0.5 \
  -o "$OUTPUT_DIR/demo_earth.png" \
  --title "Earth Map (for comparison)" \
  "$DATA_DIR/example_cities.txt"

echo "Created: $OUTPUT_DIR/demo_earth.png"
echo ""

echo "========================="
echo "All demonstrations complete!"
echo ""
echo "Created sky maps in $OUTPUT_DIR/:"
echo "  - demo_sky_basic.png (basic star catalog)"
echo "  - demo_sky_overlays.png (with ecliptic and galactic plane)"
echo "  - demo_milky_way.png (with Milky Way density)"
echo "  - demo_galactic_coords.png (galactic coordinate system)"
echo "  - demo_ecliptic_coords.png (ecliptic coordinate system)"
echo "  - demo_messier.png (Messier objects)"
echo "  - demo_publication.png (high-res publication quality)"
echo "  - demo_proj_*.png (various projections)"
echo "  - demo_coord_transform.png (coordinate transformation)"
echo "  - demo_earth.png (terrestrial map)"
