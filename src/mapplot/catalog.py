"""Bright Star Catalogue (BSC5) loading."""

import os
import sys


def get_bright_stars(max_magnitude=6.0):
    """
    Load the Bright Star Catalogue (BSC5).
    Yale Bright Star Catalog, 5th Edition
    http://tdc-www.harvard.edu/catalogs/bsc5.html
    """
    # Try to find BSC5 catalog file
    catalog_file = None
    search_paths = [
        'bsc5_data.txt',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bsc5_data.txt'),
        os.path.expanduser('~/.local/share/mapplot/bsc5_data.txt'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'bsc5_data.txt'),
    ]

    for path in search_paths:
        if os.path.exists(path):
            catalog_file = path
            break

    # Load from file if found
    if catalog_file:
        catalog = []
        try:
            with open(catalog_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split()
                    if len(parts) >= 5:
                        try:
                            name = parts[1]
                            ra_hours = float(parts[2])
                            dec_deg = float(parts[3])
                            v_mag = float(parts[4])
                            if v_mag <= max_magnitude:
                                ra_deg = ra_hours * 15.0
                                catalog.append((name, ra_deg, dec_deg, v_mag))
                        except (ValueError, IndexError):
                            continue
            if catalog:
                print(f"Loaded {len(catalog)} stars from BSC5 (mag <= {max_magnitude})", file=sys.stderr)
                return catalog
        except Exception as e:
            print(f"Warning: Error reading BSC5 catalog: {e}", file=sys.stderr)

    # Fallback: minimal built-in catalog
    print(f"Using built-in minimal catalog (bsc5_data.txt not found)", file=sys.stderr)
    stars = [
        ("Sirius", 6.752, -16.716, -1.46),
        ("Canopus", 6.399, -52.696, -0.72),
        ("Arcturus", 14.261, 19.182, -0.04),
        ("Vega", 18.615, 38.783, 0.03),
        ("Capella", 5.278, 45.998, 0.08),
        ("Rigel", 5.242, -8.202, 0.12),
        ("Procyon", 7.655, 5.225, 0.38),
        ("Betelgeuse", 5.919, 7.407, 0.50),
        ("Altair", 19.846, 8.868, 0.77),
        ("Aldebaran", 4.598, 16.509, 0.85),
    ]

    # Convert RA from hours to degrees and filter by magnitude
    catalog = []
    for name, ra_hours, dec, mag in stars:
        if mag <= max_magnitude:
            ra_deg = ra_hours * 15.0
            catalog.append((name, ra_deg, dec, mag))

    return catalog
