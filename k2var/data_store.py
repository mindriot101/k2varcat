import fitsio
from os import path
import csv
from .paths import BASE_DIR

DATA_DIR = path.realpath(
    path.join(
        BASE_DIR, 'data'))


def data_file_path(epicid):
    return path.join(DATA_DIR,
                     'ktwo{epicid}-c00_lpd-targ_X_D.fits'.format(
                         epicid=epicid))


class DataStore(object):

    def __init__(self, filename):
        self.hdu = fitsio.read(filename, 1)

    def __getitem__(self, value):
        return self.hdu[value.upper()]


class Database(object):

    DATA_NAME = path.join(
        path.dirname(__file__),
        'K2VarCat.csv')

    def __init__(self):
        self.data = self.load_data()

    def get(self, epicid):
        return self.data[epicid]

    @classmethod
    def load_data(cls):
        out = {}
        with open(cls.DATA_NAME) as infile:
            reader = csv.DictReader(infile,
                                    fieldnames=['epicid', 'type',
                                                'range', 'period', 'amplitude'])
            for row in reader:
                out[row['epicid']] = {
                    'type': row['type'],
                    'range': float(row['range']),
                    'period': float(row['period']),
                    'amplitude': float(row['amplitude']),
                }
        return out

    def __iter__(self):
        for epicid in self.data:
            yield epicid
