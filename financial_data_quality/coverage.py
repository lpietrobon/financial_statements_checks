
import pandas as pd

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
        results = []
        
        # Ensure date columns are in datetime format
        data['date_start'] = pd.to_datetime(data['date_start'])
        data['date_end'] = pd.to_datetime(data['date_end'])
        
        for _, account in account_info.iterrows():
            timeline = pd.date_range(
                account['expected_start_date'],
                account['expected_end_date'],
                freq='M'
            )
            account_data = data[data['account_name'] == account['account_name']]
            actual_months = pd.to_datetime(account_data['date_start']).dt.to_period('M')
            missing_months = set(timeline.to_period('M')) - set(actual_months)
            results.append({
                'account_name': account['account_name'],
                'missing_months': list(missing_months)
            })
        
        return results
