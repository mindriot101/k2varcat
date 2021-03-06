import os
from os import path
import shutil
import socket

from celery import Celery
from .data_store import Database
from .paths import (data_file_path, detail_output_path, BASE_DIR,
                    lightcurve_filename, ensure_dir)
from .templates import RendersTemplates
from .urls import build_stsci_url
from .rendering import LightcurvePlotter, TableRenderer
from .epic import Epic


def devel():
    return 'mbp' in socket.gethostname()

if devel():
    BROKER_URL = 'redis://localhost:6379/0'
    RESULTS_URL = 'redis://localhost:6379/1'
else:
    BROKER_URL = 'redis://norwood:6379/0'
    RESULTS_URL = 'redis://norwood:6379/1'

app = Celery('rendering', broker=BROKER_URL, backend=RESULTS_URL)

app.conf.CELERY_ACCEPT_CONTENT = ['json']
app.conf.CELERY_TASK_SERIALIZER = 'json'
app.conf.CELERY_RESULT_SERIALIZER = 'json'


def copy_download_file(output_dir, epicid, campaign):
    dest_dir = path.join(output_dir, 'download')
    os.makedirs(dest_dir, exist_ok=True)

    output_filename = path.join(
        output_dir, 'download', lightcurve_filename(epicid, campaign))
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
        campaign=campaign,
        app_root=root_url,
        epicid=epicid,
        stsci_url=build_stsci_url(epicid, campaign=campaign),
        parameters_table=TableRenderer(root_url, metadata).render(),
        lightcurves=LightcurvePlotter(root_url, metadata, filename).render())

@app.task
def render_only_png(output_dir, epicid, campaign, metadata):
    epic = Epic(epicid, campaign)
    output_path = epic.output_dir(root=output_dir)
    ensure_dir(output_path)
    for typ in ['orig', 'detrend', 'phase']:
        epic.render(root=output_dir, typ=typ, meta=metadata)
    return epicid

@app.task
def copy_data_file(output_dir, epicid, campaign):
    epic = Epic(epicid, campaign)
    epic.write_fits(output_dir)
    return epicid
