import urllib.request
import os
import pytest
import random
import string
import socket
from io import StringIO

from k2var import test_all


@pytest.fixture(scope='function')
def port():
    return random.randint(10000, 15000)


@pytest.fixture(scope='function')
def random_filename():
    return ''.join([random.choice(string.ascii_lowercase)
                    for _ in range(100)]) + '.html'


@pytest.fixture
def csvfile(tmpdir):
    file_contents = tmpdir.join('data.csv')
    file_contents.write('201122454,AP,0.84,0.000000,0.00,,1.002794,0.996079\n'
                        '201123619,AP,1.31,0.000000,0.00,,1.003451,0.993472\n')
    return file_contents


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


def test_kill_server(port):
    s = test_all.run_server(port)
    response = Request.get(port)
    assert response.status_code == 200

    s.kill_webserver()
    with pytest.raises(socket.timeout) as err:
        response = Request.get(port, timeout=0.5)


def test_build_test_directory_links(tmpdir):
    prefix = '/a/b/c'
    source_dir = tmpdir.mkdir('source')
    test_file = source_dir.join('test.html')
    test_file.write('Hello world')

    test_all.build_prefix_structure(source_dir=str(source_dir),
                                    root_dir=str(tmpdir),
                                    prefix=prefix)

    assert os.path.lexists(os.path.join(str(tmpdir), 'a/b/c/test.html'))


def test_change_directory(tmpdir):
    start_path = os.getcwd()
    with test_all.change_directory(str(tmpdir)):
        assert os.getcwd() == str(tmpdir)

    assert os.getcwd() == start_path


def test_start_server_in_source_dir(tmpdir, port, random_filename):
    prefix = '/a/b/c'
    source_dir = tmpdir.mkdir('source')
    test_file = source_dir.join(random_filename)
    test_file.write('Hello world')
    assert test_file.check()

    result_dir = test_all.build_prefix_structure(source_dir=str(source_dir),
                                                 root_dir=str(tmpdir),
                                                 prefix=prefix)

    test_all.run_server(port, path=result_dir)

    response = Request.get(port)
    contents = response.contents
    assert response.status_code == 200
    assert random_filename in contents


def test_build_list_of_test_urls_no_prefix(csvfile, port):
    urls = test_all.build_urls(port, str(csvfile))
    assert list(urls) == [
        'http://localhost:{port}/objects/201122454.html'.format(port=port),
        'http://localhost:{port}/objects/201123619.html'.format(port=port),
    ]


def test_build_list_of_test_urls_with_prefix(csvfile, port):
    urls = test_all.build_urls(port, str(csvfile),
                               prefix='/test')

    assert list(urls) == [
        'http://localhost:{port}/test/objects/201122454.html'.format(port=port),
        'http://localhost:{port}/test/objects/201123619.html'.format(port=port),
    ]


def test_build_list_of_test_urls_bad_prefix(csvfile, port):
    urls = test_all.build_urls(port, str(csvfile),
                               prefix='badprefix')

    assert list(urls) == [
        'http://localhost:{port}/badprefix/objects/201122454.html'.format(
            port=port),
        'http://localhost:{port}/badprefix/objects/201123619.html'.format(
            port=port),
    ]


def test_create_temporary_directory(tmpdir):
    dirname = str(tmpdir)
    with test_all.temporary_directory(dir=dirname) as tdirname:
        assert os.path.isdir(tdirname)

    assert not os.path.isdir(tdirname)
