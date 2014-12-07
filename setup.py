from setuptools import setup

setup(
    name='k2var',
    version='0.0.1',
    author='Simon Walker',
    author_email='s.walker.2@warwick.ac.uk',
    install_requires=['numpy', 'fitsio', 'matplotlib', 'seaborn',
                      'flask', 'frozen-flask'],
    entry_points={'console_scripts': [
        'k2var-render = k2var.render:main',
    ]},
    packages=['k2var'])
