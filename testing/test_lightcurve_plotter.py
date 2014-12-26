from k2var.rendering import LightcurvePlotter
import jinja2
import mock


@mock.patch('k2var.rendering.Plotter', autospec=True)
@mock.patch('k2var.rendering.DataStore', autospec=True)
def test_raw_lightcurve(mock_data_store, mock_plotter):
    plot_result = mock_plotter.return_value.render
    meta = mock.MagicMock()
    filename = mock.MagicMock()

    plotter = LightcurvePlotter(meta, filename)
    plotter.raw_lightcurve()

    plot_result.assert_called_once_with()


@mock.patch('k2var.rendering.Plotter', autospec=True)
@mock.patch('k2var.rendering.DataStore', autospec=True)
def test_detrended_lightcurve(mock_data_store, mock_plotter):
    plot_result = mock_plotter.return_value.render
    meta = mock.MagicMock()
    filename = mock.MagicMock()

    plotter = LightcurvePlotter(meta, filename)
    plotter.detrended_lightcurve()

    plot_result.assert_called_once_with()
