from matplotlib.pyplot import Figure
try:
    from unittest import mock
except ImportError:
    import mock
import pytest

from k2var import rendering
from k2var.rendering import RendersTemplates


@pytest.fixture
def url_root():
    return '/'


def test_render_template(url_root):
    template_stub = 'template_stub'
    with mock.patch.object(RendersTemplates, '__getitem__') as getitem:
        rendering.render_template(url_root, template_stub)
        getitem.assert_called_once_with(template_stub)


def test_empty_plotter(url_root):
    e = rendering.EmptyPlot(url_root)
    assert isinstance(e.figure(), Figure)
