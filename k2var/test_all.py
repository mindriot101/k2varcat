#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
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

def main(args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=9999)
    main(parser.parse_args())
