#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import logging
import jinja2
from os import path
import shutil
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)


def ensure_dir(p):
    if not path.isdir(p):
        logger.debug('Path %s does not exist, creating', p)
        os.makedirs(p)


def main(args):
    ensure_dir(args.output_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', default='build')
    main(parser.parse_args())
