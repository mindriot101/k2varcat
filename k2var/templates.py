from jinja2 import Environment, PackageLoader


class RendersTemplates(object):

    def __init__(self):
        self.environment = Environment(loader=PackageLoader('k2var', 'templates'))

    @staticmethod
    def template_name(template_stub):
        return '{}.html'.format(template_stub)

    def __getitem__(self, template_stub):
        return self.environment.get_template(self.template_name(template_stub))
