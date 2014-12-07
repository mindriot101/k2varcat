from flask import Flask, render_template, abort
from os import path

from .data_store import Database
from .rendering import LightcurvePlotter, TableRenderer

BASE_DIR = path.realpath(
    path.join(
        path.dirname(__file__), '..'))

DATA_DIR = path.realpath(
    path.join(
        BASE_DIR, 'data'))

app = Flask(__name__)
app.config['FREEZER_BASE_URL'] = 'http://localhost/'
app.config['FREEZER_DESTINATION'] = path.join(BASE_DIR, 'build')

database = Database()


def data_file_path(epicid):
    return path.join(DATA_DIR,
                     'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(
                         epicid=epicid))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/objects/<string:epicid>.html')
def render_epic_id(epicid):
    meta = database.get(epicid)
    filename = data_file_path(epicid)
    return render_template('lightcurve.html',
                           epicid=epicid,
                           parameters_table=TableRenderer(meta).render(),
                           lightcurves=LightcurvePlotter(meta, filename).render())

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
