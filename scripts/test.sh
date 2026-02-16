#!/bin/bash
# Quick test script for mapplot
# Run from the astro_map_plot root directory

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$ROOT_DIR/data"
OUTPUT_DIR="$ROOT_DIR/sandbox"

echo "Testing mapplot installation..."
echo ""

# Test 1: Help
echo "Test 1: Checking help output..."
python -m mapplot -h > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "  PASS: Help works"
else
    echo "  FAIL: Help failed"
    exit 1
fi

# Test 2: List projections
echo ""
echo "Test 2: Available projections:"
python -m mapplot -h | grep -A 30 "Available projections:" | head -20

# Test 3: Create a simple map
echo ""
echo "Test 3: Creating test map..."
python -m mapplot -p mollweide -o "$OUTPUT_DIR/test_map.png" "$DATA_DIR/example_cities.txt"
if [ -f "$OUTPUT_DIR/test_map.png" ]; then
    echo "  PASS: Basic map created successfully: $OUTPUT_DIR/test_map.png"
else
    echo "  FAIL: Map creation failed"
    exit 1
fi

# Test 4: Test with gridlines
echo ""
echo "Test 4: Creating map with gridlines..."
python -m mapplot -p hammer -g -o "$OUTPUT_DIR/test_grid.png" "$DATA_DIR/example_cities.txt"
if [ -f "$OUTPUT_DIR/test_grid.png" ]; then
    echo "  PASS: Map with gridlines created: $OUTPUT_DIR/test_grid.png"
else
    echo "  FAIL: Gridlines test failed"
fi

# Test 5: Variable sizes
echo ""
echo "Test 5: Creating map with variable sizes..."
python -m mapplot -p robinson -s 10 -o "$OUTPUT_DIR/test_sizes.png" "$DATA_DIR/example_cities_pop.txt"
if [ -f "$OUTPUT_DIR/test_sizes.png" ]; then
    echo "  PASS: Map with variable sizes created: $OUTPUT_DIR/test_sizes.png"
else
    echo "  FAIL: Variable sizes test failed"
fi

# Test 6: Colormap
echo ""
echo "Test 6: Creating map with colormap..."
python -m mapplot -p eckert4 --cmap coolwarm --cbar -o "$OUTPUT_DIR/test_colormap.png" "$DATA_DIR/example_temperature.txt"
if [ -f "$OUTPUT_DIR/test_colormap.png" ]; then
    echo "  PASS: Map with colormap created: $OUTPUT_DIR/test_colormap.png"
else
    echo "  FAIL: Colormap test failed"
fi

echo ""
echo "All tests completed!"
echo "Check the generated PNG files in $OUTPUT_DIR/"
