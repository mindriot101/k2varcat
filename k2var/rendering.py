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



class Plotter(object):

    def __init__(self, x, y, yerr):
        logger.debug("Creating plotter object")
        self.x, self.y, self.yerr = x, y, yerr

    def figure(self):
        logger.debug("Building figure object")
        fig, axis = plt.subplots()
        axis.errorbar(self.x, self.y, self.yerr, ls='None', marker='.')
        return fig

    def serialised(self):
        figure = self.figure()
        s = StringIO.StringIO()
        figure.savefig(s, bbox_inches='tight', format='png')
        return s.getvalue().encode('base64').strip()

    def render(self):
        return render_template('image.html', data=self.serialised())

class EmptyPlot(Plotter):

    '''Class for when no periodicity exists'''

    def __init__(self):
        pass

    def figure(self):
        fig, ax = plt.subplots()
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
        self.data_store = DataStore(self.filename)

    def raw_lightcurve(self):
        return Plotter(
            self.data_store['time'],
            self.data_store['aptflux'],
            self.data_store['aptflux_err']).render()

    def detrended_lightcurve(self):
        yerr = (self.data_store['detflux'] * (self.data_store['aptflux_err'] /
                                              self.data_store['aptflux']))
        return Plotter(
            self.data_store['time'],
            self.data_store['detflux'],
            yerr).render()

    def phase_folded(self):
        period = self.meta['period']
        yerr = (self.data_store['detflux'] * (self.data_store['aptflux_err'] /
                                              self.data_store['aptflux']))
        if period > 0:
            phase = (self.data_store['time'] / period) % 1
            return Plotter(
                phase,
                self.data_store['detflux'],
                yerr).render()
        else:
            return EmptyPlot().render()


    def render(self):
        return render_template('plots.html',
                               raw=self.raw_lightcurve(),
                               detrended=self.detrended_lightcurve(),
                               folded=self.phase_folded(),
                               )
