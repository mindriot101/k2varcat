from k2var.paths import lightcurve_filename

def test_lightcurve_filename():
    assert lightcurve_filename(1) == 'k2var-1.fits'

