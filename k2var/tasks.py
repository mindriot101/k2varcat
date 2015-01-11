from os import path

from celery import Celery
from .data_store import Database, data_file_path
from .templates import RendersTemplates
from .urls import build_stsci_url
from .rendering import LightcurvePlotter, TableRenderer

BROKER_URL = 'sqla+sqlite:///queue/queue.sqlite'
RESULTS_URL = 'db+sqlite:///queue/results.sqlite'

app = Celery('rendering', broker=BROKER_URL, backend=RESULTS_URL)
db = Database()

app.conf.CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
app.conf.CELERY_TASK_SERIALIZER = 'json'


@app.task
def render_page(output_dir, root_url, epicid):
    renderer = RendersTemplates(root_url)
    meta = db.get(epicid)
    filename = data_file_path(epicid)
    outfile_name = path.join(output_dir,
                             'objects', '{}.html'.format(epicid))
    return epicid, renderer.render_to(
        'lightcurve',
        outfile_name,
        app_root=root_url,
        epicid=epicid,
        stsci_url=build_stsci_url(epicid),
        parameters_table=TableRenderer(root_url, meta).render(),
        lightcurves=LightcurvePlotter(root_url, meta, filename).render())
