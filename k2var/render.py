from k2var.app import app
from flask_frozen import Freezer
from os import path

from .data_store import Database

db = Database()

freezer = Freezer(app)

@freezer.register_generator
def render_epic_id():
    for epicid in db:
        if epicid == '202059229':
            yield {'epicid': str(epicid)}

def main():
    freezer.freeze()


