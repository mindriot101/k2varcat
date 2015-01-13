import pytest
from os import path

from k2var import data_store


@pytest.fixture
def ds(epicid, base_dir):
    fname = path.join(base_dir, 'data', 'ktwo{}-c00_lpd-targ_X_D.fits'.format(epicid))
    return data_store.DataStore(fname)


def test_data_store(ds):
    assert ds['time'] is not None


def test_data_store_all_keys(ds):
    for key in ['time', 'aptflux', 'aptflux_err', 'detflux']:
        ds[key]


def test_data_file_path(monkeypatch):
    monkeypatch.setattr(data_store, 'DATA_DIR', '/')
    assert data_store.data_file_path(epicid=1, campaign=0) == '/ktwo1-c00_lpd-targ_X_D.fits'
