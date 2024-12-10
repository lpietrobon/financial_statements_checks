import logging
from financial_data_quality.logger_setup import DATA_VALIDATION_LOGGER_NAME

class AccountInfo:
    def __init__(self, account_info_file):
        self.metadata = metadata_file
        self.data_validation_logger = logging.getLogger(DATA_VALIDATION_LOGGER_NAME)

    def validate_metadata(self):
        if not self.metadata:
            self.data_validation_logger.error(
                "Metadata validation failed",
                extra={"details": {"reason": "Metadata file is empty"}}
            )