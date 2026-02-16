#!/bin/bash
# Test animation feature
# Run from the astro_map_plot root directory

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$ROOT_DIR/data"
OUTPUT_DIR="$ROOT_DIR/sandbox"

echo "Testing mapplot animation features..."
echo ""

# Test 1: Basic animation
echo "Test 1: Basic animation (MP4)"
python -m mapplot --animate "$DATA_DIR/example_animation_test.txt" -o "$OUTPUT_DIR/test_animation.mp4"
if [ $? -eq 0 ]; then
    echo "  PASS: Test 1 passed"
    ls -lh "$OUTPUT_DIR/test_animation.mp4"
else
    echo "  FAIL: Test 1 failed"
fi
echo ""

# Test 2: Animation with trail mode
echo "Test 2: Trail mode animation"
python -m mapplot --animate "$DATA_DIR/example_animation_test.txt" --trail-length 10 -o "$OUTPUT_DIR/test_trail.mp4"
if [ $? -eq 0 ]; then
    echo "  PASS: Test 2 passed"
    ls -lh "$OUTPUT_DIR/test_trail.mp4"
else
    echo "  FAIL: Test 2 failed"
fi
echo ""

# Test 3: Animation with time display
echo "Test 3: Animation with time display"
python -m mapplot --animate "$DATA_DIR/example_animation_test.txt" --show-time --highlight-current -o "$OUTPUT_DIR/test_time.mp4"
if [ $? -eq 0 ]; then
    echo "  PASS: Test 3 passed"
    ls -lh "$OUTPUT_DIR/test_time.mp4"
else
    echo "  FAIL: Test 3 failed"
fi
echo ""

# Test 4: GIF output (if pillow available)
echo "Test 4: GIF output"
python -m mapplot --animate "$DATA_DIR/example_animation_test.txt" --fps 10 -o "$OUTPUT_DIR/test_animation.gif"
if [ $? -eq 0 ]; then
    echo "  PASS: Test 4 passed"
    ls -lh "$OUTPUT_DIR/test_animation.gif"
else
    echo "  FAIL: Test 4 failed (may need pillow: pip install pillow)"
fi
echo ""

# Test 5: With solar-relative data
if [ -f "$DATA_DIR/example_solar_relative.txt" ]; then
    echo "Test 5: Solar-relative animation"
    python -m mapplot --animate --solar-relative "$DATA_DIR/example_solar_relative.txt" --ecliptic -o "$OUTPUT_DIR/test_solar.mp4"
    if [ $? -eq 0 ]; then
        echo "  PASS: Test 5 passed"
        ls -lh "$OUTPUT_DIR/test_solar.mp4"
    else
        echo "  FAIL: Test 5 failed"
    fi
    echo ""
fi

echo "Animation tests complete!"
echo ""
echo "Generated files:"
ls -lh "$OUTPUT_DIR"/test_*.mp4 "$OUTPUT_DIR"/test_*.gif 2>/dev/null || echo "No test files generated"
echo ""
echo "You can view these with any video player."
