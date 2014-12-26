import pytest
import glob
from os import path
from flask import url_for


@pytest.fixture(scope='session')
def epicid():
    return '202059221'


@pytest.fixture(scope='module')
def download_url(epicid):
    download_files = glob.glob('data/ktwo{epicid}-c00_lpd-*.fits'.format(
        epicid=epicid))
    chosen_file = path.basename(download_files[0])
    return '/download/{}'.format(chosen_file)


def test_download_link_status(client, download_url):
    print 'Download url: {}'.format(download_url)
    assert client.get(download_url).status_code == 200


def test_download_file(client, download_url):
    res = client.get(download_url)
    assert res.content_type == 'application/octet-stream'
