import os
from os import path
import shutil

from celery import Celery
from .data_store import Database
from .paths import data_file_path, detail_output_path
from .templates import RendersTemplates
from .urls import build_stsci_url
from .rendering import LightcurvePlotter, TableRenderer


db_url = 'queue/queue.sqlite'
BROKER_URL = '/'.join(['sqla+sqlite://', db_url])
RESULTS_URL = '/'.join(['db+sqlite://', db_url])

app = Celery('rendering', broker=BROKER_URL, backend=RESULTS_URL)

app.conf.CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
app.conf.CELERY_TASK_SERIALIZER = 'json'


def copy_download_file(output_dir, epicid, campaign):
    dest_dir = path.join(output_dir, 'download')
    os.makedirs(dest_dir, exist_ok=True)

    output_filename = path.join(output_dir, 'download', 'k2var-{}.fits'.format(epicid))
    if not path.lexists(output_filename):
        source_filename = data_file_path(epicid, campaign=campaign)
        shutil.copy(source_filename, output_filename)


@app.task
def render_page(output_dir, root_url, epicid, campaign, metadata):
    renderer = RendersTemplates(root_url)
    filename = data_file_path(epicid, campaign=campaign)
    outfile_name = detail_output_path(epicid, output_dir)
    copy_download_file(output_dir, epicid, campaign=campaign)
    return epicid, renderer.render_to(
        'lightcurve',
        outfile_name,
        app_root=root_url,
        epicid=epicid,
        stsci_url=build_stsci_url(epicid, campaign=campaign),
        parameters_table=TableRenderer(root_url, metadata).render(),
        lightcurves=LightcurvePlotter(root_url, metadata, filename).render())
