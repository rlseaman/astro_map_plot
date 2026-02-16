# mapplot Changelog

This document consolidates the development history of mapplot from its initial
versions (v3-v17) through v2.0 and subsequent feature branches. Changes are
grouped thematically. The chronological development order ran from Dec 30, 2025
through Jan 3, 2026 across approximately 37 version/feature directories.

---

## Animation System

- Core animation with trail modes, time display, speed control, and
  performance targets handling 10K-1M+ data points efficiently
- Legend, labels, title, and cardinal direction support in animations
- `--time-format year` option displays calendar years instead of raw MJD
- `--trail-days N` for time-based trails (show last N days, not N points)
- `--start-time` and `--stop-time` for custom animation time windows
- `--show-before-start` displays historical data in the first frame
- Defaults to "now-cast" (ending at current time) when stop-time is omitted
- Smart observatory expiration: 3-second fade for expired observatories,
  1-year grace period for recently-expired ones
- Fixed MJD reading in non-solar-relative animation mode
- Improved ffmpeg error messages with installation instructions
- Fixed marker style conversion for matplotlib compatibility

## Sun & Solar Features

- `--show-sun` flag displays Sun position during sky animations
- Sun moves along the ecliptic using mean longitude approximation (~1 deg accuracy)
- Yellow circle marker with orange outline, size 100
- Sun appears in legend when using `--legend --show-sun`
- Motion blur trail (8-position fade) for smooth Sun movement

## Display & Legend

- Smart legend positioning to avoid overlaps with statistics box
- Legend automatically repositioned when conflicts detected
- Enhanced legend appearance: opaque background, gray border, better padding
- No-overlap element positioning: timer (upper left), stats (upper right),
  legend (lower left)
- Fixed legend box appearance (removed broken mode parameter)
- Simplified statistics format: rounded percentages, cleaner display
- Translucent overlays with high z-order (always visible above data)
- White background default for both Earth and sky modes
- Multi-line title support with `\n`
- Fixed `-c/--color` colors in animation mode
- Fixed keyframe sequence order: animation then pause then keyframe
- Legend colors use user-specified `-c` colors correctly

## Timeline & Statistics

- `--show-timeline` secondary time-series plot showing rolling object counts
- Options: `--timeline-height`, `--timeline-reverse`, `--timeline-ylabel`
- `--timeline-xlabel-years` for year labels instead of MJD
- Keyframe feature: `--show-keyframe`, `--keyframe-at-start`
  (3-second summary frame showing all data)
- Running average statistics over N cycles (`--stats-cycles`, range 1-15)
- Real-time observatory count display in lower right corner
- Timeline x-axis labels appear from frame 1
- Integer year labels (2007, 2008 instead of 2007.5, 2008.0)
- Stacked timeline showing proportions of multiple data series
- Fixed rolling window size to use `trail_days * stats_cycles`
- Statistics show total count correctly

## Galactic Center

- Tilted ellipse for galactic center representing 3D perspective view
- Dimensions refined to 8 deg x 5 deg at 30 deg tilt angle
- Bullseye symbol: open circle with center dot
- Custom legend handler draws actual tilted ellipse in the legend
- Ecliptic pole size reduced to 120 for visual balance

## Observatory Features

- MPC observatory database integration with 2,000+ observatory codes
- Observatory code to latitude/longitude conversion from cos/sin format
- Animate observatories appearing/disappearing based on operational dates
- Observatory dates file format: `CODE START_MJD END_MJD`
- Real-time active observatory count display

## Performance

- Binary search for time lookup (100x faster, O(log n) vs O(n))
- Batched scatter plots (10-50x faster, single call vs per-point)
- Pre-computed MJD arrays for efficient searching
- 3-10x overall animation speed improvement
- H.264 video with CRF 23 (30-50% smaller files, same visual quality)

## Bug Fixes

- Fixed duplicate argument definitions for observatory features
- Fixed observatory mode validation
- Fixed solar-relative centering (opposition vs conjunction)
- Added validation for incompatible solar-relative options
- Fixed ecliptic display in solar-relative mode (straight line, not sinusoid)
- Fixed celestial coordinates to be left-handed (astronomical convention)
- Added meridian labels on x-axis (plate-carree/mercator projections only)
- Changed reference line colors to avoid data conflicts
  (darkorange, cyan, lime)
- Added title spacing (20pt padding)
- Ecliptic poles marker changed from bold X to regular x
- Galactic center marker changed from filled square to open circle
- Galactic center legend entry restored after refactoring
- Keyframe shows all data including points before `--start-time`
- Keyframe stats show total count and per-series breakdowns

---

## Version History Summary

| Phase | Dates | Versions | Focus |
|-------|-------|----------|-------|
| Initial development | Dec 30 | v3-v9 | Core mapping, projections, BSC5 catalog, data formats |
| Feature expansion | Dec 30-31 | v10-v17 | Observatories, solar-relative, grid labels, config |
| v2.0 release | Dec 31 | ver_2.0 | Animation system, professional colors, YAML config |
| Animation refinement | Dec 31 | ver_2.0_2nd_try, bugfix E-G | Performance, markers, observatory animation |
| Sun & solar | Jan 1 | sun, sun_2, sun_v3 | Sun position, motion blur, video optimization |
| Polish & legend | Jan 1 | legend, positioning, formatting | Smart positioning, statistics, display cleanup |
| Statistics & cycles | Jan 1-2 | cycles, obs_counter | Extended stats, observatory counter |
| Timeline | Jan 3 | timeline, timeline_2 | Secondary plot, year labels, keyframes |
| Rolling & polish | Jan 3 | rolling, polish, polish2, polish3 | Window fix, colors, stacked timeline |
| Galactic center | Jan 3 | ellipse, gc_resize, summary | Tilted ellipse, legend handler, final fixes |
