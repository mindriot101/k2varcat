#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import logging
import jinja2
from os import path
import shutil
import os
import csv

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


class KeplerObject(object):

    def __init__(self, data_dir, env, **keys):
        self.data_dir = data_dir
        self.env = env
        self.epicid = keys['epicid']
        self.period = float(keys['period'])
        self.amplitude = float(keys['amplitude'])

    def render(self, object_dir):
        if not path.isfile(self.data_file):
            logger.warning('Cannot find data file %s', self.data_file)
            return None

        logger.info('Rendering %s', self.epicid)

        with open(self.output_filename(object_dir), 'w') as outfile:
            outfile.write(self.template('lightcurve.html').render(kepler_object=self))

    @property
    def parameters_table(self):
        return self.template('parameters_table.html').render(
            epicid=self.epicid,
            period=self.period,
            amplitude=self.amplitude)

    @property
    def data_file(self):
        return path.join(self.data_dir, 'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(
            epicid=self.epicid))

    def template(self, fname):
        return self.env.get_template(fname)

    def output_filename(self, object_dir):
        return path.join(object_dir, '{epicid}.html'.format(
            epicid=self.epicid))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', default='build')
    args = parser.parse_args()

    ensure_dir(args.output_dir)
    env = jinja2.Environment(loader=jinja2.PackageLoader('k2var', 'templates'))
    copy_statics(args.output_dir)
    render_index(env, args.output_dir)

    object_dir = path.join(args.output_dir, 'objects')
    if not path.isdir(object_dir):
        os.makedirs(object_dir)

    logger.info('Rendering objects')
    with open(path.join(BASEDIR, 'K2VarCat.csv')) as infile:
        reader = csv.DictReader(infile,
                                fieldnames=['epicid', 'type', 'range', 'period', 'amplitude', 'proposal'])
        for row in reader:
            kepler_object = KeplerObject(args.data_dir, env, **row)
            kepler_object.render(object_dir)
