"""Main module for AI Base Template service."""

from .logging import configure_structlog, get_logger

# Configure logging
configure_structlog(testing=True)
logger = get_logger(__name__)


def hello_world() -> str:
    """Simple function to test the package."""
    logger.info("hello_world function called")
    result = "Hello from AI Base Template!"
    logger.info("hello_world function returning result", result=result)
    return result


def get_version() -> str:
    """Get the package version."""
    logger.info("get_version function called")
    from . import __version__

    logger.info("Version retrieved", version=__version__)
    return __version__
