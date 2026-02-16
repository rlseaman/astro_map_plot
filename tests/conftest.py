"""Shared test fixtures."""

import os
import pytest


@pytest.fixture
def data_dir():
    """Path to the data/ directory."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


@pytest.fixture
def tmp_data_file(tmp_path):
    """Create a temporary data file with simple lon/lat data."""
    f = tmp_path / "test_data.txt"
    f.write_text("# test data\n10.0 20.0\n30.0 40.0\n50.0 -10.0\n")
    return str(f)


@pytest.fixture
def tmp_mjd_data_file(tmp_path):
    """Create a temporary data file with MJD RA Dec columns."""
    f = tmp_path / "test_mjd_data.txt"
    f.write_text("# MJD RA Dec\n60000.0 120.0 30.0\n60001.0 121.0 31.0\n60002.0 122.0 32.0\n")
    return str(f)


@pytest.fixture
def tmp_labeled_data_file(tmp_path):
    """Create a temporary data file with labels."""
    f = tmp_path / "test_labeled.txt"
    f.write_text("# lon lat label\n10.0 20.0 Alpha\n30.0 40.0 Beta\n")
    return str(f)
