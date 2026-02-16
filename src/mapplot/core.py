"""Main orchestration: run_mapplot and main entry point."""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FFMpegWriter, PillowWriter

from mapplot.cli import parse_args
from mapplot.config import load_config, get_data_colors
from mapplot.constants import TERRESTRIAL_PROJECTIONS, MARKERS
from mapplot.coordinates import transform_coordinates, compute_solar_relative_coords
from mapplot.data_io import read_data, prepare_animation_data
from mapplot.plotting import (plot_sky_map, plot_terrestrial_map,
                              plot_cardinal_directions, plot_custom_gridlines)
from mapplot.animation import create_animation
from mapplot.observatories import load_mpc_observatories, load_observatory_dates

# Check for astropy availability
try:
    from astropy.coordinates import SkyCoord
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False


def main():
    args = parse_args()

    try:
        run_mapplot(args)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user (Ctrl-C).", file=sys.stderr)
        print("Note: Close the plot window to exit cleanly, or use -o FILE to save without displaying.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


def run_mapplot(args):
    """Main plotting logic."""

    # Load configuration file
    config = load_config(args.config if hasattr(args, 'config') else None)

    # Apply config defaults where args don't override
    if not args.figsize:
        args.figsize = config['display']['figsize']
    if not hasattr(args, 'palette') or args.palette is None:
        palette_name = config['colors']['data_palette']
    else:
        palette_name = args.palette

    # Check for astropy in sky mode
    if not args.earth and not ASTROPY_AVAILABLE:
        print("Error: Sky mode requires astropy. Install with: pip install astropy",
              file=sys.stderr)
        sys.exit(1)

    # Check that we have either files or catalog or observatories
    if not args.files and not args.catalog and not args.observatories and not args.obs_codes:
        print("Error: Must specify input files, --catalog, or --observatories", file=sys.stderr)
        sys.exit(1)

    # Validate solar-relative mode options
    if args.solar_relative:
        if args.earth:
            print("Error: --solar-relative is not compatible with --earth mode", file=sys.stderr)
            sys.exit(1)

        if args.galactic_plane:
            print("Error: --galactic-plane is not compatible with --solar-relative", file=sys.stderr)
            print("       (Galactic plane coordinates don't align with solar-relative frame)", file=sys.stderr)
            sys.exit(1)

        if args.celestial_equator:
            print("Error: --celestial-equator is not compatible with --solar-relative", file=sys.stderr)
            print("       (Celestial equator doesn't align with solar-relative frame)", file=sys.stderr)
            sys.exit(1)

        if args.milky_way:
            print("Error: --milky-way is not compatible with --solar-relative", file=sys.stderr)
            print("       (Milky Way density is in galactic coordinates)", file=sys.stderr)
            sys.exit(1)

        if args.poles:
            print("Error: --poles is not compatible with --solar-relative", file=sys.stderr)
            print("       (Coordinate poles are not meaningful in solar-relative frame)", file=sys.stderr)
            sys.exit(1)

        if args.grid_coord:
            print("Error: --grid-coord is not compatible with --solar-relative", file=sys.stderr)
            print("       (Solar-relative uses its own coordinate system)", file=sys.stderr)
            sys.exit(1)

        if args.plot_coord != 'equatorial':
            print("Error: --plot-coord is not compatible with --solar-relative", file=sys.stderr)
            print("       (Solar-relative uses its own coordinate system)", file=sys.stderr)
            sys.exit(1)

        if not args.files:
            print("Error: --solar-relative requires input files with MJD, RA, Dec", file=sys.stderr)
            sys.exit(1)

    # Validate animation mode options
    if args.animate:
        if not args.files:
            print("Error: --animate requires input files with MJD as first column", file=sys.stderr)
            sys.exit(1)

        if not args.output:
            print("Error: --animate requires output file (-o output.mp4 or .gif)", file=sys.stderr)
            sys.exit(1)

        output_ext = os.path.splitext(args.output)[1].lower()
        if output_ext not in ['.mp4', '.gif', '.avi', '.webm']:
            print("Error: Animation output must be .mp4, .gif, .avi, or .webm", file=sys.stderr)
            sys.exit(1)

        if args.trail_length and args.trail_days:
            print("Error: Cannot use both --trail-length and --trail-days", file=sys.stderr)
            print("       Use --trail-length N for last N points", file=sys.stderr)
            print("       Or --trail-days N for last N days", file=sys.stderr)
            sys.exit(1)

        if args.start_time is not None and args.stop_time is not None:
            if args.stop_time <= args.start_time:
                print(f"Error: --stop-time ({args.stop_time}) must be after --start-time ({args.start_time})",
                      file=sys.stderr)
                sys.exit(1)

        if args.show_before_start and args.start_time is None:
            print("Warning: --show-before-start has no effect without --start-time", file=sys.stderr)

    # Get marker symbol
    marker = MARKERS.get(args.marker, args.marker)

    # Create figure and axis/axes
    fig = plt.figure(figsize=args.figsize, dpi=args.dpi)
    fig.patch.set_facecolor(args.bgcolor)

    # Check if timeline plot is requested
    if args.show_timeline and args.trail_days:
        main_height = 1.0 - args.timeline_height
        timeline_height = args.timeline_height

        gs = GridSpec(2, 1, figure=fig, height_ratios=[main_height, timeline_height],
                     hspace=0.15)

        projection = TERRESTRIAL_PROJECTIONS[args.projection]()
        ax = fig.add_subplot(gs[0], projection=projection)

        ax_timeline = fig.add_subplot(gs[1])
        ax_timeline.set_facecolor('white')
        ax_timeline.grid(True, alpha=0.3)
        ax_timeline.set_ylabel(args.timeline_ylabel, fontsize=10)

        if args.timeline_xlabel_years:
            ax_timeline.set_xlabel('Year', fontsize=10)
        else:
            ax_timeline.set_xlabel('MJD', fontsize=10)

    else:
        projection = TERRESTRIAL_PROJECTIONS[args.projection]()
        ax = plt.axes(projection=projection)
        ax_timeline = None

    # Set background color
    if args.facecolor:
        ax.set_facecolor(args.facecolor)
    else:
        ax.set_facecolor(args.bgcolor)

    # Set extent if specified
    if args.extent:
        ax.set_extent(args.extent, crs=ccrs.PlateCarree())
    else:
        ax.set_global()

    # For sky mode, flip horizontal axis (astronomical convention)
    if not args.earth:
        ax.invert_xaxis()

    # Configure gridlines
    if args.gridlines:
        grid_coord = args.grid_coord if args.grid_coord else args.plot_coord

        if not args.earth and grid_coord != args.plot_coord:
            if args.grid_spacing:
                plot_custom_gridlines(ax, grid_coord, args.plot_coord, args.grid_spacing, args)
            else:
                plot_custom_gridlines(ax, grid_coord, args.plot_coord, (30, 30), args)
        else:
            if args.grid_spacing:
                gl = ax.gridlines(draw_labels=False, linewidth=1.0,
                                color=args.grid_color,
                                alpha=args.grid_alpha,
                                linestyle=args.grid_style,
                                xlocs=np.arange(-180, 181, args.grid_spacing[0]),
                                ylocs=np.arange(-90, 91, args.grid_spacing[1]))
            else:
                spacing_lon = 30
                spacing_lat = 30

                gl = ax.gridlines(draw_labels=False, linewidth=1.0,
                                color=args.grid_color,
                                alpha=args.grid_alpha,
                                linestyle=args.grid_style,
                                xlocs=np.arange(-180, 181, spacing_lon),
                                ylocs=np.arange(-90, 91, spacing_lat))

            if args.grid_labels and args.projection in ['plate-carree', 'mercator']:
                try:
                    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

                    gl.xformatter = LongitudeFormatter()
                    gl.yformatter = LatitudeFormatter()

                    gl.top_labels = False
                    gl.right_labels = False
                    gl.bottom_labels = True
                    gl.left_labels = True

                    gl.xlabel_style = {'size': 10}
                    gl.ylabel_style = {'size': 10}

                except (ImportError, AttributeError) as e:
                    print(f"Warning: Grid labels not available ({e})", file=sys.stderr)
            elif args.grid_labels and args.projection not in ['plate-carree', 'mercator']:
                print(f"Warning: --grid-labels only works with plate-carree and mercator projections",
                      file=sys.stderr)
                print(f"         Current projection: {args.projection}", file=sys.stderr)

    # ANIMATION MODE
    if args.animate:
        print("Preparing animation data...", file=sys.stderr)

        all_data = prepare_animation_data(args, palette_name)

        if len(all_data) == 0:
            print("Error: No data to animate", file=sys.stderr)
            sys.exit(1)

        print(f"Animating {len(all_data)} data points", file=sys.stderr)
        print(f"Time range: MJD {all_data[0]['mjd']:.2f} to {all_data[-1]['mjd']:.2f}", file=sys.stderr)

        # Load observatories if animating them
        observatories = None
        obs_dates = None
        if args.animate_observatories:
            if not args.obs_dates_file:
                print("Error: --animate-observatories requires --obs-dates-file", file=sys.stderr)
                sys.exit(1)

            observatories = load_mpc_observatories(args.obs_file)
            obs_dates = load_observatory_dates(args.obs_dates_file)

            if not observatories:
                print("Warning: No observatories loaded", file=sys.stderr)
            if not obs_dates:
                print("Warning: No observatory dates loaded", file=sys.stderr)

            if observatories and obs_dates:
                print(f"Will animate {len([c for c in obs_dates.keys() if any(o['code'].upper() == c for o in observatories)])} observatories",
                      file=sys.stderr)

        # Plot background
        if args.earth:
            plot_terrestrial_map(ax, args)
        else:
            plot_sky_map(ax, args)

        # Add legend if requested
        if args.legend and args.labels:
            if args.color is None:
                file_colors = get_data_colors(palette_name, len(args.files))
            else:
                file_colors = args.color[:]
                if len(file_colors) < len(args.files):
                    file_colors.extend(['black'] * (len(args.files) - len(file_colors)))

            for i, label in enumerate(args.labels):
                ax.scatter([], [], c=file_colors[i], s=args.size, label=label,
                          marker=MARKERS.get(args.marker, args.marker))

        if args.legend and args.show_sun and not args.earth:
            ax.scatter([], [], s=100, c='yellow', marker='o',
                      edgecolors='orange', linewidths=1.5, label='Sun')

        if args.legend and (args.labels or (args.show_sun and not args.earth)):
            legend_loc = args.legend_loc

            if legend_loc == 'upper right':
                bbox_anchor = (0.98, 0.98)
                loc_anchor = 'upper right'
            elif legend_loc == 'upper left':
                bbox_anchor = (0.02, 0.98)
                loc_anchor = 'upper left'
            elif legend_loc == 'lower right':
                bbox_anchor = (0.98, 0.02)
                loc_anchor = 'lower right'
            elif legend_loc == 'lower left':
                bbox_anchor = (-0.05, -0.05)
                loc_anchor = 'lower left'
            elif legend_loc == 'center':
                bbox_anchor = (0.5, 0.5)
                loc_anchor = 'center'
            else:
                bbox_anchor = None
                loc_anchor = 'best'

            handler_map = {}
            if hasattr(ax, '_gc_legend_handler'):
                handler_map.update(ax._gc_legend_handler)

            if bbox_anchor:
                legend = ax.legend(loc=loc_anchor, bbox_to_anchor=bbox_anchor,
                         bbox_transform=ax.transAxes,
                         framealpha=0.9, facecolor='white', edgecolor='gray',
                         frameon=True, borderpad=0.5,
                         handler_map=handler_map if handler_map else None)
            else:
                legend = ax.legend(loc=loc_anchor, framealpha=0.9, facecolor='white',
                         edgecolor='gray', frameon=True, borderpad=0.5,
                         handler_map=handler_map if handler_map else None)

            legend.set_zorder(100)

        if args.title:
            ax.set_title(args.title, fontsize=14, fontweight='bold', pad=20)

        if args.cardinal:
            plot_cardinal_directions(ax, args)

        # Create and save animation
        anim = create_animation(args, ax, fig, all_data, palette_name,
                               observatories, obs_dates, ax_timeline)

        output_ext = os.path.splitext(args.output)[1].lower()

        print(f"Saving animation to {args.output}...", file=sys.stderr)

        try:
            if output_ext == '.gif':
                writer = PillowWriter(fps=args.fps)
                anim.save(args.output, writer=writer)
            else:
                extra_args = ['-vcodec', 'libx264', '-crf', '23', '-preset', 'medium', '-pix_fmt', 'yuv420p']
                writer = FFMpegWriter(fps=args.fps, extra_args=extra_args)
                anim.save(args.output, writer=writer)
        except FileNotFoundError as e:
            if 'ffmpeg' in str(e).lower():
                print("\nError: ffmpeg not found!", file=sys.stderr)
                print("", file=sys.stderr)
                print("To create MP4/AVI/WebM videos, you need ffmpeg installed:", file=sys.stderr)
                print("", file=sys.stderr)
                print("  macOS:           brew install ffmpeg", file=sys.stderr)
                print("  Ubuntu/Debian:   sudo apt-get install ffmpeg", file=sys.stderr)
                print("  Red Hat/Rocky:   sudo yum install ffmpeg", file=sys.stderr)
                print("", file=sys.stderr)
                print("Alternatively, use GIF output (doesn't require ffmpeg):", file=sys.stderr)
                print(f"  mapplot --animate {' '.join(args.files)} -o output.gif", file=sys.stderr)
                sys.exit(1)
            else:
                raise

        print(f"Animation saved to {args.output}", file=sys.stderr)
        return

    # STATIC MODE
    if args.earth:
        plot_terrestrial_map(ax, args)
    else:
        plot_sky_map(ax, args)

    # Default colors if not specified
    if args.files:
        if args.color is None:
            args.color = get_data_colors(palette_name, len(args.files))
        elif len(args.color) < len(args.files):
            args.color.extend(['black'] * (len(args.files) - len(args.color)))

        if args.legend and args.labels is None:
            args.labels = [f'Dataset {i+1}' for i in range(len(args.files))]

    # Track if we have a colormap for colorbar
    has_colormap = False
    scatter_obj = None

    # Plot data from each file
    if args.files:
        for i, filename in enumerate(args.files):
            mjd, coord1, coord2, sizes, colors, labels = read_data(
                filename,
                ignore_extra=args.ignore_extra,
                labels_from_file=args.labels_from_file,
                solar_relative=args.solar_relative
            )

            if args.solar_relative:
                if mjd is None:
                    print("Error: --solar-relative requires MJD as first column", file=sys.stderr)
                    sys.exit(1)

                coord1, coord2 = compute_solar_relative_coords(
                    mjd, coord1, coord2, args.input_coord, args.solar_center
                )
            else:
                if not args.earth and args.input_coord != args.plot_coord:
                    coord1, coord2 = transform_coordinates(
                        coord1, coord2, args.input_coord, args.plot_coord
                    )

            if args.projection in ['mollweide', 'hammer', 'aitoff']:
                coord1 = np.where(coord1 > 180, coord1 - 360, coord1)

            if sizes is not None:
                s = sizes * args.size
            else:
                s = args.size

            if colors is not None:
                c = colors
                cmap = args.cmap
                has_colormap = True
            else:
                c = args.color[i]
                cmap = None

            label = args.labels[i] if args.labels and i < len(args.labels) else None

            scatter = ax.scatter(coord1, coord2, s=s, c=c, marker=marker,
                               alpha=args.alpha, transform=ccrs.PlateCarree(),
                               edgecolors=args.edgecolor, linewidths=args.edgewidth,
                               cmap=cmap, label=label, zorder=2)

            if labels and args.labels_from_file:
                for j, (x, y, lbl) in enumerate(zip(coord1, coord2, labels)):
                    if lbl:
                        ax.text(x, y, lbl, fontsize=8, ha='left', va='bottom',
                               transform=ccrs.PlateCarree(), zorder=3)

            if has_colormap:
                scatter_obj = scatter

    # Add colorbar if requested
    if args.cbar and has_colormap and scatter_obj is not None:
        plt.colorbar(scatter_obj, ax=ax, orientation='horizontal',
                    pad=0.05, shrink=0.8, label='Color Value')

    # Add cardinal direction markers
    if args.cardinal:
        plot_cardinal_directions(ax, args)

    # Add legend
    if args.legend or (not args.earth and (args.catalog or args.ecliptic or args.galactic_plane)):
        handler_map = {}
        if hasattr(ax, '_gc_legend_handler'):
            handler_map.update(ax._gc_legend_handler)

        legend = ax.legend(loc='best', framealpha=0.9, facecolor='white',
                 edgecolor='gray', frameon=True, borderpad=0.5,
                 handler_map=handler_map if handler_map else None)
        legend.set_zorder(100)

    # Add title
    if args.title:
        ax.set_title(args.title, fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout(pad=1.5)

    # Save or show
    if args.output:
        plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight',
                   facecolor=fig.get_facecolor())
        print(f"Saved to {args.output}")
    else:
        print("\nDisplaying plot... (Close the plot window to exit)")
        plt.show()
