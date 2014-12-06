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

BASEDIR = path.realpath(
    path.join(
        path.dirname(__file__)))


def ensure_dir(p):
    if path.isdir(p):
        shutil.rmtree(p)
    os.makedirs(p)


def render_index(env, output_directory):
    logger.info('Rendering index file')
    index_template = env.get_template('index.html')
    with open(path.join(output_directory, 'index.html'), 'w') as outfile:
        outfile.write(
            index_template.render()
        )


def copy_statics(output_directory):
    logger.info("Copying static files")
    source_directory = path.join(BASEDIR, 'static')
    logger.debug('Copying static files from %s', source_directory)
    for dir in os.listdir(source_directory):
        dest_dir = path.join(output_directory, dir)
        source_dir = path.join(source_directory, dir)
        if path.isdir(source_dir):
            logger.debug('Copying %s to %s', source_dir, dest_dir)
            shutil.copytree(source_dir, dest_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', default='build')
    args = parser.parse_args()

    ensure_dir(args.output_dir)
    env = jinja2.Environment(loader=jinja2.PackageLoader('k2var', 'templates'))
    copy_statics(args.output_dir)
    render_index(env, args.output_dir)
