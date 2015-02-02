from k2var import paths


def test_data_file_path(monkeypatch):
    monkeypatch.setattr(paths, 'DATA_DIR', '/')
    assert paths.data_file_path(
        epicid=1, campaign=0) == '/ktwo1-c00_lpd-targ_X_D.fits'


def test_lightcurve_filename():
    assert paths.lightcurve_filename(
        epicid=5, campaign=2) == 'ktwo5-c02_lpd-targ_X_D.fits'


def test_output_path():
    output_dir = '/tmp/out'
    epicid = 'epicid'
    expected = '/tmp/out/objects/epicid.html'
    assert paths.detail_output_path(epicid, output_dir) == expected
