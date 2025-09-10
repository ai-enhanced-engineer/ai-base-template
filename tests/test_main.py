"""Test module for AI Base Template main functionality"""

import pytest

from src import __version__
from src.main import get_version, hello_world


def test_hello_world():
    result = hello_world()
    assert result == "Hello from AI Base Template!"
    assert isinstance(result, str)


def test_get_version():
    version = get_version()
    assert version == "0.3.0"
    assert isinstance(version, str)


@pytest.mark.unit
def test_hello_world_unit():
    assert hello_world() == "Hello from AI Base Template!"


@pytest.mark.functional
def test_package_functionality():
    """Functional test for basic package functionality."""
    # Test that we can import and use the package
    assert __version__ == "0.3.0"

    # Test main functions work
    assert hello_world() == "Hello from AI Base Template!"
    assert get_version() == "0.3.0"
