"""Command-line argument parser."""

import argparse

from mapplot import __version__
from mapplot.constants import TERRESTRIAL_PROJECTIONS, MARKERS
from mapplot.config import COLOR_PALETTES


def parse_args():
    parser = argparse.ArgumentParser(
        description='Plot geographic or celestial data with various projections',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  # Sky maps (default mode) with BSC5 catalog
  mapplot --catalog -p mollweide -g
  mapplot --catalog --ecliptic --galactic-plane

  # Show poles of coordinate systems
  mapplot --catalog --ecliptic --poles ecliptic
  mapplot --catalog --poles all  # Show all poles

  # Grid in different coordinate system than data
  mapplot --catalog --plot-coord equatorial --grid-coord galactic -g

  # Terrestrial/Earth maps (use --earth flag)
  mapplot --earth cities.txt
  mapplot --earth -p mollweide -g cities.txt

  # Show all observatories from Minor Planet Center
  mapplot --earth --observatories -p robinson -g

  # Show specific observatories
  mapplot --earth --obs-codes 675 704 G96 -p mercator -g

  # Save to file (avoids interactive window)
  mapplot --catalog -o sky.png

  # Coordinate transformation
  mapplot --input-coord galactic --plot-coord equatorial data.txt

  # Solar-relative coordinates (input: MJD RA Dec)
  mapplot --solar-relative asteroid_track.txt -p mollweide -g
  mapplot --solar-relative --solar-center 90 comet.txt  # Center at quadrature

  # Labels from file (third column)
  mapplot --labels-from-file objects.txt

  # Grid with axis labels and cardinal directions
  mapplot --catalog -g --grid-labels --cardinal -p plate-carree
  mapplot --earth cities.txt -g --grid-labels --cardinal -p mercator

  # Ignore extra columns (use only lon/lat)
  mapplot --ignore-extra data_with_many_columns.txt

Tip: Close the plot window to exit cleanly, or use -o FILE to save without displaying.
Default grid spacing is now 30 deg. Sky mode is the default; use --earth for terrestrial maps.

Available projections:
  {', '.join(sorted(TERRESTRIAL_PROJECTIONS.keys()))}

Available markers:
  {', '.join(sorted(MARKERS.keys()))}

Coordinate systems (for sky mode):
  equatorial (RA, Dec), ecliptic (lon, lat), galactic (l, b)

Data format:
  Terrestrial: lon lat [size] [color_value]
  Celestial: coord1 coord2 [size] [color_value]
  Solar-relative: MJD RA Dec [size] [color_value]
        """
    )

    # Version
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Input files and mode
    parser.add_argument('files', nargs='*', help='Input file(s) with coordinate data')
    parser.add_argument('--earth', action='store_true',
                        help='Earth map mode (terrestrial coordinates) - default is sky mode')
    parser.add_argument('--catalog', action='store_true',
                        help='Show Bright Star Catalogue (BSC5) - http://tdc-www.harvard.edu/catalogs/bsc5.html')
    parser.add_argument('--max-mag', type=float, default=6.0,
                        help='Maximum stellar magnitude for catalog (default: 6.0, BSC5 contains mag <= 6.5)')

    # Coordinate systems
    parser.add_argument('--input-coord', default='equatorial',
                        choices=['equatorial', 'ecliptic', 'galactic'],
                        help='Input coordinate system (sky mode, default: equatorial)')
    parser.add_argument('--plot-coord', default='equatorial',
                        choices=['equatorial', 'ecliptic', 'galactic'],
                        help='Plot coordinate system (sky mode, default: equatorial)')
    parser.add_argument('--grid-coord',
                        choices=['equatorial', 'ecliptic', 'galactic'],
                        help='Grid coordinate system (default: same as --plot-coord)')

    # Sky map overlays
    parser.add_argument('--ecliptic', action='store_true',
                        help='Show ecliptic plane (sky mode)')
    parser.add_argument('--galactic-plane', action='store_true',
                        help='Show galactic plane (sky mode)')
    parser.add_argument('--celestial-equator', action='store_true',
                        help='Show celestial equator (sky mode)')
    parser.add_argument('--poles', nargs='+',
                        choices=['equatorial', 'ecliptic', 'galactic', 'all'],
                        help='Show coordinate system poles (e.g., --poles ecliptic galactic)')
    parser.add_argument('--milky-way', action='store_true',
                        help='Show Milky Way density (sky mode)')

    # Solar-relative coordinates
    parser.add_argument('--solar-relative', action='store_true',
                        help='Use solar-relative ecliptic longitude (input: MJD RA Dec)')
    parser.add_argument('--solar-center', type=float, default=180.0,
                        help='Center plot at this solar elongation in degrees (default: 180 for opposition)')

    # Map projection and display
    parser.add_argument('-p', '--projection', default='plate-carree',
                        choices=sorted(TERRESTRIAL_PROJECTIONS.keys()),
                        help='Map projection (default: plate-carree)')
    parser.add_argument('-o', '--output', help='Output file (default: display interactively)')

    # Gridlines
    parser.add_argument('-g', '--gridlines', action='store_true',
                        help='Show gridlines')
    parser.add_argument('--grid-spacing', type=float, nargs=2, metavar=('LON', 'LAT'),
                        help='Grid spacing in degrees (lon lat)')
    parser.add_argument('--grid-color', default='gray',
                        help='Grid line color (default: gray)')
    parser.add_argument('--grid-alpha', type=float, default=0.5,
                        help='Grid line transparency (default: 0.5)')
    parser.add_argument('--grid-style', default='--',
                        help='Grid line style (default: --)')
    parser.add_argument('--grid-labels', action='store_true',
                        help='Show axis labels on gridlines')
    parser.add_argument('--cardinal', action='store_true',
                        help='Show cardinal direction markers (N, S, E, W)')

    # Map features (terrestrial mode)
    parser.add_argument('--coastlines', action='store_true', default=True,
                        help='Show coastlines (terrestrial mode, default: True)')
    parser.add_argument('--no-coastlines', dest='coastlines', action='store_false',
                        help='Hide coastlines')
    parser.add_argument('--countries', action='store_true',
                        help='Show country boundaries (terrestrial mode)')
    parser.add_argument('--land', action='store_true',
                        help='Fill land areas (terrestrial mode)')
    parser.add_argument('--ocean', action='store_true',
                        help='Fill ocean areas (terrestrial mode)')
    parser.add_argument('--observatories', action='store_true',
                        help='Show observatory locations from MPC (terrestrial mode)')
    parser.add_argument('--obs-codes', nargs='+',
                        help='Specific observatory codes to plot (e.g., 474 809 G96). If not specified, plots all.')
    parser.add_argument('--obs-file', default='mpc_observatories.txt',
                        help='MPC observatory file (default: mpc_observatories.txt)')
    parser.add_argument('--obs-dates-file',
                        help='Observatory operational dates file (Code StartMJD EndMJD format)')
    parser.add_argument('--animate-observatories', action='store_true',
                        help='Animate observatories appearing/disappearing (requires --obs-dates-file)')

    # Marker styling
    parser.add_argument('-m', '--marker', default='circle',
                        help=f'Marker style (default: circle)')
    parser.add_argument('-c', '--color', action='append',
                        help='Marker color(s) for each file (can specify multiple times)')
    parser.add_argument('-s', '--size', type=float, default=20,
                        help='Base marker size (default: 20)')
    parser.add_argument('--alpha', type=float, default=0.7,
                        help='Marker transparency (0-1, default: 0.7)')
    parser.add_argument('--edgecolor', default='none',
                        help='Marker edge color (default: none)')
    parser.add_argument('--edgewidth', type=float, default=0.5,
                        help='Marker edge width (default: 0.5)')

    # Colormap options
    parser.add_argument('--cmap', default='viridis',
                        help='Colormap for color column (default: viridis)')
    parser.add_argument('--cbar', action='store_true',
                        help='Show colorbar when using color column')

    # Background and colors
    parser.add_argument('--bgcolor', default='white',
                        help='Background color (default: white)')
    parser.add_argument('--facecolor',
                        help='Axes face color (default: same as bgcolor)')

    # Figure options
    parser.add_argument('--figsize', type=float, nargs=2, metavar=('WIDTH', 'HEIGHT'),
                        default=[12, 8],
                        help='Figure size in inches (default: 12 8)')
    parser.add_argument('--dpi', type=int, default=100,
                        help='Figure DPI (default: 100)')
    parser.add_argument('--title', help='Plot title (use \\n for multi-line titles)')
    parser.add_argument('--config', help='Path to configuration file (YAML format, default: ~/.mapplotrc)')
    parser.add_argument('--palette', choices=list(COLOR_PALETTES.keys()),
                        help='Color palette for data series (default: tableau10)')
    parser.add_argument('--extent', type=float, nargs=4,
                        metavar=('LONMIN', 'LONMAX', 'LATMIN', 'LATMAX'),
                        help='Map extent (default: global)')

    # Legend
    parser.add_argument('--legend', action='store_true',
                        help='Show legend')
    parser.add_argument('--labels', nargs='+',
                        help='Legend labels for each file')
    parser.add_argument('--labels-from-file', action='store_true',
                        help='Use third column from data files as point labels')
    parser.add_argument('--ignore-extra', action='store_true',
                        help='Ignore all columns beyond first two (lon/lat or coord1/coord2)')

    # Animation options
    parser.add_argument('--animate', action='store_true',
                        help='Create animation from time-series data (requires MJD as first column)')
    parser.add_argument('--fps', type=float, default=30,
                        help='Frames per second for animation (default: 30)')
    parser.add_argument('--time-per-day', type=float,
                        help='Seconds per day of data (alternative to --fps, sets animation speed)')
    parser.add_argument('--speed', type=float, default=1.0,
                        help='Animation speed multiplier (default: 1.0, higher=faster)')
    parser.add_argument('--trail-length', type=int,
                        help='Show only last N points (window mode, much faster for large datasets)')
    parser.add_argument('--trail-days', type=float,
                        help='Show only last N days of data (alternative to --trail-length)')
    parser.add_argument('--trail-fade', action='store_true',
                        help='Fade older points in trail (alpha gradient)')
    parser.add_argument('--show-time', action='store_true',
                        help='Display current date/MJD on animation')
    parser.add_argument('--time-format', choices=['mjd', 'year'], default='mjd',
                        help='Time display format: mjd (default) or year (decimal calendar year)')
    parser.add_argument('--highlight-current', action='store_true',
                        help='Make current point larger/different color')
    parser.add_argument('--end-pause', type=float, default=0,
                        help='Seconds to pause at end showing all data (0=no pause, default: 0)')
    parser.add_argument('--legend-loc', default='upper right',
                        choices=['upper right', 'upper left', 'lower right', 'lower left',
                                'center', 'best'],
                        help='Legend location (default: upper right, fixed position)')
    parser.add_argument('--downsample', type=int, default=100000,
                        help='Auto-downsample if points exceed this (default: 100000, 0=disable)')
    parser.add_argument('--start-time', type=float,
                        help='Animation start time (MJD). If not specified, uses earliest data point.')
    parser.add_argument('--stop-time', type=float,
                        help='Animation stop time (MJD). If not specified, uses current time.')
    parser.add_argument('--show-before-start', action='store_true',
                        help='Show all data points before start-time in first frame (otherwise starts empty)')
    parser.add_argument('--show-sun', action='store_true',
                        help='Show sun position moving along ecliptic during animation (sky mode only)')
    parser.add_argument('--stats-cycles', type=int, default=3,
                        help='Number of trail-day cycles to average for statistics (default: 3, range: 1-15)')
    parser.add_argument('--show-timeline', action='store_true',
                        help='Show timeline plot below main plot (requires --trail-days)')
    parser.add_argument('--timeline-height', type=float, default=0.25,
                        help='Height of timeline plot as fraction of total figure (default: 0.25)')
    parser.add_argument('--timeline-reverse', action='store_true',
                        help='Reverse timeline direction (left-to-right instead of right-to-left)')
    parser.add_argument('--timeline-ylabel', type=str, default='Objects',
                        help='Y-axis label for timeline plot (default: "Objects")')
    parser.add_argument('--timeline-xlabel-years', action='store_true',
                        help='Label timeline x-axis in years instead of MJD')
    parser.add_argument('--show-keyframe', action='store_true',
                        help='Add keyframe showing complete timeline and all objects')
    parser.add_argument('--keyframe-at-start', action='store_true',
                        help='Place keyframe at start instead of end (requires --show-keyframe)')
    parser.add_argument('--keyframe-delay', type=float, default=2.0,
                        help='Seconds to wait before showing keyframe (default: 2.0)')

    return parser.parse_args()
