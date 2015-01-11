from os import path

BASE_DIR = path.realpath(
    path.join(
        path.dirname(__file__), '..'))

PACKAGE_DIR = path.realpath(
    path.join(
        BASE_DIR, __name__.split('.')[0]))

DATA_DIR = path.realpath(
    path.join(
        BASE_DIR, 'data'))

def lightcurve_filename(epicid):
    return 'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(epicid=epicid)
