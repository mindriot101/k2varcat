from k2var import paths


def test_lightcurve_filename():
    epicid = 1
    expected = 'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(epicid=epicid)
    assert paths.lightcurve_filename(1) == expected
