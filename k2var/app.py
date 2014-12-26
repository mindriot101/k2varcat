from flask import Flask, render_template, abort, send_from_directory
from os import path

from .paths import BASE_DIR
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


@app.route('/download/<epicid>')
def download(epicid):
    return ''


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
