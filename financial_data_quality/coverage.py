import logging
import pandas as pd
from financial_data_quality.logger_setup import DATA_VALIDATION_LOGGER_NAME

class Coverage:
    @staticmethod
    def check_timeframe_coverage(data, account_info):
        """
        Checks for missing months in the data for each account based on the static account information.

        Parameters:
            data (pd.DataFrame): Transaction data with 'account_name', 'date_start', and 'date_end'.
            account_info (pd.DataFrame): Static information about accounts with 'account_name',
                                         'expected_start_date', and 'expected_end_date'.

        Returns:
            list: A list of dictionaries containing account names and their missing months.
        """
        # Initialize the data validation logger
        data_validation_logger = logging.getLogger(DATA_VALIDATION_LOGGER_NAME)

        results = []

        # Ensure date columns are in datetime format
        try:
            data['date_start'] = pd.to_datetime(data['date_start'])
            data['date_end'] = pd.to_datetime(data['date_end'])
        except Exception as e:
            data_validation_logger.error(
                "Failed to parse date columns",
                extra={"details": {"error": str(e)}}
            )
            return results

        for _, account in account_info.iterrows():
            try:
                # Generate the timeline of expected months
                timeline = pd.date_range(
                    account['expected_start_date'],
                    account['expected_end_date'],
                    freq='M'
                )

                # Filter transaction data for the current account
                account_data = data[data['account_name'] == account['account_name']]
                actual_months = pd.to_datetime(account_data['date_start']).dt.to_period('M')

                # Calculate missing months
                missing_months = set(timeline.to_period('M')) - set(actual_months)
                if missing_months:
                    data_validation_logger.warning(
                        "Missing months detected for account",
                        extra={
                            "details": {
                                "account_name": account['account_name'],
                                "missing_months": list(missing_months)
                            }
                        }
                    )

                # Append the results
                results.append({
                    'account_name': account['account_name'],
                    'missing_months': list(missing_months)
                })

            except Exception as e:
                data_validation_logger.error(
                    "Error checking coverage for account",
                    extra={
                        "details": {
                            "account_name": account.get('account_name', 'Unknown'),
                            "error": str(e)
                        }
                    }
                )

        return results