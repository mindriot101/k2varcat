import pytest

from k2var import urls, paths


@pytest.fixture
def url_root():
    return ''


@pytest.fixture
def url_for(url_root):
    return urls.UrlFor(url_root)


def test_static_path(url_for):
    assert url_for('static', filename='test.css') == '/static/test.css'


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

# Check that the download urls match, and take
# the pipeline one as a basis


def test_download_urls_match(url_for):
    epicid = 10101
    campaign = 5
    expected = '/download/ktwo10101-c05_lpd-targ_X_D.fits'
    assert paths.lightcurve_filename(
        epicid, campaign) == expected.split('/')[-1]
    assert url_for('download', epicid=epicid, campaign=campaign) == expected
