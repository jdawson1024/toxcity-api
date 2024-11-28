import logging
from pythonjsonlogger import jsonlogger
import sys
from .config import get_settings

settings = get_settings()

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # JSON handler for file
    json_handler = logging.FileHandler('api.log')
    json_handler.setFormatter(
        jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
    )
    logger.addHandler(json_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    logger.addHandler(console_handler)

    return logger