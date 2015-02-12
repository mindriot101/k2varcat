#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import threading


class TestServer(object):

    def __init__(self, port):
        self.port = port
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
        self.webserver.serve_forever()
        self._webserver_died.set()

    def kill_webserver(self):
        if not self._webserver_thread:
            return

        self.webserver.shutdown()

        if not self._webserver_died.wait(5):
            raise ValueError("Could not kill webserver")


def run_server(port):
    s = TestServer(port)
    s.start_webserver()
    return s


def build_prefix_structure(source_dir, root_dir, prefix):
    full_output_path = os.path.join(root_dir, prefix.lstrip('/'))
    top_level = os.path.dirname(full_output_path)
    os.makedirs(top_level)
    os.symlink(source_dir, full_output_path)
    return full_output_path


def main(args):
    server = run_server(args.port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=9999)
    main(parser.parse_args())
