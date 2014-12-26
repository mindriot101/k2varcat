from k2var.app import app as myapp
import pytest

@pytest.fixture
def app():
    return myapp
