from setuptools import setup

setup(
    name='k2var',
    version='0.1.1',
    author='Simon Walker',
    author_email='s.walker.2@warwick.ac.uk',
    install_requires=['numpy', 'astropy', 'matplotlib', 'seaborn'],
    entry_points={'console_scripts': [
        'k2var-build = k2var.cli:main',
    ]},
    packages=['k2var'])
