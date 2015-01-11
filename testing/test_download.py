import pytest
from os import path

from k2var import tasks


def test_copy_download_file(tmpdir, epicid):
    out_dir = str(tmpdir)
    tasks.copy_download_file(out_dir, epicid)
    assert path.isfile(str(tmpdir.join('download', 'k2var-{}.fits'.format(epicid))))
