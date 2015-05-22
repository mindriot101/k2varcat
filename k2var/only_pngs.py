import argparse
from os import path

from .paths import BASE_DIR


def only_pngs(args):
    pass


def main():
    default_output = path.join(BASE_DIR, 'build')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root',
                        default='',
                        help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=default_output, required=False)
    parser.add_argument('-d', '--metadata-csv', required=True)
    only_pngs(parser.parse_args())
