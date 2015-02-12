import pytest
from os import path
try:
    from unittest import mock
except ImportError:
    import mock

from k2var import cli

def build_args(root, output_dir, csv_filename):
    class Arguments(object):
        pass

    self = Arguments()
    self.root = root
    self.output_dir = output_dir
    self.metadata_csv = csv_filename
    return self


@pytest.fixture
@mock.patch('k2var.cli.Database.load_data')
def app(load_data):
    return cli.K2Var(build_args('root', 'output_dir', 'csv_filename'))


def test_build_args():
    args = build_args('root', 'output_dir', 'csv_filename')
    assert (args.root == 'root' and
            args.output_dir == 'output_dir' and
            args.metadata_csv == 'csv_filename')


def test_build_output_paths(app):
    basedir = path.realpath(
        path.join(path.dirname(__file__), '..'))
    out_root = path.join(basedir, 'output_dir')
    assert app.output_paths == [path.join(out_root, 'objects'),
                                path.join(out_root, 'static')]


def test_ensure_output_dirs(csvfile, tmpdir):
    app = cli.K2Var(build_args('root',
                               str(tmpdir.join('output')),
                                csvfile))
    app.ensure_output_dir()

    assert all(list(map(path.isdir, [
        str(tmpdir.join('output')),
        str(tmpdir.join('output', 'objects')),
        str(tmpdir.join('output', 'static'))
    ])))
