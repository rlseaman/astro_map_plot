"""Coordinate transformations, sun position, MJD utilities, solar-relative coords."""

import sys
from datetime import datetime, timezone

import numpy as np
from astropy.coordinates import SkyCoord, GeocentricTrueEcliptic
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import get_sun


def transform_coordinates(lon, lat, from_system, to_system):
    """Transform coordinates between different systems."""
    # Handle wrapping for RA (0-360)
    if from_system == 'equatorial':
        lon = lon % 360

    # Create coordinate object based on input system
    if from_system == 'equatorial':
        coords = SkyCoord(ra=lon*u.degree, dec=lat*u.degree, frame='icrs')
    elif from_system == 'ecliptic':
        coords = SkyCoord(lon=lon*u.degree, lat=lat*u.degree,
                         frame=GeocentricTrueEcliptic)
    elif from_system == 'galactic':
        coords = SkyCoord(l=lon*u.degree, b=lat*u.degree, frame='galactic')
    else:
        raise ValueError(f"Unknown coordinate system: {from_system}")

    # Transform to output system
    if to_system == 'equatorial':
        coords_out = coords.icrs
        return coords_out.ra.degree, coords_out.dec.degree
    elif to_system == 'ecliptic':
        coords_out = coords.transform_to(GeocentricTrueEcliptic)
        return coords_out.lon.degree, coords_out.lat.degree
    elif to_system == 'galactic':
        coords_out = coords.galactic
        return coords_out.l.degree, coords_out.b.degree
    else:
        raise ValueError(f"Unknown coordinate system: {to_system}")


def get_sun_position_precise(mjd):
    """
    Get the Sun's ecliptic longitude at a given Modified Julian Date.
    Uses astropy for accurate computation.

    Parameters:
    - mjd: Modified Julian Date (float or array)

    Returns:
    - sun_lon: Sun's ecliptic longitude in degrees (float or array)
    """
    time = Time(mjd, format='mjd')
    sun = get_sun(time)
    sun_ecl = sun.transform_to(GeocentricTrueEcliptic)
    return sun_ecl.lon.degree


def get_sun_position_fast(mjd):
    """
    Calculate the Sun's position in ecliptic coordinates for a given MJD.

    Returns (longitude, latitude) in degrees.
    Latitude is always 0 (sun is on the ecliptic plane by definition).

    Uses simple mean longitude approximation, accurate to ~1 degree.
    """
    # J2000.0 epoch (MJD 51544.5 = 2000 Jan 1.5)
    mjd_j2000 = 51544.5

    # Days since J2000
    d = mjd - mjd_j2000

    # Mean longitude of the sun (degrees)
    # L0 = 280.460 deg at J2000, advances 0.9856474 deg per day
    L0 = 280.460
    rate = 0.9856474

    # Calculate mean longitude
    L = L0 + rate * d

    # Normalize to 0-360 range
    L = L % 360.0

    # Sun is always on the ecliptic plane, so latitude = 0
    return L, 0.0


def get_sun_position(mjd, precise=False):
    """
    Get the Sun's ecliptic position at a given MJD.

    Parameters:
    - mjd: Modified Julian Date (float or array)
    - precise: if True, use astropy (slower but accurate);
               if False, use mean longitude approximation (~1 deg accuracy)

    Returns:
    - If precise: sun_lon (degrees)
    - If not precise: (sun_lon, sun_lat) tuple in degrees (lat is always 0)
    """
    if precise:
        return get_sun_position_precise(mjd)
    else:
        return get_sun_position_fast(mjd)


def mjd_to_year(mjd):
    """
    Convert Modified Julian Date to decimal calendar year.

    MJD = JD - 2400000.5
    JD 2451545.0 = 2000 Jan 1.5 (12:00 TT) = MJD 51544.5

    Returns decimal year (e.g., 2024.5 for mid-2024)
    """
    jd = mjd + 2400000.5
    j2000 = 2451545.0
    days_since_j2000 = jd - j2000
    years_since_j2000 = days_since_j2000 / 365.25
    return 2000.0 + years_since_j2000


def get_current_mjd():
    """Get current MJD from system time."""
    # MJD 0 = November 17, 1858
    mjd_epoch = datetime(1858, 11, 17, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta = now - mjd_epoch
    mjd = delta.total_seconds() / 86400.0
    return mjd


def compute_solar_relative_coords(mjd, ra, dec, input_coord, solar_center=180.0):
    """
    Convert coordinates to solar-relative ecliptic coordinates.

    Parameters:
    - mjd: Modified Julian Date(s)
    - ra: Right ascension or coord1 (degrees)
    - dec: Declination or coord2 (degrees)
    - input_coord: Input coordinate system ('equatorial', 'ecliptic', 'galactic')
    - solar_center: Solar elongation to place at center of plot (degrees, default 180 for opposition)

    Returns:
    - rel_lon: Solar-relative ecliptic longitude (degrees)
    - ecl_lat: Ecliptic latitude (degrees)
    """
    # Convert input coordinates to ecliptic
    ecl_lon, ecl_lat = transform_coordinates(ra, dec, input_coord, 'ecliptic')

    # Get Sun's ecliptic longitude at the given time(s)
    sun_lon, _ = get_sun_position_fast(mjd)

    # Calculate relative longitude (elongation from Sun)
    rel_lon = ecl_lon - sun_lon

    # Wrap to -180 to 180
    rel_lon = np.where(rel_lon > 180, rel_lon - 360, rel_lon)
    rel_lon = np.where(rel_lon < -180, rel_lon + 360, rel_lon)

    # Adjust for centering
    plot_lon = rel_lon - solar_center

    # Wrap to -180 to 180 for plotting
    plot_lon = np.where(plot_lon > 180, plot_lon - 360, plot_lon)
    plot_lon = np.where(plot_lon < -180, plot_lon + 360, plot_lon)

    return plot_lon, ecl_lat
