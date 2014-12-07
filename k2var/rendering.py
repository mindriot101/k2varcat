import matplotlib
matplotlib.use('Agg')

import logging
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import StringIO
from flask import render_template

from .data_store import DataStore

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)

sns.set(style='white', rc={'lines.markeredgewidth': 0.01})


class EmptyPlot(object):

    '''Class for when no periodicity exists'''

    def figure(self):
        fig, ax = plt.subplots()
        return fig


class Plotter(object):

    def __init__(self, x, y, yerr):
        logger.debug("Creating plotter object")
        self.x, self.y, self.yerr = x, y, yerr

    def figure(self):
        logger.debug("Building figure object")
        fig, axis = plt.subplots()
        axis.errorbar(self.x, self.y, self.yerr, ls='None', marker='.')
        return fig


class TableRenderer(object):
    def __init__(self, meta):
        self.meta = meta

    def render(self):
        keys, values = zip(*self.meta.items())
        return render_template('table.html', keys=keys, values=values)

class LightcurvePlotter(object):

    def __init__(self, meta, filename):
        self.meta = meta
        self.filename = filename

    def lightcurves(self):
        return 'Lightcurves'

    def parameters_table(self):
        return TableRenderer(self.meta).render()
