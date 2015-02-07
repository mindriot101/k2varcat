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
def db():
    return Database()


@pytest.fixture
def ensure_output_dir(tmpdir):
    output_dir = str(tmpdir)
    args = mock.Mock(root='/', output_dir=output_dir)
    app = cli.K2Var(args)
    app.ensure_output_dir()
    return output_dir


def test_render_page(epicid, ensure_output_dir):
    output_dir = ensure_output_dir
    root_url = '/'
    tasks.render_page(output_dir, root_url, valid_epicid)

    assert os.path.lexists(
        os.path.join(output_dir, 'objects', '{}.html'.format(epicid)))
