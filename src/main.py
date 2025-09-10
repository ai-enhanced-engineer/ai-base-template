"""Main module for AI Base Template service."""

from .logging import configure_structlog, get_logger

# Configure logging
# Note: testing=True enables human-readable format, testing=False uses JSON format
configure_structlog(testing=True)
logger = get_logger(__name__)


def hello_world() -> str:
    logger.info("hello_world function called")
    result = "Hello from AI Base Template!"
    logger.info("hello_world function returning result", result=result)
    return result


def get_version() -> str:
    logger.info("get_version function called")
    from . import __version__

    logger.info("Version retrieved", version=__version__)
    return __version__


def main() -> None:
    """Main entry point to demonstrate logging functionality."""
    logger.info("Application starting")

    # Test hello_world function
    greeting = hello_world()
    logger.info("Received greeting", greeting=greeting)

    # Test get_version function
    version = get_version()
    logger.info("Application version check complete", version=version)

    logger.info("Application finished successfully")


if __name__ == "__main__":
    main()
