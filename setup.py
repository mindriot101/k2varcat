from setuptools import setup

setup(
    name='k2var',
    version='0.1.0',
    author='Simon Walker',
    author_email='s.walker.2@warwick.ac.uk',
    install_requires=['numpy', 'fitsio', 'matplotlib', 'seaborn',
                      'flask', 'frozen-flask'],
    entry_points={'console_scripts': [
        'k2var-freeze = k2var.freeze:main',
        'k2var-serve = k2var.app:main',
    ]},
    packages=['k2var'])
