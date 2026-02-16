"""Tests for coordinate transformations, MJD utilities, and sun position."""

import numpy as np
import pytest

from mapplot.coordinates import (
    transform_coordinates, mjd_to_year, get_current_mjd,
    get_sun_position_fast, get_sun_position_precise, get_sun_position,
    compute_solar_relative_coords,
)


class TestTransformCoordinates:
    """Test coordinate transformation round-trips."""

    def test_equatorial_to_ecliptic_roundtrip(self):
        ra = np.array([45.0, 90.0, 180.0, 270.0])
        dec = np.array([30.0, -15.0, 0.0, 45.0])

        ecl_lon, ecl_lat = transform_coordinates(ra, dec, 'equatorial', 'ecliptic')
        ra2, dec2 = transform_coordinates(ecl_lon, ecl_lat, 'ecliptic', 'equatorial')

        np.testing.assert_allclose(ra, ra2, atol=0.01)
        np.testing.assert_allclose(dec, dec2, atol=0.01)

    def test_equatorial_to_galactic_roundtrip(self):
        ra = np.array([0.0, 90.0, 180.0])
        dec = np.array([0.0, 45.0, -30.0])

        gal_l, gal_b = transform_coordinates(ra, dec, 'equatorial', 'galactic')
        ra2, dec2 = transform_coordinates(gal_l, gal_b, 'galactic', 'equatorial')

        np.testing.assert_allclose(ra, ra2, atol=0.01)
        np.testing.assert_allclose(dec, dec2, atol=0.01)

    def test_ecliptic_to_galactic_roundtrip(self):
        lon = np.array([10.0, 120.0, 240.0])
        lat = np.array([10.0, -20.0, 45.0])

        gal_l, gal_b = transform_coordinates(lon, lat, 'ecliptic', 'galactic')
        lon2, lat2 = transform_coordinates(gal_l, gal_b, 'galactic', 'ecliptic')

        # Handle 0/360 wrapping
        lon_diff = np.abs(lon - lon2) % 360
        lon_diff = np.minimum(lon_diff, 360 - lon_diff)
        np.testing.assert_allclose(lon_diff, 0, atol=0.01)
        np.testing.assert_allclose(lat, lat2, atol=0.01)

    def test_identity_transform(self):
        lon = np.array([100.0, 200.0])
        lat = np.array([30.0, -30.0])

        lon2, lat2 = transform_coordinates(lon, lat, 'equatorial', 'equatorial')
        np.testing.assert_allclose(lon, lon2, atol=0.001)
        np.testing.assert_allclose(lat, lat2, atol=0.001)

    def test_invalid_system_raises(self):
        with pytest.raises(ValueError):
            transform_coordinates(np.array([0.0]), np.array([0.0]), 'invalid', 'equatorial')

        with pytest.raises(ValueError):
            transform_coordinates(np.array([0.0]), np.array([0.0]), 'equatorial', 'invalid')

    def test_wrapping(self):
        """RA values > 360 should be wrapped."""
        ra = np.array([370.0])
        dec = np.array([0.0])
        lon, lat = transform_coordinates(ra, dec, 'equatorial', 'ecliptic')
        # Should not crash and should produce valid output
        assert np.isfinite(lon).all()
        assert np.isfinite(lat).all()


class TestMJDToYear:
    def test_j2000_epoch(self):
        # MJD 51544.5 = 2000 Jan 1.5 = year 2000.0
        year = mjd_to_year(51544.5)
        assert abs(year - 2000.0) < 0.01

    def test_known_date(self):
        # MJD 60000 is approximately 2023.2
        year = mjd_to_year(60000.0)
        assert 2023.0 < year < 2024.0

    def test_monotonic(self):
        mjds = [50000, 51000, 52000, 53000]
        years = [mjd_to_year(m) for m in mjds]
        for i in range(len(years) - 1):
            assert years[i] < years[i + 1]


class TestGetCurrentMJD:
    def test_reasonable_range(self):
        mjd = get_current_mjd()
        # Current MJD should be roughly 60000+ (2023+)
        assert mjd > 59000
        assert mjd < 70000


class TestSunPosition:
    def test_fast_returns_tuple(self):
        lon, lat = get_sun_position_fast(60000.0)
        assert 0 <= lon < 360
        assert lat == 0.0

    def test_precise_returns_float(self):
        lon = get_sun_position_precise(60000.0)
        assert 0 <= lon < 360

    def test_fast_vs_precise_agreement(self):
        """Fast and precise should agree within ~2 degrees."""
        mjd = 60000.0
        lon_fast, _ = get_sun_position_fast(mjd)
        lon_precise = get_sun_position_precise(mjd)
        diff = abs(lon_fast - lon_precise)
        if diff > 180:
            diff = 360 - diff
        assert diff < 3.0  # within 3 degrees

    def test_public_api_dispatch(self):
        result_fast = get_sun_position(60000.0, precise=False)
        assert isinstance(result_fast, tuple)

        result_precise = get_sun_position(60000.0, precise=True)
        assert isinstance(result_precise, (float, np.floating))

    def test_sun_longitude_changes_over_year(self):
        """Sun should traverse ~360 degrees over a year."""
        lon1, _ = get_sun_position_fast(60000.0)
        lon2, _ = get_sun_position_fast(60182.5)  # ~half year later
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff
        assert diff > 150  # should be roughly opposite


class TestComputeSolarRelativeCoords:
    def test_basic(self):
        mjd = np.array([60000.0])
        ra = np.array([180.0])
        dec = np.array([0.0])
        lon, lat = compute_solar_relative_coords(mjd, ra, dec, 'equatorial')
        assert np.isfinite(lon).all()
        assert np.isfinite(lat).all()

    def test_output_range(self):
        mjd = np.array([60000.0, 60100.0, 60200.0])
        ra = np.array([0.0, 90.0, 180.0])
        dec = np.array([0.0, 30.0, -30.0])
        lon, lat = compute_solar_relative_coords(mjd, ra, dec, 'equatorial')
        assert (lon >= -360).all() and (lon <= 360).all()
        assert (lat >= -90).all() and (lat <= 90).all()
