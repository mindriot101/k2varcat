import pytest
from os import path
from collections import namedtuple

from k2var import cli

Arguments = namedtuple('Arguments', ['root', 'output_dir'])


def build_args(root, output_dir):
    return Arguments(root, output_dir)


@pytest.fixture
def app():
    return cli.K2Var(build_args('root', 'output_dir'))


def test_build_args():
    args = build_args('root', 'output_dir')
    assert args.root == 'root' and args.output_dir == 'output_dir'


def test_build_output_paths(app):
    basedir = path.realpath(
        path.join(path.dirname(__file__), '..'))
    out_root = path.join(basedir, 'output_dir')
    assert app.output_paths == [path.join(out_root, 'objects'),
                                path.join(out_root, 'static')]


def test_ensure_output_dirs(tmpdir):
    app = cli.K2Var(build_args('root', str(tmpdir.join('output'))))
    app.ensure_output_dir()

    assert all(list(map(path.isdir, [
        str(tmpdir.join('output')),
        str(tmpdir.join('output', 'objects')),
        str(tmpdir.join('output', 'static'))
    ])))
