import pytest
import glob
from os import path


def test_download_link_status(client):
    download_files = glob.glob('data/ktwo202059221-c00_lpd-*.fits')
    chosen_file = path.basename(download_files[0])
    download_url = '/download/{}'.format(chosen_file)
    print 'Download url: {}'.format(download_url)
    assert client.get(download_url).status_code == 200
