import os

BASE_DIR = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__), '..'))

PACKAGE_DIR = os.path.realpath(
    os.path.join(
        BASE_DIR, __name__.split('.')[0]))

DATA_DIR = os.path.realpath(
    os.path.join(
        BASE_DIR, 'data'))


def lightcurve_filename(epicid, campaign=0):
    return 'ktwo{epicid}-c{campaign:02d}_lpd-targ_X_D.fits'.format(
        epicid=epicid, campaign=campaign)


def data_file_path(epicid, campaign=0):
    return os.path.join(DATA_DIR, lightcurve_filename(epicid, campaign))


def detail_output_path(epicid, output_dir):
    return os.path.join(output_dir, 'objects', '{}.html'.format(epicid))

def ensure_dir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    finally:
        assert os.path.isdir(path)
