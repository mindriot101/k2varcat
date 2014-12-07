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

sns.set(style='white', rc={'lines.markeredgewidth': 0.5})


class Plotter(object):

    colours = sns.color_palette('gray', n_colors=5)

    def __init__(self, x, y, yerr, xlabel=None, ylabel=None):
        self.x, self.y, self.yerr = x, y, yerr
        self.xlabel, self.ylabel = xlabel, ylabel
        self.fig = self.figure()

    def figure(self):
        fig, axis = plt.subplots()
        axis.errorbar(self.x, self.y, self.yerr, ls='None', marker='.',
                      color=self.colours[0], alpha=0.3, capsize=0.)
        axis.plot(self.x, self.y, ls='None', marker='.',
                      color=self.colours[0])
        if self.xlabel:
            axis.set_xlabel(self.xlabel)

        if self.ylabel:
            axis.set_ylabel(self.ylabel)
        return fig

    def add_amplitude_markers(self, amplitude):
        ax = self.fig.get_axes()[0]
        ax.axhline(1. + amplitude / 100., color=self.colours[1], ls=':')
        ax.axhline(1. - amplitude / 100., color=self.colours[1], ls=':')
        return self

    def serialised(self):
        s = StringIO.StringIO()
        self.fig.savefig(s, bbox_inches='tight', format='png')
        return s.getvalue().encode('base64').strip()

    def render(self):
        return render_template('image.html', data=self.serialised())


class EmptyPlot(Plotter):

    '''Class for when no periodicity exists'''

    def __init__(self):
        self.fig, _ = plt.subplots()

    def figure(self):
        return self.fig


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
            self.data_store['aptflux_err'],
            xlabel=r'BJD',
        ).render()

    def detrended_lightcurve(self):
        yerr = (self.data_store['detflux'] * (self.data_store['aptflux_err'] /
                                              self.data_store['aptflux']))
        return Plotter(
            self.data_store['time'],
            self.data_store['detflux'],
            yerr,
            xlabel='BJD',
            ylabel='Detrended flux',
        ).render()

    def phase_folded(self):
        period = self.meta['period']
        yerr = (self.data_store['detflux'] * (self.data_store['aptflux_err'] /
                                              self.data_store['aptflux']))
        if period > 0:
            phase = (self.data_store['time'] / period) % 1
            return Plotter(
                phase,
                self.data_store['detflux'],
                yerr,
                xlabel='Orbital phase',
                ylabel='Detrended flux',
            ).add_amplitude_markers(self.meta['amplitude']).render()
        else:
            return EmptyPlot().render()

    def render(self):
        return render_template('plots.html',
                               raw=self.raw_lightcurve(),
                               detrended=self.detrended_lightcurve(),
                               folded=self.phase_folded(),
                               )
