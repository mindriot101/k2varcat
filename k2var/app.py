from flask import Flask, render_template, abort, send_from_directory
from os import path

from .paths import BASE_DIR, DATA_DIR, lightcurve_filename
from .data_store import Database, data_file_path
from .rendering import LightcurvePlotter, TableRenderer

app = Flask(__name__)
database = Database()


def build_stsci_url(epicid):
    return "https://archive.stsci.edu/k2/preview.php?dsn=KTWO{epicid}-C00&type=LC".format(
        epicid=epicid)


@app.route('/')
def index():
    return render_template('index.html',
                           app_root=app.config['APPLICATION_ROOT'])


@app.route('/objects/<string:epicid>.html')
def render_epic_id(epicid):
    meta = database.get(epicid)
    filename = data_file_path(epicid)
    return render_template('lightcurve.html',
                           app_root=app.config['APPLICATION_ROOT'],
                           filename=filename,
                           epicid=epicid,
                           stsci_url=build_stsci_url(epicid),
                           parameters_table=TableRenderer(meta).render(),
                           lightcurves=LightcurvePlotter(meta, filename).render())


@app.route('/download/k2var-<epicid>.fits')
def download(epicid):
    filename = path.join(DATA_DIR, lightcurve_filename(epicid))
    if not path.isfile(filename):
        abort(404)
    else:
        return send_from_directory(DATA_DIR, path.basename(filename))


def main():
    if not path.isdir(DATA_DIR):
        raise RuntimeError("No data directory found at {dirname}. Ensure this exists"
                           .format(dirname=DATA_DIR))
    app.run(debug=True)


if __name__ == '__main__':
    main()
