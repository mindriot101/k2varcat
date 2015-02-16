#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import threading
from contextlib import contextmanager
import csv
import tempfile
import shutil


class ValidationServer(object):

    def __init__(self, port, path):
        self.port = port
        self.path = path if path is not None else os.getcwd()
        server_address = ('', self.port)
        self.webserver = HTTPServer(server_address,
                                    SimpleHTTPRequestHandler)

    def start_webserver(self):
        self._webserver_died = threading.Event()
        self._webserver_thread = threading.Thread(
            target=self._run_webserver_thread)
        self._webserver_thread.daemon = True
        self._webserver_thread.start()

    def _run_webserver_thread(self):
        with change_directory(self.path):
            self.webserver.serve_forever()
            self._webserver_died.set()

    def kill_webserver(self):
        if not self._webserver_thread:
            return

        self.webserver.shutdown()

        if not self._webserver_died.wait(5):
            raise ValueError("Could not kill webserver")

    @classmethod
    def start(cls, port, path=None):
        self = cls(port, path)
        self.start_webserver()
        return self


def build_prefix_structure(source_dir, root_dir, prefix):
    full_output_path = os.path.join(root_dir, prefix.lstrip('/'))
    top_level = os.path.dirname(full_output_path)
    os.makedirs(top_level)
    os.symlink(source_dir, full_output_path)
    return full_output_path


@contextmanager
def change_directory(path):
    old_path = os.getcwd()
    try:
        yield os.chdir(path)
    finally:
        os.chdir(old_path)


@contextmanager
def temporary_directory(*args, **kwargs):
    try:
        tdir = tempfile.mkdtemp(*args, **kwargs)
        yield tdir
    finally:
        shutil.rmtree(tdir)


def build_urls(port, filename, prefix=''):
    if prefix != '':
        prefix = prefix if prefix.startswith('/') else '/' + prefix
        prefix.rstrip('/')

    with open(filename) as infile:
        reader = csv.reader(infile)
        for row in reader:
            epicid = row[0]
            yield 'http://localhost:{port}{prefix}/objects/{epicid}.html'.format(
                port=port, epicid=epicid, prefix=prefix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=9999, type=int)
    parser.add_argument('dir')
    parser.add_argument('-p', '--prefix', required=False, default='')
    parser.add_argument('-c', '--csvfile', required=True)
    args = parser.parse_args()

    with temporary_directory() as tdir:
        htmldir = build_prefix_structure(args.dir, tdir, args.prefix)
        server = ValidationServer.start(args.port, tdir)

        for url in build_urls(args.port, args.csvfile, args.prefix):
            print(url)
            input('Press enter to continue')


if __name__ == '__main__':
    main()
