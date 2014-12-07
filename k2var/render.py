from k2var.app import app
from flask_frozen import Freezer
from os import path
import csv

freezer = Freezer(app)

@freezer.register_generator
def render_epic_id():
    csv_filename = path.join(
        path.dirname(__file__),
        'K2VarCat.csv')
    with open(csv_filename) as infile:
        reader = csv.DictReader(infile,
                                fieldnames=['epicid', 'type',
                                       'range', 'period', 'amplitude'])
        for row in reader:
            if row['epicid'] == '202059229':
                yield {'epicid': str(row['epicid'])}

def main():
    freezer.freeze()


