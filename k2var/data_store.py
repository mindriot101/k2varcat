import fitsio
from os import path
import csv


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
                    'period': float(row['period']),
                    'amplitude': float(row['amplitude']),
                }
        return out

    def __iter__(self):
        for epicid in self.data:
            yield epicid

