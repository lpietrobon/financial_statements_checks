import logging
from pythonjsonlogger import jsonlogger

def initialize_loggers(event_log_file="event_logs.log", quality_log_file="quality_logs.json"):
    """
    Initializes and returns two loggers: one for event logs and one for quality check logs.

    Parameters:
        event_log_file (str): File path for storing event logs.
        quality_log_file (str): File path for storing quality check logs.

    Returns:
        tuple: (event_logger, quality_logger)
    """
    # Event Logger
    event_logger = logging.getLogger("event_logger")
    event_logger.setLevel(logging.DEBUG)
    event_handler = logging.FileHandler(event_log_file)
    event_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    event_handler.setFormatter(event_formatter)
    event_logger.addHandler(event_handler)

    # Quality Check Logger
    quality_logger = logging.getLogger("quality_logger")
    quality_logger.setLevel(logging.INFO)
    quality_handler = logging.FileHandler(quality_log_file)
    quality_formatter = jsonlogger.JsonFormatter()
    quality_handler.setFormatter(quality_formatter)
    quality_logger.addHandler(quality_handler)

    return event_logger, quality_logger