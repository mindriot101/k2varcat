class UrlFor(object):

    def __init__(self, root):
        self.root = root

    def static_url(self, filename):
        return '/'.join([self.root, 'static', filename])

    def __call__(self, endpoint, **kwargs):
        if endpoint == 'static':
            return self.static_url(kwargs['filename'])
