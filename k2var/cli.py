#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
from os import path
import logging

from .data_store import Database, data_file_path
from .paths import BASE_DIR
from .rendering import LightcurvePlotter, TableRenderer
from .tasks import render_page
from .templates import RendersTemplates
from .urls import build_stsci_url

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)


class K2Var(object):

    def __init__(self, args):
        self.args = args
        self.renderer = RendersTemplates(self.args.root)
        self.db = Database()

    def render(self):
        logger.debug('Arguments: %s', self.args)
        self.render_static()
        self.render_index_page()
        self.render_detail_pages()

    def render_static(self):
        logger.info('Rendering static files')

    def render_index_page(self):
        logger.info('Rendering index page')
        outfile_name = path.join(self.args.output_dir, 'index.html')
        return self.renderer.render_to('index', outfile_name, app_root=self.args.root)

    def render_detail_pages(self):
        logger.info('Rendering detail pages')
        results = []

        for epicid in self.db.valid_epic_ids():
            logger.debug('Submitting task for {}'.format(epicid))
            results.append(render_page.delay(
                output_dir=self.args.output_dir,
                root_url=self.args.root,
                epicid=epicid))

        for result in results:
            epicid, _ = result.wait()
            logger.debug('Job {} complete'.format(epicid))


def main():
    default_output = path.join(BASE_DIR, 'build')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='', help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=default_output, required=False)
    K2Var(parser.parse_args()).render()
