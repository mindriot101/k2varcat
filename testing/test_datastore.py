import pytest
from os import path

from k2var import data_store


@pytest.fixture
def ds(filename_campaign_0, base_dir):
    return data_store.DataStore(filename_campaign_0)


def test_data_store(ds):
    assert ds['time'] is not None


def test_data_store_all_keys(ds):
    for key in ['time', 'aptflux', 'aptflux_err', 'detflux']:
        ds[key]

