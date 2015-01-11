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


def test_download_path(url_for):
    assert url_for('download', epicid=1) == '/download/k2var-1.fits'


def test_bad_endpoint(url_for):
    with pytest.raises(AttributeError) as err:
        assert url_for('no-endpoint')

    assert 'may need to define' in str(err).lower()
