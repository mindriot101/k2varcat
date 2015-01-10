#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
from os import path
import logging

from .data_store import Database, data_file_path
from .templates import RendersTemplates
from .paths import BASE_DIR

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)


class K2Var(object):

    def __init__(self, args):
        self.args = args
        self.renderer = RendersTemplates(self.args.root)

    def render_static(self):
        logger.info('Rendering static files')

    def render_index_page(self):
        logger.info('Rendering index page')
        outfile_name = path.join(self.args.output_dir, 'index.html')
        self.renderer.render_to('index', outfile_name, app_root=self.args.root)

    def render_detail_page(self, epicid):
        logger.info('Rendering detail page for object %s', epicid)

    def render(self):
        logger.debug('Arguments: %s', self.args)
        db = Database()
        self.render_static()
        self.render_index_page()
        for epicid in db.valid_epic_ids():
            self.render_detail_page(epicid)


def main():
    default_output = path.join(BASE_DIR, 'build')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='', help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=default_output, required=False)
    K2Var(parser.parse_args()).render()
