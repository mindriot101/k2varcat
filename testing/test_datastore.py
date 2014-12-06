from k2var.data_store import DataStore
import pytest

@pytest.fixture
def ds():
    return DataStore('data/ktwo202059221-c00_lpd-targ_X_D.fits')

def test_data_store(ds):
    assert ds['time'] is not None

def test_data_store_all_keys(ds):
    for key in ['time', 'aptflux', 'aptflux_err', 'detflux']:
        ds[key]

