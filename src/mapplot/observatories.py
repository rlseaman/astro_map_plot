"""MPC observatory database: download, parse, and load."""

import os
import sys
import urllib.request

import numpy as np


def download_mpc_observatories(url=None):
    """
    Download observatory codes from Minor Planet Center.

    Returns observatory data as list of dicts with:
    - code: 3-character observatory code
    - lon: longitude in degrees (-180 to 180)
    - lat: latitude in degrees
    - name: observatory name
    """
    if url is None:
        url = "https://www.minorplanetcenter.net/iau/lists/ObsCodesF.html"

    try:
        response = urllib.request.urlopen(url, timeout=30)
        content = response.read().decode('utf-8')
        return parse_mpc_observatories(content)
    except Exception as e:
        print(f"Warning: Could not download MPC observatories: {e}", file=sys.stderr)
        return []


def parse_mpc_observatories(content):
    """
    Parse MPC observatory codes from file content.

    Format is fixed-width:
    Code Longitude rho*cos(phi) rho*sin(phi) Name

    where phi is geocentric latitude, rho is Earth radii
    """
    observatories = []

    for line in content.split('\n'):
        line = line.strip()
        if not line or len(line) < 30:
            continue

        # Skip HTML tags if present
        if '<' in line or '>' in line:
            continue

        try:
            # Parse fixed-width format
            code = line[0:3].strip()
            if not code or not code.replace('.', '').isalnum():
                continue

            lon_str = line[4:13].strip()
            rho_cos_str = line[14:21].strip()
            rho_sin_str = line[22:30].strip()
            name = line[30:].strip()

            if not lon_str or not rho_cos_str or not rho_sin_str:
                continue

            lon = float(lon_str)
            rho_cos = float(rho_cos_str)
            rho_sin = float(rho_sin_str)

            # Convert to latitude using arctan2
            lat = np.degrees(np.arctan2(rho_sin, rho_cos))

            # Convert longitude to -180 to 180 range
            if lon > 180:
                lon = lon - 360

            observatories.append({
                'code': code,
                'lon': lon,
                'lat': lat,
                'name': name if name else f"Observatory {code}"
            })

        except (ValueError, IndexError):
            continue

    return observatories


def load_mpc_observatories(obs_file=None):
    """Load MPC observatories from file or download."""
    # Try to find file
    if obs_file:
        # Try as-is
        if not os.path.exists(obs_file):
            # Try in package data directory
            pkg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), obs_file)
            if os.path.exists(pkg_path):
                obs_file = pkg_path
            # Try in ../data/ relative to package
            elif obs_file == 'mpc_observatories.txt':
                data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         '..', '..', 'data', 'mpc_observatories.txt')
                if os.path.exists(data_path):
                    obs_file = data_path
                else:
                    user_path = os.path.expanduser('~/.local/share/mapplot/mpc_observatories.txt')
                    if os.path.exists(user_path):
                        obs_file = user_path

    if obs_file and os.path.exists(obs_file):
        try:
            with open(obs_file, 'r') as f:
                content = f.read()
            observatories = parse_mpc_observatories(content)
            print(f"Loaded {len(observatories)} observatories from {obs_file}",
                  file=sys.stderr)
            return observatories
        except Exception as e:
            print(f"Warning: Could not read {obs_file}: {e}", file=sys.stderr)

    # Try downloading if file not found
    if not obs_file or obs_file == 'mpc_observatories.txt':
        print("Downloading observatory data from Minor Planet Center...",
              file=sys.stderr)
        observatories = download_mpc_observatories()
        if observatories:
            print(f"Downloaded {len(observatories)} observatories", file=sys.stderr)
        return observatories

    return []


def load_observatory_dates(dates_file):
    """
    Load observatory operational dates from file.

    Format: Code StartMJD EndMJD
    Example:
        474 48000 60000
        G96 50000 -1

    EndMJD of -1 means still operational
    """
    dates = {}

    if not dates_file or not os.path.exists(dates_file):
        return dates

    try:
        with open(dates_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                if len(parts) >= 3:
                    code = parts[0].upper()
                    try:
                        start_mjd = float(parts[1])
                        end_mjd = float(parts[2])
                        dates[code] = {
                            'start_mjd': start_mjd,
                            'end_mjd': end_mjd if end_mjd > 0 else 99999.0
                        }
                    except ValueError:
                        continue

        print(f"Loaded dates for {len(dates)} observatories from {dates_file}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not read {dates_file}: {e}", file=sys.stderr)

    return dates
