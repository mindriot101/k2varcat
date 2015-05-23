import pytest
import os
from astropy.io import fits
import warnings

from k2var import tasks
from k2var.epic import Epic

warnings.filterwarnings('error', message='Checksum verification failed')
warnings.filterwarnings('error', message='Datasum verification failed')


def fitscheck(filename):
    try:
        hdulist = fits.open(filename, checksum=True)
    except UserWarning as w:
        return True

    for hdu in hdulist:
        if not hdu._checksum or not hdu._datasum:
            return True

    return False


@pytest.fixture
def render(epicid_campaign_1, tmpdir):
    tasks.copy_data_file(str(tmpdir), epicid_campaign_1, 1)


@pytest.fixture
def expected_path(tmpdir):
    path = ('/{}/c1/201100000/22000/'
            'hlsp_k2varcat_k2_lightcurve_201122454-c01_kepler_v2_llc.fits'.format(
                str(tmpdir)))
    return path

def test_copy_data_file(render, tmpdir, expected_path):
    assert os.path.isfile(expected_path)


def test_fits_filename():
    e = Epic(201129544, 1)
    assert e.fits_file_stub(
    ) == 'hlsp_k2varcat_k2_lightcurve_201129544-c01_kepler_v2_llc.fits'


def test_checksum(filename_campaign_1, render, expected_path, monkeypatch):
    assert fitscheck(filename_campaign_1)
    assert not fitscheck(expected_path)
