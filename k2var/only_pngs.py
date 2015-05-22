import argparse
import os

from .paths import BASE_DIR, lightcurve_filename
from .data_store import Database
from .rendering import Plotter


def only_pngs(args):
    pass



def main():
    default_output = os.path.join(BASE_DIR, 'build')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root',
                        default='',
                        help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=default_output, required=False)
    parser.add_argument('-d', '--metadata-csv', required=True)
    only_pngs(parser.parse_args())
