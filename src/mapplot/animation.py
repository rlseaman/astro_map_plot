"""Animation engine for time-series visualization."""

import sys
from collections import defaultdict

import numpy as np
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.ticker import FuncFormatter

from mapplot.constants import MARKERS
from mapplot.config import get_data_colors
from mapplot.coordinates import get_sun_position, mjd_to_year, get_current_mjd, transform_coordinates


def create_animation(args, ax, fig, all_data, palette_name, observatories=None, obs_dates=None, ax_timeline=None):
    """
    Create animation using FuncAnimation.

    Parameters:
    - observatories: list of observatory dicts with code, lon, lat, name
    - obs_dates: dict mapping code -> {start_mjd, end_mjd}
    - ax_timeline: optional secondary axis for timeline plot
    """
    # Convert marker name to matplotlib code
    marker = MARKERS.get(args.marker, args.marker)

    # Calculate time-based animation parameters
    data_mjd_start = all_data[0]['mjd']
    data_mjd_end = all_data[-1]['mjd']

    # Use specified start time or earliest data point
    if args.start_time is not None:
        mjd_start = args.start_time
    else:
        mjd_start = data_mjd_start

    # Use specified stop time or current time
    if args.stop_time is not None:
        mjd_end = args.stop_time
    else:
        mjd_end = get_current_mjd()
        print(f"Using current time as stop: MJD {mjd_end:.2f} ({mjd_to_year(mjd_end):.1f})",
              file=sys.stderr)

    # Ensure stop is after start
    if mjd_end <= mjd_start:
        print(f"Error: Stop time ({mjd_end}) must be after start time ({mjd_start})",
              file=sys.stderr)
        sys.exit(1)

    mjd_span = mjd_end - mjd_start

    print(f"Animation time range: MJD {mjd_start:.2f} to {mjd_end:.2f} ({mjd_span:.1f} days)",
          file=sys.stderr)

    if args.time_per_day:
        total_seconds = mjd_span * args.time_per_day / args.speed
        frames_count = int(total_seconds * args.fps)
        interval = 1000 / args.fps
        days_per_frame = mjd_span / frames_count
    else:
        frames_count = len(all_data)
        interval = (1000 / args.fps) / args.speed
        days_per_frame = mjd_span / frames_count

    print(f"Animation: {frames_count} frames, {days_per_frame:.2f} days/frame, " +
          f"{1000/interval:.1f} fps", file=sys.stderr)

    # Add end pause frames if requested
    end_pause_frames = 0
    if args.end_pause > 0:
        end_pause_frames = int(args.end_pause * args.fps)
        print(f"End pause: {end_pause_frames} frames ({args.end_pause} sec)", file=sys.stderr)

    # Add keyframe if requested
    keyframe_frames = 0
    keyframe_delay_frames = 0
    keyframe_duration = 3.0
    if args.show_keyframe:
        keyframe_frames = int(keyframe_duration * args.fps)
        keyframe_delay_frames = int(args.keyframe_delay * args.fps)
        print(f"Keyframe: {keyframe_delay_frames} delay frames + {keyframe_frames} keyframe frames " +
              f"({args.keyframe_delay + keyframe_duration} sec total) at " +
              f"{'start' if args.keyframe_at_start else 'end'}", file=sys.stderr)

    # Calculate total frames based on keyframe position
    if args.show_keyframe and args.keyframe_at_start:
        total_frames = keyframe_delay_frames + keyframe_frames + frames_count + end_pause_frames
        keyframe_delay_start = 0
        keyframe_start = keyframe_delay_frames
        animation_offset = keyframe_delay_frames + keyframe_frames
    else:
        total_frames = frames_count + end_pause_frames + keyframe_delay_frames + keyframe_frames
        keyframe_delay_start = frames_count + end_pause_frames
        keyframe_start = frames_count + end_pause_frames + keyframe_delay_frames
        animation_offset = 0

    # Storage for plot artists
    scatter_artists = {}
    time_text = None
    stats_text = None
    obs_count_text = None

    # Window size for statistics and timeline
    max_stats_cycles = max(1, min(15, args.stats_cycles))

    # Get file colors for timeline stacked plot
    if args.color is None:
        file_colors = get_data_colors(palette_name, len(args.files))
    else:
        file_colors = args.color[:]
        if len(file_colors) < len(args.files):
            file_colors.extend(['black'] * (len(args.files) - len(file_colors)))

    # Storage for timeline data
    timeline_data = []
    timeline_polys = []
    timeline_started = False

    # Initialize timeline axis if present
    if ax_timeline is not None:
        if args.timeline_reverse:
            ax_timeline.set_xlim(mjd_start, mjd_end)
        else:
            ax_timeline.set_xlim(mjd_end, mjd_start)

        if args.timeline_xlabel_years:
            def mjd_to_year_label(x, pos):
                return f'{mjd_to_year(x):.0f}'
            ax_timeline.xaxis.set_major_formatter(FuncFormatter(mjd_to_year_label))

        ax_timeline.set_ylim(0, 100)

    # Storage for sun trail
    sun_trail = []
    max_sun_trail = 8

    # Pre-compute MJD lookup table for fast binary search
    mjd_values = np.array([record['mjd'] for record in all_data])

    def init_frame():
        """Initialize animation."""
        return []

    def update_frame(frame_num):
        """Update function for each frame."""
        nonlocal time_text, stats_text, obs_count_text
        nonlocal timeline_data, timeline_polys, timeline_started

        # Check if this is in the delay period before keyframe
        is_keyframe_delay = False
        if args.show_keyframe:
            if args.keyframe_at_start and frame_num < keyframe_delay_frames:
                is_keyframe_delay = True
            elif not args.keyframe_at_start and frame_num >= keyframe_delay_start and frame_num < keyframe_start:
                is_keyframe_delay = True

        # Check if this is a keyframe
        is_keyframe = False
        if args.show_keyframe:
            if args.keyframe_at_start and frame_num >= keyframe_delay_frames and frame_num < (keyframe_delay_frames + keyframe_frames):
                is_keyframe = True
            elif not args.keyframe_at_start and frame_num >= keyframe_start:
                is_keyframe = True

        # Adjust frame_num for animation offset
        if args.show_keyframe and args.keyframe_at_start and not is_keyframe and not is_keyframe_delay:
            adjusted_frame = frame_num - animation_offset
        else:
            adjusted_frame = frame_num - (animation_offset if not is_keyframe and not is_keyframe_delay else 0)

        # Handle keyframe delay
        if is_keyframe_delay:
            current_mjd = mjd_end
            show_all = False
            show_sun_frame = args.show_sun
        elif is_keyframe:
            current_mjd = mjd_end
            show_all = True
            show_sun_frame = False
        elif adjusted_frame >= frames_count:
            current_mjd = mjd_end
            show_all = False
            show_sun_frame = args.show_sun
        else:
            current_mjd = mjd_start + (adjusted_frame * days_per_frame)
            show_all = False
            show_sun_frame = args.show_sun

        # Find all points up to current time using binary search
        if show_all:
            current_idx = len(all_data) - 1
        else:
            current_idx = np.searchsorted(mjd_values, current_mjd, side='right') - 1
            if current_idx < 0:
                current_idx = 0

        # Determine which points to show
        if show_all:
            start_idx = 0
            end_idx = len(all_data)
            visible_data = all_data[start_idx:end_idx]
        else:
            if frame_num == 0 and args.show_before_start:
                start_time_idx = np.searchsorted(mjd_values, mjd_start, side='left')
                start_idx = 0
                end_idx = max(current_idx + 1, start_time_idx)
                visible_data = all_data[start_idx:end_idx]
            else:
                if args.trail_days:
                    cutoff_mjd = current_mjd - args.trail_days
                    start_idx = np.searchsorted(mjd_values, cutoff_mjd, side='left')
                elif args.trail_length and current_idx > args.trail_length:
                    start_idx = current_idx - args.trail_length
                else:
                    start_idx = 0

                end_idx = current_idx + 1
                visible_data = all_data[start_idx:end_idx]

        if not visible_data:
            return []

        # Clear previous scatter plots
        for artist in scatter_artists.values():
            artist.remove()
        scatter_artists.clear()

        # Group by file for separate scatter plots
        by_file = defaultdict(list)
        for record in visible_data:
            by_file[record['file_index']].append(record)

        artists = []

        # Plot each file's points
        for file_idx, records in by_file.items():
            lons = np.array([r['lon'] for r in records])
            lats = np.array([r['lat'] for r in records])
            sizes = np.array([r['size'] for r in records])
            colors = [r['color'] for r in records]

            if args.trail_fade and len(records) > 1:
                alphas = np.linspace(0.2, 1.0, len(records))
            else:
                alphas = np.full(len(records), 0.7)

            if args.highlight_current and not show_all and current_idx < len(all_data):
                current_record = all_data[current_idx]
                if file_idx == current_record['file_index']:
                    if len(lons) > 1:
                        colors_with_alpha = [(mcolors.to_rgb(c) + (alpha,))
                                            for c, alpha in zip(colors[:-1], alphas[:-1])]
                        sc = ax.scatter(lons[:-1], lats[:-1], s=sizes[:-1], c=colors_with_alpha,
                                       marker=marker, edgecolors='none',
                                       transform=ccrs.PlateCarree(), zorder=3)
                        scatter_artists[f'file_{file_idx}_trail'] = sc
                        artists.append(sc)

                    sc_current = ax.scatter([lons[-1]], [lats[-1]], s=[sizes[-1] * 2],
                                           c=[colors[-1]], marker=marker, alpha=1.0,
                                           edgecolors='black', linewidths=1,
                                           transform=ccrs.PlateCarree(), zorder=4)
                    scatter_artists[f'file_{file_idx}_current'] = sc_current
                    artists.append(sc_current)
                else:
                    colors_with_alpha = [(mcolors.to_rgb(c) + (alpha,))
                                        for c, alpha in zip(colors, alphas)]
                    sc = ax.scatter(lons, lats, s=sizes, c=colors_with_alpha,
                                   marker=marker, edgecolors='none',
                                   transform=ccrs.PlateCarree(), zorder=3)
                    scatter_artists[f'file_{file_idx}'] = sc
                    artists.append(sc)
            else:
                colors_with_alpha = [(mcolors.to_rgb(c) + (alpha,))
                                    for c, alpha in zip(colors, alphas)]
                sc = ax.scatter(lons, lats, s=sizes, c=colors_with_alpha,
                               marker=marker, edgecolors='none',
                               transform=ccrs.PlateCarree(), zorder=3)
                scatter_artists[f'file_{file_idx}'] = sc
                artists.append(sc)

        # Plot observatories if animated
        if observatories and obs_dates and args.animate_observatories:
            grace_period_start = mjd_end - 365.25
            fade_duration_days = 3.0 / (24.0 * 3600.0) * (1000.0 / interval)
            fade_cutoff = mjd_start + fade_duration_days

            active_obs = []
            for obs in observatories:
                code = obs['code'].upper()
                if code in obs_dates:
                    dates = obs_dates[code]
                    obs_start = dates['start_mjd']
                    obs_end = dates['end_mjd']

                    if obs_start > current_mjd:
                        continue
                    if obs_end < mjd_start and current_mjd > fade_cutoff:
                        continue
                    if obs_end >= current_mjd or obs_end >= grace_period_start:
                        active_obs.append(obs)

            if active_obs:
                obs_lons = [obs['lon'] for obs in active_obs]
                obs_lats = [obs['lat'] for obs in active_obs]

                obs_scatter = ax.scatter(obs_lons, obs_lats, s=50, c='red',
                                        marker='^', edgecolors='darkred',
                                        linewidths=1, alpha=0.8,
                                        transform=ccrs.PlateCarree(), zorder=5)
                scatter_artists['observatories'] = obs_scatter
                artists.append(obs_scatter)

                if len(active_obs) <= 30:
                    for obs in active_obs:
                        obs_label = ax.text(obs['lon'], obs['lat'], f" {obs['code']}",
                                           fontsize=6, ha='left', va='center',
                                           transform=ccrs.PlateCarree(), zorder=6,
                                           bbox=dict(boxstyle='round,pad=0.2',
                                                   facecolor='white', alpha=0.7,
                                                   edgecolor='none'))
                        scatter_artists[f"obs_label_{obs['code']}"] = obs_label
                        artists.append(obs_label)

            if obs_count_text:
                obs_count_text.remove()

            obs_count = len(active_obs)
            obs_count_str = f'total: {obs_count}'

            obs_count_text = ax.text(0.98, 0.02, obs_count_str,
                                    transform=ax.transAxes, fontsize=10,
                                    verticalalignment='bottom', horizontalalignment='right',
                                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
                                    zorder=100)
            artists.append(obs_count_text)

        # Plot sun position if requested
        if show_sun_frame and not args.earth:
            sun_lon, sun_lat = get_sun_position(current_mjd)

            if args.plot_coord == 'ecliptic':
                plot_sun_lon, plot_sun_lat = sun_lon, sun_lat
            else:
                plot_sun_lon, plot_sun_lat = transform_coordinates(
                    np.array([sun_lon]), np.array([sun_lat]),
                    'ecliptic', args.plot_coord
                )
                plot_sun_lon, plot_sun_lat = plot_sun_lon[0], plot_sun_lat[0]

            if args.projection in ['mollweide', 'hammer', 'aitoff']:
                plot_sun_lon = plot_sun_lon - 360 if plot_sun_lon > 180 else plot_sun_lon

            sun_trail.append((plot_sun_lon, plot_sun_lat))

            if len(sun_trail) > max_sun_trail:
                sun_trail.pop(0)

            if len(sun_trail) > 1:
                for i, (trail_lon, trail_lat) in enumerate(sun_trail[:-1]):
                    alpha = 0.15 + (i / max(len(sun_trail) - 2, 1)) * 0.25
                    size = 60 + (i / max(len(sun_trail) - 2, 1)) * 30

                    trail_scatter = ax.scatter([trail_lon], [trail_lat],
                                              s=size, c='yellow', marker='o',
                                              edgecolors='orange', linewidths=1.0,
                                              alpha=alpha, transform=ccrs.PlateCarree(),
                                              zorder=9)
                    scatter_artists[f'sun_trail_{i}'] = trail_scatter
                    artists.append(trail_scatter)

            sun_scatter = ax.scatter([plot_sun_lon], [plot_sun_lat],
                                    s=100, c='yellow', marker='o',
                                    edgecolors='orange', linewidths=1.5,
                                    alpha=1.0, transform=ccrs.PlateCarree(),
                                    zorder=10)
            scatter_artists['sun'] = sun_scatter
            artists.append(sun_scatter)

        # Update time display
        if args.show_time and not show_all:
            if time_text:
                time_text.remove()

            if args.time_format == 'year':
                year = mjd_to_year(current_mjd)
                time_str = f'Year: {year:.3f}'
            else:
                time_str = f'MJD: {current_mjd:.2f}'

            time_text = ax.text(0.02, 0.98, time_str,
                               transform=ax.transAxes, fontsize=12,
                               verticalalignment='top',
                               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
                               zorder=100)
            artists.append(time_text)

        # Update statistics display
        if args.trail_days and args.labels and not show_all:
            if stats_text:
                stats_text.remove()

            full_window_days = args.trail_days * max_stats_cycles
            cutoff_mjd = current_mjd - full_window_days

            window_start_idx = np.searchsorted(mjd_values, cutoff_mjd, side='left')
            window_end_idx = current_idx + 1
            window_data = all_data[window_start_idx:window_end_idx]

            file_counts = defaultdict(int)
            for record in window_data:
                file_counts[record['file_index']] += 1

            total_count = len(window_data)

            window_info = f'({full_window_days:.0f} day window)'
            stats_lines = [f'Objects: {total_count} {window_info}']

            if len(args.labels) > 1:
                for i, label in enumerate(args.labels):
                    count = file_counts.get(i, 0)
                    if total_count > 0:
                        fraction = count / total_count
                        percentage = int(round(fraction * 100))
                        stats_lines.append(f'{label}: {percentage}%')
                    else:
                        stats_lines.append(f'{label}: 0%')

            stats_str = '\n'.join(stats_lines)

            stats_text = ax.text(0.98, 0.98, stats_str,
                                transform=ax.transAxes, fontsize=10,
                                verticalalignment='top', horizontalalignment='right',
                                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
                                zorder=100)
            artists.append(stats_text)

        elif is_keyframe and args.labels:
            if stats_text:
                stats_text.remove()

            file_counts = defaultdict(int)
            for record in all_data:
                file_counts[record['file_index']] += 1

            total_count = len(all_data)

            stats_lines = [f'Total: {total_count}']

            if len(args.labels) > 1:
                for i, label in enumerate(args.labels):
                    count = file_counts.get(i, 0)
                    if total_count > 0:
                        fraction = count / total_count
                        percentage = int(round(fraction * 100))
                        stats_lines.append(f'{label}: {count} ({percentage}%)')
                    else:
                        stats_lines.append(f'{label}: 0 (0%)')

            stats_str = '\n'.join(stats_lines)

            stats_text = ax.text(0.98, 0.98, stats_str,
                                transform=ax.transAxes, fontsize=10,
                                verticalalignment='top', horizontalalignment='right',
                                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
                                zorder=100)
            artists.append(stats_text)

        # Update timeline plot if requested
        if ax_timeline is not None and args.trail_days and not show_all:
            window_days = args.trail_days * max_stats_cycles
            cutoff_mjd = current_mjd - window_days

            window_start_idx = np.searchsorted(mjd_values, cutoff_mjd, side='left')
            window_end_idx = current_idx + 1
            window_data = all_data[window_start_idx:window_end_idx]

            file_counts = defaultdict(int)
            for record in window_data:
                file_counts[record['file_index']] += 1

            timeline_data.append((current_mjd, dict(file_counts)))

            if not timeline_started and len(timeline_data) > 0:
                first_mjd = timeline_data[0][0]
                if current_mjd - first_mjd >= window_days:
                    timeline_started = True

            if timeline_started or is_keyframe:
                mjds = [d[0] for d in timeline_data]

                n_files = len(args.files) if args.files else 0
                file_data = []
                for file_idx in range(n_files):
                    counts = [d[1].get(file_idx, 0) for d in timeline_data]
                    file_data.append(counts)

                for poly in timeline_polys:
                    poly.remove()
                timeline_polys.clear()

                if n_files > 1 and args.labels:
                    polys = ax_timeline.stackplot(mjds, *file_data,
                                                  colors=file_colors[:n_files],
                                                  alpha=0.7)
                    timeline_polys.extend(polys)
                    artists.extend(polys)
                else:
                    total_counts = [sum(d[1].values()) for d in timeline_data]
                    line, = ax_timeline.plot(mjds, total_counts, 'b-', linewidth=1.5)
                    timeline_polys.append(line)
                    artists.append(line)

                if timeline_data:
                    max_count = max(sum(d[1].values()) for d in timeline_data)
                    ax_timeline.set_ylim(0, max_count * 1.1)

        return artists

    # Create animation
    print(f"Creating animation: {total_frames} frames at {1000/interval:.1f} fps", file=sys.stderr)
    anim = FuncAnimation(fig, update_frame, frames=total_frames,
                        init_func=init_frame, blit=False, interval=interval,
                        repeat=True)

    return anim
