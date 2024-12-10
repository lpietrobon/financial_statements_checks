import pandas as pd
import logging
from typing import Optional
from financial_data_quality.logger_setup import DATA_VALIDATION_LOGGER_NAME


def log_discrepancies(
    discrepancies: pd.DataFrame,
    message: str,
    log_level: int = logging.ERROR
) -> None:
    """
    Helper function to log all discrepancies from a DataFrame.

    Parameters:
        discrepancies (pd.DataFrame): DataFrame containing discrepancies.
        message (str): Log message.
        log_level (int): Logging level (default: logging.ERROR).
    """
    logger = logging.getLogger(DATA_VALIDATION_LOGGER_NAME)
    if not discrepancies.empty:
        logger.log(
            log_level,
            message,
            extra={"details": discrepancies.to_dict(orient="records")}
        )


def check_balance_reconciliation(data: pd.DataFrame, tolerance: float = 1e-5) -> pd.DataFrame:
    """
    Check if ending_balance matches the expected calculation:
    ending_balance = beginning_balance + my_contributions + employer_contributions + credits + change_in_market_value,
    within a given tolerance.

    Parameters:
        data (pd.DataFrame): DataFrame containing financial data.
        tolerance (float): Tolerance level for precision errors.

    Returns:
        pd.DataFrame: Rows where the balance reconciliation fails.
    """
    # Calculate expected ending balance
    data['expected_ending_balance'] = (
        data['beginning_balance']
        + data['my_contributions']
        + data['employer_contributions']
        + data['credits']
        + data['change_in_market_value']
    )

    # Identify rows where the difference exceeds the tolerance
    data['balance_difference'] = abs(data['ending_balance'] - data['expected_ending_balance'])
    discrepancies = data[data['balance_difference'] > tolerance][
        ['account_name', 'start_date', 'end_date', 'beginning_balance', 'ending_balance', 'expected_ending_balance']
    ]

    # Log all discrepancies
    log_discrepancies(discrepancies, "Balance reconciliation discrepancies detected")

    return discrepancies


def check_date_range_validity(data: pd.DataFrame) -> pd.DataFrame:
    """
    Check if start_date is earlier than or equal to end_date.

    Parameters:
        data (pd.DataFrame): DataFrame containing financial data.

    Returns:
        pd.DataFrame: Rows with invalid date ranges.
    """
    # Identify rows where start_date > end_date
    invalid_date_ranges = data[pd.to_datetime(data['start_date']) > pd.to_datetime(data['end_date'])][
        ['account_name', 'start_date', 'end_date']
    ]

    # Log all invalid date ranges
    log_discrepancies(invalid_date_ranges, "Invalid date ranges detected")

    return invalid_date_ranges


def check_balance_progression(data: pd.DataFrame) -> pd.DataFrame:
    """
    For each account, ensure that the ending_balance of one statement matches the beginning_balance of the next.

    Parameters:
        data (pd.DataFrame): DataFrame containing financial data.

    Returns:
        pd.DataFrame: Rows with mismatched balance progression.
    """
    # Sort data by account_name and start_date
    data = data.sort_values(by=['account_name', 'start_date'])

    # Identify mismatched balances
    mismatches = []
    grouped = data.groupby('account_name')
    for account_name, group in grouped:
        group = group.reset_index()
        for i in range(1, len(group)):
            if group.loc[i, 'beginning_balance'] != group.loc[i - 1, 'ending_balance']:
                mismatches.append({
                    'account_name': account_name,
                    'previous_end_date': group.loc[i - 1, 'end_date'],
                    'previous_ending_balance': group.loc[i - 1, 'ending_balance'],
                    'current_start_date': group.loc[i, 'start_date'],
                    'current_beginning_balance': group.loc[i, 'beginning_balance']
                })

    mismatches_df = pd.DataFrame(mismatches)

    # Log all mismatches
    log_discrepancies(mismatches_df, "Balance progression mismatches detected")

    return mismatches_df


def run_consistency_checks(
    data: pd.DataFrame,
    tolerance: float = 1e-5
) -> dict[str, Optional[pd.DataFrame]]:
    """
    Run all consistency checks on the data.

    Parameters:
        data (pd.DataFrame): DataFrame containing financial data.
        tolerance (float): Tolerance level for precision errors in balance reconciliation.

    Returns:
        dict[str, Optional[pd.DataFrame]]: A dictionary with the results of each consistency check.
    """
    results = {
        "balance_reconciliation": check_balance_reconciliation(data, tolerance),
        "date_range_validity": check_date_range_validity(data),
        "balance_progression": check_balance_progression(data)
    }
    return results