import os
from os import path
import shutil

from celery import Celery
from .data_store import Database
from .paths import data_file_path
from .templates import RendersTemplates
from .urls import build_stsci_url
from .rendering import LightcurvePlotter, TableRenderer


db_url = 'queue/queue.sqlite'
BROKER_URL = '/'.join(['sqla+sqlite://', db_url])
RESULTS_URL = '/'.join(['db+sqlite://', db_url])

app = Celery('rendering', broker=BROKER_URL, backend=RESULTS_URL)
db = Database()

app.conf.CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
app.conf.CELERY_TASK_SERIALIZER = 'json'


def copy_download_file(output_dir, epicid):
    dest_dir = path.join(output_dir, 'download')
    os.makedirs(dest_dir, exist_ok=True)

    output_filename = path.join(output_dir, 'download', 'k2var-{}.fits'.format(epicid))
    if not path.isfile(output_filename):
        source_filename = data_file_path(epicid)
        shutil.copy(source_filename, output_filename)


@app.task
def render_page(output_dir, root_url, epicid):
    renderer = RendersTemplates(root_url)
    meta = db.get(epicid)
    filename = data_file_path(epicid)
    outfile_name = path.join(output_dir,
                             'objects', '{}.html'.format(epicid))
    copy_download_file(output_dir, epicid)
    return epicid, renderer.render_to(
        'lightcurve',
        outfile_name,
        app_root=root_url,
        epicid=epicid,
        stsci_url=build_stsci_url(epicid),
        parameters_table=TableRenderer(root_url, meta).render(),
        lightcurves=LightcurvePlotter(root_url, meta, filename).render())
