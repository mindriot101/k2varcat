import argparse
import os

from .paths import BASE_DIR
from .data_store import Database


class Epic(object):

    def __init__(self, epicid, campaign):
        self.epicid, self.campaign = epicid, campaign

    @property
    def campaign_dir(self):
        return 'c{campaign:d}'.format(campaign=self.campaign)

    @property
    def top_level(self):
        return '{top}{zeros}'.format(top=str(self.epicid)[:4], zeros='0' * 5)

    @property
    def bottom_level(self):
        end = str(self.epicid)[-5:]
        return str(round(int(end), -3))

    def output_dir(self, root):
        return os.path.join(root, self.campaign_dir, self.top_level, self.bottom_level)


class K2VarPngs(object):

    def __init__(self, args):
        self.db = Database(args.metadata_csv)
        self.output_dir = args.output_dir

    def render(self):
        for epicid, campaign in self.db.valid_epic_ids():
            epic = Epic(epicid, campaign)
            output_dir = self.ensure_output_dir(epic)

    def ensure_output_dir(self, epic):
        dirname = epic.output_dir(self.output_dir)
        print(dirname)


def main():
    default_output = os.path.join(BASE_DIR, 'build')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root',
                        default='',
                        help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=default_output, required=False)
    parser.add_argument('-d', '--metadata-csv', required=True)
    K2VarPngs(parser.parse_args()).render()
