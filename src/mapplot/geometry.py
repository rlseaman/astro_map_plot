"""Geometric path generators for celestial reference features."""

import numpy as np


def ecliptic_path(n_points=360):
    """Generate points along the ecliptic."""
    lon = np.linspace(0, 360, n_points)
    lat = np.zeros(n_points)
    return lon, lat


def galactic_plane_path(n_points=360):
    """Generate points along the galactic plane."""
    l = np.linspace(0, 360, n_points)
    b = np.zeros(n_points)
    return l, b


def celestial_equator_path(n_points=360):
    """Generate points along the celestial equator (equatorial plane)."""
    ra = np.linspace(0, 360, n_points)
    dec = np.zeros(n_points)
    return ra, dec


def get_pole_coordinates(pole_system):
    """
    Get the coordinates of celestial poles in their native system.
    Returns dict with 'north' and 'south' pole coordinates.
    """
    poles = {}

    if pole_system == 'equatorial':
        poles['north'] = {'coord1': 0.0, 'coord2': 90.0, 'name': 'CP'}
        poles['south'] = {'coord1': 0.0, 'coord2': -90.0, 'name': 'CP'}
        poles['color'] = 'green'
        poles['marker'] = '^'

    elif pole_system == 'ecliptic':
        poles['north'] = {'coord1': 0.0, 'coord2': 90.0, 'name': 'EP'}
        poles['south'] = {'coord1': 0.0, 'coord2': -90.0, 'name': 'EP'}
        poles['color'] = 'red'
        poles['marker'] = 'x'

    elif pole_system == 'galactic':
        poles['north'] = {'coord1': 0.0, 'coord2': 90.0, 'name': 'GP'}
        poles['south'] = {'coord1': 0.0, 'coord2': -90.0, 'name': 'GP'}
        poles['color'] = 'blue'
        poles['marker'] = '+'

    return poles


def milky_way_density_contours():
    """Return approximate Milky Way density contours in galactic coordinates."""
    contours = []

    for l in np.arange(0, 361, 5):
        center_dist = min(abs(l), abs(l - 180), abs(l - 360))
        if center_dist < 30:
            width = 25  # Bulge region
        elif center_dist < 90:
            width = 15  # Inner disk
        else:
            width = 10  # Outer disk

        contours.append((l, 0, width))

    return contours
