from unittest import mock
import pytest

from k2var import rendering

@pytest.fixture
def meta():
    return mock.Mock(items=lambda: [('a', 'b')])

@pytest.fixture
def url_root():
    return '/url_root'

@pytest.fixture
def renderer(meta, url_root):
    return rendering.TableRenderer(url_root, meta)

@pytest.fixture
def render_content(renderer):
    return renderer.render()

def test_table_renderer_render_content(url_root, render_content):
    assert '<th>A</th>' in render_content and '<td>b</td>' in render_content
