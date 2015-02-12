# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import logging
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import sys
try:
    import StringIO
except ImportError:
    if sys.version_info.major == 3:
        import io as StringIO
    else:
        raise

from .data_store import DataStore
from .templates import RendersTemplates

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)

sns.set(context='poster', style='white', rc={'lines.markeredgewidth': 0.5})

PHASE_LABEL = r'Orbital phase'
DETFLUX_LABEL = r'Detrended flux'


def render_template(url_root, template_stub, **context):
    renderer = RendersTemplates(url_root)
    return renderer.render(template_stub, **context)


class Plotter(object):

    colours = sns.color_palette(n_colors=5)

    def __init__(self, url_root, x, y, yerr, xlabel=None, ylabel=None, ylims=None):
        self.url_root = url_root
        self.x, self.y, self.yerr = x, y, yerr
        self.xlabel, self.ylabel = xlabel, ylabel
        self.ylims = ylims

        self.fig = self.figure()

    def figure(self):
        fig, axis = plt.subplots()
        axis.errorbar(self.x, self.y, self.yerr, ls='None', marker='.',
                      color=self.colours[0], alpha=0.3, capsize=0.)
        axis.plot(self.x, self.y, ls='None', marker='.',
                  color=self.colours[0])
        if self.xlabel is not None:
            axis.set_xlabel(self.xlabel)

        if self.ylabel is not None:
            axis.set_ylabel(self.ylabel)

        if self.ylims is not None:
            axis.set_ylim(*self.ylims)

        return fig

    def add_amplitude_markers(self, amplitude):
        ax = self.fig.get_axes()[0]
        ax.axhline(1. + amplitude / 100., color=self.colours[1], ls=':')
        ax.axhline(1. - amplitude / 100., color=self.colours[1], ls=':')
        return self

    def serialised(self):
        s = StringIO.BytesIO()
        self.fig.tight_layout()
        self.fig.savefig(s, bbox_inches='tight', format='png')
        plt.close(self.fig)
        return base64.b64encode(s.getvalue()).strip().decode('utf-8')

    def render(self):
        return render_template(self.url_root, 'image', data=self.serialised())


class EmptyPlot(Plotter):

    '''Class for when no periodicity exists'''

    def __init__(self, url_root):
        self.url_root = url_root
        self.fig, _ = plt.subplots()
        self.add_labels()

    def add_labels(self):
        ax = self.fig.get_axes()[0]
        ax.set_xlabel(PHASE_LABEL)
        ax.set_ylabel(DETFLUX_LABEL)

    def figure(self):
        return self.fig


class TableRenderer(object):

    def __init__(self, url_root, meta):
        self.url_root = url_root
        self.meta = meta

    def render(self):
        keys, values = zip(*self.meta.items())
        return render_template(self.url_root, 'table', keys=keys, values=values)


class LightcurvePlotter(object):

    def __init__(self, url_root, meta, filename):
        self.url_root = url_root
        self.meta = meta
        self.filename = filename
        self.data_store = DataStore(self.filename)

    def raw_lightcurve(self):
        return Plotter(
            self.url_root,
            self.data_store['time'],
            self.data_store['aptflux'],
            self.data_store['aptflux_err'],
            xlabel=r'BJD',
        ).render()

    def detrended_lightcurve(self):
        yerr = (self.data_store['detflux'] * (self.data_store['aptflux_err'] /
                                              self.data_store['aptflux']))
        return Plotter(
            self.url_root,
            self.data_store['time'],
            self.data_store['detflux'],
            yerr,
            xlabel='BJD',
            ylabel=DETFLUX_LABEL,
            ylims=self.range_ylims(),
        ).render()

    def phase_folded(self):
        period = self.meta['period']
        yerr = (self.data_store['detflux'] * (self.data_store['aptflux_err'] /
                                              self.data_store['aptflux']))
        if period > 0:
            phase = (self.data_store['time'] / period) % 1
            return Plotter(
                self.url_root,
                phase,
                self.data_store['detflux'],
                yerr,
                xlabel=PHASE_LABEL,
                ylabel=DETFLUX_LABEL,
                ylims=self.range_ylims(),
            ).render()
        else:
            return EmptyPlot(self.url_root).render()

    def render(self):
        return render_template(self.url_root, 'plots',
                               raw=self.raw_lightcurve(),
                               detrended=self.detrended_lightcurve(),
                               folded=self.phase_folded(),
                               )

    def range_ylims(self):
        plot_range = self.meta['range']
        return (1. - plot_range / 100., 1. + plot_range / 100.)
