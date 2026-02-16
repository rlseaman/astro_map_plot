"""Tests for argument parsing."""

import sys
import pytest

from mapplot.cli import parse_args


class TestParseArgs:
    def test_help_flag(self):
        """--help should exit with 0."""
        with pytest.raises(SystemExit) as exc_info:
            sys.argv = ['mapplot', '--help']
            parse_args()
        assert exc_info.value.code == 0

    def test_version_flag(self):
        """--version should exit with 0."""
        with pytest.raises(SystemExit) as exc_info:
            sys.argv = ['mapplot', '--version']
            parse_args()
        assert exc_info.value.code == 0

    def test_defaults(self):
        sys.argv = ['mapplot', '--catalog']
        args = parse_args()
        assert args.catalog is True
        assert args.earth is False
        assert args.projection == 'plate-carree'
        assert args.gridlines is False
        assert args.size == 20
        assert args.alpha == 0.7

    def test_projection_choice(self):
        sys.argv = ['mapplot', '--catalog', '-p', 'mollweide']
        args = parse_args()
        assert args.projection == 'mollweide'

    def test_invalid_projection(self):
        with pytest.raises(SystemExit):
            sys.argv = ['mapplot', '--catalog', '-p', 'nonexistent']
            parse_args()

    def test_earth_mode(self):
        sys.argv = ['mapplot', '--earth', '--observatories']
        args = parse_args()
        assert args.earth is True
        assert args.observatories is True

    def test_animation_args(self):
        sys.argv = ['mapplot', '--animate', '--fps', '15', '--trail-days', '30',
                    '--show-time', '-o', 'out.mp4', 'data.txt']
        args = parse_args()
        assert args.animate is True
        assert args.fps == 15
        assert args.trail_days == 30
        assert args.show_time is True
        assert args.output == 'out.mp4'

    def test_multiple_files(self):
        sys.argv = ['mapplot', 'file1.txt', 'file2.txt', 'file3.txt']
        args = parse_args()
        assert args.files == ['file1.txt', 'file2.txt', 'file3.txt']

    def test_labels(self):
        sys.argv = ['mapplot', '--labels', 'Near', 'Far', '--legend',
                    'file1.txt', 'file2.txt']
        args = parse_args()
        assert args.labels == ['Near', 'Far']
        assert args.legend is True

    def test_grid_spacing(self):
        sys.argv = ['mapplot', '--catalog', '-g', '--grid-spacing', '15', '15']
        args = parse_args()
        assert args.grid_spacing == [15.0, 15.0]
