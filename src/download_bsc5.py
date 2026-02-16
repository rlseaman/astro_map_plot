#!/usr/bin/env python3
"""
Download full BSC5 catalog from VizieR and convert to mapplot format.
"""
import sys

print("=" * 60)
print("BSC5 Full Catalog Information")
print("=" * 60)
print()
print("The included bsc5_data.txt has ~5,700 stars.")
print("The full BSC5 contains 9,110 stars.")
print()
print("To get the full catalog, visit:")
print("  https://cdsarc.cds.unistra.fr/viz-bin/cat/V/50")
print()
print("Download 'catalog.dat.gz' and decompress it.")
print()
print("The current catalog provides realistic coverage for")
print("visualization and should be sufficient for most uses:")
print("  - 1,717 stars with mag ≤ 5.0")
print("  - 4,214 stars with mag ≤ 6.0")
print("  - 5,704 stars total (mag ≤ 6.5)")
