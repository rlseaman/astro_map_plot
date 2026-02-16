"""Data file reading and animation data preparation."""

import sys

import numpy as np

from mapplot.config import get_data_colors


def read_data(filename, ignore_extra=False, labels_from_file=False, solar_relative=False, read_mjd=False):
    """Read coordinates and optional size/color/label columns from file

    Parameters:
    - filename: path to data file
    - ignore_extra: ignore columns beyond first two (or three if solar_relative/read_mjd)
    - labels_from_file: use third column (or fourth if solar_relative/read_mjd) as labels
    - solar_relative: if True, first column is MJD, then RA/coord1, then Dec/coord2
    - read_mjd: if True, read first column as MJD (for animation, without solar-relative transform)

    Returns:
    - mjd, coord1, coord2, sizes, colors, labels
    """
    try:
        labels = None
        mjd = None

        # Determine if we're reading MJD (either for solar-relative or animation)
        has_mjd = solar_relative or read_mjd

        # If we need labels, read differently
        if labels_from_file:
            if has_mjd:
                # Format: MJD RA Dec Label [size] [color]
                mjd_list, coord1_list, coord2_list, labels_list = [], [], [], []
                with open(filename, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        parts = line.split()
                        if len(parts) >= 4:
                            mjd_list.append(float(parts[0]))
                            coord1_list.append(float(parts[1]))
                            coord2_list.append(float(parts[2]))
                            labels_list.append(parts[3])
                        elif len(parts) >= 3:
                            mjd_list.append(float(parts[0]))
                            coord1_list.append(float(parts[1]))
                            coord2_list.append(float(parts[2]))
                            labels_list.append('')
                mjd = np.array(mjd_list)
                coord1 = np.array(coord1_list)
                coord2 = np.array(coord2_list)
                labels = labels_list
                sizes = None
                colors = None
            else:
                # Format: RA Dec Label [size] [color]
                coord1_list, coord2_list, labels_list = [], [], []
                with open(filename, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        parts = line.split()
                        if len(parts) >= 3:
                            coord1_list.append(float(parts[0]))
                            coord2_list.append(float(parts[1]))
                            labels_list.append(parts[2])
                        elif len(parts) >= 2:
                            coord1_list.append(float(parts[0]))
                            coord2_list.append(float(parts[1]))
                            labels_list.append('')
                coord1 = np.array(coord1_list)
                coord2 = np.array(coord2_list)
                labels = labels_list
                sizes = None
                colors = None
        else:
            # Normal numeric reading
            data = np.loadtxt(filename, comments='#')
            if data.ndim == 1:
                data = data.reshape(1, -1)

            if has_mjd:
                # Format: MJD RA Dec [size] [color]
                if data.shape[1] < 3:
                    print(f"Error: {filename} with time data must have at least 3 columns (MJD coord1 coord2)",
                          file=sys.stderr)
                    sys.exit(1)

                mjd = data[:, 0]
                coord1 = data[:, 1]
                coord2 = data[:, 2]

                if ignore_extra:
                    sizes = None
                    colors = None
                else:
                    sizes = data[:, 3] if data.shape[1] > 3 else None
                    colors = data[:, 4] if data.shape[1] > 4 else None
            else:
                # Format: RA Dec [size] [color]
                if data.shape[1] < 2:
                    print(f"Error: {filename} must have at least 2 columns", file=sys.stderr)
                    sys.exit(1)

                coord1 = data[:, 0]
                coord2 = data[:, 1]

                if ignore_extra:
                    sizes = None
                    colors = None
                else:
                    sizes = data[:, 2] if data.shape[1] > 2 else None
                    colors = data[:, 3] if data.shape[1] > 3 else None

        return mjd, coord1, coord2, sizes, colors, labels
    except Exception as e:
        print(f"Error reading {filename}: {e}", file=sys.stderr)
        sys.exit(1)


def prepare_animation_data(args, palette_name):
    """
    Prepare and sort data for animation.
    Returns list of dicts with: {'mjd', 'lon', 'lat', 'size', 'color', 'label', 'file_index'}
    """
    all_data = []

    # Set up colors for files (use user-specified colors if provided)
    if args.color is None:
        file_colors = get_data_colors(palette_name, len(args.files))
    else:
        file_colors = args.color[:]
        if len(file_colors) < len(args.files):
            file_colors.extend(['black'] * (len(args.files) - len(file_colors)))

    for file_idx, filename in enumerate(args.files):
        # Read data with MJD (either for animation or solar-relative)
        mjd, lon, lat, sizes, colors, labels = read_data(
            filename,
            ignore_extra=args.ignore_extra,
            labels_from_file=args.labels_from_file,
            solar_relative=args.solar_relative,
            read_mjd=True
        )

        if mjd is None:
            print(f"Error: --animate requires MJD as first column in {filename}", file=sys.stderr)
            sys.exit(1)

        file_color = file_colors[file_idx]

        for i in range(len(lon)):
            record = {
                'mjd': mjd[i],
                'lon': lon[i],
                'lat': lat[i],
                'size': sizes[i] if sizes is not None else args.size,
                'color': colors[i] if colors is not None else file_color,
                'label': labels[i] if labels is not None else None,
                'file_index': file_idx
            }
            all_data.append(record)

    # Sort by MJD
    all_data.sort(key=lambda x: x['mjd'])

    # Downsample if needed
    if args.downsample > 0 and len(all_data) > args.downsample:
        step = len(all_data) // args.downsample
        all_data = all_data[::step]
        print(f"Downsampled {len(all_data) * step} points to {len(all_data)}", file=sys.stderr)

    return all_data
