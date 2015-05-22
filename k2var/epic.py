import os


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

    @property
    def filename(self):
        return lightcurve_filename(self.epicid, self.campaign)
