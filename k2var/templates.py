from jinja2 import Environment, PackageLoader


class RendersTemplates(object):

    def __init__(self):
        self.environment = Environment(loader=PackageLoader('k2var', 'templates'))

    def render(self, template_stub, **context):
        template = self[template_stub]
        return template.render(**context)

    def render_to(self, template_stub, filename, **context):
        with open(filename, 'w') as outfile:
            outfile.write(self.render(template_stub, **context))

    @staticmethod
    def template_name(template_stub):
        return '{}.html'.format(template_stub)

    def __getitem__(self, template_stub):
        return self.environment.get_template(self.template_name(template_stub))
