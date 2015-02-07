import pytest
from os import path
try:
    import mock
except ImportError:
    from unittest import mock

from k2var import tasks


@mock.patch('k2var.data_store.Database.load_data')
def test_copy_download_file(load_data, tmpdir, epicid):
    out_dir = str(tmpdir)
    tasks.copy_download_file(out_dir, epicid, campaign=1)
    assert path.lexists(str(tmpdir.join('download',
                                        'k2var-{}.fits'.format(epicid))))
