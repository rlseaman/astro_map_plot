"""Configuration loading and color palettes."""

import copy
import os
import sys

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Professional color palettes for data series
COLOR_PALETTES = {
    'tableau10': [
        '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
        '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC'
    ],
    'set2': [
        '#66C2A5', '#FC8D62', '#8DA0CB', '#E78AC3', '#A6D854',
        '#FFD92F', '#E5C494', '#B3B3B3'
    ],
    'vibrant': [
        '#EE7733', '#0077BB', '#33BBEE', '#EE3377', '#CC3311',
        '#009988', '#BBBBBB'
    ],
    'muted': [
        '#CC6677', '#332288', '#DDCC77', '#117733', '#88CCEE',
        '#882255', '#44AA99', '#999933', '#AA4499'
    ],
    'default': [
        'red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray'
    ]
}

# Default configuration
DEFAULT_CONFIG = {
    'display': {
        'projection': 'plate-carree',
        'figsize': [12, 8],
        'dpi': 100,
        'bgcolor': 'white',
        'facecolor': None,
    },
    'grid': {
        'spacing': [30, 30],
        'color': 'gray',
        'alpha': 0.5,
        'style': '--',
    },
    'colors': {
        'data_palette': 'tableau10',
        'ecliptic': 'red',
        'equator': 'green',
        'galactic': 'blue',
    },
    'celestial': {
        'max_mag': 6.0,
    },
    'paths': {
        'config': '~/.mapplotrc',
        'bsc5_data': '~/.local/share/mapplot/bsc5_data.txt',
        'mpc_observatories': '~/.local/share/mapplot/mpc_observatories.txt',
    }
}


def load_config(config_path=None):
    """
    Load configuration from YAML file.

    Precedence: DEFAULT_CONFIG -> user config file -> command-line args
    """
    config = copy.deepcopy(DEFAULT_CONFIG)

    if not YAML_AVAILABLE:
        return config

    # Determine config file path
    if config_path is None:
        config_path = os.path.expanduser(DEFAULT_CONFIG['paths']['config'])
    else:
        config_path = os.path.expanduser(config_path)

    # Load config file if it exists
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    # Deep merge user config into default config
                    for section, values in user_config.items():
                        if section in config and isinstance(values, dict):
                            config[section].update(values)
                        else:
                            config[section] = values
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}",
                  file=sys.stderr)

    return config


def get_data_colors(palette_name='tableau10', count=8):
    """
    Get a list of colors from a named palette.

    Parameters:
    - palette_name: Name of the palette or 'default'
    - count: Number of colors needed

    Returns list of color strings
    """
    if palette_name in COLOR_PALETTES:
        palette = COLOR_PALETTES[palette_name]
    else:
        palette = COLOR_PALETTES['tableau10']

    # Repeat palette if we need more colors
    if count > len(palette):
        repeats = (count // len(palette)) + 1
        return (palette * repeats)[:count]

    return palette[:count]
