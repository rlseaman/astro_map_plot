"""Static plotting functions for sky and terrestrial maps."""

import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Ellipse
from matplotlib.legend_handler import HandlerPatch
from matplotlib.patches import Circle

from mapplot.catalog import get_bright_stars
from mapplot.coordinates import transform_coordinates
from mapplot.geometry import (ecliptic_path, galactic_plane_path, celestial_equator_path,
                              get_pole_coordinates, milky_way_density_contours)
from mapplot.observatories import load_mpc_observatories


def plot_sky_map(ax, args):
    """Plot celestial data on sky map."""

    # Set background color
    if args.facecolor:
        ax.set_facecolor(args.facecolor)
    else:
        ax.set_facecolor(args.bgcolor)

    # Plot built-in star catalog if requested
    if args.catalog:
        stars = get_bright_stars(args.max_mag)
        ra_list, dec_list, mag_list = [], [], []

        for name, ra, dec, mag in stars:
            ra_list.append(ra)
            dec_list.append(dec)
            mag_list.append(mag)

        ra_arr = np.array(ra_list)
        dec_arr = np.array(dec_list)
        mag_arr = np.array(mag_list)

        # Transform to plot coordinates if needed
        if args.plot_coord != 'equatorial':
            ra_arr, dec_arr = transform_coordinates(
                ra_arr, dec_arr, 'equatorial', args.plot_coord
            )

        # Adjust RA for plotting (0-360 or -180 to 180)
        if args.projection in ['mollweide', 'hammer', 'aitoff']:
            ra_arr = np.where(ra_arr > 180, ra_arr - 360, ra_arr)

        # Size inversely proportional to magnitude (brighter = bigger)
        sizes = 100 * 10**(-mag_arr / 2.5)

        ax.scatter(ra_arr, dec_arr, s=sizes, c='yellow', marker='*',
                  edgecolors='orange', linewidths=0.5, alpha=0.9,
                  transform=ccrs.PlateCarree(), zorder=3,
                  label=f'BSC5 (mag <= {args.max_mag})')

    # Plot Milky Way density if requested
    if args.milky_way:
        contours = milky_way_density_contours()
        for l, b, width in contours:
            b_range = np.linspace(-width, width, 20)
            l_array = np.full_like(b_range, l)

            if args.plot_coord == 'galactic':
                plot_l, plot_b = l_array, b_range
            else:
                plot_l, plot_b = transform_coordinates(
                    l_array, b_range, 'galactic', args.plot_coord
                )

            if args.projection in ['mollweide', 'hammer', 'aitoff']:
                plot_l = np.where(plot_l > 180, plot_l - 360, plot_l)

            ax.fill(plot_l, plot_b, color='gray', alpha=0.03,
                   transform=ccrs.PlateCarree(), zorder=1)

    # Plot ecliptic
    if args.ecliptic:
        if args.solar_relative:
            ecl_lon = np.linspace(-180, 180, 360)
            ecl_lat = np.zeros_like(ecl_lon)
            ax.plot(ecl_lon, ecl_lat, color='red', linewidth=1.5, alpha=0.7,
                   transform=ccrs.PlateCarree(), label='Ecliptic')
        else:
            ecl_lon, ecl_lat = ecliptic_path(n_points=720)

            if args.plot_coord == 'ecliptic':
                plot_lon, plot_lat = ecl_lon, ecl_lat
            else:
                plot_lon, plot_lat = transform_coordinates(
                    ecl_lon, ecl_lat, 'ecliptic', args.plot_coord
                )

            if args.projection in ['mollweide', 'hammer', 'aitoff']:
                plot_lon = np.where(plot_lon > 180, plot_lon - 360, plot_lon)

            _plot_segmented_line(ax, plot_lon, plot_lat, color='red',
                                linewidth=1.5, alpha=0.7, label='Ecliptic')

    # Plot galactic plane
    if args.galactic_plane:
        gal_l, gal_b = galactic_plane_path(n_points=720)

        if args.plot_coord == 'galactic':
            plot_l, plot_b = gal_l, gal_b
        else:
            plot_l, plot_b = transform_coordinates(
                gal_l, gal_b, 'galactic', args.plot_coord
            )

        if args.projection in ['mollweide', 'hammer', 'aitoff']:
            plot_l = np.where(plot_l > 180, plot_l - 360, plot_l)

        _plot_segmented_line(ax, plot_l, plot_b, color='blue',
                            linewidth=1.5, alpha=0.7, label='Galactic Plane')

        # Plot galactic center with tilted ellipse
        gc_l, gc_b = 0.0, 0.0

        if args.plot_coord == 'galactic':
            gc_plot_l, gc_plot_b = gc_l, gc_b
        else:
            gc_plot_l, gc_plot_b = transform_coordinates(
                np.array([gc_l]), np.array([gc_b]), 'galactic', args.plot_coord
            )
            gc_plot_l, gc_plot_b = gc_plot_l[0], gc_plot_b[0]

        if args.projection in ['mollweide', 'hammer', 'aitoff']:
            gc_plot_l = gc_plot_l - 360 if gc_plot_l > 180 else gc_plot_l

        # Fuzzy white interior
        ax.scatter(gc_plot_l, gc_plot_b, s=100, c='white',
                  marker='o', alpha=0.5,
                  transform=ccrs.PlateCarree(), zorder=4)

        # Tilted ellipse outline
        ellipse = Ellipse((gc_plot_l, gc_plot_b), width=8, height=5,
                         angle=30, facecolor='none',
                         edgecolor='blue', linewidth=1.5, alpha=0.9,
                         transform=ccrs.PlateCarree(), zorder=4)
        ax.add_patch(ellipse)

        # Proxy ellipse for legend
        legend_ellipse = Ellipse((0, 0), width=1, height=0.6,
                                 angle=30, facecolor='none',
                                 edgecolor='blue', linewidth=1.5,
                                 label='Galactic Center')

        class EllipseHandler(HandlerPatch):
            def create_artists(self, legend, orig_handle,
                             xdescent, ydescent, width, height, fontsize, trans):
                center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 0.5 * ydescent
                p = Ellipse(xy=center, width=width * 0.8, height=height * 0.5,
                           angle=30, facecolor='none', edgecolor='blue',
                           linewidth=1.5, transform=trans)
                dot = Circle(xy=center, radius=width * 0.08,
                           facecolor='blue', edgecolor='none',
                           transform=trans, zorder=10)
                return [p, dot]

        ax.add_artist(legend_ellipse)

        if not hasattr(ax, '_gc_legend_handler'):
            ax._gc_legend_handler = {legend_ellipse: EllipseHandler()}
            ax._gc_legend_proxy = legend_ellipse

        # Center dot
        ax.scatter(gc_plot_l, gc_plot_b, s=15, c='blue',
                  marker='o', alpha=0.9,
                  transform=ccrs.PlateCarree(), zorder=5)

    # Plot celestial equator
    if args.celestial_equator:
        eq_ra, eq_dec = celestial_equator_path(n_points=720)

        if args.plot_coord == 'equatorial':
            plot_ra, plot_dec = eq_ra, eq_dec
        else:
            plot_ra, plot_dec = transform_coordinates(
                eq_ra, eq_dec, 'equatorial', args.plot_coord
            )

        if args.projection in ['mollweide', 'hammer', 'aitoff']:
            plot_ra = np.where(plot_ra > 180, plot_ra - 360, plot_ra)

        _plot_segmented_line(ax, plot_ra, plot_dec, color='green',
                            linewidth=1.5, alpha=0.7, label='Celestial Equator')

    # Plot poles
    if args.poles:
        pole_systems = []
        if 'all' in args.poles:
            pole_systems = ['equatorial', 'ecliptic', 'galactic']
        else:
            pole_systems = args.poles

        for pole_system in pole_systems:
            poles = get_pole_coordinates(pole_system)

            for pole_name in ['north', 'south']:
                pole = poles[pole_name]
                coord1, coord2 = pole['coord1'], pole['coord2']

                if pole_system != args.plot_coord:
                    coord1_arr = np.array([coord1])
                    coord2_arr = np.array([coord2])
                    coord1_arr, coord2_arr = transform_coordinates(
                        coord1_arr, coord2_arr, pole_system, args.plot_coord
                    )
                    coord1, coord2 = coord1_arr[0], coord2_arr[0]

                if args.projection in ['mollweide', 'hammer', 'aitoff']:
                    coord1 = coord1 - 360 if coord1 > 180 else coord1

                label = f"{pole['name']}" if pole_name == 'north' else None
                marker_size = 120 if poles['marker'] == 'x' else 150

                if poles['marker'] in ['x', '+']:
                    ax.scatter(coord1, coord2, s=marker_size, c=poles['color'],
                              marker=poles['marker'], linewidths=1.5,
                              alpha=0.9, transform=ccrs.PlateCarree(), zorder=4,
                              label=label)
                else:
                    ax.scatter(coord1, coord2, s=marker_size, c=poles['color'],
                              marker=poles['marker'], edgecolors='black', linewidths=1.5,
                              alpha=0.9, transform=ccrs.PlateCarree(), zorder=4,
                              label=label)

    return True


def plot_cardinal_directions(ax, args):
    """
    Add cardinal direction markers (N, S, E, W) to the plot.

    Position depends on mode:
    - Earth mode: N=top, S=bottom, E=right, W=left (right-handed)
    - Sky mode: N=top, S=bottom, E=LEFT, W=right (left-handed, astronomical convention)
    """
    if args.earth:
        ax.text(0, 88, 'N', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)
        ax.text(0, -88, 'S', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)
        ax.text(178, 0, 'E', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)
        ax.text(-178, 0, 'W', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)
    else:
        # Sky mode (left-handed, astronomical convention)
        ax.text(0, 88, 'N', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)
        ax.text(0, -88, 'S', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)
        ax.text(178, 0, 'E', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)
        ax.text(-178, 0, 'W', ha='center', va='center', fontsize=14, fontweight='bold',
               transform=ccrs.PlateCarree(), bbox=dict(boxstyle='circle', facecolor='white', alpha=0.9), zorder=100)


def plot_custom_gridlines(ax, grid_coord, plot_coord, grid_spacing, args):
    """
    Plot gridlines in a different coordinate system.

    Parameters:
    - grid_coord: coordinate system for the grid
    - plot_coord: coordinate system for plotting
    - grid_spacing: tuple of (lon_spacing, lat_spacing)
    """
    lon_spacing, lat_spacing = grid_spacing

    # Longitude lines (constant longitude, varying latitude)
    for lon in np.arange(0, 360, lon_spacing):
        lat_vals = np.linspace(-90, 90, 180)
        lon_vals = np.full_like(lat_vals, lon)

        if grid_coord != plot_coord:
            lon_vals, lat_vals = transform_coordinates(
                lon_vals, lat_vals, grid_coord, plot_coord
            )

        if args.projection in ['mollweide', 'hammer', 'aitoff']:
            lon_vals = np.where(lon_vals > 180, lon_vals - 360, lon_vals)

        _plot_grid_line(ax, lon_vals, lat_vals, args)

    # Latitude lines (constant latitude, varying longitude)
    for lat in np.arange(-90, 91, lat_spacing):
        if abs(lat) > 89:
            continue
        lon_vals = np.linspace(0, 360, 360)
        lat_vals = np.full_like(lon_vals, lat)

        if grid_coord != plot_coord:
            lon_vals, lat_vals = transform_coordinates(
                lon_vals, lat_vals, grid_coord, plot_coord
            )

        if args.projection in ['mollweide', 'hammer', 'aitoff']:
            lon_vals = np.where(lon_vals > 180, lon_vals - 360, lon_vals)

        _plot_grid_line(ax, lon_vals, lat_vals, args)


def plot_terrestrial_map(ax, args):
    """Plot terrestrial map features."""

    if args.coastlines:
        ax.coastlines(linewidth=0.5, color='black')

    if args.countries:
        ax.add_feature(cfeature.BORDERS, linewidth=0.3, edgecolor='gray')

    if args.land:
        ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=0)

    if args.ocean:
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue', zorder=0)

    # Plot observatories if requested
    if args.observatories or args.obs_codes:
        observatories = load_mpc_observatories(args.obs_file)

        if observatories:
            if args.obs_codes:
                obs_codes_upper = [c.upper() for c in args.obs_codes]
                obs_to_plot = [obs for obs in observatories
                              if obs['code'].upper() in obs_codes_upper]
                if not obs_to_plot:
                    import sys
                    print(f"Warning: No observatories found with codes: {args.obs_codes}",
                          file=sys.stderr)
            else:
                obs_to_plot = observatories

            if obs_to_plot:
                lons = [obs['lon'] for obs in obs_to_plot]
                lats = [obs['lat'] for obs in obs_to_plot]

                ax.scatter(lons, lats, s=50, c='red', marker='^',
                          edgecolors='darkred', linewidths=1,
                          alpha=0.8, transform=ccrs.PlateCarree(),
                          zorder=5, label='Observatories')

                if len(obs_to_plot) <= 50:
                    for obs in obs_to_plot:
                        ax.text(obs['lon'], obs['lat'], f" {obs['code']}",
                               fontsize=6, ha='left', va='center',
                               transform=ccrs.PlateCarree(), zorder=6)

                import sys
                print(f"Plotted {len(obs_to_plot)} observatories", file=sys.stderr)


def _plot_segmented_line(ax, lon, lat, color, linewidth, alpha, label=None):
    """Plot a line, splitting at 180-degree discontinuities."""
    dl = np.diff(lon)
    breaks = np.where(np.abs(dl) > 180)[0]

    if len(breaks) > 0:
        start = 0
        for break_point in breaks:
            ax.plot(lon[start:break_point+1], lat[start:break_point+1],
                   color=color, linewidth=linewidth, alpha=alpha,
                   transform=ccrs.PlateCarree())
            start = break_point + 1
        ax.plot(lon[start:], lat[start:],
               color=color, linewidth=linewidth, alpha=alpha,
               transform=ccrs.PlateCarree(), label=label)
    else:
        ax.plot(lon, lat, color=color, linewidth=linewidth, alpha=alpha,
               transform=ccrs.PlateCarree(), label=label)


def _plot_grid_line(ax, lon_vals, lat_vals, args):
    """Plot a single grid line, splitting at discontinuities."""
    dl = np.diff(lon_vals)
    breaks = np.where(np.abs(dl) > 180)[0]

    if len(breaks) > 0:
        start = 0
        for break_point in breaks:
            ax.plot(lon_vals[start:break_point+1], lat_vals[start:break_point+1],
                   color=args.grid_color, linewidth=0.5, alpha=args.grid_alpha,
                   linestyle=args.grid_style, transform=ccrs.PlateCarree(), zorder=0.5)
            start = break_point + 1
        ax.plot(lon_vals[start:], lat_vals[start:],
               color=args.grid_color, linewidth=0.5, alpha=args.grid_alpha,
               linestyle=args.grid_style, transform=ccrs.PlateCarree(), zorder=0.5)
    else:
        ax.plot(lon_vals, lat_vals, color=args.grid_color, linewidth=0.5,
               alpha=args.grid_alpha, linestyle=args.grid_style,
               transform=ccrs.PlateCarree(), zorder=0.5)
