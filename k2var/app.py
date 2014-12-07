from flask import Flask, render_template, abort, send_from_directory
from os import path

from .paths import BASE_DIR
from .data_store import Database, data_file_path
from .rendering import LightcurvePlotter, TableRenderer

app = Flask(__name__)
app.config['FREEZER_BASE_URL'] = 'http://localhost/'
app.config['FREEZER_DESTINATION'] = path.join(BASE_DIR, 'build')

database = Database()


def build_stsci_url(epicid):
    return "https://archive.stsci.edu/k2/preview.php?dsn=KTWO{epicid}-C00&type=LC".format(
        epicid=epicid)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/objects/<string:epicid>.html')
def render_epic_id(epicid):
    meta = database.get(epicid)
    filename = data_file_path(epicid)
    return render_template('lightcurve.html',
                           filename=filename,
                           epicid=epicid,
                           stsci_url=build_stsci_url(epicid),
                           parameters_table=TableRenderer(meta).render(),
                           lightcurves=LightcurvePlotter(meta, filename).render())


@app.route('/download/k2var-<string:epicid>.fits')
def send_file(epicid):
    filename = data_file_path(epicid)
    return send_from_directory(
        path.dirname(filename),
        path.basename(filename))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
