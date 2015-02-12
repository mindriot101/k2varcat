import os
import pytest
import itertools
try:
    from unittest import mock
except ImportError:
    import mock

from k2var.data_store import Database
from k2var import cli
from k2var import tasks


@pytest.fixture
def db(csvfile):
    return Database(csvfile)


@pytest.fixture
def ensure_output_dir(tmpdir, csvfile):
    output_dir = str(tmpdir)
    args = mock.Mock(root='/', output_dir=output_dir,
                     metadata_csv=csvfile)
    app = cli.K2Var(args)
    app.ensure_output_dir()
    return output_dir


def test_render_page_campaign_0(epicid_campaign_0, db, ensure_output_dir):
    output_dir = ensure_output_dir
    root_url = '/'
    meta = {'period': 1., 'range': 1.}
    tasks.render_page(output_dir, root_url, epicid_campaign_0, campaign=0, metadata=meta)

    assert os.path.lexists(
        os.path.join(output_dir, 'objects', '{}.html'.format(epicid_campaign_0)))

def test_render_page_campaign_1(epicid_campaign_1, db, ensure_output_dir):
    output_dir = ensure_output_dir
    root_url = '/'
    meta = {'period': 1., 'range': 1.}
    tasks.render_page(output_dir, root_url, epicid_campaign_1, campaign=1, metadata=meta)

    assert os.path.lexists(
        os.path.join(output_dir, 'objects', '{}.html'.format(epicid_campaign_1)))
