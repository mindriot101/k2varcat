import pytest
from k2var.urls import UrlFor


@pytest.fixture
def url_root():
    return ''


@pytest.fixture
def url_for(url_root):
    return UrlFor(url_root)

def test_static_path(url_for):
    assert url_for('static', filename='test.css') == '/static/test.css'
