import urllib.request

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
