from collections import namedtuple

from k2var import cli

Arguments = namedtuple('Arguments', ['root', 'output_dir'])

def build_args(root, output_dir):
    return Arguments(root, output_dir)

def test_build_args():
    args = build_args('root', 'output_dir')
    assert args.root == 'root' and args.output_dir == 'output_dir'
