import urllib.request

from k2var import test_all

def test_run_server():
    port = 10105
    s = test_all.run_server(port)
    s.join(1)
    response = urllib.request.urlopen('http://127.0.0.1:{}'.format(port))
    assert response.status == 200
