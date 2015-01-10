#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
from os import path

from .data_store import Database, data_file_path


def render(args):
    db = Database()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='', help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=None, required=False)
    render(parser.parse_args())
