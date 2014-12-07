from .app import app
from .paths import BASE_DIR
from flask_frozen import Freezer
from os import path

from .data_store import Database, data_file_path

db = Database()

app.config['APPLICATION_ROOT'] = '/phsnag/'
app.config['FREEZER_BASE_URL'] = app.config['APPLICATION_ROOT']
app.config['FREEZER_DESTINATION'] = path.join(BASE_DIR, 'build')

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
    freezer.freeze()
