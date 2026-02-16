# Animation Feature Documentation

## Overview

mapplot-with-animation adds time-based animation capabilities to mapplot, allowing you to visualize data that changes over time. Perfect for:
- Asteroid and comet tracking
- Satellite orbits
- Celestial object motion
- Time-series astronomical data

## Key Features

### ✅ **Efficient Handling of Large Datasets**
- **Trail mode**: Show only last N points (handles millions efficiently)
- **Cumulative mode**: Show all points up to current time (best for <100K points)
- **Auto-downsampling**: Automatically reduces data if too dense
- **Optimized rendering**: Uses matplotlib's FuncAnimation with efficient updates

### ✅ **Performance Targets**

| Points | Mode | Estimated Render Time | Practical? |
|--------|------|----------------------|------------|
| 10,000 | Cumulative | 30 seconds | ✅ Excellent |
| 50,000 | Cumulative | 2-5 minutes | ✅ Good |
| 100,000 | Trail (5K window) | 2-4 minutes | ✅ Good |
| 500,000 | Trail (5K window) | 3-6 minutes | ✅ Good |
| 1,000,000 | Trail (5K window) | 4-8 minutes | ✅ Acceptable |

### ✅ **Output Formats**
- **MP4** - Best quality/size ratio, most compatible (recommended)
- **GIF** - Web-friendly, larger file size, limited colors
- **AVI** - Uncompressed, huge files
- **WebM** - Modern format, good compression

## Basic Usage

### Minimal Example
```bash
# Create animation from time-series data
./mapplot-with-animation --animate example_solar_relative.txt -o asteroid.mp4

# With reference lines
./mapplot-with-animation --animate --ecliptic example_solar_relative.txt -o asteroid.mp4
```

### Data Format

**Required:** MJD (Modified Julian Date) as first column, then coordinates:

```
# MJD RA Dec
60000.0 120.5 -15.2
60001.0 121.3 -14.8
60002.0 122.1 -14.4
...
```

Same format as solar-relative mode - works with any coordinate system.

## Command-Line Options

### Core Animation Options

**--animate**
- Enables animation mode
- Requires MJD as first column in data files
- Must specify output file with -o

**--fps N** (default: 30)
- Frames per second for output video
- Higher = smoother but larger file
- Typical values: 10-60

**--time-per-day N**
- Alternative to --fps
- Seconds of video per day of data
- Example: `--time-per-day 0.1` = 10 days per second

**-o FILE** (required for animation)
- Output filename
- Must be .mp4, .gif, .avi, or .webm
- Example: `-o asteroid_track.mp4`

### Performance Options

**--trail-length N**
- Show only last N points (window mode)
- MUCH faster for large datasets
- Example: `--trail-length 5000`
- Use this for millions of points

**--downsample N** (default: 100000)
- Auto-reduce if points exceed this number
- Set to 0 to disable
- Preserves overall pattern while reducing render time

### Display Options

**--show-time**
- Display current MJD on each frame
- Appears in top-left corner
- Updates as animation plays

**--highlight-current**
- Make the most recent point larger and highlighted
- Good for tracking current position
- Adds black outline to current point

## Examples

### Example 1: Basic Asteroid Animation
```bash
./mapplot-with-animation --animate \
  example_solar_relative.txt \
  --ecliptic \
  --fps 30 \
  -o asteroid_30fps.mp4
```

### Example 2: With Time Display
```bash
./mapplot-with-animation --animate \
  example_solar_relative.txt \
  --ecliptic --show-time --highlight-current \
  -o asteroid_labeled.mp4
```

### Example 3: Trail Mode (Large Dataset)
```bash
# Show only last 1000 points - much faster!
./mapplot-with-animation --animate \
  large_asteroid_data.txt \
  --trail-length 1000 \
  --ecliptic --galactic-plane \
  --fps 30 \
  -o asteroid_trail.mp4
```

### Example 4: Multiple Objects
```bash
# Animate multiple asteroids with different colors
./mapplot-with-animation --animate \
  asteroid1.txt asteroid2.txt asteroid3.txt \
  --palette tableau10 \
  --ecliptic \
  --show-time --highlight-current \
  --fps 30 \
  -o three_asteroids.mp4
```

### Example 5: GIF Output
```bash
# Create GIF (web-friendly but larger)
./mapplot-with-animation --animate \
  comet.txt \
  --ecliptic \
  --fps 10 \
  -o comet.gif
```

### Example 6: Slow Motion
```bash
# Very slow animation - 1 second per day
./mapplot-with-animation --animate \
  fast_object.txt \
  --time-per-day 1.0 \
  --ecliptic \
  -o slow_motion.mp4
```

### Example 7: Time-Lapse (Many Years Compressed)
```bash
# 36 years in 3 minutes
# 36 years = ~13,000 days
# 3 minutes = 180 seconds
# 13000 / 180 = 72 days per second
./mapplot-with-animation --animate \
  long_term_data.txt \
  --time-per-day 0.014 \
  --trail-length 5000 \
  --ecliptic --celestial-equator \
  --show-time \
  --fps 30 \
  -o timelapse_36years.mp4
```

### Example 8: High Quality
```bash
# Higher resolution and frame rate
./mapplot-with-animation --animate \
  data.txt \
  --figsize 16 9 \
  --dpi 150 \
  --fps 60 \
  --ecliptic \
  -o high_quality.mp4
```

## Performance Tips

### For Small Datasets (<50,000 points)
- Use default cumulative mode
- 30 fps is fine
- No need for trail mode

```bash
./mapplot-with-animation --animate data.txt --fps 30 -o output.mp4
```

### For Medium Datasets (50,000-200,000 points)
- Consider trail mode
- Use downsampling if needed
- 20-30 fps

```bash
./mapplot-with-animation --animate data.txt \
  --trail-length 10000 \
  --fps 20 \
  -o output.mp4
```

### For Large Datasets (200,000+ points)
- **Always use trail mode**
- Lower fps acceptable (15-20)
- Enable downsampling

```bash
./mapplot-with-animation --animate data.txt \
  --trail-length 5000 \
  --downsample 100000 \
  --fps 20 \
  -o output.mp4
```

### For Million+ Points
- Trail mode essential
- Consider shorter trail
- Accept longer render time

```bash
./mapplot-with-animation --animate huge_data.txt \
  --trail-length 2000 \
  --downsample 50000 \
  --fps 15 \
  -o output.mp4
```

## Technical Details

### How It Works

1. **Data Preparation**
   - Reads all input files
   - Combines and sorts by MJD
   - Applies downsampling if needed

2. **Frame Generation**
   - Creates one frame per data point (or subset)
   - Each frame shows data up to that time
   - Trail mode shows only recent points

3. **Video Encoding**
   - Uses FFMpegWriter (MP4/AVI/WebM) or PillowWriter (GIF)
   - Encodes frames to video file
   - Compression happens automatically

### Memory Usage

- **Cumulative mode**: Memory grows with data
- **Trail mode**: Constant memory (only N points in memory)
- For 1M points: Trail mode uses ~50MB, cumulative uses ~500MB

### Render Time Estimation

Approximate formula:
```
render_time = (num_frames × 0.05 seconds) for trail mode
render_time = (num_frames × 0.1 seconds) for cumulative mode
```

Plus video encoding time (~10-30 seconds).

### Requirements

**Required:**
- matplotlib (with animation support - standard)
- ffmpeg (for MP4/AVI/WebM output)
- pillow (for GIF output)

**Install:**
```bash
# FFmpeg (for video output)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Red Hat/Rocky:
sudo yum install ffmpeg

# Python packages (usually already installed):
pip install pillow
```

## Compatibility

### Works With All mapplot Features
- ✅ All projections
- ✅ Reference lines (ecliptic, galactic, equator)
- ✅ Grid lines
- ✅ Cardinal directions
- ✅ Custom colors and markers
- ✅ Multiple input files
- ✅ Solar-relative mode
- ✅ Regular coordinate modes

### Does NOT Support (Animation-Specific)
- ❌ Interactive playback controls (use video player)
- ❌ Pause/resume during generation
- ❌ Real-time speed changes (generate multiple videos)
- ❌ Static elements in legend (animation only shows data)

## Controlling Playback Speed

### Option 1: Video Player Controls
Most video players (VLC, QuickTime, etc.) have speed controls:
- Play at 0.5x, 1x, 2x, etc.
- No need to re-render

### Option 2: Generate Multiple Speeds
```bash
# Slow version
./mapplot-with-animation --animate data.txt --fps 10 -o slow.mp4

# Medium version
./mapplot-with-animation --animate data.txt --fps 30 -o medium.mp4

# Fast version
./mapplot-with-animation --animate data.txt --fps 60 -o fast.mp4
```

### Option 3: Use --time-per-day
```bash
# Slow: 1 second per day
./mapplot-with-animation --animate data.txt --time-per-day 1.0 -o slow.mp4

# Fast: 0.01 second per day (100 days per second)
./mapplot-with-animation --animate data.txt --time-per-day 0.01 -o fast.mp4
```

## Troubleshooting

### "Error: Animation requires matplotlib.animation"
- This should be included with matplotlib
- Try: `pip install matplotlib --upgrade`

### "Error: ffmpeg not found"
- Install ffmpeg (see Requirements section)
- Or use GIF output instead: `-o output.gif`

### Animation is too slow to render
- Use `--trail-length` to reduce visible points
- Enable `--downsample`
- Reduce `--fps`
- Example: `--trail-length 1000 --fps 15`

### File size too large
- Use MP4 instead of GIF (10x smaller)
- Reduce resolution: `--figsize 10 6`
- Reduce fps: `--fps 15`
- Reduce dpi: `--dpi 72`

### Animation plays too fast/slow
- Adjust `--fps` or `--time-per-day`
- Or use video player speed controls

### Out of memory
- Use `--trail-length` (essential for large data)
- Increase `--downsample` threshold
- Close other applications

## Comparison: Animation vs Static

### When to Use Animation
- ✅ Data has time component (MJD)
- ✅ Want to show motion/evolution
- ✅ Have reasonable dataset size
- ✅ Need video output

### When to Use Static
- ✅ Single time snapshot
- ✅ Very large datasets (millions) without trail mode
- ✅ Need interactive plot
- ✅ Print/publication output

## Example Workflows

### Asteroid Discovery Campaign
```bash
# Long-term tracking with trail
./mapplot-with-animation --animate \
  asteroid_detections.txt \
  --trail-length 3000 \
  --ecliptic --celestial-equator \
  --show-time --highlight-current \
  --time-per-day 0.05 \
  --palette vibrant \
  --title "Asteroid 2024XY Discovery" \
  -o asteroid_discovery.mp4
```

### Comet Approach
```bash
# Show comet approaching Sun
./mapplot-with-animation --animate \
  --solar-relative comet_approach.txt \
  --ecliptic \
  --show-time --highlight-current \
  --fps 30 \
  --title "Comet C/2024 A1 Solar Approach" \
  -o comet_approach.mp4
```

### Multi-Object Survey
```bash
# Multiple asteroids from survey
./mapplot-with-animation --animate \
  survey_ast1.txt survey_ast2.txt survey_ast3.txt \
  --palette set2 \
  --trail-length 2000 \
  --ecliptic --galactic-plane \
  --show-time \
  --fps 25 \
  -o survey_results.mp4
```

## See Also

- **SOLAR_RELATIVE.md** - Data format for solar-relative mode
- **README.md** - Main mapplot documentation
- **COLORS_AND_CONFIG.md** - Color palettes and configuration
- **QUICKREF.md** - Quick command reference

## Summary

Animation adds powerful time-based visualization to mapplot:
- Handles datasets from thousands to millions of points
- Efficient trail mode for large data
- Professional video output (MP4, GIF, etc.)
- Works with all existing mapplot features
- Simple command-line interface

**Quick start:**
```bash
./mapplot-with-animation --animate your_data.txt -o output.mp4
```

That's it! ✨
