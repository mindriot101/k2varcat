from .app import app
from .paths import BASE_DIR
from flask_frozen import Freezer
from os import path
import argparse

from .data_store import Database, data_file_path

db = Database()

freezer = Freezer(app)


@freezer.register_generator
def render_epic_id():
    for epicid in db:
        if path.isfile(data_file_path(epicid)):
            yield {'epicid': str(epicid)}


@freezer.register_generator
def send_file():
    for epicid in db:
        if path.isfile(data_file_path(epicid)):
            yield {'epicid': str(epicid)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='', help='Application root')
    parser.add_argument('-o', '--output-dir', default=None, required=False)
    args = parser.parse_args()

    app.config['APPLICATION_ROOT'] = args.root
    app.config['FREEZER_BASE_URL'] = app.config['APPLICATION_ROOT']
    if args.output_dir is not None:
        app.config['FREEZER_DESTINATION'] = path.realpath(args.output_dir)
    else:
        app.config['FREEZER_DESTINATION'] = path.join(BASE_DIR, 'build')

    freezer.freeze()
