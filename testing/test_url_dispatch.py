import pytest

from k2var import urls


@pytest.fixture
def url_root():
    return ''


@pytest.fixture
def url_for(url_root):
    return urls.UrlFor(url_root)


def test_static_path(url_for):
    assert url_for('static', filename='test.css') == '/static/test.css'


def test_download_path(url_for):
    assert url_for('download', epicid=1) == '/download/k2var-1.fits'


def test_index_path(url_for):
    assert url_for('index') == '/'


def test_bad_endpoint(url_for):
    with pytest.raises(AttributeError) as err:
        assert url_for('no-endpoint')

    assert 'may need to define' in str(err).lower()


def test_build_stsci_url():
    epicid = 1
    campaign = 2
    expected = ("https://archive.stsci.edu/k2/preview.php"
               "?dsn=KTWO1-C02&type=LC")
    assert urls.build_stsci_url(epicid=epicid, campaign=campaign) == expected
