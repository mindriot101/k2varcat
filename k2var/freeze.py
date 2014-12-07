from k2var.app import app
from flask_frozen import Freezer
from os import path

from .data_store import Database, data_file_path

db = Database()

freezer = Freezer(app)


@freezer.register_generator
def render_epic_id():
    for epicid in db:
        if path.isfile(data_file_path(epicid)):
            yield {'epicid': str(epicid)}


def main():
    freezer.freeze()
