from flask import Flask, render_template, abort
from os import path

BASE_DIR = path.realpath(
    path.join(
        path.dirname(__file__), '..'))

DATA_DIR = path.realpath(
    path.join(
        path.dirname(__file__),
        'data'))

app = Flask(__name__)
app.config['FREEZER_BASE_URL'] = 'http://localhost/'
app.config['FREEZER_DESTINATION'] = path.join(BASE_DIR, 'build')


def data_file_path(epicid):
    return path.join(DATA_DIR,
                     'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(
                         epicid=epicid))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/objects/<string:epicid>.html')
def render_epic_id(epicid):
    filename = data_file_path(epicid)
    return render_template('lightcurve.html', epicid=epicid)


if __name__ == '__main__':
    app.run(debug=True)
