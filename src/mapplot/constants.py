"""Constants used across mapplot modules."""

import cartopy.crs as ccrs

# Define available projections
TERRESTRIAL_PROJECTIONS = {
    'plate-carree': lambda: ccrs.PlateCarree(),
    'mercator': lambda: ccrs.Mercator(),
    'miller': lambda: ccrs.Miller(),
    'mollweide': lambda: ccrs.Mollweide(),
    'robinson': lambda: ccrs.Robinson(),
    'hammer': lambda: ccrs.Hammer(),
    'aitoff': lambda: ccrs.Aitoff(),
    'lambert-conformal': lambda: ccrs.LambertConformal(),
    'lambert-azimuthal': lambda: ccrs.LambertAzimuthalEqualArea(),
    'albers': lambda: ccrs.AlbersEqualArea(),
    'orthographic': lambda: ccrs.Orthographic(),
    'stereographic': lambda: ccrs.Stereographic(),
    'gnomonic': lambda: ccrs.Gnomonic(),
    'north-polar-stereo': lambda: ccrs.NorthPolarStereo(),
    'south-polar-stereo': lambda: ccrs.SouthPolarStereo(),
    'azimuthal-equidistant': lambda: ccrs.AzimuthalEquidistant(),
    'sinusoidal': lambda: ccrs.Sinusoidal(),
    'equal-earth': lambda: ccrs.EqualEarth(),
    'eckert4': lambda: ccrs.EckertIV(),
    'eckert6': lambda: ccrs.EckertVI(),
}

# Define available markers
MARKERS = {
    'circle': 'o', 'square': 's', 'triangle': '^', 'diamond': 'D',
    'plus': '+', 'cross': 'x', 'star': '*', 'pentagon': 'p',
    'hexagon': 'h', 'point': '.', 'pixel': ','
}
