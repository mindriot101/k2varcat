import argparse
import os

from .paths import BASE_DIR
from .data_store import Database
from .tasks import render_only_png, copy_data_file


def only_pngs(args):
    db = Database(args.metadata_csv)
    tasks = []
    for (epic_id, campaign) in db.valid_epic_ids():
        print(epic_id, campaign)
        tasks.append(render_only_png.delay(
            output_dir=args.output_dir,
            epicid=epic_id,
            campaign=campaign,
            metadata=db.get(epic_id)))
        tasks.append(copy_data_file.delay(
            output_dir=args.output_dir,
            epicid=epic_id,
            campaign=campaign))

    for task in tasks:
        epic_id = task.wait()
        print('Task {0} complete'.format(epic_id))



def main():
    default_output = os.path.join(BASE_DIR, 'build')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root',
                        default='',
                        help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=default_output, required=False)
    parser.add_argument('-d', '--metadata-csv', required=True)
    only_pngs(parser.parse_args())
