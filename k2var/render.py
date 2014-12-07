from k2var.app import app
from flask_frozen import Freezer

def main():
    freezer = Freezer(app)
    freezer.freeze()


