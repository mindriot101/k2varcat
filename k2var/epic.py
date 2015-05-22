import os

from .rendering import LightcurvePlotter

class Epic(object):

    def __init__(self, epicid, campaign):
        self.epicid, self.campaign = epicid, campaign

    @property
    def campaign_dir(self):
        return 'c{campaign:d}'.format(campaign=self.campaign)

    @property
    def top_level(self):
        return '{top}{zeros}'.format(top=str(self.epicid)[:4], zeros='0' * 5)

    @property
    def bottom_level(self):
        end = str(self.epicid)[-5:]
        return str(round(int(end), -3))

    def output_dir(self, root):
        return os.path.join(root, self.campaign_dir, self.top_level, self.bottom_level)

    def plotter(self, meta):
        return LightcurvePlotter(None, meta, self.data_filename)

    @property
    def data_filename(self):
        return lightcurve_filename(self.epicid, self.campaign)

    def png_filename_stub(self, typ):
        valid_types = {'orig', 'detrend', 'phase'}
        if typ.lower() not in valid_types:
            raise ValueError('Image type must be one of {0}'.format(valid_types))

        return ('hlsp_k2varcat_k2_lightcurve_{epicid}-c{campaign:02d}_'
                'kepler_v2_llc-{typ}.png'.format(
                    epicid=self.epicid,
                    campaign=self.campaign,
                    typ=typ.lower()))

    def png_filename(self, root, typ):
        return os.path.join(self.output_dir(root),
                self.png_filename_stub(typ))
