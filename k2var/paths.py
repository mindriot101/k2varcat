from os import path

BASE_DIR = path.realpath(
    path.join(
        path.dirname(__file__), '..'))
DATA_DIR = path.realpath(
    path.join(
        BASE_DIR, 'data'))
