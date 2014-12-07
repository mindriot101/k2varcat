import fitsio

class DataStore(object):

    def __init__(self, filename):
        self.hdu = fitsio.read(filename, 1)

    def __getitem__(self, value):
        return self.hdu[value.upper()]
