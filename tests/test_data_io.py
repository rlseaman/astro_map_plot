"""Tests for data file parsing."""

import numpy as np
import pytest

from mapplot.data_io import read_data


class TestReadData:
    def test_basic_two_columns(self, tmp_data_file):
        mjd, coord1, coord2, sizes, colors, labels = read_data(tmp_data_file)
        assert mjd is None
        np.testing.assert_array_equal(coord1, [10.0, 30.0, 50.0])
        np.testing.assert_array_equal(coord2, [20.0, 40.0, -10.0])
        assert sizes is None
        assert colors is None
        assert labels is None

    def test_mjd_three_columns(self, tmp_mjd_data_file):
        mjd, coord1, coord2, sizes, colors, labels = read_data(
            tmp_mjd_data_file, read_mjd=True
        )
        assert mjd is not None
        np.testing.assert_array_equal(mjd, [60000.0, 60001.0, 60002.0])
        np.testing.assert_array_equal(coord1, [120.0, 121.0, 122.0])
        np.testing.assert_array_equal(coord2, [30.0, 31.0, 32.0])

    def test_labels_from_file(self, tmp_labeled_data_file):
        mjd, coord1, coord2, sizes, colors, labels = read_data(
            tmp_labeled_data_file, labels_from_file=True
        )
        assert labels == ['Alpha', 'Beta']
        np.testing.assert_array_equal(coord1, [10.0, 30.0])
        np.testing.assert_array_equal(coord2, [20.0, 40.0])

    def test_ignore_extra(self, tmp_path):
        f = tmp_path / "extra.txt"
        f.write_text("10.0 20.0 5.0 0.5\n30.0 40.0 10.0 1.0\n")
        mjd, coord1, coord2, sizes, colors, labels = read_data(
            str(f), ignore_extra=True
        )
        assert sizes is None
        assert colors is None

    def test_size_column(self, tmp_path):
        f = tmp_path / "sized.txt"
        f.write_text("10.0 20.0 5.0\n30.0 40.0 10.0\n")
        mjd, coord1, coord2, sizes, colors, labels = read_data(str(f))
        assert sizes is not None
        np.testing.assert_array_equal(sizes, [5.0, 10.0])

    def test_comments_skipped(self, tmp_path):
        f = tmp_path / "commented.txt"
        f.write_text("# header\n10.0 20.0\n# another comment\n30.0 40.0\n")
        mjd, coord1, coord2, sizes, colors, labels = read_data(str(f))
        assert len(coord1) == 2

    def test_single_point(self, tmp_path):
        f = tmp_path / "single.txt"
        f.write_text("10.0 20.0\n")
        mjd, coord1, coord2, sizes, colors, labels = read_data(str(f))
        np.testing.assert_array_equal(coord1, [10.0])
        np.testing.assert_array_equal(coord2, [20.0])
