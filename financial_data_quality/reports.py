
import pandas as pd
import matplotlib.pyplot as plt

class ReportGenerator:
    @staticmethod
    def generate_summary_report(issues, output_file='data_quality_issues.csv'):
        """
        Generates a CSV file summarizing the data quality issues.

        Parameters:
            issues (list): A list of dictionaries containing data quality issues.
            output_file (str): The path to save the CSV file.
        """
        pd.DataFrame(issues).to_csv(output_file, index=False)
        print(f"Summary report saved to {output_file}")

    @staticmethod
    def plot_missing_months(missing_data):
        """
        Creates a bar chart showing the number of missing months for each account.

        Parameters:
            missing_data (list): A list of dictionaries with 'account_name' and 'missing_months'.
        """
        account_names = [item['account_name'] for item in missing_data]
        missing_counts = [len(item['missing_months']) for item in missing_data]

        plt.bar(account_names, missing_counts)
        plt.xlabel('Account Name')
        plt.ylabel('Number of Missing Months')
        plt.title('Missing Months by Account')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
