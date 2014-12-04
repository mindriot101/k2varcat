#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import logging
from os import path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)

def ensure_dir(p):
    if not path.isdir(p):
        logger.debug('Path %s does not exist, creating', p)
        path.makedirs(p)


def main(args):
    logger.debug('Hello world')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main(parser.parse_args())
