from k2var.plotting import LightcurvesPlotter
import jinja2

def test_raw_lightcurve():
    env = jinja2.Environment(loader=jinja2.PackageLoader('k2var', 'templates'))
    l = LightcurvesPlotter(env, 'data/ktwo202059221-c00_lpd-targ_X_D.fits',
                           2., 0.2)
    assert l.raw_lightcurve()

