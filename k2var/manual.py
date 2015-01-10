#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse


def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='', help='Application root. For phsnag: /phsnag/')
    parser.add_argument('-o', '--output-dir', default=None, required=False)
    main(parser.parse_args())
