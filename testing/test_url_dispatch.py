import pytest
from k2var.urls import UrlFor


@pytest.fixture
def url_root():
    return ''


def test_static_path(url_root):
    u = UrlFor(url_root)
    assert u('static', filename='test.css') == '/static/test.css'
