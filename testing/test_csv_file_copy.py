from unittest import mock
import pytest
import os

from k2var import cli


def test_csv_file_copied(csvfile, tmpdir):
    output_dir = str(tmpdir)
    args = mock.Mock(root='/', output_dir=output_dir,
                     metadata_csv=csvfile)
    app = cli.K2Var(args)
    app.ensure_output_dir()
    app.copy_csv_file()
    assert os.path.isfile(str(tmpdir.join('K2VarCat.csv')))
