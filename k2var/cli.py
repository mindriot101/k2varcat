#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
from os import path
import logging

from .data_store import Database, data_file_path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)


def render(args):
    logger.debug('Arguments: %s', args)
    db = Database()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='', help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=None, required=False)
    render(parser.parse_args())
