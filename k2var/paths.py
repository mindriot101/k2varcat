from os import path

BASE_DIR = path.realpath(
    path.join(
        path.dirname(__file__), '..'))

DATA_DIR = path.realpath(
    path.join(
        BASE_DIR, 'data'))

def lightcurve_filename(epicid):
    return 'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(epicid=epicid)
