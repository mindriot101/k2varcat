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

