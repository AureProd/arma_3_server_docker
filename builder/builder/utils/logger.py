import logging
from logging import getLogger
from pathlib import Path

LOGGER = getLogger()

def setup_logger(debug: bool = False) -> None:
    logger_level = logging.DEBUG if debug else logging.INFO
    
    # Define default level of logger
    LOGGER.setLevel(logger_level)
    
    # Get logs folder
    logs_folder_path = Path(__file__).parent.parent.parent

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    LOGGER.addHandler(console_handler)

    # Test the logger with an error message
    LOGGER.debug("Logger setup completed")