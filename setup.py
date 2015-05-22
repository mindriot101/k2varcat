from setuptools import setup

setup(
    name='k2var',
    version='0.1.1',
    author='Simon Walker',
    author_email='s.walker.2@warwick.ac.uk',
    install_requires=['numpy', 'astropy', 'matplotlib', 'seaborn', 'celery', 'sqlalchemy',
                      'jinja2'],
    entry_points={'console_scripts': [
        'k2var-build = k2var.cli:main',
        'k2var-validation-server = k2var.test_all:main',
        'k2var-pngs = k2var.only_pngs:main',
    ]},
    packages=['k2var'])
