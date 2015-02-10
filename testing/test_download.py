import pytest
from os import path
try:
    import mock
except ImportError:
    from unittest import mock

from k2var import tasks


@mock.patch('k2var.data_store.Database.load_data')
def test_copy_download_file_campaign_0(load_data, tmpdir, epicid_campaign_0):
    out_dir = str(tmpdir)
    tasks.copy_download_file(out_dir, epicid_campaign_0, campaign=0)
    assert path.lexists(str(
        tmpdir.join('download',
                    'k2var-{}-c00.fits'.format(epicid_campaign_0))))


@mock.patch('k2var.data_store.Database.load_data')
def test_copy_download_file_campaign_1(load_data, tmpdir, epicid_campaign_1):
    out_dir = str(tmpdir)
    tasks.copy_download_file(out_dir, epicid_campaign_1, campaign=1)
    assert path.lexists(str(
        tmpdir.join('download',
                    'k2var-{}-c01.fits'.format(epicid_campaign_1))))
