import jinja2
try:
    import mock
except ImportError:
    import sys
    if sys.version_info.major == 3:
        from unittest import mock
    else:
        raise
import pytest

from k2var import rendering


@pytest.fixture
def url_root():
    return ''


@mock.patch('k2var.rendering.Plotter', autospec=True)
@mock.patch('k2var.rendering.DataStore', autospec=True)
def test_raw_lightcurve(mock_data_store, mock_plotter, url_root):
    plot_result = mock_plotter.return_value.render
    meta = mock.MagicMock()
    filename = mock.MagicMock()

    plotter = rendering.LightcurvePlotter(url_root, meta, filename)
    plotter.raw_lightcurve()

    plot_result.assert_called_once_with()


@mock.patch('k2var.rendering.Plotter', autospec=True)
@mock.patch('k2var.rendering.DataStore', autospec=True)
def test_detrended_lightcurve(mock_data_store, mock_plotter, url_root):
    plot_result = mock_plotter.return_value.render
    meta = mock.MagicMock()
    filename = mock.MagicMock()

    plotter = rendering.LightcurvePlotter(url_root, meta, filename)
    plotter.detrended_lightcurve()

    plot_result.assert_called_once_with()
