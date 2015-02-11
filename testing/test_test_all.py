import urllib.request
import csv
import os

from k2var import test_all


class Request(object):

    @classmethod
    def get(cls, port, url='http://localhost'):
        return cls(urllib.request.urlopen(':'.join([url, str(port)])))

    def __init__(self, response):
        self.response = response

    @property
    def status_code(self):
        return self.response.status


def test_run_server():
    port = 10105
    s = test_all.run_server(port)
    s.join(0.1)
    response = Request.get(port)
    assert response.status_code == 200


def test_build_test_directory_links(tmpdir):
    prefix = '/a/b/c'
    source_dir = tmpdir.mkdir('source')
    test_file = source_dir.join('test.html')
    test_file.write('Hello world')

    test_all.build_prefix_structure(source_dir=str(source_dir),
                                    root_dir=str(tmpdir),
                                    prefix=prefix)

    assert os.path.lexists(
        os.path.join(str(tmpdir), prefix.lstrip('/'), 'test.html'))
