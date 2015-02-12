import urllib.request
import csv
import os
import random

from k2var import test_all


@pytest.fixture(scope='function')
def port():
    return random.randint(10000, 15000)


class Request(object):

    @classmethod
    def get(cls, port, url='http://localhost', timeout=None):
        return cls(urllib.request.urlopen(':'.join([url, str(port)]),
                                          timeout=timeout))

    def __init__(self, response):
        self.response = response

    @property
    def contents(self):
        return self.response.read().decode('utf-8')

    @property
    def status_code(self):
        return self.response.status


def test_run_server(port):
    s = test_all.run_server(port)
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

    assert os.path.lexists(os.path.join(str(tmpdir), 'a/b/c/test.html'))
