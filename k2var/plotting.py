import matplotlib
matplotlib.use('Agg')

import logging
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import StringIO

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


class LightcurvePlotter(object):

    def __init__(self, meta, filename):
        self.period = meta['period']
        self.amplitude = meta['amplitude']

    def lightcurves(self):
        return 'Lightcurves'

    def parameters_table(self):
        return 'Parameters'

# class LightcurvesPlotter(object):

#     def __init__(self, env, data_file, period, amplitude):
#         super(self.__class__, self).__init__()
#         self.env = env
#         self.data_file = data_file
#         self.period = period
#         self.amplitude = amplitude

#         self.data_store = DataStore(self.data_file)

#     @property
#     def template(self):
#         return self.env.get_template('plots.html')

#     def render(self):
#         raw = self.raw_lightcurve()
#         return self.template.render(raw=self.raw_lightcurve(),
#                                     detrended=self.detrended_lightcurve(),
#                                     folded=self.phase_foleded_lightcurve())

#     def raw_lightcurve(self):
#         logger.debug('Plotting raw lightcurve')
#         figure = Plotter(self.data_store['time'],
#                          self.data_store['aptflux'],
#                          self.data_store['aptflux_err']).figure()
#         return self.image(data=self.save_to_string(figure))

#     def detrended_lightcurve(self):
#         logger.debug('Plotting detrended lightcurve')
#         flux_errors = self.data_store['detflux'] * (
#             self.data_store['aptflux_err'] / self.data_store['aptflux']
#         )
#         figure = Plotter(self.data_store['time'],
#                          self.data_store['detflux'],
#                          flux_errors).figure()
#         return self.image(data=self.save_to_string(figure))

#     def phase_foleded_lightcurve(self):
#         logger.debug('Plotting phase folded lightcurve')
#         flux_errors = self.data_store['detflux'] * (
#             self.data_store['aptflux_err'] / self.data_store['aptflux']
#         )
#         if self.period > 0:
#             phase = (self.data_store['time'] / self.period) % 1
#             figure = Plotter(phase,
#                              self.data_store['detflux'],
#                              flux_errors).figure()
#             return self.image(data=self.save_to_string(figure))

#         else:
#             return self.image(data=self.save_to_string(EmptyPlot().figure()))

#     def image(self, data):
#         return self.env.get_template('image.html').render(data=data)

#     @staticmethod
#     def save_to_string(fig):
#         s = StringIO.StringIO()
#         fig.savefig(s, bbox_inches='tight', format='png')
#         return s.getvalue().encode('base64').strip()
