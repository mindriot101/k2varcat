import pytest
from os import path
import glob

BASEDIR = path.join(
    path.dirname(__file__),
    '..')


@pytest.fixture(scope='session')
def base_dir():
    return BASEDIR


@pytest.fixture(scope='session')
def epicid_campaign_0():
    return 202059221


@pytest.fixture(scope='session')
def epicid_campaign_1():
    return 201122454


@pytest.fixture(scope='session')
def filename_campaign_0(epicid_campaign_0, base_dir):
    return path.join(base_dir, 'testing', 'fixtures',
                     'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(
                         epicid=epicid_campaign_0))


@pytest.fixture(scope='session')
def filename_campaign_1(epicid_campaign_1, base_dir):
    return path.join(base_dir, 'testing', 'fixtures',
                     'ktwo{epicid}-c01_lpd-targ_X_D.fits'.format(
                         epicid=epicid_campaign_1))


@pytest.fixture(autouse=True)
def change_data_dir(base_dir, monkeypatch):
    monkeypatch.setattr('k2var.paths.DATA_DIR',
                        path.join(base_dir, 'testing', 'fixtures'))


@pytest.fixture
def csvfile(base_dir):
    return path.join(base_dir, 'testing', 'fixtures',
                        'K2VarCat.csv')
