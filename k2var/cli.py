#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
from os import path
import logging

from .data_store import Database, data_file_path
from .paths import BASE_DIR

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)


def render_static(args):
    logger.info('Rendering static files')


def render_index_page(args):
    logger.info('Rendering index page')


def render_detail_page(epicid, args):
    logger.info('Rendering detail page for object %s', epicid)


def render(args):
    logger.debug('Arguments: %s', args)
    db = Database()
    render_static(args)
    render_index_page(args)
    for epicid in db.valid_epic_ids():
        render_detail_page(epicid, args)


def main():
    default_output = path.join(BASE_DIR, 'build')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='', help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=default_output, required=False)
    render(parser.parse_args())
