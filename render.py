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


def render_index(env, output_directory):
    logger.info('Rendering index file')
    index_template = env.get_template('index.html')
    with open(path.join(output_directory, 'index.html'), 'w') as outfile:
        outfile.write(
            index_template.render()
        )


def main(args):
    ensure_dir(args.output_dir)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.template_dir))
    render_index(env, args.output_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', default='build')
    parser.add_argument('-t', '--template-dir', default='templates')
    main(parser.parse_args())
