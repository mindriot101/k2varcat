import pytest
from os import path
import glob

ALLOWED_IDS = ['202059224', '202059221', '202059229', '201122454']
BASEDIR = path.join(
    path.dirname(__file__),
    '..')


@pytest.fixture(scope='session')
def base_dir():
    return BASEDIR


@pytest.fixture(scope='session')
def epicid(base_dir):
    files = glob.glob('{}/*.fits'.format(
        path.join(base_dir, 'data')))
    for fname in files:
        for i in ALLOWED_IDS:
            if i in fname:
                return i

@pytest.fixture(scope='session')
def filename(epicid, base_dir):
    files = glob.glob('{}/ktwo{}*.fits'.format(
        path.join(base_dir, 'data'), epicid))
    return files[0]
