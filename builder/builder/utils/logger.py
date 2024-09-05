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

    # Create file handler which logs even debug messages
    file_handler = logging.FileHandler(logs_folder_path / "builder.log")
    file_handler.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(console_handler)

    # Test the logger with an error message
    LOGGER.debug("Logger setup completed")