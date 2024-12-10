import logging
from pythonjsonlogger import jsonlogger

# Define the data validation logger name as a constant
DATA_VALIDATION_LOGGER_NAME = "data_validation_logger"

def initialize_data_validation_logger(log_file="data_validation_logs.json"):
    """
    Initialize a centralized data validation logger for the repository.

    Parameters:
        log_file (str): Path to the file for storing data validation logs.

    Returns:
        logging.Logger: The initialized data validation logger.
    """
    # Get or create the data validation logger
    logger = logging.getLogger(DATA_VALIDATION_LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        handler = logging.FileHandler(log_file)

        # JSON formatter with module name
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(module)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger