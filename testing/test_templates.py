import pytest
from os import path

from k2var import templates


@pytest.fixture
def url_root():
    return ''


@pytest.fixture
def renderer(url_root):
    return templates.RendersTemplates(url_root)


@pytest.fixture
def template(renderer):
    return renderer['index']


def test_template_name(renderer):
    assert renderer.template_name('index') == 'index.html'


def test_index_template(template, renderer):
    assert path.basename(template.filename) == 'index.html'
