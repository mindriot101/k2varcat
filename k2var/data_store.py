from astropy.io import fits as pyfits
from os import path
import csv
from .paths import data_file_path


class DataStore(object):

    def __init__(self, filename):
        self.hdu = pyfits.getdata(filename, 1)

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

    def valid_epic_ids(self):
        for epicid in self:
            for campaign in campaigns:
                if path.lexists(data_file_path(epicid, campaign=campaign)):
                    yield epicid

    def __iter__(self):
        return iter(self.data)
