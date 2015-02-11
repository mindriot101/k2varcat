#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import threading


class TestServer(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        server_address = ('', self.port)
        httpd = HTTPServer(server_address,
                           SimpleHTTPRequestHandler)
        httpd.serve_forever()


def run_server(port):
    s = TestServer(port)
    s.daemon = True
    s.start()
    return s


def build_prefix_structure(source_dir, root_dir, prefix):
    full_output_path = os.path.join(root_dir, prefix.lstrip('/'))
    top_level = os.path.dirname(full_output_path)
    os.makedirs(top_level)
    os.symlink(source_dir, full_output_path)


def main(args):
    server = run_server(args.port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=9999)
    main(parser.parse_args())
