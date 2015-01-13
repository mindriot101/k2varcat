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


def lightcurve_filename(epicid, campaign=0):
    return 'ktwo{epicid}-c{campaign:02d}_lpd-targ_X_D.fits'.format(
        epicid=epicid, campaign=campaign)


def data_file_path(epicid, campaign=0):
    return path.join(DATA_DIR, lightcurve_filename(epicid, campaign))
